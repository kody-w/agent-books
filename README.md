# Two Agent Programming Books

**Docs as of 2026-11-05.** Two companion tutorial/reference books with one chapter
skeleton: [The Brainstem Agent Programming Language](brainstem/README.md) and
[The Claude Agent Programming Language](claude/README.md).

Read chapter N beside chapter N. Each book contains a preface, ten chapters,
a reference manual, a glossary, and the same mapping appendix. Each has ten
numbered executable Python examples. Both build the same synthetic library
follow-up: chat file → draft → exact review handoff → replay step 1 with a later file.
No messages are sent.

## Read

Open the Markdown contents above on GitHub, or build and serve the styled edition:

```bash
python3 build.py
python3 -m http.server 8000 --bind 127.0.0.1
```

Visit `http://127.0.0.1:8000/`. The two-column shelf reads
[api/v1/books.json](api/v1/books.json), not live GitHub APIs. Each book also has a
complete print edition: [Brainstem](brainstem/print.html) and
[Claude](claude/print.html). Browser Print → Save as PDF uses the 6×9 print stylesheet.
No generated PDF or Jekyll installation is required.

The frontmatter, navigation, chapter boxes, numbered sections, runnable-first
sequence, exercises, and reference/glossary conventions follow the public
[`rapp-1` reference book](https://github.com/kody-w/rapp-1/tree/main/book).
The local reference directory was inaccessible, so the five named source files
were fetched from its public repository.

## Run and verify

Brainstem examples require Python 3.10+ and only the standard library:

```bash
python3 brainstem/examples/01_hello.py
python3 brainstem/examples/10_system.py
```

`mini_loop.py` is a deterministic caller selecting tools by explicit name, not a
model and not an installed Brainstem runtime. Drafting is an evidence-preserving
template in **both** books, not a claim of model-generated writing quality.

Claude examples use the actual official SDKs. Use Python 3.13 for the reproducible
CI environment:

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r claude/examples/requirements.txt
.venv/bin/python claude/examples/02_interface.py
```

For authenticated examples, set `ANTHROPIC_API_KEY` through your usual secret
management, then run `.venv/bin/python claude/examples/10_system.py`.
The code uses `claude-opus-5-5` and makes real requests. It never uses a fake
transport to turn a missing key into a pass. Example 8 uses SDK session forks;
example 9 uses an in-process SDK MCP tool. SDK imports alone do not prove live access.

```bash
python3 build.py
.venv/bin/python -m unittest discover -s tests -v
python3 scripts/check_links.py
```

Without installed SDK dependencies, use `python3 -m unittest discover -s tests -v`:
all files and Python fences still compile, Brainstem examples execute, and SDK
import/live tests are clearly skipped. CI installs dependencies and import-checks
every Claude example. Live tests require both a key and explicit
`BOOKS_LIVE_TESTS=1`; normal CI does not spend API credits.

The suite checks all relative book links, numbering, frontmatter, source allowlists,
example/fence parity, a maximum 15% manuscript-length difference, exact handoffs,
replay refusals, immutable snapshots, generated HTML links, and build idempotence.
Word counts include manuscript bodies, tables, code, navigation, and the shared
appendix; they exclude frontmatter, contents pages, source files, and generated HTML.

## Sources and limits

The supplied [news](ref-hacker_news_agent.py),
[memory writer](ref-manage_memory_agent.py), and
[memory reader](ref-context_memory_agent.py) are quoted and analyzed, not imported
as standalone examples. The [source essay](ref-blog-post.html) supplies the six rules
and research starting points. Product claims in the Claude book cite only fetched
official Anthropic sources, inline.

**(unverified)** Installed Brainstem runtime/loader and concrete LearnNew behavior,
authenticated scope binding and instance reuse, working Pyodide/browser deployment,
and Copilot Studio adapters: local runtime access was denied and those hosts were
not executed. The books distinguish these from the observed supplied source files.

**(unverified)** Live authenticated API and Agent SDK execution unless explicitly
enabled: compilation and imports do not establish account access, server-tool
availability, or live behavior. The opt-in suite reports this honestly.

**(unverified)** Full SDK import compatibility in the authoring environment:
the dependency download failed its integrity check (empty artifact), and subsequent
installation attempts were denied. No integrity check was bypassed. All examples
compile; pure Claude handler/replay checks and the no-key refusal run without SDKs.
CI still requires installation and the full import check rather than weakening them.

`last_checked` is the editorial documentation-check timestamp, not the time of every
build. Weekly/manual CI GET-checks every unique official citation and fails on
HTTP errors, empty responses, or off-site redirects. Its artifact records current
link evidence; it does not pretend a 200 response proves semantic claims remain true.
Review changed documentation and update the manuscripts and manifest together.

## Static API and publication

[manifest.json](manifest.json) is the single authored publication configuration;
manuscripts and `site.css` are its source content. `python3 build.py` is the only
publication build. It generates [registry.json](registry.json), the versioned books
endpoint, [llms.txt](llms.txt), `.nojekyll`, the shelf, contents, styled chapters,
print editions, and SHA-256 snapshots under `versions/`.
The mapping appendix is copied from [one shared source](shared/C-mapping-table.md).

The implementation follows
[`rapp-static-api/1.1`](https://github.com/kody-w/rapp-static-apis/blob/main/SPEC.md):
same-origin reads, stable writes, schema-tagged JSON, versioned endpoints, 12-hex
`sha8` values, immutable append-only snapshots, and no cache bypass.
The configured Pages/raw URLs name the intended destination, not a verified live site.

The check workflow runs on pushes, pull requests, weekly schedules, and manual
dispatch. Pages uses artifact deployment, pushes no commits, and is off until the
repository variable `BOOKS_PAGES_ENABLED=true` is set and Pages is configured for
GitHub Actions. That activation belongs to the repository owner after creating
the remote. The local build creates no remote and never pushes.
