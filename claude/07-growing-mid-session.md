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

## 7.1 Tool search: load only relevant definitions

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

**When:** a catalog has many rarely used tools, so loading all schemas wastes
context and can make selection harder. Regex and BM25 search variants give
different discovery interfaces. **Limits:** search operates on supplied tool
names, descriptions, and schema metadata, not on unseen Python source. Keep at
least one tool non-deferred. Avoid deferring a tool the task needs on nearly
every turn; discovery adds its own latency. Search finds a declaration, while
your executor must still implement and authorize the selected operation.
[Search variants and trade-offs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool).

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

## 7.3 MCP servers in Claude Code

Claude Code can connect tools through MCP using local or remote server arrangements;
the Messages API MCP connector instead connects to reachable remote HTTP servers
and currently supports tool calls. The connector is not a local Python importer.
[Claude Code MCP](https://code.claude.com/docs/en/mcp),
[API connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector).

**What:** MCP servers advertise tools, resources, and prompts to the host.
**Example:** this read-only official documentation server needs no private
application credential:

```sh
claude mcp add --transport http --scope project anthropic-docs https://platform.claude.com/docs/mcp
claude mcp list
```

In the resulting Claude Code session, use `/mcp` to inspect connection state and
ask it to search the Anthropic documentation. **When:** reuse a maintained
integration rather than writing one adapter for each host. Project scope writes
shared `.mcp.json`; a collaborator must still trust and authenticate a server
when required. Local stdio servers can instead run a reviewed executable on the
host; a remote URL does not imply a local process.
[Transport, scope, and authentication](https://code.claude.com/docs/en/mcp).

Application guidance: distinguish "the host can discover this declaration" from
"an authenticated executor is reachable." A visible tool whose server cannot be
reached is not an installed working capability.

**Limits:** server tool descriptions and results can carry prompt injections.
OAuth authorization is service-specific; it is not permission to let every tool
run without review. Keep credentials out of committed `.mcp.json`, restrict
available operations, and distinguish host permission prompts from the remote
service's own access control.
[MCP security](https://code.claude.com/docs/en/mcp).

## 7.4 Plugins: package a reviewed capability set

A Claude Code plugin packages skills, agents, hooks, MCP servers, or other
components as one unit. The manifest lives in `.claude-plugin/plugin.json`.
Some component changes require `/reload-plugins`; skill text watching alone is
not a blanket plugin reload guarantee.
[Plugins](https://code.claude.com/docs/en/plugins/overview),
[skill/plugin reload boundary](https://code.claude.com/docs/en/skills).

**Example:** copy [the minimal manifest](config/plugin/.claude-plugin/plugin.json)
and [its skill](config/plugin/skills/follow-up/SKILL.md) as this exact tree:

```text
library-plugin/
  .claude-plugin/plugin.json
  skills/follow-up/SKILL.md
```

The manifest is:

```json
{"name":"library-book","version":"1.0.0","description":"Draft-only library follow-up procedures"}
```

Load that reviewed local directory with `claude --plugin-dir ./library-plugin`
and invoke `/library-book:follow-up`. **When:** distribute related skills,
agents, hooks, servers, and styles together with a versioned identity.
**Limits:** component directories belong at the plugin root, not inside
`.claude-plugin`. Installation is a trust decision: hooks and server commands
can execute code. A manifest is packaging, not sandboxing or proof that all
dependencies are available.
[Plugin structure and loading](https://code.claude.com/docs/en/plugins/overview).

Managed Agents separates tool declaration on the agent from implementation in a
worker. The worker serves only registered implementations; a missing executor
can leave a session waiting for a custom result. The worker lists tools once at
startup and cannot add tools to a running session. The current guide permits
redeclaring tools on the agent or an idle session and then restarting the worker;
do not confuse that idle-session update with unrestricted live mutation.
[Self-hosted custom tools](https://platform.claude.com/docs/en/managed-agents/self-hosted-sandboxes-custom-tools.md).

## 7.5 MCP connector in the Messages API

```python
import anthropic

with anthropic.Anthropic() as client:
    response = client.beta.messages.create(
        model="claude-opus-5-5", max_tokens=1024,
        betas=["mcp-client-2025-11-20"],
        mcp_servers=[{
            "type": "url", "name": "anthropic-docs",
            "url": "https://platform.claude.com/docs/mcp",
        }],
        tools=[{"type": "mcp_toolset", "mcp_server_name": "anthropic-docs"}],
        messages=[{"role": "user", "content":
                   "Find official guidance about client tool result IDs."}],
    )
    print(response.model_dump_json(indent=2))
```

**What:** the API connects to a remote HTTP MCP server and handles tool calls
without requiring your application to run an MCP client loop. **When:** the
integration is already exposed as a reachable MCP service. The example uses a
real public documentation endpoint from the fetched index.
[MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector).

**Limits:** this connector currently supports MCP tool calls, not every resource
or prompt feature of the protocol, and does not launch a local stdio server.
Each server must have exactly one corresponding `mcp_toolset`. Put a private
service token in `authorization_token` from your secret manager, never in the
manuscript or committed configuration. Pinning a returned tool list requires the
newer `mcp-client-2026-09-15` beta and its documented listing fields; the simpler
example intentionally uses the supported basic connector header.
[Connector capabilities and tool-list pinning](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector).

## 7.6 MCP tunnels: reach a private server without an inbound port

**What:** a tunnel agent makes an outbound connection that lets the platform
reach an MCP server running on a private network. It solves connectivity, not
tool authorization. **When:** use the API connector with a development or
internal service that cannot accept public inbound connections.
**Example:** follow the Console-created tunnel flow in the official quickstart:
create a tunnel, obtain its tunnel credential, start the supplied tunnel agent
beside your MCP server, then use the returned tunnel endpoint as the connector's
server URL. Do not substitute your API key for the tunnel credential.
[MCP tunnel quickstart](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/quickstart).

**Exact proxy configuration:** after provisioning the tunnel and a trusted
certificate through the documented Console flow, `config/mcp-proxy.yaml` uses:

```yaml
listen_addr: ":8080"
tunnel_domain: YOUR_TUNNEL_DOMAIN
tls:
  cert_file: /data/tls.crt
  key_file: /data/tls.key
routes:
  library: http://library-mcp:9000
```

Replace `YOUR_TUNNEL_DOMAIN` with the Console-issued domain and supply the
certificate/key at the mounted paths. The `library` route becomes
host `library.YOUR_TUNNEL_DOMAIN` with HTTPS and path `/mcp`; run the proxy plus `cloudflared` using
the quickstart's pinned Compose images. There is deliberately no credential in
this configuration.
[Proxy and Compose configuration](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/quickstart).

**Limits:** tunnels are a research preview requiring access. A tunnel exposes the configured MCP service to authorized platform
requests; it is not a general VPN and does not make untrusted tool output safe.
Use scoped credentials and review the service's effective operations before
connecting it. Certificate provisioning and tunnel-domain ownership are required;
a route configuration alone does not establish a working connection.
[Tunnel setup contract](https://platform.claude.com/docs/en/agents-and-tools/mcp-tunnels/quickstart).

## 7.7 Enterprise inference hooks: govern requests before inference

**What:** a Claude Enterprise organization can send governed prompts to its
HTTPS policy service for an allow/deny verdict before the model runs.
Optional `tool_call` validation checks calls before execution. These are
server-side organizational inference hooks, not Claude Code's local shell hooks.
**Exact verdict examples:**

```json
{"action": "allow"}
```

```json
{"action": "deny", "deny_reason": "Use approved synthetic evidence for this workflow."}
```

**When:** a governed deployment needs a uniform policy boundary across supported
Claude products instead of relying on each local client. An owner configures the
endpoint, signs/verifies requests under the documented webhook protocol, and
tests first in shadow mode. Set failure handling explicitly rather than
assuming a timeout always blocks.
[Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks),
[configuration](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration).

**Limits:** this feature is for Claude Enterprise organizations, not Platform
API organizations. The endpoint receives transcript text, tool calls/results,
and extracted attachment text, not raw image bytes or system prompts. Verdicts
allow or deny; they do not rewrite content. The default verdict timeout is five
seconds; failures and the circuit breaker apply the organization's configured
fail-open/fail-closed behavior. Validate signatures and account for the endpoint
as another data recipient.
[Endpoint contract and boundaries](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint).

## 7.8 Exercises

**Exercise 7-1.** Add a skill in an existing watched directory and observe its
availability without restarting.

**Exercise 7-2.** Compare a tool-search request with a newly authored subagent.
Identify which changes implementation and which changes visibility.

**Exercise 7-3.** Package the skill, reviewer, and hook templates into a plugin
in a disposable project and test reload behavior.

---

[← Chapter 6: Memory](06-memory.md) · [Book contents](README.md) · [Chapter 8: Replay and Time Travel →](08-replay-and-time-travel.md)
