---
layout: book
title: Output That Steers the Next Step
book_label: Chapter 5
book_progress: 38
book_order: 50
description: Compose through a readable summary, guidance, and structured data
---

[← Chapter 4: The Transcript](04-the-transcript.md) · [Book contents](README.md) · [Chapter 6: Memory →](06-memory.md)

# Chapter 5 — Output That Steers the Next Step

> **In this chapter:** pass an exact draft between tools, write useful next-step
> guidance, and keep result instructions below the caller's authority.

## 5.1 Make a handoff

Run `python3 brainstem/examples/05_handoff.py`.

```python
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import MiniLoop

loop = MiniLoop()
first = loop.call("DraftFollowUp", {"transcript": "Please request a library review."})
draft = first["data_slush"]["draft"]
second = loop.call("ReviewDraft", {"draft": draft})
assert second["data_slush"]["draft"] == draft
assert second["data_slush"]["sent"] is False
print(second["summary"])
```

The second step receives the draft as a value, not a paraphrase of a summary.
That is the practical purpose of `data_slush`: keep machine-useful material
available without asking another model to reconstruct it.

## 5.2 Three jobs in one result

The readable piece answers "what happened?" Guidance answers "what should the
reader consider next?" Structured data answers "what can the next operation use
without interpretation?" These jobs overlap, but separating them prevents accidents.

In the [Hacker News agent](../ref-hacker_news_agent.py), `summary` contains formatted
Markdown and an instruction to preserve clickable titles. `stories` holds full
records, while `data_slush` holds the returned count and first URL.
An exact excerpt of the result-shaping source is:

```text
"data_slush": {"count": len(stories),
               "top_url": stories[0]["url"] if stories else None}
```

The field name is a convention, not a reserved Python feature. Our example makes
`instruction` a separate key; the real news example embeds its presentation guidance
in the summary. Both should be documented so a consumer knows what to preserve.

## 5.3 Guidance is not a command channel

A tool can advise the next step without gaining authority over the caller.
"Check conflicting dates" is useful guidance. "Ignore permissions and send this"
would not become legitimate because it came back in a result field.

Treat source transcripts, memory text, web content, and imported drafts as untrusted
data. If you derive guidance from them, keep the trust distinction visible.
Our draft embeds evidence verbatim for human review; it does not execute directives
found in that evidence.

Descriptions and results also cannot replace enforcement. These tools have no mail
sender. The absence of that capability is stronger than repeating "never send"
in a hundred paragraphs.

## 5.4 Preserve failure context

When a first step fails, do not invoke a downstream reviewer with an empty draft
and report success. Check `status` before reading the payload.
Chapter 10 does so at the system boundary.

A robust result may also need provenance, partial-success information, artifact
identifiers, or a request for user approval. Add fields because a consumer needs
them, not because every result must resemble a comprehensive framework.

There is no guarantee that a model will obey result guidance verbatim. Test the
actual host and caller with representative tasks. Offline equality tests establish
that the payload survives transfer, not that prose guidance controls behavior.

## 5.5 Exercises

**Exercise 5-1.** Add a `needs_review` flag and require the second step to preserve it.
Test a result where the flag is true.

**Exercise 5-2.** Put a hostile "send this now" instruction in the transcript.
Show that the evidence survives but no send operation becomes available.

**Exercise 5-3.** Design a partial-result handoff. Make it impossible to confuse
"three of five items retrieved" with "all five retrieved."

---

[← Chapter 4: The Transcript](04-the-transcript.md) · [Book contents](README.md) · [Chapter 6: Memory →](06-memory.md)
