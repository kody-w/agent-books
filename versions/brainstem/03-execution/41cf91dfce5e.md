---
layout: book
title: Execution
book_label: Chapter 3
book_progress: 24
book_order: 30
description: Keep work and domain validation behind perform()
---

[← Chapter 2: The Interface](02-the-interface.md) · [Book contents](README.md) · [Chapter 4: The Transcript →](04-the-transcript.md)

# Chapter 3 — Execution

> **In this chapter:** implement the hidden work, preserve explicit errors, and
> identify where network access and side effects change the contract.

## 3.1 Start with a refusal

Run `python3 brainstem/examples/03_execution.py`.

```python
import sys
sys.path.insert(0, "brainstem/examples")
from agent import DraftFollowUp

result = DraftFollowUp().perform(transcript="")
assert result == {"status": "error", "message": "transcript must be nonempty text"}
print(result["message"])
```

Direct execution needs no model. `perform()` validates text, hashes its exact input,
assembles the draft, and returns the result.

## 3.2 Follow a real implementation

The [Hacker News source](../ref-hacker_news_agent.py) converts and bounds `count`,
fetches the top identifiers, fetches each item, formats Markdown links, and returns
a JSON string. That is more than "a prompt in a file." Python performs the network
and formatting operations.

Its count conversion handles `TypeError` and `ValueError` explicitly. A top-list
fetch failure returns `status: error`. Individual item failures are skipped.
The latter policy means a nominally successful result can contain fewer stories
than requested. A production consumer should compare the returned count with its
requirements; a caller must not infer that ten were retrieved merely because ten
were requested.

The source first attempts Pyodide's `open_url`, then falls back to `urllib`.
That code is observable. A successful browser run was not observed here; it remains
**(unverified)**. Reading an adapter is not equivalent to executing it under browser
network rules.

## 3.3 Errors are outputs

Return a repairable domain refusal as an error result. Surface infrastructure and
programming failures separately: the profile propagates exceptions, including a
corrupt memory file. "No matches" must not stand in for "backend unavailable."

## 3.4 Execution locations

Local, subprocess, and HTTP hosts can preserve the interface while changing
dependencies, credentials, timeouts, and persistence. The teaching loop is
synchronous and sequential, without cancellation, retries, or sandboxing.
Those are host facilities, not promises a description can enforce.

## 3.5 Exercises

**Exercise 3-1.** Add a maximum input size and test the exact accepted boundary.
Return a refusal that tells the caller how to retry.

**Exercise 3-2.** Read the story-fetch loop and specify when partial success is
acceptable. Design a result field that makes missing stories visible.

**Exercise 3-3.** Wrap a pure tool in an HTTP adapter. Keep request decoding,
domain validation, and transport failures distinguishable.

---

[← Chapter 2: The Interface](02-the-interface.md) · [Book contents](README.md) · [Chapter 4: The Transcript →](04-the-transcript.md)
