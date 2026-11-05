---
layout: book
title: Claude Reference Manual
book_label: Appendix A
book_progress: 82
book_order: 110
description: Terse host-aware reference to the documented Claude interfaces
---

[← Chapter 10: Building a Real System End to End](10-building-a-real-system.md) · [Book contents](README.md) · [Appendix B: Glossary →](B-glossary.md)

# Appendix A — Claude Reference Manual

> **In this chapter:** locate the correct declaration, executor, result envelope,
> persistence mechanism, and continuation boundary.

## A.1 Messages API tools

User-defined tools use `name`, `description`, and `input_schema`.
Assistant `tool_use` blocks identify calls; user `tool_result` blocks reference
`tool_use_id`. Preserve all assistant content and return a result for each requested
client call. Error results use `is_error`.
[Tool-use reference](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

Our helper uses `claude-opus-5-5`, bounds the loop at eight requests, checks terminal
stop reasons, and validates domain arguments. The helper's result shape and replay
format are application conventions, not SDK requirements.
Opus 5.5 rejects forced `any` and named `tool` selection. Use `auto`, strict
schemas, and an application check for required events; schema validity does not
force an operation to run.
[Selection restrictions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools).

## A.2 Execution and scale

Server tools run on Anthropic infrastructure; client tools run in the application.
Code execution uses the documented versioned tool type. Tool search searches
supplied definitions marked `defer_loading`; it does not install code.
Programmatic tool calling uses code execution and `allowed_callers` to let a
generated program call tools and filter intermediate data.
[Overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool),
[tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool),
[programmatic calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

This edition declares `code_execution_20260521` and uses the same value in
`allowed_callers`. Both the `20260120` and `20260521` caller values are accepted;
returned caller tags normalize to `code_execution_20260120`. That response tag
does not identify a different container runtime.
[Caller identifiers](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

## A.3 Files and callbacks

Skills use `SKILL.md`; name and description advertise their procedure.
Subagents use Markdown frontmatter including name, description, tools, and optional
model selection. Hooks bind lifecycle events to handlers and structured output.
Plugins package these components with a manifest.
[Skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents),
[hooks](https://code.claude.com/docs/en/hooks),
[plugins](https://code.claude.com/docs/en/plugins/overview).

Live skill changes require existing watched directories outside bare mode.
New top-level directories may need `/reload-skills`; other plugin components can
need `/reload-plugins`. Read the host's exact reload boundary rather than assuming
every file is watched. [Skill reload](https://code.claude.com/docs/en/skills).

## A.4 Context and memory

The memory tool requests client-side file operations under `/memories`; applications
own the store and must confine paths. `BetaLocalFilesystemMemoryTool` is the official
Python local helper. `CLAUDE.md` and auto memory provide Claude Code context;
Projects provide a separate knowledge and instruction surface.
[Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool),
[Code memory](https://code.claude.com/docs/en/memory),
[Projects](https://support.claude.com/en/articles/9517075-what-are-projects).

Context editing changes presented context while the client preserves history.
Prompt caching reuses computation over matching prefixes; it is not durable memory.
[Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing),
[prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

## A.5 Agent SDK

`query()` creates a session by default. `ClaudeSDKClient` supports continuing
multi-turn exchanges. `ClaudeAgentOptions` configures tools and session options.
`@tool` and `create_sdk_mcp_server()` expose local functions; MCP results use
`content`, optional `structuredContent`, and `isError`.
[Python API](https://code.claude.com/docs/en/agent-sdk/python),
[custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools).

Resume selects an existing conversation; fork creates a separate branch.
Sessions are not filesystem snapshots. Checkpointing has separate edit-tracking
and restore limits. [Sessions](https://code.claude.com/docs/en/agent-sdk/sessions),
[checkpoints](https://code.claude.com/docs/en/checkpointing).

## A.6 Hosted surfaces

Managed Agents tools and worker events use their own declared configuration.
Cowork, claude.ai skills, and Chrome each have account and permission requirements.
They are not implied by importing a Python package.
[Managed tools](https://platform.claude.com/docs/en/managed-agents/tools.md),
[workers](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-custom-tools.md),
[Cowork](https://support.claude.com/en/articles/13345190-getting-started-with-cowork),
[chat skills](https://support.claude.com/en/articles/12512180-using-skills-in-claude),
[Chrome](https://code.claude.com/docs/en/chrome).

## A.7 Additional API mechanisms

| Mechanism | Exact interface or configuration | Detailed treatment |
|---|---|---|
| Strict arguments | `strict: true` on a client tool | 2.7 |
| Web search/fetch | `web_search_20260318`, `web_fetch_20260318` | 3.5–3.6 |
| SDK runner | `client.beta.messages.tool_runner()` | 3.7 |
| Client computer/browser toolsets | `computer_toolset_20260801`, `browser_toolset_20260801` | 3.9 |
| Compaction | `compaction={"type":"summarize"}`, `compact-2026-09-04` | 4.5 |
| Message threads | `client.beta.messages.thread()` | 4.6 |
| Inline changes | `inline-tools-2026-09-15` | 4.7 |
| Early argument streaming | `eager_input_streaming: true` | 4.8 |
| Typed final output | `client.messages.parse(output_format=...)` | 5.5 |
| File resources | Stable `client.files` | 6.6 |
| Skills resources | Stable `client.skills`; `container.skills` | 9.9 |
| Managed resources | `client.beta.agents`, `.sessions`, `.environments` | 9.5–9.8 |
| Managed orchestration | `multiagent_20261001`, session event stream | 9.16, 9.19 |
| Managed outcomes | `user.define_outcome` | 9.18 |
| Memory consolidation | `client.beta.dreams` | 9.20 |
| Thinking/effort/budgets | `thinking`, `output_config` | 10.5–10.6 |
| Advisor | `advisor_20260301` | 10.7 |
| Capacity planning | `messages.count_tokens`, `messages.batches` | 10.8–10.9 |

These are not interchangeable transports. Keep source data, authorization,
continuation state, and final stop-reason handling explicit in each host.
[API feature index](https://platform.claude.com/docs/llms.txt),
[Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview).

## A.8 Exercises

**Exercise A-1.** Choose one operation and specify its host, declaration, executor,
result envelope, persistence, and approval boundary.

---

[← Chapter 10: Building a Real System End to End](10-building-a-real-system.md) · [Book contents](README.md) · [Appendix B: Glossary →](B-glossary.md)
