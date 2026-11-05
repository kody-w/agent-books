---
layout: book
title: Preface
book_label: Preface
book_progress: 4
book_order: 0
description: A tutorial and reference for the agent.py programming pattern
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

This book calls that arrangement a language because it has recurring forms and
composition rules. Python supplies the executable grammar. The agent pattern supplies
the boundary: describe what can be done, keep execution behind that description, and
make the result useful to whoever reads it next.

The supplied [Hacker News agent](../ref-hacker_news_agent.py) makes the arrangement
concrete. Its metadata describes fetching stories; its `perform()` fetches and shapes
them; its return value contains a linked summary and structured records. The
[memory writer](../ref-manage_memory_agent.py) and
[memory reader](../ref-context_memory_agent.py) show persistence and context injection.
These are source evidence, not dependencies of the book's examples.

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

Run chapter 1, then read chapters 2 through 5 as one unit: interface, execution,
transcript, and handoff. Chapters 6 through 9 add memory, growth, replay, and hosts.
Chapter 10 assembles the same library follow-up task as the companion Claude book.
Appendix A is the working reference; B names the terms; C maps chapters without ranking
the systems. Keep both chapter N pages open when comparing.

The ten numbered programs run with Python alone. `mini_loop.py` is a deterministic
test caller: you supply the tool name, and it dispatches that name. It does not choose
tools intelligently, contact a model, or implement the full Brainstem runtime.
The draft is deliberately an evidence-preserving template, not generated prose.

## 0.4 Evidence and limits

Local access to `~/.brainstem/src/rapp_brainstem/` was unavailable during authoring.
Installed loader behavior, the concrete `LearnNew` implementation, and working
Copilot Studio and Pyodide adapters are **(unverified)**. They are identified again
where relevant; this book does not present its small caller as proof of those hosts.
The requested local reference-book directory was also inaccessible; its five named
files were read from the public `kody-w/rapp-1` repository instead.

The shipped examples establish the portable pattern and selected failure behavior.
They do not establish sandboxing, production durability, or semantic drafting quality.
That separation is part of the lesson: know exactly what your evidence proves.

---

[Book contents](README.md) · [Chapter 1: A Tutorial Introduction →](01-a-tutorial-introduction.md)
