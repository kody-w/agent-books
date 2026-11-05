---
layout: book
title: Execution
book_label: Chapter 3
book_progress: 24
book_order: 30
description: Locate work in client handlers, server tools, scripts, subagents, and hooks
---

[← Chapter 2: The Interface](02-the-interface.md) · [Book contents](README.md) · [Chapter 4: The Transcript →](04-the-transcript.md)

# Chapter 3 — Execution

> **In this chapter:** execute code on Anthropic's server, identify the client's
> responsibilities, and use hooks for lifecycle behavior rather than prompting alone.

## 3.1 Run server-side code

Run `python3 claude/examples/03_execution.py`. The complete program handles
`pause_turn`; this first-request form shows the execution boundary:

```python
import anthropic

with anthropic.Anthropic() as client:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=2048,
        tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
        messages=[{"role": "user", "content": "Use code execution to compute sum([2, 3, 5])."}],
    )
    print(response.model_dump_json(indent=2))
```

Code execution is a server tool: Anthropic runs code in a sandboxed container.
The documented current version above adds explicit wall-clock-limit guidance to
the runtime that supports persistent Python state and programmatic calls.
No code-execution beta header is required for this tool version.
[Code execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool).

## 3.2 Client work and server work

In chapter 1, our application executes the handler and returns a result.
For server tools such as web search and code execution, the API executes the work.
Server responses may require continuation with `pause_turn`; that is not the same
as a client `tool_use` request. Our numbered program bounds continuation and raises
on incomplete stop reasons rather than reporting a partial answer as complete.
[Tool execution and stop behavior](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

This division is a useful strength: an application can keep domain-specific
credentials and validation local while delegating supported search or computation
to the server. It still needs to assess the feature's retention and availability
contract. The code-execution page documents container retention separately from
tool syntax. [Code execution contract](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool).

## 3.3 Scripts and subagents

A skill can invoke a script without placing the script's source in context.
A subagent can inspect many files in a separate context and return a small summary.
Both are legitimate ways to keep implementation or working material out of the
parent conversation. [Skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents).

Application guidance: use a script for stable transformations and a subagent for
work that requires judgment or exploration. A wrapper around a model call does
not make the operation deterministic. Measure both latency and result quality
when choosing an execution location.

## 3.4 Hooks run at boundaries

Claude Code fires hooks at events including `PreToolUse`, `PostToolUse`,
`UserPromptSubmit`, and `Stop`. Command hooks receive JSON on stdin and may return
structured decisions. They can enforce a deterministic precondition before a tool
runs instead of hoping the model remembers a paragraph.
[Hook lifecycle and output](https://code.claude.com/docs/en/hooks).

The [hook template](config/hooks.json) demonstrates an event handler returning a
deny decision for Bash calls. It is intentionally conservative and belongs in a
disposable test project, not your working configuration. Read it before installing.
A hook can run code with the host's permissions; a "hook" label is not a sandbox.
[Hook configuration](https://code.claude.com/docs/en/hooks).

## 3.5 Exercises

**Exercise 3-1.** Inspect the server result blocks and distinguish execution output
from the final natural-language answer.

**Exercise 3-2.** Install the deny hook in a disposable project and verify both a
denied Bash call and an unaffected read operation.

**Exercise 3-3.** Move one deterministic transformation from a skill's prose into
a script. Compare what enters the conversation before and after.

---

[← Chapter 2: The Interface](02-the-interface.md) · [Book contents](README.md) · [Chapter 4: The Transcript →](04-the-transcript.md)
