---
layout: book
title: A Tutorial Introduction
book_label: Chapter 1
book_progress: 10
book_order: 10
description: Run a complete described agent against a real text file
---

[← Preface](00-preface.md) · [Book contents](README.md) · [Chapter 2: The Interface →](02-the-interface.md)

# Chapter 1 — A Tutorial Introduction

> **In this chapter:** read a chat file, call one agent, inspect its draft, and
> distinguish a deterministic test from model-driven selection.

## 1.1 Getting started

From the repository root, run `python3 brainstem/examples/01_hello.py`.
Here is the complete operation, also runnable from that root:

```python
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import FIXTURES, MiniLoop

text = (FIXTURES / "chat.txt").read_text(encoding="utf-8")
result = MiniLoop().call("DraftFollowUp", {"transcript": text})
assert result["status"] == "success"
print(result["summary"])
```

Output starts with `Draft follow-up for review`, asks for comments, and includes
the synthetic library discussion as evidence. Nothing is sent.

## 1.2 What the caller sees

Open [agent.py](examples/agent.py). `DraftFollowUp.metadata` contains three public
pieces: a name, a description, and an object schema with one required string,
`transcript`. The description says both what to do and what not to do.

`MiniLoop.call()` checks the requested name and a small schema subset, invokes
`perform()`, and records the result. The caller never needs the template internals.

Read [mini_loop.py](examples/mini_loop.py): explicit names test dispatch, validation,
and data movement, not a model's selection from a vague request.

The real loader needs a `name`, `to_tool()`, and `system_context()` as well.
`BasicAgent` supplies the last two; the standalone example does not inherit it.
The [live runner](../scripts/run_brainstem_live.py) therefore wraps the same draft
implementation in a small `BasicAgent` adapter. In the
[real chapter 1 turn](../fixtures/brainstem-live.json), the Copilot model selected
`DraftFollowUp`, the runtime executed it, and `agent_logs` contains its actual result.
This tests an explicitly named request, not selection from an ambiguous brief.
The model removed the file's final newline before constructing its tool argument:
the returned digest identifies that supplied argument, not the original file bytes.
Keep file hashes at the caller boundary when byte-exact provenance matters.

## 1.3 What execution returns

The result has `status`, `summary`, `instruction`, and `data_slush`.
`summary` is readable text. `instruction` says to review, not send.
`data_slush` contains the exact draft and the SHA-256 of the supplied text.
The digest gives the review artifact a source identity; it is not proof that the
source is true or that the draft is good.

The profile returns dictionaries; the news agent returns JSON text.
The host adapter must serialize the chosen representation.

## 1.4 Make it fail

Try a missing `transcript` key. The caller refuses before execution. Try an empty
string: the schema accepts a string, but `perform()` returns an error because there
is no useful text. Try an unknown name: no implementation runs.

The registry checks availability, the schema checks shape, and the method checks
meaning. Rerunning is safe because the tool cannot send anything.

## 1.5 Exercises

**Exercise 1-1.** Copy the fixture into a temporary directory, add one sentence,
and verify that both the draft and source digest change.

**Exercise 1-2.** Call the tool with an integer, an empty string, and an unknown
parameter. Identify which layer refuses each input.

**Exercise 1-3.** Rewrite the description for a new reader without changing its
schema or implementation. Explain what an offline test can and cannot tell you.

---

[← Preface](00-preface.md) · [Book contents](README.md) · [Chapter 2: The Interface →](02-the-interface.md)
