---
layout: book
title: Preface
book_label: Preface
book_progress: 4
book_order: 0
description: A tutorial and reference across Claude tools, skills, agents, and hosts
concepts: [
  {"name":"client tools","chapter":"02-the-interface.md","section":"2.1 Client tools: publish an executable boundary"},
  {"name":"tool_choice","chapter":"02-the-interface.md","section":"2.5 tool_choice: control selection without granting authority"},
  {"name":"web search","chapter":"03-execution.md","section":"3.5 Server tools: web search"},
  {"name":"web fetch","chapter":"03-execution.md","section":"3.6 Server tools: web fetch"},
  {"name":"code execution","chapter":"03-execution.md","section":"3.1 Server tools: code execution"},
  {"name":"tool runner","chapter":"03-execution.md","section":"3.7 Tool runner: let the SDK maintain the loop"},
  {"name":"programmatic tool calling","chapter":"04-the-transcript.md","section":"4.3 Programmatic tool calling"},
  {"name":"tool search","chapter":"07-growing-mid-session.md","section":"7.1 Tool search: load only relevant definitions"},
  {"name":"memory tool","chapter":"06-memory.md","section":"6.1 Memory tool: application-owned durable notes"},
  {"name":"context editing","chapter":"04-the-transcript.md","section":"4.1 Context editing: retain the archive, trim active context"},
  {"name":"prompt caching","chapter":"06-memory.md","section":"6.5 Prompt caching"},
  {"name":"Files API","chapter":"06-memory.md","section":"6.6 Files API: reuse inputs and retrieve generated artifacts"},
  {"name":"MCP connector","chapter":"07-growing-mid-session.md","section":"7.5 MCP connector in the Messages API"},
  {"name":"Agent Skills: Claude Code","chapter":"02-the-interface.md","section":"2.2 Agent Skills in Claude Code"},
  {"name":"Agent Skills: API","chapter":"09-hosts-and-portability.md","section":"9.9 Agent Skills in the API"},
  {"name":"Agent Skills: claude.ai","chapter":"09-hosts-and-portability.md","section":"9.10 Agent Skills in claude.ai"},
  {"name":"subagents","chapter":"02-the-interface.md","section":"2.3 Subagents: delegate a separate context"},
  {"name":"slash commands","chapter":"02-the-interface.md","section":"2.6 Slash commands: invoke a procedure explicitly"},
  {"name":"hooks","chapter":"03-execution.md","section":"3.4 Hooks: run deterministic lifecycle checks"},
  {"name":"plugins","chapter":"07-growing-mid-session.md","section":"7.4 Plugins: package a reviewed capability set"},
  {"name":"MCP servers in Claude Code","chapter":"07-growing-mid-session.md","section":"7.3 MCP servers in Claude Code"},
  {"name":"output styles","chapter":"05-output-that-steers.md","section":"5.6 Output styles: change Claude Code's working voice"},
  {"name":"CLAUDE.md and auto memory","chapter":"06-memory.md","section":"6.3 CLAUDE.md and auto memory"},
  {"name":"checkpoints and rewind","chapter":"08-replay-and-time-travel.md","section":"8.2 Checkpoints and rewind"},
  {"name":"background tasks","chapter":"08-replay-and-time-travel.md","section":"8.5 Background tasks: keep working while independent work runs"},
  {"name":"Agent SDK","chapter":"09-hosts-and-portability.md","section":"9.2 Agent SDK query(): one bounded task"},
  {"name":"Managed Agents","chapter":"09-hosts-and-portability.md","section":"9.5 Managed Agents: define a versioned agent"},
  {"name":"Projects","chapter":"06-memory.md","section":"6.4 Projects"},
  {"name":"connectors","chapter":"09-hosts-and-portability.md","section":"9.11 Connectors: product integrations and service identity"},
  {"name":"Cowork","chapter":"09-hosts-and-portability.md","section":"9.12 Cowork: a knowledge-work agent host"},
  {"name":"Claude in Chrome","chapter":"09-hosts-and-portability.md","section":"9.13 Claude in Chrome: the signed-in browser as a host"},
  {"name":"strict tool use","chapter":"02-the-interface.md","section":"2.7 Strict tool use and parallel tool use"},
  {"name":"parallel tool use","chapter":"02-the-interface.md","section":"2.7 Strict tool use and parallel tool use"},
  {"name":"Bash tool","chapter":"03-execution.md","section":"3.8 Bash and text editor tools: client execution, standard schemas"},
  {"name":"text editor tool","chapter":"03-execution.md","section":"3.8 Bash and text editor tools: client execution, standard schemas"},
  {"name":"browser use toolsets","chapter":"03-execution.md","section":"3.9 Browser and computer use: a client-controlled environment"},
  {"name":"computer use toolsets","chapter":"03-execution.md","section":"3.9 Browser and computer use: a client-controlled environment"},
  {"name":"compaction","chapter":"04-the-transcript.md","section":"4.5 Compaction: summarize a long conversation"},
  {"name":"message threads","chapter":"04-the-transcript.md","section":"4.6 Message threads: send only the new turns"},
  {"name":"mid-conversation system messages and tool changes","chapter":"04-the-transcript.md","section":"4.7 Mid-conversation system messages and tool changes"},
  {"name":"fine-grained tool streaming","chapter":"04-the-transcript.md","section":"4.8 Fine-grained tool streaming"},
  {"name":"structured outputs","chapter":"05-output-that-steers.md","section":"5.5 Structured outputs: make the final answer machine-readable"},
  {"name":"citations","chapter":"05-output-that-steers.md","section":"5.7 Citations and search-result blocks: preserve evidence links"},
  {"name":"search-result blocks","chapter":"05-output-that-steers.md","section":"5.7 Citations and search-result blocks: preserve evidence links"},
  {"name":"MCP tunnels","chapter":"07-growing-mid-session.md","section":"7.6 MCP tunnels: reach a private server without an inbound port"},
  {"name":"Enterprise inference hooks","chapter":"07-growing-mid-session.md","section":"7.7 Enterprise inference hooks: govern requests before inference"},
  {"name":"Agent SDK sessions: resume and fork","chapter":"08-replay-and-time-travel.md","section":"8.1 Agent SDK sessions: resume and fork"},
  {"name":"Agent SDK custom tools","chapter":"09-hosts-and-portability.md","section":"9.1 Agent SDK custom tools: wrap domain logic in MCP"},
  {"name":"Agent SDK ClaudeSDKClient","chapter":"09-hosts-and-portability.md","section":"9.3 Agent SDK ClaudeSDKClient: a continuing application"},
  {"name":"Agent SDK permissions","chapter":"09-hosts-and-portability.md","section":"9.4 Agent SDK permissions: availability is not approval"},
  {"name":"Managed Agents sessions","chapter":"09-hosts-and-portability.md","section":"9.6 Managed Agents sessions: hosted state and streamed events"},
  {"name":"Managed Agents custom tools","chapter":"09-hosts-and-portability.md","section":"9.7 Managed Agents custom tools: pair events with results"},
  {"name":"Managed Agents self-hosted workers","chapter":"09-hosts-and-portability.md","section":"9.8 Managed Agents self-hosted workers: move execution, not inference"},
  {"name":"Managed memory stores","chapter":"09-hosts-and-portability.md","section":"9.14 Managed memory stores: share selected durable context"},
  {"name":"Managed Agent Skills","chapter":"09-hosts-and-portability.md","section":"9.15 Managed Agent Skills: mount a versioned procedure"},
  {"name":"Managed multiagent orchestration","chapter":"09-hosts-and-portability.md","section":"9.16 Managed multiagent orchestration: delegate hosted work"},
  {"name":"scheduled deployments","chapter":"09-hosts-and-portability.md","section":"9.17 Scheduled deployments: run a configured task later"},
  {"name":"define outcomes","chapter":"09-hosts-and-portability.md","section":"9.18 Define outcomes: a rubric-driven completion loop"},
  {"name":"workflow runs","chapter":"09-hosts-and-portability.md","section":"9.19 Workflow runs: observe parallel work to completion"},
  {"name":"Dreams","chapter":"09-hosts-and-portability.md","section":"9.20 Dreams: consolidate session learning into memory"},
  {"name":"Claude Code agent teams","chapter":"09-hosts-and-portability.md","section":"9.21 Claude Code agent teams: collaborating sessions"},
  {"name":"Remote Control","chapter":"09-hosts-and-portability.md","section":"9.22 Remote Control: another view of a local session"},
  {"name":"channels","chapter":"09-hosts-and-portability.md","section":"9.23 Channels: receive external events in a Code session"},
  {"name":"adaptive thinking","chapter":"10-building-a-real-system.md","section":"10.5 Thinking and effort: spend reasoning where it helps"},
  {"name":"effort","chapter":"10-building-a-real-system.md","section":"10.5 Thinking and effort: spend reasoning where it helps"},
  {"name":"task budgets","chapter":"10-building-a-real-system.md","section":"10.6 Task budgets: give a multi-turn job a resource target"},
  {"name":"advisor tool","chapter":"10-building-a-real-system.md","section":"10.7 Advisor tool: consult a specialist model mid-generation"},
  {"name":"token counting","chapter":"10-building-a-real-system.md","section":"10.8 Token counting: estimate before a large request"},
  {"name":"Message Batches","chapter":"10-building-a-real-system.md","section":"10.9 Message Batches: independent jobs without an interactive loop"}
  ]
hosts: ["Messages API", "Claude Code", "Agent SDK", "Managed Agents", "claude.ai", "Cowork", "Claude in Chrome"]
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
API call. Authenticated execution of the API, Agent SDK, Managed Agents, and product-UI
recipes is **(unverified)** in this edition. The explicit live API/SDK test requires
a key; product hosts need their own acceptance runs. Compilation does not establish
account access or server-tool availability.

Our drafting tool produces an evidence-preserving template; it does not pretend
that a deterministic fixture is model-generated prose. The live model selects and
calls tools. Those mechanics and the semantic quality of a future drafting model
need different evaluations.

## 0.5 Counts

<!-- book-counts:start -->
| Book | Concepts | Hosts | Words | Examples |
|---|---:|---:|---:|---:|
| Brainstem | 1 | 3 | 8172 | 11 |
| Claude | 69 | 7 | 17953 | 71 |
<!-- book-counts:end -->

---

[Book contents](README.md) · [Chapter 1: A Tutorial Introduction →](01-a-tutorial-introduction.md)
