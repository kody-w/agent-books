---
layout: book
title: Replay and Time Travel
book_label: Chapter 8
book_progress: 59
book_order: 80
description: Re-execute one recorded pure step with later evidence
---

[← Chapter 7: Growing Mid-Session](07-growing-mid-session.md) · [Book contents](README.md) · [Chapter 9: Hosts and Portability →](09-hosts-and-portability.md)

# Chapter 8 — Replay and Time Travel

> **In this chapter:** save a call, replay just its draft step, preserve the
> original result, and refuse a changed implementation.

## 8.1 Run the past step again

Run `python3 brainstem/examples/08_replay.py`.

```python
import copy
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import MiniLoop, source_hash

loop = MiniLoop()
original = loop.call("DraftFollowUp", {"transcript": "Comments due Friday."})
archive = {"schema": "book-replay/1.0", "source_sha256": source_hash(),
           "events": copy.deepcopy(loop.transcript)}
replayed = loop.replay(archive, 0, "Deadline changed to Monday.")
assert "Monday" not in original["summary"]
assert "Monday" in replayed["summary"]
assert len(archive["events"]) == 1
print(replayed["summary"])
```

One recorded operation runs again with appended evidence. No reviewer runs.
The original still says Friday; the new draft contains the correction as well.
The template does not resolve that conflict automatically. It preserves the
evidence so a human or a separately tested drafting step can resolve it.

## 8.2 What must be fixed

A useful replay record identifies the tool, exact arguments, result, and implementation.
Our archive stores all four and a schema version. Its source hash covers `agent.py`.
If that file changes, `replay()` refuses rather than quietly claiming to reproduce
the old implementation.

The profile pins neither interpreter nor external responses. Its pure draft method
needs only supplied text and standard hashing. A network tool must distinguish
recorded responses from fresh observations. Preserve the matching source artifact:
a digest identifies bytes but does not store them.

## 8.3 Replay is not rewind

Rewind restores a selected prior state. Replay executes a selected prior operation.
A fork preserves history and continues along a new branch. These can be combined,
but their effects differ.

The function copies arguments and appends evidence without mutating the archive.
Rerunning the whole system could repeat side effects; resubmitting a model call
could change its result. Selected-step replay promises neither undo nor deterministic
model output.

## 8.4 Side effects set the boundary

The replay function only allows `DraftFollowUp`. It rejects `ReviewDraft` and all
other names in this teaching profile, even though our reviewer is currently pure.
This allowlist makes the intended boundary explicit.

For sending mail, charging a card, or writing to a shared system, use explicit
approval and idempotency keys. A transcript alone cannot undo an external effect.
Treat "time travel" as a metaphor for controlled re-execution, not reversal of the
world outside the program.

## 8.5 Exercises

**Exercise 8-1.** Change the recorded source digest and verify refusal before any
event is added.

**Exercise 8-2.** Replay in a fresh process using a serialized archive. Compare the
unchanged-input result with the original byte for byte.

**Exercise 8-3.** Design a replay policy for an HTTP lookup. Decide whether it uses
a captured response or current data, and label that choice in its result.

---

[← Chapter 7: Growing Mid-Session](07-growing-mid-session.md) · [Book contents](README.md) · [Chapter 9: Hosts and Portability →](09-hosts-and-portability.md)
