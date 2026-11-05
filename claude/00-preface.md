---
layout: book
title: Preface
book_label: Preface
book_progress: 4
book_order: 0
description: A tutorial and reference across Claude tools, skills, agents, and hosts
---

[Book contents](README.md) · [Chapter 1: A Tutorial Introduction →](01-a-tutorial-introduction.md)

# The Claude Agent Programming Language

### A tutorial, programming workbook, and field reference

*Docs as of 2026-11-05. "Language" names a family of programming interfaces, not an
Anthropic product or a new Python grammar.*

> **In this chapter:** distinguish the products, choose the right executable unit,
> and understand what the book's examples and citations establish.

## 0.1 Begin with a capability

Claude can call a capability from its name, description, and schema without seeing
the implementation. Your application executes a client tool; Anthropic executes a
server tool. This is the ordinary tool-use boundary, not a feature confined to
skills or subagents. [Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

Claude also offers several ways to organize work. Skills load procedures when
relevant; subagents perform delegated work in separate contexts; hooks run at
defined lifecycle events; the Agent SDK exposes the Claude Code agent loop to
applications. Use those differences rather than forcing everything into one file
format. [Skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents),
[hooks](https://code.claude.com/docs/en/hooks),
[Python Agent SDK](https://code.claude.com/docs/en/agent-sdk/python).

This book treats those mechanisms as a coherent programming vocabulary. It begins
with a complete tool round trip, then shows when to move execution to a server,
delegate context-heavy work, package procedures, retain memory, or resume a session.
The host remains explicit throughout.

## 0.2 A map of hosts

The Messages API is the application-owned request/response surface. Claude Code
provides an existing coding host. The Agent SDK lets an application configure that
agent loop and add tools. Managed Agents supplies hosted, stateful sessions and
configurable tools. These are distinct execution contracts.
[Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[SDK reference](https://code.claude.com/docs/en/agent-sdk/python),
[Managed Agents tools](https://platform.claude.com/docs/en/managed-agents/tools.md).

Cowork brings the agentic architecture to knowledge work without a terminal;
claude.ai supports uploaded and managed skills; Claude in Chrome connects browser
actions to a signed-in browser. Their permissions and availability are
host-specific. [Cowork](https://support.claude.com/en/articles/13345190-getting-started-with-cowork),
[Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude),
[Chrome](https://code.claude.com/docs/en/chrome).

## 0.3 How to read

Read chapters 1 through 5 as one unit: interface, execution, transcript, and
handoff. Chapters 6 through 9 cover memory, growth, replay, and hosts.
Chapter 10 builds the same library follow-up task as the companion Brainstem book.
Appendix A is a terse reference, B a glossary, and C a concept map with no verdict.

The ten numbered programs use the official `anthropic` Python SDK or
`claude-agent-sdk`. The model identifier is `claude-opus-5-5`, as in the fetched
tool-use documentation. Install dependencies in a virtual environment and use
your own API key only for synthetic or otherwise authorized inputs.
[SDK examples and model](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## 0.4 Evidence and limits

Product claims cite fetched Anthropic documentation inline. The source essay's
comparison was a research starting point, not permission to repeat uncited claims.
Application guidance and book conventions are identified as such.

The offline tests compile all Python fences and import the example modules when
the declared SDK dependencies are installed. They do not impersonate a successful
API call. Live authenticated execution of API and Agent SDK examples is
**(unverified)** unless the explicit live test is enabled with a key.
Server-tool availability and account access are not established by compilation.

Our drafting tool produces an evidence-preserving template; it does not pretend
that a deterministic fixture is model-generated prose. The live model selects and
calls tools. Those mechanics and the semantic quality of a future drafting model
need different evaluations.

---

[Book contents](README.md) · [Chapter 1: A Tutorial Introduction →](01-a-tutorial-introduction.md)
