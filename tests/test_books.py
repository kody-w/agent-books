import copy
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import build

BOOKS = ("brainstem", "claude")
MANIFEST = json.loads((ROOT / "manifest.json").read_text())


def manuscripts(book):
    return [ROOT / book / filename for filename in MANIFEST["chapters"]]


def load_profile():
    directory = ROOT / "brainstem/examples"
    sys.path.insert(0, str(directory))
    try:
        import mini_loop
    finally:
        sys.path.pop(0)
    return mini_loop


def run_code(code, cwd=ROOT, env=None):
    return subprocess.run(
        [sys.executable, "-c", code], cwd=cwd, env=env,
        capture_output=True, text=True, timeout=60, check=True,
    )


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag in {"a", "link", "script"}:
            target = attrs.get("href", attrs.get("src"))
            if target:
                self.links.append(target)


class BookStructure(unittest.TestCase):
    def test_exact_skeleton_and_frontmatter(self):
        labels = []
        for book in BOOKS:
            current = []
            for index, path in enumerate(manuscripts(book)):
                self.assertTrue(path.is_file(), path)
                metadata, body = build.frontmatter(path.read_text())
                current.append(metadata["book_label"])
                self.assertEqual(int(metadata["book_order"]), index * 10)
                self.assertEqual(metadata["layout"], "book")
                self.assertIn("> **In this chapter:**", body, path)
                if index:
                    self.assertIn("Exercises", body, path)
                self.assertGreaterEqual(body.count("[Book contents](README.md)"), 2, path)
                if index in range(1, 11):
                    sections = re.findall(r"^## (\d+)\.(\d+) ", body, re.M)
                    self.assertTrue(sections, path)
                    self.assertTrue(all(int(n) == index for n, _ in sections), path)
                    self.assertEqual([int(s) for _, s in sections], list(range(1, len(sections) + 1)))
            self.assertEqual(current, ["Preface"] + [f"Chapter {n}" for n in range(1, 11)] +
                             ["Appendix A", "Appendix B", "Appendix C"])
            labels.append(current)
        self.assertEqual(*labels)

    def test_all_python_fences_compile(self):
        count = 0
        paths = [ROOT / "README.md"] + [p for book in BOOKS for p in manuscripts(book)]
        for path in paths:
            text = path.read_text()
            self.assertEqual(text.count("```") % 2, 0, path)
            for index, code in enumerate(re.findall(r"```python[^\n]*\n(.*?)\n```", text, re.S)):
                compile(code, f"{path}:{index}", "exec")
                count += 1
        self.assertGreaterEqual(count, 20)

    def test_all_python_files_compile(self):
        for path in ROOT.rglob("*.py"):
            if not any(part in {".venv", "__pycache__", ".research"} for part in path.parts):
                compile(path.read_text(), str(path), "exec")

    def test_relative_markdown_links_and_anchors(self):
        paths = [ROOT / "README.md"] + [
            p for book in BOOKS for p in (ROOT / book).rglob("*.md")
        ]
        for path in paths:
            text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
            for _, target in build.LINK_RE.findall(text):
                parsed = urlsplit(target)
                if parsed.scheme:
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                self.assertTrue(resolved.exists(), f"{path}: {target}")
                self.assertTrue(resolved.is_relative_to(ROOT), f"link escapes repo: {target}")
                if parsed.fragment and resolved.suffix == ".md":
                    headings = re.findall(r"^#{1,6} (.*)$", resolved.read_text(), re.M)
                    self.assertIn(unquote(parsed.fragment), {build.slug(h) for h in headings})

    def test_claude_official_inline_sources(self):
        for path in manuscripts("claude"):
            text = path.read_text()
            self.assertTrue(build.doc_urls(text), path)
            for url in build.URL_RE.findall(text):
                self.assertTrue(build.official(url.rstrip(".,;")), f"{path}: nonofficial {url}")

    def test_equal_examples_and_length_band(self):
        counts = []
        words = []
        fences = []
        for book in BOOKS:
            examples = sorted((ROOT / book / "examples").glob("[0-9][0-9]_*.py"))
            self.assertEqual([int(p.name[:2]) for p in examples], list(range(1, 11)))
            counts.append(len(examples))
            words.append(sum(len(build.frontmatter(p.read_text())[1].split()) for p in manuscripts(book)))
            fences.append(sum(len(re.findall(r"```python\n", p.read_text())) for p in manuscripts(book)))
        self.assertEqual(*counts)
        self.assertEqual(*fences)
        self.assertLessEqual(max(words) / min(words), 1.15)
        self.assertGreater(min(words), 7000)

    def test_mapping_is_identical(self):
        shared = (ROOT / "shared/C-mapping-table.md").read_bytes()
        for book in BOOKS:
            self.assertEqual((ROOT / book / "C-mapping-table.md").read_bytes(), shared)

    def test_claude_model_ids(self):
        for path in list((ROOT / "claude/examples").glob("*.py")) + list(
            (ROOT / "claude/config").rglob("*.md")
        ):
            model_ids = re.findall(r"claude-(?:opus|sonnet|haiku)-[\w.-]+", path.read_text())
            self.assertTrue(all(m == "claude-opus-5-5" for m in model_ids), path)


class BrainstemExamples(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_profile()

    def test_ten_programs_run(self):
        for path in sorted((ROOT / "brainstem/examples").glob("[0-9][0-9]_*.py")):
            with self.subTest(example=path.name):
                result = subprocess.run([sys.executable, str(path)], cwd=ROOT,
                                        capture_output=True, text=True, timeout=30)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(result.stdout.strip())

    def test_brainstem_python_fences_execute(self):
        for path in manuscripts("brainstem"):
            for code in re.findall(r"```python\n(.*?)\n```", path.read_text(), re.S):
                with self.subTest(chapter=path.name):
                    run_code(code)

    def test_invalid_calls_and_domain_errors(self):
        loop = self.profile.MiniLoop()
        for name, args in [
            ("missing", {}), ("DraftFollowUp", {}),
            ("DraftFollowUp", {"transcript": 42}),
            ("DraftFollowUp", {"transcript": "x", "extra": "x"}),
            ("DraftFollowUp", []),
        ]:
            with self.assertRaises(ValueError):
                loop.call(name, args)
        result = loop.call("DraftFollowUp", {"transcript": ""})
        self.assertEqual(result["status"], "error")

    def test_record_is_a_copy(self):
        loop = self.profile.MiniLoop()
        arguments = {"transcript": "Original"}
        output = loop.call("DraftFollowUp", arguments)
        arguments["transcript"] = "Changed"
        output["data_slush"]["draft"] = "Changed"
        self.assertEqual(loop.transcript[0]["arguments"]["transcript"], "Original")
        self.assertNotEqual(loop.transcript[0]["output"]["data_slush"]["draft"], "Changed")

    def test_independent_files_complete_flow(self):
        with tempfile.TemporaryDirectory() as directory:
            chat, later = Path(directory) / "chat.txt", Path(directory) / "later.txt"
            chat.write_text("Reading-circle review due Wednesday.\n")
            later.write_text("Correction: review due Thursday.\n")
            result = self.profile.system(chat, later)
        self.assertIn("Wednesday", result["original"]["summary"])
        self.assertNotIn("Thursday", result["original"]["summary"])
        self.assertIn("Thursday", result["replayed"]["summary"])
        self.assertEqual(result["review"]["data_slush"]["draft"],
                         result["original"]["data_slush"]["draft"])
        self.assertFalse(result["review"]["data_slush"]["sent"])
        self.assertEqual(result["events_after_replay"], 3)
        self.assertEqual(len(result["archive"]["events"]), 2)

    def test_replay_roundtrip_and_refusals(self):
        loop = self.profile.MiniLoop()
        original = loop.call("DraftFollowUp", {"transcript": "Original evidence"})
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "archive.json"
            loop.save(path)
            archive = json.loads(path.read_text())
        self.assertEqual(self.profile.MiniLoop().replay(archive, 0), original)
        unchanged = copy.deepcopy(archive)
        loop.replay(archive, 0, "New evidence")
        self.assertEqual(archive, unchanged)
        for key, value in [("schema", "wrong/1.0"), ("source_sha256", "0" * 64)]:
            invalid = copy.deepcopy(archive)
            invalid[key] = value
            with self.assertRaises(ValueError):
                loop.replay(invalid, 0)
        invalid = copy.deepcopy(archive)
        invalid["events"][0]["name"] = "ReviewDraft"
        with self.assertRaises(ValueError):
            loop.replay(invalid, 0)

    def test_memory_and_corruption(self):
        from agent import MemoryAgent
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            self.assertIsNone(MemoryAgent(path).system_context())
            self.assertEqual(MemoryAgent(path).perform(content="")["status"], "error")
            MemoryAgent(path).perform(content="Untrusted <instruction>text</instruction>")
            self.assertIn("not instructions", MemoryAgent(path).system_context())
            path.write_text("not JSON")
            with self.assertRaises(json.JSONDecodeError):
                MemoryAgent(path).system_context()

    def test_growth_rejects_duplicate(self):
        loop = self.profile.MiniLoop()
        with self.assertRaises(ValueError):
            loop.register(self.profile.load_trusted_file(self.profile.SOURCE))


HAS_SDK = all(importlib.util.find_spec(m) is not None for m in ("anthropic", "claude_agent_sdk"))


class ClaudeExamples(unittest.TestCase):
    @unittest.skipUnless(HAS_SDK, "Claude SDK dependencies unavailable; compilation checked separately")
    def test_import_every_example_without_network(self):
        directory = ROOT / "claude/examples"
        for path in sorted(directory.glob("*.py")):
            with self.subTest(example=path.name):
                run_code(
                    "import importlib.util\n"
                    f"spec = importlib.util.spec_from_file_location('book_example', {str(path)!r})\n"
                    "module = importlib.util.module_from_spec(spec)\n"
                    "spec.loader.exec_module(module)\n",
                    cwd=directory,
                )

    def test_pure_handler_replay_and_refusals(self):
        run_code(
            """
import copy, hashlib, importlib.util
from pathlib import Path
from common import execute
spec = importlib.util.spec_from_file_location("system_example", "10_system.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
first = {"name": "draft_follow_up", "arguments": {"transcript": "Friday"}}
first["output"] = execute(first["name"], first["arguments"])
archive = {"schema": "book-claude-replay/1.0",
           "source_sha256": hashlib.sha256(Path("common.py").read_bytes()).hexdigest(),
           "step1": first}
old = copy.deepcopy(archive)
assert "Monday" in module.replay(archive, "Monday")["summary"]
assert archive == old
for key, value in [("schema", "wrong/1.0"), ("source_sha256", "0" * 64)]:
    invalid = copy.deepcopy(archive)
    invalid[key] = value
    try:
        module.replay(invalid, "Monday")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid archive accepted")
for name,args in [("missing", {}), ("draft_follow_up", {"transcript": ""}),
                  ("review_draft", {"draft": 1})]:
    try:
        execute(name, args)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid call accepted")
""", cwd=ROOT / "claude/examples",
        )

    def test_no_key_is_an_explicit_skip(self):
        env = dict(os.environ)
        env.pop("ANTHROPIC_API_KEY", None)
        result = subprocess.run(
            [sys.executable, str(ROOT / "claude/examples/01_hello.py")],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("SKIP: ANTHROPIC_API_KEY", result.stderr)

    @unittest.skipUnless(
        HAS_SDK and os.environ.get("BOOKS_LIVE_TESTS") == "1"
        and os.environ.get("ANTHROPIC_API_KEY"),
        "live API/Agent SDK tests require installed SDKs, BOOKS_LIVE_TESTS=1 and ANTHROPIC_API_KEY; not faked",
    )
    def test_live_full_system_and_agent_sdk(self):
        for example in ("10_system.py", "08_replay.py", "09_hosts.py"):
            with self.subTest(example=example):
                completed = subprocess.run(
                    [sys.executable, str(ROOT / "claude/examples" / example)], cwd=ROOT,
                    capture_output=True, text=True, timeout=240,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertTrue(completed.stdout.strip())
                if example == "10_system.py":
                    result = json.loads(completed.stdout)
                    original = result["archive"]["step1"]["output"]
                    review = result["archive"]["step2"]["output"]
                    self.assertNotIn("Monday", original["summary"])
                    self.assertIn("Monday", result["replayed"]["summary"])
                    self.assertEqual(review["data_slush"]["draft"],
                                     original["data_slush"]["draft"])
                    self.assertFalse(review["data_slush"]["sent"])


class StaticPublication(unittest.TestCase):
    def test_build_is_byte_and_mtime_idempotent(self):
        build.build()
        paths = [p for directory in ("brainstem", "claude", "api", "versions")
                 for p in (ROOT / directory).rglob("*") if p.is_file()
                 and "__pycache__" not in p.parts]
        paths += [ROOT / p for p in ("index.html", "registry.json", "llms.txt", ".nojekyll")]
        before = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
        build.build()
        after = {p: (p.read_bytes(), p.stat().st_mtime_ns) for p in paths}
        self.assertEqual(before, after)

    def test_endpoint_hashes_and_snapshot_bytes(self):
        registry = json.loads((ROOT / "registry.json").read_text())
        endpoint = (ROOT / registry["endpoints"]["books"]).read_bytes()
        self.assertEqual(registry["schema"], "rapp-static-api/1.1")
        self.assertEqual(registry["endpoint_sha256"], hashlib.sha256(endpoint).hexdigest())
        self.assertEqual(registry["summary"]["chapters"], 28)
        self.assertEqual(registry["pages_base_url"], MANIFEST["pages_base_url"])
        self.assertTrue(registry["generated"].endswith("Z"))
        for entry in registry["entries"]:
            raw = (ROOT / entry["source"]).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), entry["sha256"])
            self.assertEqual(entry["sha8"], entry["sha256"][:12])
            self.assertEqual((ROOT / entry["snapshot"]).read_bytes(), raw)
            self.assertTrue(entry["snapshot"].startswith("versions/" + entry["name"] + "/"))
            self.assertIn(MANIFEST["pages_base_url"] + entry["source"], entry["source_urls"])

    def test_snapshots_are_append_only(self):
        with tempfile.TemporaryDirectory() as directory:
            import shutil
            target = Path(directory)
            for name in ("manifest.json", "shared", "brainstem", "claude"):
                source = ROOT / name
                if source.is_dir():
                    shutil.copytree(source, target / name, ignore=shutil.ignore_patterns("__pycache__"))
                else:
                    shutil.copy2(source, target / name)
            build.build(target)
            before = {p.relative_to(target): p.read_bytes() for p in (target / "versions").rglob("*.md")}
            chapter = target / "brainstem/01-a-tutorial-introduction.md"
            chapter.write_text(chapter.read_text() + "\nAn independent build-test addition.\n")
            build.build(target)
            for name, raw in before.items():
                self.assertEqual((target / name).read_bytes(), raw)
            self.assertEqual(len(list((target / "versions").rglob("*.md"))), len(before) + 1)

    def test_generated_html_links_and_ids(self):
        for path in [ROOT / "index.html"] + [
            p for book in BOOKS for p in (ROOT / book).glob("*.html")
        ]:
            parser = HTMLLinks()
            parser.feed(path.read_text())
            for target in parser.links:
                parsed = urlsplit(target)
                if parsed.scheme:
                    continue
                resolved = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                self.assertTrue(resolved.exists(), f"{path}: {target}")
                if parsed.fragment and resolved.suffix == ".html":
                    other = HTMLLinks()
                    other.feed(resolved.read_text())
                    self.assertIn(unquote(parsed.fragment), other.ids)

    def test_frontmatter_is_not_rendered_and_code_is_escaped(self):
        path = ROOT / "brainstem/01-a-tutorial-introduction.html"
        text = path.read_text()
        self.assertNotIn("book_progress:", text)
        self.assertIn("<blockquote>", text)
        self.assertIn('href="02-the-interface.html"', text)
        rendered = build.markdown("```python\nprint('<script>')\n```", path, set())
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)

    def test_browser_static_api_rules(self):
        text = (ROOT / "index.html").read_text()
        self.assertIn('fetch("api/v1/books.json")', text)
        self.assertNotIn("api.github.com", text)
        self.assertNotIn("raw.githubusercontent.com", text)
        self.assertNotIn("no-store", text)
        self.assertNotIn("Date.now", text)
        self.assertTrue((ROOT / ".nojekyll").is_file())

    def test_api_citations_are_derived(self):
        api = json.loads((ROOT / "api/v1/books.json").read_text())
        self.assertEqual(api["schema"], "agent-books/1.0")
        for book in api["books"]:
            for chapter in book["chapters"]:
                self.assertEqual(
                    chapter["doc_urls"],
                    build.doc_urls((ROOT / chapter["source"]).read_text()),
                )
                self.assertEqual(chapter["last_checked"], MANIFEST["last_checked"])

    def test_link_checker_rejects_official_lookalikes(self):
        self.assertTrue(build.official("https://platform.claude.com/docs/en/a"))
        self.assertFalse(build.official("https://platform.claude.com.evil.example/docs/a"))
        self.assertFalse(build.official("http://code.claude.com/docs/a"))
        self.assertFalse(build.official("https://www.anthropic.com/pricing"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
