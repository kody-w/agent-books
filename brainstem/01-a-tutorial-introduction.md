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

The first line of output is `Draft follow-up for review`. A short message asks for
comments and confirmation of next steps; its evidence section contains the
library discussion verbatim. It is a useful starting artifact: someone can check
the source before turning it into a message. Nothing is sent.

Start with this small behavior rather than a model that can write plausible prose.
If you cannot prove which text the tool received, a polished draft makes the defect
harder to see. The fixture is synthetic; it carries no private chat history.

## 1.2 What the caller sees

Open [agent.py](examples/agent.py). `DraftFollowUp.metadata` contains three public
pieces: a name, a description, and an object schema with one required string,
`transcript`. The description says both what to do and what not to do.

The caller does not need to know about hashing or the template. An actual model-facing
host would translate the metadata into that model's tool declaration. Here
`MiniLoop.call()` is deliberately less ambitious: it checks the requested name and a
small subset of schema rules, invokes `perform()`, and records the result.

Read [mini_loop.py](examples/mini_loop.py) now. There is no model inside it.
Tests choose names explicitly. Consequently this example proves dispatch, validation,
and data movement; it says nothing about whether a particular model will select the
right tool from a vague request.

## 1.3 What execution returns

The result has `status`, `summary`, `instruction`, and `data_slush`.
`summary` is readable text. `instruction` says to review, not send.
`data_slush` contains the exact draft and the SHA-256 of the supplied text.
The digest gives the review artifact a source identity; it is not proof that the
source is true or that the draft is good.

The teaching profile uses Python dictionaries. The supplied production-style
Hacker News agent returns a JSON string. Those are different transport
representations of a similar boundary. Do not silently assume every host accepts
both; put serialization at its adapter.

## 1.4 Make it fail

Try a missing `transcript` key. The caller refuses before execution. Try an empty
string: the schema accepts a string, but `perform()` returns an error because there
is no useful text. Try an unknown name: no implementation runs.

These are three different failures. A schema checks shape, a tool checks domain
meaning, and a registry checks availability. Treating every refusal as "the model
did not understand" prevents you from repairing the right layer.

The example has no side effects beyond reading the fixture and printing output.
That is why rerunning it is safe. Adding a mail sender later would change this
property even if its interface looked almost identical.

## 1.5 Exercises

**Exercise 1-1.** Copy the fixture into a temporary directory, add one sentence,
and verify that both the draft and source digest change.

**Exercise 1-2.** Call the tool with an integer, an empty string, and an unknown
parameter. Identify which layer refuses each input.

**Exercise 1-3.** Rewrite the description for a new reader without changing its
schema or implementation. Explain what an offline test can and cannot tell you.

---

[← Preface](00-preface.md) · [Book contents](README.md) · [Chapter 2: The Interface →](02-the-interface.md)
