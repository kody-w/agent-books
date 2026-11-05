---
layout: book
title: Glossary
book_label: Appendix B
book_progress: 91
book_order: 120
description: Vocabulary and common boundary mistakes
---

[← Appendix A: Reference Manual](A-reference-manual.md) · [Book contents](README.md) · [Appendix C: Mapping Table →](C-mapping-table.md)

# Appendix B — Glossary

> **In this chapter:** name the boundaries precisely enough to diagnose a failure.

## B.1 Vocabulary

| Term | Meaning in this book |
|---|---|
| Agent | Described executable capability with hidden implementation and returned output. |
| Agent.py pattern | Metadata, `perform()`, and output convention carried in a Python unit. |
| Caller | Component that receives declarations and requests execution. A model-facing host and a deterministic test dispatcher are different callers. |
| Declaration | Name, description, and parameter schema visible before invocation. |
| Description | Selection guidance and semantic contract, not executable authorization. |
| Schema | Machine-readable argument shape; it does not prove a task is permitted or meaningful. |
| `perform()` | Hidden execution entry point. |
| Result | The relevant product or explicit error that crosses the execution boundary. |
| Summary | A readable account or artifact intended for the next reader. |
| Instruction | Next-step guidance carried with output, subordinate to caller policy. |
| `data_slush` | Convention for values that downstream operations should use without paraphrase. |
| Transcript | Inputs, calls, and relevant outputs; not a dump of internal tool state. |
| Archive | Durable record sufficient to identify a prior call and its implementation. |
| Context | The selected material actually presented to a model at one turn. |
| Memory | Persisted information, distinct from its current presentation in context. |
| `system_context()` | Optional method producing pre-turn context in the supplied agent pattern. |
| Scope | The authenticated storage or execution boundary; not merely a model-supplied user identifier. |
| LearnNew | Agent generator that writes beside its own source; creation and next-turn invocation were observed, with a stock scaffold fallback. |
| Conversation statelessness | The core reconstructs each conversation from caller-supplied history, not a session-ID lookup; files and optional memory still persist. |
| RAPP/1 frame | Protocol event envelope with canonical payload/frame addresses and chain rules; not emitted automatically by this runtime. |
| Hot load | Making a new implementation or declaration available without replacing the whole caller. |
| Discovery | Revealing existing capabilities; not necessarily creating or installing code. |
| Replay | Re-executing a selected recorded operation. |
| Rewind | Restoring an earlier state rather than rerunning an operation. |
| Fork | Preserving the original history while creating a branch. |
| Idempotency | Repeating an operation has no additional effect under its declared key or semantics. |
| Host adapter | Mapping declarations, calls, results, and permissions to a concrete runtime. |
| Teaching profile | The deliberately small, stdlib-only implementation shipped with this book. |

## B.2 Failure vocabulary

An **unknown tool** is a registry failure. A **missing argument** is a call-shape
failure. An **empty transcript** is a domain refusal. A **corrupt store** is an
execution failure. A **source digest mismatch** is a replay refusal.

A **selection failure** occurs when a model chooses the wrong capability.
The miniature caller cannot exhibit or measure that failure because names are
selected explicitly. A **quality failure** occurs when an artifact is misleading,
unhelpful, or unsupported even though its structure and transport were valid.

These categories are intentionally separate. Repairing a schema will not fix an
unauthorized backend, and increasing a model's context will not make a corrupt
archive accurate.

## B.3 Exercises

**Exercise B-1.** Classify five failures in a system you build. For each, name the
layer that should refuse and the evidence a caller should receive.

---

[← Appendix A: Reference Manual](A-reference-manual.md) · [Book contents](README.md) · [Appendix C: Mapping Table →](C-mapping-table.md)
