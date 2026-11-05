# ORDER: two K&R-style books, one shape, fair to both

You are the muscle. Build two companion books in this repo, in the exact style and formatting of
`~/Documents/GitHub/rapp-1/book/` ("The RAPP Programming Language", K&R style). Read that book first
(00-preface.md, 01-a-tutorial-introduction.md, A-reference-manual.md, README.md, build-pdf.sh) and copy
its conventions: Jekyll front matter (layout/title/book_label/book_progress/book_order/description),
prev/contents/next nav line, "> **In this chapter:**" box, numbered sections (1.1, 1.2 ...), runnable code
first then explanation, exercises at chapter end, Appendix A reference manual, glossary.

## The two books (same chapter skeleton, so a reader can compare chapter N to chapter N)
1. `brainstem/` — **The Brainstem Agent Programming Language** (the agent.py pattern, end to end).
2. `claude/` — **The Claude Agent Programming Language** (Anthropic's whole ecosystem, end to end).

Shared skeleton (both books, same numbers):
- Preface
- 1 A Tutorial Introduction (hello-world agent/tool that does something real)
- 2 The Interface: what the caller sees (name, description, parameters / tool schema, skill frontmatter, subagent frontmatter)
- 3 Execution: where the work happens (perform(); client tools, server tools, code execution, skill scripts, subagents, hooks)
- 4 The Transcript: what comes back (outputs only; tool_result, subagent summaries, programmatic tool calling, context editing)
- 5 Output that steers the next step (summary + instruction + data_slush; Claude's equivalents and guidance)
- 6 Memory (ManageMemory/ContextMemory + system_context(); Claude memory tool, CLAUDE.md, Projects)
- 7 Growing mid-session (LearnNew hot-load; Claude Code skill/subagent hot reload, tool search, MCP, plugins)
- 8 Replay and time travel (static transcript through static caller; checkpoints/rewind, SDK sessions/fork)
- 9 Hosts and portability (Brainstem local, Pyodide/browser, Copilot Studio; Claude Code, API, Agent SDK, Managed Agents, Cowork, claude.ai Skills, Claude in Chrome)
- 10 Building a real system end to end (same task in both: "read a chat transcript, draft a follow-up, hand its result to a second step, then replay step 1 with a later file")
- Appendix A Reference manual; Appendix B Glossary; Appendix C "Mapping table" (chapter-by-chapter concept map between the two books — identical file in both)

## Fairness rules (non-negotiable — Kody: "be fair to claude")
- The Claude book is written as its best advocate would write it, same care, same length band, same
  number of runnable examples as the Brainstem book. Show Claude's real strengths (server tools,
  prompt caching, tool search, subagents, skills, hooks, checkpoints, Managed Agents, enterprise hosts).
- Every Claude claim cites the official doc URL inline. Use ONLY Anthropic official docs
  (platform.claude.com/docs, code.claude.com/docs, support.claude.com, anthropic.com/engineering).
  Fetch them; do not write from memory. Mark anything you could not verify as "(unverified)".
- Verified research findings to honor are in ref-blog-post.html (section "Anthropic already does this").
- No marketing language either way. No "better/worse" verdicts in the books; Appendix C only maps.
- Claude code samples use the current official SDK (`anthropic` Python, Agent SDK) and model id
  `claude-opus-5-5` where a model is needed.

## Brainstem book sources
- ref-hacker_news_agent.py, ref-manage_memory_agent.py, ref-context_memory_agent.py (real agents; quote them).
- ref-blog-post.html (the six rules). Brainstem code: ~/.brainstem/src/rapp_brainstem/ (read-only; never edit).
- Write the six rules in the Brainstem voice; no AIBAST, Microsoft-internal, customer or personal data.

## Runnable examples
- `brainstem/examples/` : stdlib-only agent.py files + a tiny `mini_loop.py` caller so examples run with
  `python3` alone (a fake deterministic "model" that picks tools by name is fine for tests; say so).
- `claude/examples/` : real SDK code. Tests must at least import-check / compile them; anything that
  needs an API key is skipped in CI with a clear message, never faked as a pass.
- `tests/test_books.py`: every fenced python block compiles; every relative link resolves; every
  Claude chapter has >=1 official-doc URL; both books have identical chapter numbering.

## Hosting (GitHub Pages, kept updated)
- Conform to rapp-static-api/1.1 (read https://github.com/kody-w/rapp-static-apis SPEC.md):
  `registry.json`, `api/v1/books.json` (chapters, titles, doc-URL list, last_checked), `llms.txt`,
  `.nojekyll`, one idempotent `build.py`. Root `index.html` = thin two-column view over the JSON.
- `.github/workflows/check.yml`: runs tests + a weekly link check of the cited Anthropic URLs so drift shows red.
- README: what this is, how to read side by side, how to run examples, "docs as of <date>".

## Done when
- Both books complete (preface, 10 chapters, 3 appendices each), tests pass locally (paste output),
  build.py run, repo committed on branch main. DO NOT create a GitHub remote or push — the cortex does that.
- End with a report: file list, word counts per book, test output, every "(unverified)" item.
