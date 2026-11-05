#!/usr/bin/env python3
"""One offline, idempotent build from manifest + authored manuscripts/assets."""

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
OFFICIAL = {"platform.claude.com", "code.claude.com", "support.claude.com"}
URL_RE = re.compile(r"https://[^\s<>\"')]+")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")
COUNTS_RE = re.compile(r"<!-- book-counts:start -->.*?<!-- book-counts:end -->", re.S)
EXAMPLE_RE = re.compile(r"^```(?:python|bash|sh|json|yaml|toml|javascript|markdown)\s*$", re.M)


def official(url):
    parsed = urlsplit(url)
    return parsed.scheme == "https" and (
        parsed.hostname in OFFICIAL or
        parsed.hostname in {"anthropic.com", "www.anthropic.com"}
        and parsed.path.startswith("/engineering/")
    )


def doc_urls(text):
    return sorted({url.rstrip(".,;") for url in URL_RE.findall(text) if official(url)})


def frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    head, body = text[4:].split("\n---\n", 1)
    metadata = {}
    optional = {"concepts", "hosts"}
    key = None
    for line in head.splitlines():
        if line.startswith("  "):
            if key not in optional:
                raise ValueError("only JSON list metadata may span lines")
            metadata[key] += "\n" + line.strip()
            continue
        key, value = line.split(":", 1)
        metadata[key] = value.strip()
    required = {"layout", "title", "book_label", "book_progress", "book_order", "description"}
    if not required <= set(metadata) or set(metadata) - required - optional:
        raise ValueError(f"invalid frontmatter keys: {set(metadata)}")
    for key in optional & set(metadata):
        metadata[key] = json.loads(metadata[key])
    return metadata, body.lstrip()


def slug(text):
    return re.sub(r"[^\w -]", "", text.lower()).strip().replace(" ", "-")


def stable_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        data = data.encode("utf-8")
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def book_counts(root, manifest):
    counts = {}
    for book in manifest["books"]:
        directory = root / book["name"]
        metadata, _ = frontmatter((directory / "00-preface.md").read_text())
        concepts, hosts = metadata["concepts"], metadata["hosts"]
        if not concepts or len({c["name"] for c in concepts}) != len(concepts):
            raise ValueError(f"empty or duplicate concepts: {book['name']}")
        if not hosts or len(set(hosts)) != len(hosts):
            raise ValueError(f"empty or duplicate hosts: {book['name']}")
        bodies = [
            COUNTS_RE.sub("", frontmatter((directory / filename).read_text())[1])
            for filename in manifest["chapters"]
        ]
        counts[book["name"]] = {
            "concepts": concepts, "hosts": hosts,
            "concept_count": len(concepts), "host_count": len(hosts),
            "word_count": sum(len(body.split()) for body in bodies),
            "example_count": sum(len(EXAMPLE_RE.findall(body)) for body in bodies),
        }
    return counts


def write_counts(root, manifest, counts):
    lines = ["<!-- book-counts:start -->",
             "| Book | Concepts | Hosts | Words | Examples |",
             "|---|---:|---:|---:|---:|"]
    for book in manifest["books"]:
        count = counts[book["name"]]
        lines.append(f"| {book['name'].capitalize()} | {count['concept_count']} | "
                     f"{count['host_count']} | {count['word_count']} | {count['example_count']} |")
    lines.append("<!-- book-counts:end -->")
    table = "\n".join(lines)
    for book in manifest["books"]:
        path = root / book["name"] / "00-preface.md"
        text = path.read_text()
        if len(COUNTS_RE.findall(text)) != 1:
            raise ValueError(f"expected one generated counts region: {path}")
        stable_write(path, COUNTS_RE.sub(lambda _: table, text))


def inline(text, source, rendered):
    tokens = []

    def token(markup):
        tokens.append(markup)
        return f"\x00{len(tokens) - 1}\x00"

    text = re.sub(r"`([^`]+)`", lambda m: token("<code>" + html.escape(m[1]) + "</code>"), text)

    def link(match):
        label, target = match.groups()
        if not urlsplit(target).scheme and not target.startswith("#"):
            path, separator, fragment = target.partition("#")
            resolved = (source.parent / path).resolve()
            if resolved in rendered:
                target = str(Path(path).with_suffix(".html"))
                if separator:
                    target += "#" + fragment
        if urlsplit(target).scheme not in {"", "http", "https"}:
            raise ValueError(f"unsafe link: {target}")
        return token('<a href="' + html.escape(target, quote=True) + '">' +
                     html.escape(label) + "</a>")

    text = LINK_RE.sub(link, text)
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    for index, value in enumerate(tokens):
        text = text.replace(f"\x00{index}\x00", value)
    return text


def markdown(text, source, rendered):
    """Render the deliberately bounded Markdown dialect used by the manuscripts."""
    lines, output, paragraph = text.splitlines(), [], []

    def flush():
        if paragraph:
            output.append("<p>" + inline(" ".join(paragraph), source, rendered) + "</p>")
            paragraph.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            flush()
            language = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError(f"unclosed fence: {source}")
            output.append('<pre><code class="language-' + html.escape(language) + '">' +
                          html.escape("\n".join(code)) + "</code></pre>")
        elif line.startswith("#"):
            flush()
            match = re.match(r"^(#{1,6}) (.+)$", line)
            if not match:
                raise ValueError(f"invalid heading: {line}")
            level, title = len(match[1]), match[2]
            output.append(f'<h{level} id="{slug(title)}">' +
                          inline(title, source, rendered) + f"</h{level}>")
        elif line.startswith(">"):
            flush()
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> "))
                i += 1
            output.append("<blockquote><p>" + inline(" ".join(quote), source, rendered) +
                          "</p></blockquote>")
            continue
        elif line.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    tag = "th" if not rows else "td"
                    rows.append("<tr>" + "".join(
                        f"<{tag}>" + inline(c, source, rendered) + f"</{tag}>" for c in cells
                    ) + "</tr>")
                i += 1
            output.append("<table>" + "".join(rows) + "</table>")
            continue
        elif re.match(r"^(?:- |\d+\. )", line):
            flush()
            numbered = bool(re.match(r"^\d+\. ", line))
            pattern = r"^\d+\. " if numbered else r"^- "
            items = []
            while i < len(lines) and re.match(pattern, lines[i]):
                item = re.sub(pattern, "", lines[i])
                i += 1
                while i < len(lines) and lines[i].startswith("   "):
                    item += " " + lines[i].strip()
                    i += 1
                items.append("<li>" + inline(item, source, rendered) + "</li>")
            tag = "ol" if numbered else "ul"
            output.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        elif line == "---":
            flush()
            output.append("<hr>")
        elif line in {"<!-- book-counts:start -->", "<!-- book-counts:end -->"}:
            flush()
        elif not line.strip():
            flush()
        else:
            paragraph.append(line)
        i += 1
    flush()
    return "\n".join(output)


def page(title, content, depth=1, progress=100):
    prefix = "../" * depth
    return (
        '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f"<title>{html.escape(title)}</title>"
        f'<link rel="stylesheet" href="{prefix}site.css"></head><body>'
        f'<div class="progress" style="width:{int(progress)}%"></div><main>'
        f'<nav><a href="{prefix}index.html">Companion shelf</a></nav>'
        '<p class="edition">Docs as of 2026-11-05 · Tutorial and reference edition</p>'
        + content + "</main></body></html>\n"
    )


def contents(book, chapters, date):
    lines = [f"# {book['title']}", "",
             "## A tutorial, programming workbook, and field reference", "",
             f"**Docs as of {date}.**", "",
             "[Companion shelf](../index.html) · [Complete print edition](print.html)", "",
             "Read chapter N beside chapter N in the other book. Ten numbered programs",
             "accompany the ten chapters; additional examples and configurations appear inline.", "",
             "## Contents", ""]
    for chapter in chapters:
        lines.append(f"- [{chapter['label']}: {chapter['title']}]({chapter['file']})")
    lines += ["", "## Run with a terminal open", "",
              "Use repository-root commands and setup from the [root README](../README.md).",
              "Begin with [the preface](00-preface.md), then run the first numbered program.",
              "The tests distinguish offline checks from skipped authenticated execution.", ""]
    return "\n".join(lines)


DASHBOARD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Two Agent Programming Books</title><link rel="stylesheet" href="site.css">
</head><body><main class="shelf"><h1>Two Agent Programming Books</h1>
<p>One chapter skeleton. Two host-aware tutorials. Read chapter N beside chapter N.</p>
<p id="asof" class="edition">Loading book index…</p>
<div id="books" class="columns"></div>
<noscript><p>JavaScript is off. Open <a href="brainstem/README.html">Brainstem</a>
or <a href="claude/README.html">Claude</a>, or read <a href="api/v1/books.json">the JSON index</a>.</p></noscript>
<p><a href="registry.json">Registry</a> · <a href="llms.txt">LLM index</a> · <a href="README.md">Setup and evidence limits</a></p>
</main><script>
"use strict";
fetch("api/v1/books.json").then(response => {
  if (!response.ok) throw new Error("Book index HTTP " + response.status);
  return response.json();
}).then(index => {
  document.getElementById("asof").textContent = "Docs as of " + index.docs_as_of +
    " · editorial checks " + index.last_checked + " · not a live-service claim";
  for (const book of index.books) {
    const section = document.createElement("section");
    const title = document.createElement("h2"); title.textContent = book.title;
    section.append(title);
    const list = document.createElement("ol");
    for (const chapter of book.chapters) {
      const item = document.createElement("li"), link = document.createElement("a");
      link.href = chapter.html; link.textContent = chapter.label + ": " + chapter.title;
      item.append(link); list.append(item);
    }
    section.append(list); document.getElementById("books").append(section);
  }
}).catch(error => {
  const status = document.getElementById("asof");
  status.className = "error"; status.textContent = "Could not load books: " + error.message;
});
</script></body></html>
"""


def build(root=ROOT):
    manifest = json.loads((root / "manifest.json").read_text())
    shared = (root / "shared/C-mapping-table.md").read_bytes()
    for book in manifest["books"]:
        stable_write(root / book["name"] / "C-mapping-table.md", shared)
    counts = book_counts(root, manifest)
    write_counts(root, manifest, counts)
    rendered = {
        (root / b["name"] / filename).resolve()
        for b in manifest["books"] for filename in manifest["chapters"] + ["README.md"]
    }
    books, entries = [], []
    for book in manifest["books"]:
        directory = root / book["name"]
        chapters, print_parts = [], []
        for filename in manifest["chapters"]:
            source = directory / filename
            raw = source.read_bytes()
            text = raw.decode("utf-8")
            metadata, body = frontmatter(text)
            digest = hashlib.sha256(raw).hexdigest()
            name = book["name"] + "/" + source.stem
            snapshot = f"versions/{name}/{digest[:12]}.md"
            target = root / snapshot
            if target.exists() and target.read_bytes() != raw:
                raise ValueError(f"immutable snapshot collision: {snapshot}")
            stable_write(target, raw)
            chapter = {
                "number": metadata["book_label"].removeprefix("Chapter "),
                "label": metadata["book_label"], "title": metadata["title"],
                "order": int(metadata["book_order"]), "file": filename,
                "source": f"{book['name']}/{filename}",
                "html": f"{book['name']}/{source.stem}.html",
                "doc_urls": doc_urls(body), "last_checked": manifest["last_checked"],
                "sha256": digest, "sha8": digest[:12], "snapshot": snapshot,
                "words": len(COUNTS_RE.sub("", body).split()),
            }
            chapters.append(chapter)
            entries.append({
                "name": name, "title": metadata["title"],
                "source": chapter["source"],
                "source_urls": [manifest["pages_base_url"] + chapter["source"]] + chapter["doc_urls"],
                "sha256": digest, "sha8": digest[:12], "snapshot": snapshot,
                "html": chapter["html"],
            })
            content = markdown(body, source, rendered)
            stable_write(source.with_suffix(".html"), page(
                book["title"] + " — " + metadata["title"], content,
                progress=int(metadata["book_progress"]),
            ))
            print_parts.append(content)
        readme = contents(book, chapters, manifest["docs_as_of"])
        stable_write(directory / "README.md", readme)
        stable_write(directory / "README.html", page(
            book["title"], markdown(readme, directory / "README.md", rendered),
        ))
        stable_write(directory / "print.html", page(book["title"], "\n<hr>\n".join(print_parts)))
        books.append({
            **book, "chapters": chapters, **counts[book["name"]],
            "numbered_examples": [str(p.relative_to(root)) for p in sorted(
                (directory / "examples").glob("[0-9][0-9]_*.py"))],
        })
    api = {
        "schema": "agent-books/1.0", "generated": manifest["last_checked"],
        "docs_as_of": manifest["docs_as_of"], "last_checked": manifest["last_checked"],
        "books": books,
    }
    api_raw = json_bytes(api)
    stable_write(root / "api/v1/books.json", api_raw)
    registry = {
        "schema": "rapp-static-api/1.1", "generated": manifest["last_checked"],
        "pages_base_url": manifest["pages_base_url"],
        "raw_base_url": manifest["raw_base_url"], "policy": manifest["policy"],
        "summary": {"books": len(books), "chapters": len(entries),
                    "official_doc_urls": len({u for e in entries for u in e["source_urls"]
                                              if official(u)})},
        "endpoints": {"books": "api/v1/books.json"},
        "endpoint_sha256": hashlib.sha256(api_raw).hexdigest(),
        "entries": entries,
    }
    stable_write(root / "registry.json", json_bytes(registry))
    llms = ["# Two Agent Programming Books", "",
            f"> Docs as of {manifest['docs_as_of']}; source and host limits are explicit.", "",
            "## Machine-readable", "- [Registry](registry.json)",
            "- [Books and official citations](api/v1/books.json)", "", "## Books"]
    for book in books:
        llms += [f"- [{book['title']}]({book['name']}/README.md)"]
        llms += [f"- [{c['label']}: {c['title']}]({c['source']})" for c in book["chapters"]]
    stable_write(root / "llms.txt", "\n".join(llms) + "\n")
    stable_write(root / ".nojekyll", b"")
    stable_write(root / "index.html", DASHBOARD)
    return api


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    result = build()
    print(f"Built {len(result['books'])} books, "
          f"{sum(len(b['chapters']) for b in result['books'])} chapters/appendices.")
    for book in result["books"]:
        print(f"{book['name']}: {book['word_count']} manuscript words, "
              f"{book['concept_count']} concepts, {book['host_count']} hosts, "
              f"{book['example_count']} examples "
              f"({len(book['numbered_examples'])} numbered programs)")
