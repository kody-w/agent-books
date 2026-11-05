---
layout: book
title: Memory
book_label: Chapter 6
book_progress: 45
book_order: 60
description: Use the memory tool, CLAUDE.md, auto memory, Projects, and prompt caching correctly
---

[← Chapter 5: Output That Steers the Next Step](05-output-that-steers.md) · [Book contents](README.md) · [Chapter 7: Growing Mid-Session →](07-growing-mid-session.md)

# Chapter 6 — Memory

> **In this chapter:** store a working note with the official memory helper and
> distinguish durable notes, standing instructions, project knowledge, and caches.

## 6.1 Use application-owned memory

Run `python3 claude/examples/06_memory.py`. It uses the official helper and writes
only the synthetic working note under `example-output/claude-memory`.

```python
import anthropic
from anthropic.tools import BetaLocalFilesystemMemoryTool

memory = BetaLocalFilesystemMemoryTool(base_path="example-output/claude-memory")
with anthropic.Anthropic() as client:
    runner = client.beta.messages.tool_runner(
        model="claude-opus-5-5", max_tokens=1024, max_iterations=8,
        tools=[memory],
        messages=[{"role": "user", "content":
                   "Remember this approved working note: library follow-ups stay drafts."}],
    )
    print(runner.until_done().content)
```

The memory tool is client-side. Claude requests file operations; your application
serves storage under the virtual `/memories` prefix. The Python helper provides
a local-filesystem implementation. The tool itself is stable even though the helper
and runner live on beta SDK surfaces.
[Memory tool and helper](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).

## 6.2 Retrieval, not an unlimited prompt

Memory supports just-in-time retrieval. Claude can inspect the directory, write
notes, and read relevant files later instead of keeping everything in the active
context. A later conversation must serve the same store to recover those notes.
[Memory lifecycle](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).

Application guidance: authenticate the user before selecting a backing directory,
enforce path confinement, and define retention and deletion. The official guide
specifically requires rejecting operations outside `/memories`.
Do not concatenate model-supplied paths onto an unrestricted filesystem root.
[Path traversal protection](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool).

## 6.3 Claude Code instructions and auto memory

`CLAUDE.md` supplies standing instructions written for the project, user, or
organization. Auto memory stores notes Claude writes from corrections and preferences.
The documentation distinguishes their writers, content, scope, and loading behavior;
both are context rather than enforced configuration.
[Claude Code memory](https://code.claude.com/docs/en/memory).

The checked-in [instruction template](config/CLAUDE.md) records the book system's
draft-only boundary. It is a template to copy deliberately, not an active root
configuration for this repository. Long procedures belong in skills rather than
making every session carry them.
[Instruction organization](https://code.claude.com/docs/en/memory).

## 6.4 Projects

The current Projects documentation describes workspaces with chat histories,
knowledge, and instructions. It also distinguishes a staged beta rollout of a new
project model with cloud threads and shared project context.
Do not assume every account sees the same interface.
[Projects and rollout](https://support.claude.com/en/articles/9517075-what-are-projects).

Application guidance: choose the narrowest place that matches the information's
purpose. Put project-wide conventions in project instructions, large source
documents in project knowledge, and application-specific persistent records in the
application's store. They are not interchangeable persistence APIs.

## 6.5 Prompt caching

Prompt caching reuses computation for repeated prefixes. The Messages API accepts
top-level or block-level `cache_control`; default entries have a five-minute
lifetime, with a one-hour option. Minimum lengths and usage reporting matter:
setting the field does not guarantee a cache hit.
[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

Caching is an execution-cost facility, not durable memory, replay, or proof of
identical output. Application guidance: keep stable instructions and tool declarations
in a stable prefix and inspect cache usage counters before claiming savings.

## 6.6 Exercises

**Exercise 6-1.** Start a fresh request against the same synthetic memory directory
and verify a real recall.

**Exercise 6-2.** Test path confinement and two authenticated storage scopes.

**Exercise 6-3.** Use a sufficiently long repeated prefix and measure cache reads
rather than assuming they occurred.

---

[← Chapter 5: Output That Steers the Next Step](05-output-that-steers.md) · [Book contents](README.md) · [Chapter 7: Growing Mid-Session →](07-growing-mid-session.md)
