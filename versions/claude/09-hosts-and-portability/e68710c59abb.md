---
layout: book
title: Hosts and Portability
book_label: Chapter 9
book_progress: 66
book_order: 90
description: Carry capabilities across API, Code, SDK, Managed Agents, Cowork, chat, and Chrome
---

[← Chapter 8: Replay and Time Travel](08-replay-and-time-travel.md) · [Book contents](README.md) · [Chapter 10: Building a Real System End to End →](10-building-a-real-system.md)

# Chapter 9 — Hosts and Portability

> **In this chapter:** expose a Python handler through SDK MCP and compare host
> contracts without assuming every surface runs the same package unchanged.

## 9.1 Wrap the handler

Run `python3 claude/examples/09_hosts.py` for the live Agent SDK invocation.
This complete declaration is importable without making a model request:

```python
from claude_agent_sdk import create_sdk_mcp_server, tool

@tool("review_draft", "Prepare a draft for human review; never send.", {"draft": str})
async def review_draft(args):
    return {"content": [{"type": "text", "text": args["draft"]}],
            "structuredContent": {"draft": args["draft"], "sent": False}}

server = create_sdk_mcp_server(name="book", tools=[review_draft])
print(server["type"])
```

The SDK creates an in-process MCP server. The live example passes it under the key
`book` and allows `mcp__book__review_draft`. That name derives from the server key
and tool name, not from an arbitrary Python variable.
[Custom tools and naming](https://code.claude.com/docs/en/agent-sdk/custom-tools).

## 9.2 API, Code, and SDK

The Messages API leaves the client loop and client-tool implementation with the
application. Claude Code provides an existing interactive host. The Agent SDK
provides `query()` for one-shot work and `ClaudeSDKClient` for multi-turn applications,
plus configurable tools, hooks, and session handling.
[Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[Python SDK](https://code.claude.com/docs/en/agent-sdk/python).

Application guidance: share domain logic, not assumptions about transport.
The same draft function can serve an API handler or an SDK MCP wrapper, but its
declaration and result envelope must match the chosen host.

## 9.3 Managed Agents

Managed Agents provides built-in sandbox tools and custom-tool declarations.
Custom calls are emitted as events; an application or worker runs the implementation
and posts the corresponding result. A self-hosted worker can reach internal services
within its configured network without exposing an inbound MCP endpoint publicly.
[Managed tools](https://platform.claude.com/docs/en/managed-agents/tools.md),
[self-hosted workers and custom tools](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-custom-tools.md).

The fetched documentation labels Managed Agents beta. Its hosted sessions and
worker configuration are not the same runtime as a local SDK process. Application
guidance: verify event delivery, tool availability, permission policy, and data
retention for the actual deployment rather than porting by name alone.
[Managed Agents feature contract](https://platform.claude.com/docs/en/managed-agents/tools.md).

## 9.4 Cowork, chat skills, and Chrome

Cowork uses the same agentic architecture for knowledge work and now runs sessions
in the cloud, with local access mediated through the desktop app when needed.
Closing a laptop is not the same lifecycle boundary as a local process exit.
[Cowork execution](https://support.claude.com/en/articles/13345190-getting-started-with-cowork).

claude.ai skills can be enabled, uploaded, shared, or provisioned subject to account
and organization controls. The current guide also documents skills syncing into
Claude Code for the same signed-in account on supported versions. This is a real
reuse path, but host-specific frontmatter and resource behavior still matter.
[Skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude),
[Code skill portability](https://code.claude.com/docs/en/skills).

Claude Code's Chrome integration uses the Claude in Chrome extension and the
browser's signed-in state. Browser actions are visible, site permissions matter,
and login or CAPTCHA can require manual intervention. API-key authentication alone
does not enable this browser integration.
[Chrome prerequisites and permissions](https://code.claude.com/docs/en/chrome).

## 9.5 Exercise the destination

Application guidance: test each host separately for filesystem, networking,
credentials, package availability, persistence, approval, and failure handling.
The SDK wrapper above proves a declaration can be constructed; only its live
invocation proves authenticated tool execution in that environment.

## 9.6 Exercises

**Exercise 9-1.** Compare an API result envelope with an SDK MCP result envelope
around the same pure function.

**Exercise 9-2.** Write a host checklist for moving the library workflow to
Managed Agents. Identify what becomes an event consumer.

**Exercise 9-3.** Run a read-only browser task and record the actual permission
boundary without submitting a form or sending a message.

---

[← Chapter 8: Replay and Time Travel](08-replay-and-time-travel.md) · [Book contents](README.md) · [Chapter 10: Building a Real System End to End →](10-building-a-real-system.md)
