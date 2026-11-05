---
layout: book
title: Glossary
book_label: Appendix B
book_progress: 91
book_order: 120
description: Host-aware vocabulary for Claude tools, memory, and sessions
---

[← Appendix A: Reference Manual](A-reference-manual.md) · [Book contents](README.md) · [Appendix C: Mapping Table →](C-mapping-table.md)

# Appendix B — Glossary

> **In this chapter:** distinguish product terms from the book's application conventions.

## B.1 Execution vocabulary

| Term | Meaning |
|---|---|
| Client tool | A declared operation executed by your application. |
| Server tool | An operation executed by Anthropic, such as code execution or tool search. |
| `tool_use` | Assistant content block requesting a client operation. |
| `tool_result` | User content block returning the corresponding operation's result. |
| `input_schema` | JSON Schema describing a tool's argument shape. |
| Tool choice | Request policy controlling automatic or named tool selection. |
| Programmatic tool calling | Code in the execution container calls permitted tools and processes results. |
| Tool search | On-demand discovery of definitions supplied in a tool catalog. |
| MCP | Tool connection protocol used by Code, the SDK, and product-specific connectors. |
| SDK MCP server | In-process tool server created by the Agent SDK application. |

These are documented tool and SDK concepts.
[Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[programmatic calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling),
[search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool),
[SDK custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools).

## B.2 Organization vocabulary

| Term | Meaning |
|---|---|
| Skill | Reusable instructions and resources loaded when relevant or explicitly invoked. |
| Frontmatter | YAML metadata at the start of a skill or subagent file. |
| Subagent | Delegated assistant with its own context, instructions, and tool configuration. |
| Hook | Lifecycle handler, possibly returning a structured decision. |
| Plugin | Package of skills, agents, hooks, servers, or other supported components. |
| `CLAUDE.md` | Standing contextual instructions for a user, project, or organization. |
| Auto memory | Notes Claude Code accumulates from working context and corrections. |
| Project | Host workspace carrying knowledge and instructions; rollout affects its exact behavior. |

[Skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents),
[hooks](https://code.claude.com/docs/en/hooks),
[plugins](https://code.claude.com/docs/en/plugins/overview),
[Code memory](https://code.claude.com/docs/en/memory),
[Projects](https://support.claude.com/en/articles/9517075-what-are-projects).

## B.3 State vocabulary

| Term | Meaning |
|---|---|
| Memory tool | Client-owned persistent file operations under a virtual memory directory. |
| Prompt cache | Reused computation over matching prompt prefixes, not durable notes. |
| Context editing | Selective removal of old content from the model's presented context. |
| Checkpoint | Session recovery point with specific file-tracking limits. |
| Resume | Continue a selected saved conversation. |
| Fork | Create a new session from a saved conversation while preserving the original. |
| Step replay | Book convention: re-execute one recorded pure application handler. |
| `data_slush` | Book convention: exact structured values passed downstream without paraphrase. |

[Memory](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool),
[caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching),
[context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing),
[checkpointing](https://code.claude.com/docs/en/checkpointing),
[sessions](https://code.claude.com/docs/en/agent-sdk/sessions).

## B.4 Failure vocabulary

Application guidance: distinguish authentication failure, incomplete model response,
invalid arguments, handler refusal, exact-evidence mismatch, and missing executor.
A final paragraph does not prove that the intended tool ran. An import check does
not prove live account access. A context summary does not prove filesystem rollback.

## B.5 Resource and orchestration vocabulary

| Term | Meaning |
|---|---|
| Files API | Workspace-scoped reusable uploads and downloadable generated artifacts. |
| Structured output | Schema-constrained final answer, distinct from strict tool arguments. |
| Tool runner | SDK helper that executes declared functions and maintains the model loop. |
| Compaction | A condensed representation of earlier conversation for future turns. |
| Message thread | Beta server-side Messages prefix storage, with client recovery history. |
| Connector | A product or API integration surface; its host and authentication must be named. |
| Managed agent | Versioned hosted model/instruction/tool definition. |
| Managed session | Stateful work resource with events, environment, and configured agent. |
| Environment worker | Self-hosted executor serving a managed environment's work queue. |
| Memory store | Hosted addressable memories explicitly attached to a session. |
| Deployment | Persistent agent/environment/task configuration that can have a schedule. |
| Outcome | Desired result plus an evaluation rubric and bounded iteration policy. |
| Workflow run | Hosted multi-phase work with its own status inside a session. |
| Dream | Preview consolidation process producing a rebuilt memory store. |
| Agent team | Experimental collaborating Claude Code sessions with task coordination. |
| Channel | Preview external-event delivery into an enabled running Code session. |
| Remote Control | A remote UI for execution that remains on the original local machine. |
| Advisor | Separately billed model consultation within the server-side turn. |
| Effort | Requested reasoning intensity, not a proof of quality or a hard budget. |

[Files](https://platform.claude.com/docs/en/build-with-claude/files),
[API feature index](https://platform.claude.com/docs/llms.txt),
[Managed resources](https://platform.claude.com/docs/en/managed-agents/overview),
[teams](https://code.claude.com/docs/en/agent-teams),
[channels](https://code.claude.com/docs/en/channels),
[Remote Control](https://code.claude.com/docs/en/remote-control).

## B.6 Exercises

**Exercise B-1.** Describe one failure using both the product's transport term and
the application's domain term. Decide where each should be reported.

---

[← Appendix A: Reference Manual](A-reference-manual.md) · [Book contents](README.md) · [Appendix C: Mapping Table →](C-mapping-table.md)
