---
layout: book
title: The Interface
book_label: Chapter 2
book_progress: 17
book_order: 20
description: Design names, descriptions, and parameter schemas without coupling the caller
---

[← Chapter 1: A Tutorial Introduction](01-a-tutorial-introduction.md) · [Book contents](README.md) · [Chapter 3: Execution →](03-execution.md)

# Chapter 2 — The Interface

> **In this chapter:** publish the smallest useful contract, write selection
> descriptions, and separate invitation, validation, and authority.

## 2.1 Read the declaration first

Run `python3 brainstem/examples/02_interface.py`. To inspect the same declaration:

```python
import json
import sys
sys.path.insert(0, "brainstem/examples")
from agent import DraftFollowUp

print(json.dumps(DraftFollowUp.metadata, indent=2))
assert DraftFollowUp.metadata["parameters"]["required"] == ["transcript"]
```

Name the capability, not its internals: `DraftFollowUp`, not `ReadFileThenFormatV3`.
Describe when to call and what result to expect.

## 2.2 Description and schema

The source [Hacker News agent](../ref-hacker_news_agent.py) describes its selection
conditions directly:

```text
"Use when the user asks what's on Hacker News, what's trending in tech,
or for news headlines."
```

Its `count` schema bounds an integer from 1 to 30. Asking for five does not require
knowing the network implementation.

The draft takes free text to preserve qualifications and corrections. Reserve enums
for genuinely finite choices, such as an output format.

The miniature caller supports required fields, unknown-field rejection, and strings.
It is **not** a JSON Schema implementation. A production adapter must use its host's
validator or an appropriate schema library; do not extend a few `if` statements
until they impersonate a standard.

## 2.3 Liberty is not authorization

Freedom to supply information is not permission to read files or send messages.
Enforce authority outside model-supplied arguments.

In the memory writer's real metadata, `memory_type` is an enum, `importance` has a
range, and `user_guid` is optional. A user identifier is a scope hint, not proof of
identity. A multi-user host must bind scope to authenticated identity outside the
model's discretion. Our examples avoid that issue by storing only synthetic,
single-user working notes.

## 2.4 A file is not necessarily a tool

An executable declaration, a skill procedure, and a delegated model's configuration
are distinct surfaces. This profile parses neither skills nor subagent frontmatter.
The chapters' Jekyll headers control publication only; the companion book shows
Claude's runtime formats.

## 2.5 Exercises

**Exercise 2-1.** Add an optional tone field to the declaration and implementation.
Decide whether arbitrary text or an enum is justified, and test the decision.

**Exercise 2-2.** Write two descriptions that differ only in the phrase "never send."
Explain why neither description can replace removing the sending capability.

**Exercise 2-3.** Document the exact subset of schema rules the miniature caller
enforces. Give a valid JSON Schema keyword it deliberately does not implement.

---

[← Chapter 1: A Tutorial Introduction](01-a-tutorial-introduction.md) · [Book contents](README.md) · [Chapter 3: Execution →](03-execution.md)
