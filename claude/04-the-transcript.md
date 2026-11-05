---
layout: book
title: The Transcript
book_label: Chapter 4
book_progress: 31
book_order: 40
description: Manage tool results, delegated summaries, programmatic calls, and context editing
---

[← Chapter 3: Execution](03-execution.md) · [Book contents](README.md) · [Chapter 5: Output That Steers the Next Step →](05-output-that-steers.md)

# Chapter 4 — The Transcript

> **In this chapter:** distinguish the durable record from active context and
> reduce irrelevant material with delegation, programmatic calls, and context editing.

## 4.1 Enable a context policy

Run `python3 claude/examples/04_transcript.py`. It makes a real beta request; its
short conversation demonstrates configuration, not a measured clearing event:

```python
import anthropic

with anthropic.Anthropic() as client:
    response = client.beta.messages.create(
        model="claude-opus-5-5", max_tokens=1024,
        betas=["context-management-2025-06-27"],
        context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
        messages=[{"role": "user", "content": "Explain why old tool results may be cleared."}],
    )
    print(response.model_dump_json(indent=2))
```

Context editing can clear old tool results before the prompt reaches Claude.
The client retains its full conversation history. The feature is beta and uses
the explicit header above. A tiny request need not reach its clearing threshold.
[Context editing](https://platform.claude.com/docs/en/build-with-claude/context-editing).

## 4.2 Keep relevant outputs

Ordinary client tools hide their implementation and return a `tool_result`.
Subagents keep working context separate and return a summary. Skill scripts can
execute without loading source. These are different routes to a concise parent
conversation; none requires exposing every internal step.
[Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[subagents](https://code.claude.com/docs/en/sub-agents),
[skills](https://code.claude.com/docs/en/skills).

Application guidance: preserve an audit record separately from the material you
show the model. A summary is useful context, but it is not an adequate replacement
for exact evidence when correctness depends on a particular date or identifier.
The book's client loop keeps assistant blocks and paired tool results intact.

## 4.3 Programmatic tool calling

Claude can write code inside the code-execution container that calls application
tools, aggregates responses, and prints only the useful portion. The request makes
a tool callable from code with `allowed_callers: ["code_execution_20260120"]`,
alongside the corresponding execution tool. This can reduce model round trips and
keep bulk intermediate results out of model context.
[Programmatic tool calling](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

The programmatic caller does not magically move your private database into the
container. Your application still serves its client tools; generated code controls
how their returned values are processed before presentation.
Keep tool inputs narrowly scoped and validate them even when a generated program
is the immediate caller. [Execution flow](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

For the library system, this matters when hundreds of transcript excerpts must
be filtered before drafting. It is unnecessary overhead for a three-line fixture.
Choose it for an actual data-volume problem rather than for the feature count.

## 4.4 Editing and caching are different

Context editing changes what the model receives. Prompt caching reuses computation
over an unchanged prefix. Tool-result clearing can invalidate cached prefixes;
the documentation recommends making the amount cleared worthwhile.
[Context editing and caching](https://platform.claude.com/docs/en/build-with-claude/context-editing).

Neither mechanism is durable memory. Store needed artifacts before clearing them,
and keep a retrieval path for omitted detail. Application guidance: test a long
conversation that really crosses the configured threshold; merely receiving a
successful short response does not verify the clearing behavior.

## 4.5 Exercises

**Exercise 4-1.** Build a synthetic long history and observe an actual clearing
event. Preserve the client archive and compare the reported usage.

**Exercise 4-2.** Delegate a context-heavy lookup and compare the parent transcript
with the subagent's working record.

**Exercise 4-3.** Design an aggregation tool for many excerpts. State which data
must remain retrievable after only the aggregate enters context.

---

[← Chapter 3: Execution](03-execution.md) · [Book contents](README.md) · [Chapter 5: Output That Steers the Next Step →](05-output-that-steers.md)
