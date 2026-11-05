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

## 3.1 Server tools: code execution

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

**When:** calculate, transform datasets, or generate downloadable artifacts
without provisioning your own interpreter. **Limits:** the sandbox has no
internet access; use installed libraries rather than assuming `pip install`
will work. Reuse `response.container.id` explicitly to preserve files and REPL
state between requests. Each programmatic Python cell has a 90-second wall-clock
limit; container data is retained for up to 30 days. Files created in the Files
API have a separate deletion/expiration lifecycle.
[Runtime, reuse, and retention](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool).

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

## 3.4 Hooks: run deterministic lifecycle checks

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

The checked-in configuration's decision payload is exactly:

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "This demonstration disables Bash; use a disposable project."
  }
}
```

**When:** enforce a precondition or record an audit event independently of the
model's willingness to follow prose. **Example:** copy
[hooks.json](config/hooks.json) into a disposable project's
`.claude/settings.json`, ask Claude to execute `printf hello`, and inspect the
denial. Its `PreToolUse` matcher is `Bash`; it does not deny `Read`.
**Limits:** hook event schemas differ. A permission decision object for
`PreToolUse` is not a valid universal response for every event. Hook failure,
timeout, and exit-code handling are part of the documented event contract, so
test them before relying on a check as enforcement.
[Hook inputs and decisions](https://code.claude.com/docs/en/hooks).

## 3.5 Server tools: web search

Run `python3 claude/examples/03_execution.py --tool search`. Its exact declaration:

```python
search = {
    "type": "web_search_20260318", "name": "web_search",
    "max_uses": 2, "allowed_domains": ["platform.claude.com"],
    "allowed_callers": ["direct"],
}
```

**What:** Anthropic performs search and returns web results and citations in the
response. **When:** an answer needs current evidence rather than the model's
training data. The example restricts searches to the official documentation and
asks for a source-backed answer.
[Web search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool).

**Limits:** the domain filter is not a general browser policy. `max_uses` caps
searches, not all model tokens; handle tool error blocks even when HTTP succeeds.
Do not set both allowed and blocked domain lists. This example opts into direct
search deliberately. Current search versions otherwise default to programmatic
dynamic filtering, which provisions code execution and filters bulky results
before they enter context. Preserve and display the returned citations when
presenting searched claims.
[Search configuration and dynamic filtering](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool).

## 3.6 Server tools: web fetch

Run `python3 claude/examples/03_execution.py --tool fetch`. The request uses:

```python
fetch = {
    "type": "web_fetch_20260318", "name": "web_fetch",
    "max_uses": 2, "max_content_tokens": 12000,
    "allowed_domains": ["platform.claude.com"],
    "allowed_callers": ["direct"], "citations": {"enabled": True},
}
```

**What:** retrieve the content of a known URL, including supported PDF content,
instead of searching for a URL. **When:** the task already supplies the official
page to analyze; combine search then fetch when discovery and detailed reading
are separate steps.
[Web fetch](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool).

**Limits:** fetch is not an authenticated interactive browser and does not
execute a page's JavaScript. URLs must be available in the conversation or prior
results; that restriction reduces exfiltration risk but does not make retrieved
content trustworthy. Limit content tokens and handle inaccessible URLs. Direct
mode here avoids silently introducing a code-execution dependency; use dynamic
filtering intentionally for large pages.
[Fetch controls and risks](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool).

## 3.7 Tool runner: let the SDK maintain the loop

```python
import json
import anthropic
from anthropic import beta_tool

@beta_tool
def review_draft(draft: str) -> str:
    """Return a supplied draft for human review, without sending it.

    Args:
        draft: Exact draft text to preserve.
    """
    if not draft.strip():
        raise ValueError("draft must not be empty")
    return json.dumps({"draft": draft, "sent": False})

with anthropic.Anthropic() as client:
    runner = client.beta.messages.tool_runner(
        model="claude-opus-5-5", max_tokens=1024, max_iterations=8,
        tools=[review_draft],
        messages=[{"role": "user", "content":
                   "Use review_draft on: Please review the library plan."}],
    )
    result = runner.until_done()
    if result.stop_reason != "end_turn":
        raise RuntimeError(f"Incomplete run: {result.stop_reason}")
    print(result.content)
```

**What:** the beta SDK helper derives schemas from typed functions, invokes
handlers, appends results, and continues the model conversation. **When:** use
ordinary functions without maintaining the protocol loop yourself. Iterating
the runner exposes intermediate messages; chapter 1 keeps a manual loop because
its explicit event archive is part of the lesson.
[Tool runner](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner).

**Limits:** type hints do not authorize an operation. Retain validation,
iteration limits, cancellation, and observability in application policy.
`until_done()` is convenient but does not establish that a specific handler ran;
assert a recorded handler event when the workflow requires it.
[Runner control](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-runner).

## 3.8 Bash and text editor tools: client execution, standard schemas

**What:** Anthropic defines standard shell and file-editing tool interfaces; your
application provides their executor. They are not the server code sandbox.
**Example:** these are exact `tools` entries for the client request:

```python
client_tools = [
    {"type": "bash_20250124", "name": "bash"},
    {"type": "text_editor_20250728", "name": "str_replace_based_edit_tool"},
]
```

**When:** an application has a provisioned, controlled workspace and wants
familiar shell and editing operations. Implement tool dispatch using the same
ID-paired `tool_result` loop as chapter 1, but run commands only in an isolated
workspace with explicit timeouts and path policy.
[Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool),
[text editor](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool).

**Limits:** declaring these tools does not create a shell, sandbox, permission
prompt, or filesystem snapshot. The current editor version does not implement
`undo_edit`; keep application version history rather than promising rollback.
Do not point a book demonstration at a real user's home directory.
[Editor version differences](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool).

## 3.9 Browser and computer use: a client-controlled environment

**What:** browser toolsets describe navigation, reading, and interaction;
computer toolsets describe screen and input operations. The application executes
them and returns state/results. This differs from Claude in Chrome, a ready-made
host covered in chapter 9.
**Example:** these exact declarations select the current interfaces:

```python
browser = {"type": "browser_toolset_20260801"}
computer = {"type": "computer_toolset_20260801"}
```

**When:** a necessary task has a user interface but no suitable application API.
Implement the selected toolset using the official action/state reference and
return screenshots or browser accessibility state as requested. The SDK
toolset adapter guide explains how executors integrate with the tool runner;
it deliberately does not supply a universal browser provider.
[Browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool),
[computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool),
[SDK adapters](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-sdk).

**Limits:** neither declaration launches a browser or grants safe access to a
desktop. Use a dedicated test identity, least-privilege site access, and human
approval for consequential actions. Browser titles, URLs, downloaded content,
and screenshots are untrusted evidence. Coordinate dimensions must match the
actual display; an incorrect viewport can target the wrong control.
[Browser trust boundaries](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool),
[computer-use risks](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool).

## 3.10 Exercises

**Exercise 3-1.** Inspect the server result blocks and distinguish execution output
from the final natural-language answer.

**Exercise 3-2.** Install the deny hook in a disposable project and verify both a
denied Bash call and an unaffected read operation.

**Exercise 3-3.** Move one deterministic transformation from a skill's prose into
a script. Compare what enters the conversation before and after.

---

[← Chapter 2: The Interface](02-the-interface.md) · [Book contents](README.md) · [Chapter 4: The Transcript →](04-the-transcript.md)
