---
layout: book
title: The Transcript
book_label: Chapter 4
book_progress: 31
book_order: 40
description: Record relevant results without loading implementation state
---

[← Chapter 3: Execution](03-execution.md) · [Book contents](README.md) · [Chapter 5: Output That Steers the Next Step →](05-output-that-steers.md)

# Chapter 4 — The Transcript

> **In this chapter:** examine a call record, preserve what downstream steps need,
> and separate the conversation view from the durable audit record.

## 4.1 Look at the record

Run `python3 brainstem/examples/04_transcript.py`.

```python
import json
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import MiniLoop

loop = MiniLoop()
loop.call("DraftFollowUp", {"transcript": "Please request a library review."})
event = loop.transcript[0]
assert set(event) == {"name", "arguments", "output"}
print(json.dumps(event, indent=2))
```

You will see the call name, supplied arguments, and returned output. You will not
see the method body, local variables, or private scratch work.

This is the fourth rule in practice. "Outputs only" refers to execution internals:
return the relevant product, not the machinery. A replayable conversation necessarily
also records what was asked. Removing the arguments would make exact replay impossible.

## 4.2 The conversation is a composition surface

Suppose the first result contains an approved working preference, the second contains
a draft, and the third contains a review. The next caller can use those outputs
without opening each tool's storage or knowing which internal helpers it called.
That is composition through a shared stream.

The teaching caller stores results but does not feed them to a model. Chapter 5
passes one field explicitly to make the transfer observable. A real host would
serialize results into the model's conversation format and let the model decide what
is useful next. Do not attribute that selection behavior to this name-dispatch fixture.

## 4.3 Copies matter

`MiniLoop.call()` deep-copies both arguments and results before recording them.
Without that copy, downstream code could mutate a dictionary after the call and
silently rewrite the apparent past. The original object returned to the caller
remains convenient to use, while the record preserves what actually crossed the boundary.

This is in-memory protection, not an append-only storage system or a signature.
Someone with access to the transcript list can still edit it. If an audit needs
tamper evidence, add an appropriate storage and integrity design; do not imply
that a list of dictionaries already provides it.

## 4.4 Context is not the archive

A model's active context is limited. Keep a complete, access-controlled archive
outside it, and present only the material relevant to the next decision.
Summarization, filtering, and retrieval are views over evidence, not permission
to erase the evidence itself.

For large tool results, put the bulk artifact in a controlled store, return a stable
identifier and a useful digest, and include the small part needed immediately.
If later reasoning requires omitted details, make a retrieval capability available.
Never replace a failed retrieval with a confident summary from stale memory.

The supplied ContextMemory agent demonstrates bounded presentation: individual
memory content is limited, and `system_context()` limits the injected text.
Those are context limits, not proof that all memories were recalled. Chapter 6
examines that distinction.

## 4.5 Exercises

**Exercise 4-1.** Mutate the returned result after a call. Assert that the stored
event does not change.

**Exercise 4-2.** Build a short presentation view and a full archive from the same
events. State which one is suitable for replay and why.

**Exercise 4-3.** Add a large synthetic artifact. Return a digest and a retrieval
identifier without placing the entire artifact in every event's summary.

---

[← Chapter 3: Execution](03-execution.md) · [Book contents](README.md) · [Chapter 5: Output That Steers the Next Step →](05-output-that-steers.md)
