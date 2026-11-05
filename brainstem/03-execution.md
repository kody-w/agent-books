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

This is a complete execution test without a model or caller. It establishes that
the tool refuses semantically empty input even when invoked directly.

`perform()` is where the public promise becomes work. In our example it validates
text, hashes the exact input, assembles a draft, and returns a structured result.
Neither hashing nor template details belong in the selection description.

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

Use an error result for an expected domain refusal that a caller can repair.
Use an exception for an infrastructure or programming failure that the host must
surface. Our miniature caller does not broadly catch exceptions and pretend that
work succeeded. A corrupt memory file, for example, raises a decoding error.

Avoid empty-list fallbacks for failed operations. "No records matched" and
"the backend was unavailable" imply different next steps. Give the next caller
enough information to distinguish them without revealing secrets or stack traces
to an untrusted audience.

## 3.4 Execution locations

A Python method can run locally, behind an HTTP service, or inside another process.
The caller's contract need not change, but filesystem paths, credentials,
timeouts, dependency availability, and persistence do.

A helper script is not a separate agent simply because it has a file extension.
A delegated model is not deterministic simply because its invocation is wrapped
in Python. Hooks are host callbacks, not a substitute for tool validation.
Name these boundaries accurately when documenting a deployed system.

The book's loop runs synchronously and sequentially. There is no concurrency,
cancellation, network retry, or sandbox. Adding those facilities belongs in the
host, with explicit timeout and failure rules, rather than in a description that
only hopes execution will be safe.

## 3.5 Exercises

**Exercise 3-1.** Add a maximum input size and test the exact accepted boundary.
Return a refusal that tells the caller how to retry.

**Exercise 3-2.** Read the story-fetch loop and specify when partial success is
acceptable. Design a result field that makes missing stories visible.

**Exercise 3-3.** Wrap a pure tool in an HTTP adapter. Keep request decoding,
domain validation, and transport failures distinguishable.

---

[← Chapter 2: The Interface](02-the-interface.md) · [Book contents](README.md) · [Chapter 4: The Transcript →](04-the-transcript.md)
