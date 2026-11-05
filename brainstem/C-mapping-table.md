---
layout: book
title: Mapping Table
book_label: Appendix C
book_progress: 100
book_order: 130
description: Chapter-by-chapter concept map between the companion books
---

[← Appendix B: Glossary](B-glossary.md) · [Book contents](README.md) · [Companion shelf →](../index.html)

# Appendix C — Mapping Table

> **In this chapter:** align the questions asked by both books. This is a map of
> concepts and boundaries, not a ranking or a claim that the mechanisms are identical.

## C.1 Read chapter N beside chapter N

| Chapter | Brainstem unit or convention | Claude mechanism and boundary |
|---|---|---|
| Preface | Agent.py as a described executable pattern; explicit teaching profile | A family of tools, procedures, delegation, and hosts; not a single new syntax |
| 1 Tutorial | Deterministic name-dispatch caller runs a real local draft operation | Real Messages API emits a call; the application runs the same kind of local operation |
| 2 Interface | `metadata`: name, description, parameters | Tool name, description, `input_schema`; skill and subagent frontmatter are separate interfaces |
| 3 Execution | Hidden `perform()`; dependencies belong to the concrete host | Client handlers, server tools, code execution, skill scripts, subagents, and hooks |
| 4 Transcript | Relevant outputs cross the execution boundary; replay also records arguments | Tool results, isolated subagent summaries, script outputs, programmatic filtering, and context editing |
| 5 Steering output | Summary, next-step guidance, structured `data_slush` convention | Adoptable tool-result convention; API text or SDK MCP structured content can carry it |
| 6 Memory | ManageMemory writes; ContextMemory recalls and offers `system_context()` | Client-owned memory tool; Code instructions and auto memory; Projects have distinct scope |
| 7 Growth | Source-inspected LearnNew creation and real next-turn invocation; stock generator fallback recorded | Live skill/subagent file updates with documented limits; API tool search discovers supplied definitions; MCP and plugins supply execution and packaging |
| 8 Replay | Book archive re-executes one pinned pure handler with later evidence | Checkpoints restore tracked state; SDK resume/fork continues or branches history; application-owned replay can re-execute a pure tool |
| 9 Hosts | Caller-carried conversation state, local model run, RAPP/1 framing boundary; browser/studio not deployed | Code, API, Agent SDK, Managed Agents, Cowork, chat skills, and Chrome have distinct execution and permission contracts |
| 10 System | Chat file → draft → exact review handoff → selected draft replay | Same files and task; real model tool calls for initial steps, then local pure-handler replay |
| A Reference | Teaching-profile contracts and source-agent boundaries | Host-aware interface and lifecycle reference |
| B Glossary | Caller, declaration, result, context, archive, replay | Tool, skill, subagent, hook, cache, checkpoint, session, fork |

Claude mechanisms in this table are documented at:
[tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[skills](https://code.claude.com/docs/en/skills),
[subagents](https://code.claude.com/docs/en/sub-agents),
[hooks](https://code.claude.com/docs/en/hooks),
[programmatic calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling),
[context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing),
[memory](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool),
[Code memory](https://code.claude.com/docs/en/memory),
[Projects](https://support.claude.com/en/articles/9517075-what-are-projects),
[tool search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool),
[MCP](https://code.claude.com/docs/en/mcp),
[plugins](https://code.claude.com/docs/en/plugins/overview),
[checkpoints](https://code.claude.com/docs/en/checkpointing),
[sessions](https://code.claude.com/docs/en/agent-sdk/sessions),
[custom SDK tools](https://code.claude.com/docs/en/agent-sdk/custom-tools),
[Managed Agents](https://platform.claude.com/docs/en/managed-agents/tools.md),
[Cowork](https://support.claude.com/en/articles/13345190-getting-started-with-cowork),
[chat skills](https://support.claude.com/en/articles/12512180-using-skills-in-claude),
and [Chrome](https://code.claude.com/docs/en/chrome).

## C.2 Avoid false equivalences

A description is selection guidance, not proof of permission.
A skill is not merely a schema-less substitute for every executable tool.
A transcript view is not the full archive.
Discovery of an existing definition is not creation of an implementation.
A session fork is not byte-identical model replay.
Prompt caching is not durable memory.
A portable interface is not proof that all hosts provide the same dependencies.

The teaching examples make their execution locations explicit so these distinctions
can be tested rather than settled by terminology.

## C.3 Reading paths

Open [Brainstem chapter 1](../brainstem/01-a-tutorial-introduction.md) and
[Claude chapter 1](../claude/01-a-tutorial-introduction.md), then move through the
same chapter numbers. For an implementation lookup, compare the two Appendix A
pages. For persistence and replay, read 6 and 8 together before designing storage.

This appendix is generated byte-for-byte identically into both books from one
shared source. Its relative links intentionally work from either book directory.

## C.4 Exercises

**Exercise C-1.** Implement the same new operation through both interfaces.
Record which logic is shared and which part belongs to a host adapter.

---

[← Appendix B: Glossary](B-glossary.md) · [Book contents](README.md) · [Companion shelf →](../index.html)
