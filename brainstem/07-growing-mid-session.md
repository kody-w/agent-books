---
layout: book
title: Growing Mid-Session
book_label: Chapter 7
book_progress: 52
book_order: 70
description: Add reviewed capabilities without teaching the caller their implementation
---

[← Chapter 6: Memory](06-memory.md) · [Book contents](README.md) · [Chapter 8: Replay and Time Travel →](08-replay-and-time-travel.md)

# Chapter 7 — Growing Mid-Session

> **In this chapter:** load trusted code into a running registry, describe the
> LearnNew cycle, and distinguish installation from discovery.

## 7.1 Add a capability

Run `python3 brainstem/examples/07_growth.py`.

```python
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import MiniLoop, SOURCE, load_trusted_file

loop = MiniLoop()
del loop.tools["ReviewDraft"]
assert "ReviewDraft" not in loop.tools
loop.register(load_trusted_file(SOURCE))
print(loop.call("ReviewDraft", {"draft": "Library follow-up draft"})["summary"])
```

The registry changes while the caller object stays alive. We remove an already
known capability first only to make the before-and-after boundary visible.
The file is the reviewed, checked-in `agent.py`; the example does not download,
generate, or execute arbitrary remote code.

## 7.2 The learning cycle

The [source essay](../ref-blog-post.html) describes LearnNew returning a message
that a capability was created and will load on the next request.
The caller then sees the new declaration beside the old ones, without needing to
learn the implementation.

That is the intended cycle: create, validate, make available, advertise, invoke.
The installed LearnNew source and its production loader were inaccessible during
authoring, so automatic next-request hot loading is **(unverified)** here.
The runnable program proves only explicit import and registration in our profile.

A useful teaching example must say that plainly. A successful `importlib` call
does not prove that a separate host watches a directory or refreshes a live model's
tool inventory at the right boundary.

## 7.3 Installation is not discovery

Creating Python code, importing it, adding an instance to a registry, and exposing
its declaration to a model are four different actions.
Searching a catalog of existing tools changes visibility, not implementation.
Reloading a file can change implementation even when its name stays the same.

Track both the declaration and implementation identity when you care about replay.
A repeated tool name is not proof that the same code ran.
`MiniLoop.register()` rejects duplicate names rather than silently replacing an
existing instance, because an accidental overwrite would make the demonstration's
history ambiguous.

The caller should not need a special case for each learned agent. It should need a
general registry refresh and a normal call interface. New per-agent branches in
the host are a sign that implementation details are leaking across the boundary.

## 7.4 Import is execution

Python executes module-level code during import. Compilation proves syntax, not
safety. A generated file can read credentials before its class is even instantiated.
Review and permission checks therefore belong before loading, not after the first
tool result.

For an actual learning system, stage the file, validate its public declaration,
run bounded tests in an appropriate isolation boundary, approve its permissions,
then publish it to the active registry. Do not label code safe merely because a
model wrote it or its filename ends in `_agent.py`.

The miniature example intentionally omits an automatic code-generation facility.
Its purpose is to show capability availability without pretending that arbitrary
code generation has become harmless.

## 7.5 Exercises

**Exercise 7-1.** Attempt to register the same name twice and assert that it fails
without replacing the original object.

**Exercise 7-2.** Add declaration and source digests to the registration record.
Change one independently and observe the difference.

**Exercise 7-3.** Specify the approval boundary for a generated agent that needs
network access. Separate code review from credential assignment.

---

[← Chapter 6: Memory](06-memory.md) · [Book contents](README.md) · [Chapter 8: Replay and Time Travel →](08-replay-and-time-travel.md)
