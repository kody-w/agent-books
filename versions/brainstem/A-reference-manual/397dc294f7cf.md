---
layout: book
title: Brainstem Reference Manual
book_label: Appendix A
book_progress: 82
book_order: 110
description: Terse reference for the agent.py pattern and the book teaching profile
---

[← Chapter 10: Building a Real System End to End](10-building-a-real-system.md) · [Book contents](README.md) · [Appendix B: Glossary →](B-glossary.md)

# Appendix A — Brainstem Reference Manual

> **In this chapter:** look up the declaration, execution, result, memory, and replay
> contracts without mistaking the teaching caller for a production runtime.

## A.1 Declaration

The supplied source agents expose `metadata` containing `name`, `description`, and
`parameters`. `parameters` is a JSON Schema object. `perform(self, **kwargs)` is the
execution entry point. Supplied agents derive from `agents.basic_agent.BasicAgent`;
the book's standalone agents deliberately do not require that dependency.

| Surface | Meaning | Teaching profile |
|---|---|---|
| `name` | selection identity | unique registry key |
| `description` | when, inputs, outcome, boundaries | published verbatim |
| `parameters` | argument shape | required fields, strings, unknown keys |
| `perform()` | hidden work | synchronous dictionary result |
| `system_context()` | optional pre-turn context | explicitly called by the example |

The profile validates only its documented subset. There is no general schema
coercion or default insertion. Domain validation remains in the method.

## A.2 Result

Success uses `status: success`. A recoverable domain refusal uses `status: error`
with `message`. Successful draft results carry `summary`, `instruction`, and
`data_slush`; these field names are book conventions, not universal host requirements.

The supplied Hacker News source returns JSON text, full `stories`, a formatted
summary with presentation guidance, and a small `data_slush`. The memory writer
returns human-readable text. Normalize such representations in the host adapter
without losing explicit failure semantics.

Instructions in returned content are guidance under the caller's existing authority.
They do not override permissions. Treat retrieved material as untrusted data.

## A.3 MiniLoop

`MiniLoop()` installs the draft and reviewer. `register(agent)` rejects a duplicate
name. `call(name, arguments)` validates the teaching subset, invokes the method,
deep-copies the event, and returns the result. Unknown names and invalid call shapes
raise `ValueError`. Unexpected execution failures propagate.

The event shape is exactly `name`, `arguments`, and `output`. The caller is
deterministic dispatch, not a model simulator. It has no automatic memory injection,
background workers, permissions engine, or general-purpose isolation boundary.

## A.4 Memory

The real writer creates records through `memory_store.insert_memory`.
The real reader uses `count_memories` and `list_memories`. Its automatic context
limits are 50 messages and 12,000 characters; explicit recall caps at 100 messages,
with individual content limited to 2,000 characters.

The teaching `MemoryAgent(path)` stores one JSON note and returns a JSON-quoted
presentation through `system_context()`. It is single-user demonstration storage.
Malformed storage raises rather than becoming an empty recall.

## A.5 Growth and replay

`load_trusted_file(path)` imports reviewed Python and instantiates `ReviewDraft`.
Importing executes code; there is no safety guarantee from successful compilation.
Automatic installed LearnNew and loader behavior is **(unverified)**.

`save(path)` writes `schema: book-replay/1.0`, `source_sha256`, and `events`.
`replay(archive, index, later)` requires that schema, the current `agent.py` digest,
and a `DraftFollowUp` event. It copies arguments, appends later evidence, and calls
only that step. Archive mutation and arbitrary side-effect replay are not permitted.

Exact deterministic replay requires the matching source and environment.
Re-executing a model or network call does not guarantee identical results.

## A.6 Operating checklist

Before deploying, establish authenticated scope, allowed operations, dependency
versions, timeouts, data retention, error mapping, and tests for each destination.
Local runtime lifecycle, Pyodide deployment, and Copilot Studio integration remain
**(unverified)** in this edition.

## A.7 Exercises

**Exercise A-1.** Write a conformance checklist for one new agent without adding
agent-specific branches to the caller.

---

[← Chapter 10: Building a Real System End to End](10-building-a-real-system.md) · [Book contents](README.md) · [Appendix B: Glossary →](B-glossary.md)
