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

## A.7 Exercises

**Exercise A-1.** Choose one operation and specify its host, declaration, executor,
result envelope, persistence, and approval boundary.

---

[← Chapter 10: Building a Real System End to End](10-building-a-real-system.md) · [Book contents](README.md) · [Appendix B: Glossary →](B-glossary.md)
