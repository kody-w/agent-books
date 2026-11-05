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

The profile relies on the checked-in caller and Python environment. It does not
pin interpreter binaries, imported dependencies, external responses, clocks, or a
production runtime. Because the draft method uses only supplied text and standard
hashing, this is a manageable teaching boundary. A network tool would need recorded
responses or a clear statement that it is performing a fresh observation.

Hashing a file identifies bytes; it does not preserve those bytes forever.
Archive the corresponding revision or source artifact if replay must work after
the working tree changes.

## 8.3 Replay is not rewind

Rewind restores a selected prior state. Replay executes a selected prior operation.
A fork preserves history and continues along a new branch. These can be combined,
but their effects differ.

Our function copies the arguments and appends later evidence. It does not mutate
the source archive or erase the earlier result. Rerunning the whole program is not
equivalent: it might repeat later side effects or make different choices before the
selected step.

In particular, "static caller" does not make a model deterministic. If the operation
calls a model, new sampling or a model update may change the result. Distinguish
the ability to resubmit a recorded step from a guarantee of byte-identical output.

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
