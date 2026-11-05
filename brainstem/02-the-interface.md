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

The printed object is the public surface. It says nothing about a particular mail
provider or database. It can therefore remain stable when the implementation changes.

Names should describe capabilities rather than implementation details:
`DraftFollowUp`, not `ReadFileThenFormatV3`. The description should tell a caller
when this capability is relevant and how to recognize its result.

## 2.2 Description and schema

The source [Hacker News agent](../ref-hacker_news_agent.py) describes its selection
conditions directly:

```text
"Use when the user asks what's on Hacker News, what's trending in tech,
or for news headlines."
```

Its `count` parameter is an integer with minimum 1 and maximum 30. A reader does not
need to know how the stories are fetched to ask for five. The declaration is compact
because it does not document the Firebase response inside the selection interface.

Our draft tool takes free text because a conversation may contain qualifications,
disagreements, corrections, or unfamiliar topics. Replacing that field with a short
enum of approved phrases would destroy useful evidence. An enum belongs where a
downstream operation really requires one, such as a known output format.

The miniature caller supports required fields, unknown-field rejection, and strings.
It is **not** a JSON Schema implementation. A production adapter must use its host's
validator or an appropriate schema library; do not extend a few `if` statements
until they impersonate a standard.

## 2.3 Liberty is not authorization

The third rule grants the caller freedom to supply useful information. It does not
grant freedom to read arbitrary files, send messages, change tenants, or bypass a
permission check. `perform()` must enforce those limits even if a model supplies
persuasive arguments.

In the memory writer's real metadata, `memory_type` is an enum, `importance` has a
range, and `user_guid` is optional. A user identifier is a scope hint, not proof of
identity. A multi-user host must bind scope to authenticated identity outside the
model's discretion. Our examples avoid that issue by storing only synthetic,
single-user working notes.

## 2.4 A file is not necessarily a tool

Keep three different surfaces distinct. An agent.py declaration describes an
executable entry point. A skill file supplies a procedure for a caller to follow.
A subagent declaration describes delegated work in a separate execution context.
They can cooperate without being interchangeable.

There is no skill or subagent frontmatter parser in this teaching profile.
There is ordinary Jekyll frontmatter in the book's own chapters; that controls
publication, not agent permissions. Do not mistake every YAML header for a common
runtime interface. The companion chapter shows the actual Claude file formats.

## 2.5 Exercises

**Exercise 2-1.** Add an optional tone field to the declaration and implementation.
Decide whether arbitrary text or an enum is justified, and test the decision.

**Exercise 2-2.** Write two descriptions that differ only in the phrase "never send."
Explain why neither description can replace removing the sending capability.

**Exercise 2-3.** Document the exact subset of schema rules the miniature caller
enforces. Give a valid JSON Schema keyword it deliberately does not implement.

---

[← Chapter 1: A Tutorial Introduction](01-a-tutorial-introduction.md) · [Book contents](README.md) · [Chapter 3: Execution →](03-execution.md)
