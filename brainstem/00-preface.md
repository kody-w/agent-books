---
layout: book
title: Preface
book_label: Preface
book_progress: 4
book_order: 0
description: A tutorial and reference for the agent.py programming pattern
concepts: [{"name":"Described executable capability","chapter":"01-a-tutorial-introduction.md","section":"1.2 What the caller sees"}]
hosts: ["Local CPython", "Pyodide/browser", "Copilot Studio"]
---

[Book contents](README.md) · [Chapter 1: A Tutorial Introduction →](01-a-tutorial-introduction.md)

# The Brainstem Agent Programming Language

### A tutorial, programming workbook, and field reference

*Docs as of 2026-11-05. This book teaches a programming pattern, not a new Python
grammar. Its examples are an explicitly labeled teaching profile.*

> **In this chapter:** meet the unit, the caller, the transcript, and the evidence
> that separates a working example from a claim about a production host.

## 0.1 Begin with a file

An agent is a capability that a caller can select without learning its implementation.
The caller sees a name, a description, and parameters. Code does the work. Its result
returns to the conversation, where the next step can use it.

Python supplies the grammar; the pattern supplies this one boundary.
The [news](../ref-hacker_news_agent.py), [memory writer](../ref-manage_memory_agent.py),
and [memory reader](../ref-context_memory_agent.py) sources make it concrete.

## 0.2 Six rules

The [source essay](../ref-blog-post.html) gives six rules. Here they are as working
discipline rather than slogans:

1. **The caller knows nothing about the inside.** Publish the interface, not storage
   layout, internal prompts, or implementation branches.
2. **The description is the whole interface.** Explain when to call, what to supply,
   what comes back, and what must not happen. The schema gives the machine-checkable shape.
3. **The caller has full liberty.** Accept useful material you did not anticipate;
   constrain only what correctness or permission actually requires.
4. **The transcript carries only outputs.** Do not dump private execution state into
   the conversation. Preserve the relevant result, including failures.
5. **The agent writes the next prompt.** Return a readable piece, useful next-step
   guidance, and structured data instead of making the next caller reconstruct them.
6. **You can time travel.** Record inputs and implementation identity so a selected
   step can be run again with later evidence, without erasing the original.

The fourth rule concerns what crosses the execution boundary. A replay archive still
needs call names and arguments. It is not a literal ban on user inputs, tool calls,
or the assistant's ordinary messages.

## 0.3 How to read

Chapters 1–5 teach interface, execution, transcript, and handoff. Chapters 6–9
apply that boundary to memory, growth, replay, and hosts. Chapter 10 assembles the
library follow-up shared with the Claude book. Appendices supply reference,
vocabulary, and the chapter map.

The ten numbered programs run with Python alone. `mini_loop.py` is a deterministic
test caller: you supply the tool name. It is not a model or the full runtime.
The draft is an evidence-preserving template, not generated prose.

## 0.4 Evidence and limits

The installed `brainstem.py`, `BasicAgent`, LearnNew, and memory agents were read
without changing the installation. Chapters 1, 5, 7, and 10 also ran through a real
model and `/chat` in a temporary, book-only runtime. The
[recorded fixture](../fixtures/brainstem-live.json) preserves the synthetic requests,
responses, and tool outputs. LearnNew created and exposed a new tool on the next
turn, but its code-generation command failed and used its stock scaffold instead.
That is a hot-load observation, not a successful implementation of the requested behavior.

The stdlib examples remain a small deterministic teaching caller. Browser execution
and Copilot Studio deployment are **(unverified)**. No example establishes
sandboxing, production durability, or semantic drafting quality.

## 0.5 Counts

<!-- book-counts:start -->
| Book | Concepts | Hosts | Words | Examples |
|---|---:|---:|---:|---:|
| Brainstem | 1 | 3 | 8172 | 11 |
| Claude | 69 | 7 | 17953 | 71 |
<!-- book-counts:end -->

---

[Book contents](README.md) · [Chapter 1: A Tutorial Introduction →](01-a-tutorial-introduction.md)
