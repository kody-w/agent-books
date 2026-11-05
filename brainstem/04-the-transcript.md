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

A next step consumes outputs without opening the preceding tool's storage.
The teaching caller stores results; chapter 5 explicitly passes one field.
A model-facing host instead serializes results into the conversation.

The inspected runtime does exactly that serialization: `run_tool_calls()`
(`brainstem.py:2180–2230`) invokes `perform(**args)` and puts `str(result)` in a
tool message with its call ID. The live adapter returns JSON text deliberately;
a raw Python dictionary would become Python `repr`, not JSON. `/chat` returns
response text and readable `agent_logs`, not the complete internal `messages` array.
Keep caller-owned input/output records if later replay needs them.

## 4.3 Copies matter

`MiniLoop.call()` deep-copies arguments and results so later mutation of a returned
dictionary does not rewrite the record. The transcript list remains editable:
copying is not tamper evidence. Chapter 9 describes the framing boundary.

## 4.4 Context is not the archive

Keep the complete archive outside limited model context. Large artifacts can stay
in a controlled store while results carry identifiers, digests, and useful extracts.
Summaries and bounded memory recall are presentation views, not complete archives;
chapter 6 examines those bounds.

## 4.5 Exercises

**Exercise 4-1.** Mutate the returned result after a call. Assert that the stored
event does not change.

**Exercise 4-2.** Build a short presentation view and a full archive from the same
events. State which one is suitable for replay and why.

**Exercise 4-3.** Add a large synthetic artifact. Return a digest and a retrieval
identifier without placing the entire artifact in every event's summary.

---

[← Chapter 3: Execution](03-execution.md) · [Book contents](README.md) · [Chapter 5: Output That Steers the Next Step →](05-output-that-steers.md)
