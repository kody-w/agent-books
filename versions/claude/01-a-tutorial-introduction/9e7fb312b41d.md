---
layout: book
title: A Tutorial Introduction
book_label: Chapter 1
book_progress: 10
book_order: 10
description: Run a real SDK tool round trip over a synthetic chat file
---

[← Preface](00-preface.md) · [Book contents](README.md) · [Chapter 2: The Interface →](02-the-interface.md)

# Chapter 1 — A Tutorial Introduction

> **In this chapter:** ask Claude to call a draft tool, execute it in Python,
> return its result, and check that the source text did not change.

## 1.1 Getting started

From the repository root, create a virtual environment and install
`claude/examples/requirements.txt`. Set `ANTHROPIC_API_KEY` through your ordinary
secret-management mechanism; do not put it in a source file. Run
`python3 claude/examples/01_hello.py` with the environment's Python.
The Python SDK constructs a client from environment credentials.
[Official Python usage](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

Here is the complete book-level operation:

```python
import sys
sys.path.insert(0, "claude/examples")
from common import FIXTURES, draft_once

event = draft_once((FIXTURES / "chat.txt").read_text(encoding="utf-8"))
assert event["output"]["status"] == "success"
print(event["output"]["summary"])
```

The helper is not a fake client. Read [common.py](examples/common.py): it calls
`anthropic.Anthropic().messages.create()`, receives actual tool calls, executes
the declared local operation, and sends results back. This is the round trip in
the official tool-use guide. [Client tool lifecycle](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## 1.2 Follow the round trip

A request contains the tool declaration and a user message. A tool call comes back
as an assistant `tool_use` block with an identifier, name, and input. The application
runs that call and returns a user `tool_result` block referencing the identifier.
The next request includes both the assistant response and the result.
[Tool-use messages](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

Our helper preserves the full assistant content, not only the tool-call fragment.
It handles every client call in the response, returns explicit `is_error` results
for domain refusals, and limits the loop to eight model turns. These are application
choices built around the documented message protocol.
[Tool result protocol](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## 1.3 Make one real thing happen

The local tool creates a draft from the file's actual contents and hashes that
exact input. It has no mail sender. The helper also checks that the model supplied
the source text verbatim. If Claude paraphrases the transcript before calling,
the example raises instead of claiming exact provenance.

The first request requires the named draft tool. Later requests permit automatic
selection so the model can finish. Named tool choice is an API facility, not evidence
that a model would always choose this tool from an ambiguous prompt.
[Tool choice](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## 1.4 Know what a successful run proves

The expected first line is `Draft follow-up for review`, followed by a short request
for comments and deadline confirmation, then the synthetic discussion as evidence.
It proves an authenticated request, a real model-emitted call,
local execution, a tool-result round trip, and exact-source checking.
It does not prove semantic drafting quality: the tool intentionally uses a template.

With no key, the program prints a clear `SKIP` message and makes no live request.
The test suite separately reports live checks as skipped. An import or compilation
success is never relabeled as an authenticated API success.

## 1.5 Exercises

**Exercise 1-1.** Run with a separate synthetic chat file. Check the returned
digest against a local SHA-256 calculation.

**Exercise 1-2.** Remove required tool choice and evaluate whether descriptions
alone select the tool for five different requests.

**Exercise 1-3.** Trigger a domain refusal and inspect the paired `tool_use_id`
and `is_error` fields without printing your API key.

---

[← Preface](00-preface.md) · [Book contents](README.md) · [Chapter 2: The Interface →](02-the-interface.md)
