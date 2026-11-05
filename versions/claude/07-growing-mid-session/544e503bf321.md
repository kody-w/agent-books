---
layout: book
title: Growing Mid-Session
book_label: Chapter 7
book_progress: 52
book_order: 70
description: Add skills and subagents, discover tools, and package capabilities with plugins
---

[← Chapter 6: Memory](06-memory.md) · [Book contents](README.md) · [Chapter 8: Replay and Time Travel →](08-replay-and-time-travel.md)

# Chapter 7 — Growing Mid-Session

> **In this chapter:** discover a deferred tool, update live instruction files,
> and distinguish creation, installation, discovery, and session configuration.

## 7.1 Discover a deferred capability

Run `python3 claude/examples/07_growth.py`.

```python
import copy
import sys
sys.path.insert(0, "claude/examples")
from common import DRAFT, run

deferred = copy.deepcopy(DRAFT)
deferred["defer_loading"] = True
result = run(
    "Find the drafting tool and draft a follow-up from: Please review the library plan.",
    tools=[{"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
           deferred],
)
assert any(e["name"] == "draft_follow_up" for e in result["events"])
print(result["text"])
```

The server searches definitions supplied in the request, returns references, and
loads relevant tool definitions into context. At least one tool, normally search
itself, stays non-deferred. This scales a supplied catalog without initially loading
every schema. It does not create new tool implementations.
[Tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).

## 7.2 Create skills and subagents during work

Claude Code watches existing skill directories and picks up additions or edits in
the current session. If the top-level skills directory did not exist at startup,
`/reload-skills` is needed; live detection covers `SKILL.md` text, not all plugin
components. Bare mode is another documented exception.
[Live skill editing](https://code.claude.com/docs/en/skills).

The subagent guide documents creating an agent during a session and using it
without a general restart requirement. It notes a specific limitation when the
user agents directory did not exist when the session began.
That is a real create-and-use cycle, not merely searching already supplied API tools.
[Subagent creation](https://code.claude.com/docs/en/sub-agents).

Application guidance: have Claude write a reviewed, project-local skill or subagent
file, inspect its permissions and instructions, then invoke it on synthetic input.
Do not infer that a new Python implementation has been safely installed merely
because a Markdown file appeared.

## 7.3 MCP connects execution

Claude Code can connect tools through MCP using local or remote server arrangements;
the Messages API MCP connector instead connects to reachable remote HTTP servers
and currently supports tool calls. The connector is not a local Python importer.
[Claude Code MCP](https://code.claude.com/docs/en/mcp),
[API connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector).

Application guidance: distinguish "the host can discover this declaration" from
"an authenticated executor is reachable." A visible tool whose server cannot be
reached is not an installed working capability.

## 7.4 Plugins package the set

A Claude Code plugin packages skills, agents, hooks, MCP servers, or other
components as one unit. The manifest lives in `.claude-plugin/plugin.json`.
Some component changes require `/reload-plugins`; skill text watching alone is
not a blanket plugin reload guarantee.
[Plugins](https://code.claude.com/docs/en/plugins/overview),
[skill/plugin reload boundary](https://code.claude.com/docs/en/skills).

Managed Agents separates tool declaration on the agent from implementation in a
worker. The worker serves only registered implementations; a missing executor
can leave a session waiting for a custom result. The worker lists tools once at
startup and cannot add tools to a running session. The current guide permits
redeclaring tools on the agent or an idle session and then restarting the worker;
do not confuse that idle-session update with unrestricted live mutation.
[Self-hosted custom tools](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-custom-tools.md).

## 7.5 Exercises

**Exercise 7-1.** Add a skill in an existing watched directory and observe its
availability without restarting.

**Exercise 7-2.** Compare a tool-search request with a newly authored subagent.
Identify which changes implementation and which changes visibility.

**Exercise 7-3.** Package the skill, reviewer, and hook templates into a plugin
in a disposable project and test reload behavior.

---

[← Chapter 6: Memory](06-memory.md) · [Book contents](README.md) · [Chapter 8: Replay and Time Travel →](08-replay-and-time-travel.md)
