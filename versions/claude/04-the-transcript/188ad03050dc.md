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

## 4.1 Context editing: retain the archive, trim active context

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

**When:** long tool traces displace the evidence needed for the next decision.
**Exact policy:** replace the example's `edits` array with the following to
trigger at 30,000 input tokens, retain three tool uses, and require a worthwhile
minimum clearing:

```python
context_management = {"edits": [{
    "type": "clear_tool_uses_20250919",
    "trigger": {"type": "input_tokens", "value": 30000},
    "keep": {"type": "tool_uses", "value": 3},
    "clear_at_least": {"type": "input_tokens", "value": 5000},
    "exclude_tools": ["review_draft"],
}]}
```

**Limits:** clearing cannot act until eligible content and the threshold exist.
Inspect `context_management.applied_edits` in the response before claiming a
clearing event. Tool-result clearing differs from thinking-block clearing; the
order of edits matters when combining strategies. This changes the model's view,
not the client's archive or the underlying files.
[Policy fields and reporting](https://platform.claude.com/docs/en/build-with-claude/context-editing).

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
a tool callable from code with `allowed_callers: ["code_execution_20260521"]`,
alongside `code_execution_20260521`. This can reduce model round trips and
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

**Example:** run
`python3 claude/examples/04_transcript.py --mode programmatic`. The program
exposes a read-only synthetic catalog, verifies that a programmatic caller
actually used it, and resumes the same container after returning results.
Its exact catalog declaration is:

```python
catalog_tool = {
    "name": "list_review_items",
    "description": "Return synthetic review items with page counts.",
    "input_schema": {"type": "object", "properties": {},
                     "additionalProperties": False},
    "allowed_callers": ["code_execution_20260521"],
}
```

**Version rule:** both `code_execution_20260120` and
`code_execution_20260521` are accepted caller identifiers and are interchangeable.
The response's `caller.type` is always `code_execution_20260120`, even when the
request uses `20260521`. Thus request and response identifiers need not look
identical. This edition uses `20260521` consistently in declarations and checks
the documented `20260120` response tag; it does not invent a newer caller
response type.
[Caller versions](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

**Limits:** the application still executes the custom operation. Return its
results promptly: a paused generated program stops waiting after about four
minutes, and idle containers are currently reclaimed after about five minutes.
Programs have no network egress of their own; access controlled services through
validated tools. Measure billed tokens and elapsed time on representative data,
because container startup can cost more than it saves for a small first request.
[Programmatic execution lifecycle](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling).

## 4.4 Editing and caching are different

Context editing changes what the model receives. Prompt caching reuses computation
over an unchanged prefix. Tool-result clearing can invalidate cached prefixes;
the documentation recommends making the amount cleared worthwhile.
[Context editing and caching](https://platform.claude.com/docs/en/build-with-claude/context-editing).

Neither mechanism is durable memory. Store needed artifacts before clearing them,
and keep a retrieval path for omitted detail. Application guidance: test a long
conversation that really crosses the configured threshold; merely receiving a
successful short response does not verify the clearing behavior.

## 4.5 Compaction: summarize a long conversation

```python
import anthropic

history = [
    {"role": "user", "content": "The original library review date was Friday."},
    {"role": "assistant", "content": "I will preserve Friday as the original date."},
    {"role": "user", "content": "Later evidence says Monday; preserve the conflict."},
]
with anthropic.Anthropic() as client:
    response = client.beta.messages.create(
        model="claude-opus-5-5", max_tokens=4096,
        betas=["compact-2026-09-04"],
        messages=history, compaction={"type": "summarize"},
    )
    if response.stop_reason != "compaction":
        raise RuntimeError(f"No compaction: {response.stop_reason}")
    compacted_history = [{"role": "assistant", "content": response.content}]
    print(response.content)
```

**What:** compaction produces an explicit compacted representation of prior
conversation; context editing selectively clears eligible blocks instead.
**When:** important state is distributed across a long task rather than confined
to old tool results. The index documents threshold-triggered, on-demand,
keep-recent-turns, and background approaches.
[Compaction overview](https://platform.claude.com/docs/en/build-with-claude/compaction),
[on demand](https://platform.claude.com/docs/en/build-with-claude/compaction-on-demand).

**Limits:** a summary can omit detail. Preserve source files, exact artifact IDs,
and the original archive outside the compacted context. Background compaction
must replace only the prefix actually submitted to the summarizer; keep newer
turns after it, and wait for a completed compaction result before swapping.
The beta header here is the current on-demand interface, not the older context
editing beta.
[Background compaction](https://platform.claude.com/docs/en/build-with-claude/compaction-background).

## 4.6 Message threads: send only the new turns

```python
import anthropic

with anthropic.Anthropic() as client:
    thread = client.beta.messages.thread(
        model="claude-opus-5-5", max_tokens=1024,
        cache_control={"type": "ephemeral"},
        system="Keep library follow-ups as drafts. Preserve conflicting dates.",
    )
    thread.send({"role": "user", "content": "The review was planned for Friday."})
    reply = thread.send({"role": "user", "content":
                         "Later evidence says Monday. Explain what needs review."})
    print(reply.content)
```

**What:** a beta Messages thread stores a conversation prefix server-side; the
SDK helper keeps the local history and sends only new messages on continuation.
**When:** application-owned tool loops have long transcripts and repeated
transmission is unnecessary overhead. This is a Messages feature, not an Agent
SDK session ID.
[Message threads](https://platform.claude.com/docs/en/build-with-claude/message-threads).

**Limits:** keep your own history. Prefix storage is transient, not durable
application persistence; the helper can replay full history after a missing
thread. Changed fingerprints or unsupported requests need explicit handling.
The helper manages `message-threads-2026-08-12`; raw calls must supply the
documented header and create/continue fields. A thread does not execute tools
or restore a filesystem.
[Thread recovery and retention](https://platform.claude.com/docs/en/build-with-claude/message-threads).

## 4.7 Mid-conversation system messages and tool changes

**What:** the beta inline-tools interface changes instructions or tool
availability at a particular conversation point without rewriting the prefix.
**When:** switch a task from research to review while preserving earlier
context and its cacheability. **Exact example:** this configuration withdraws
our tool after its initial user turn:

```python
import sys
sys.path.insert(0, "claude/examples")
from common import DRAFT, MODEL
import anthropic

with anthropic.Anthropic() as client:
    result = client.beta.messages.create(
        model=MODEL, max_tokens=1024, betas=["inline-tools-2026-09-15"],
        tools=[DRAFT],
        messages=[
            {"role": "user", "content": "Acknowledge this review-only phase."},
            {"role": "system", "content": [{
                "type": "tool_removal",
                "tool": {"type": "tool_reference", "name": "draft_follow_up"},
            }]},
        ],
    )
    print(result.content)
```

**Limits:** these are trusted application messages, never text copied from an
untrusted transcript. Tool removal is selection/context control, not revocation
of a credential already held by your executor. Keep the executor's own current
authorization check.
[Inline tool and system-message protocol](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages).

## 4.8 Fine-grained tool streaming

**What:** stream tool arguments as they are generated rather than waiting for
buffered, validated argument JSON. **Exact configuration:**

```python
import copy
import sys
sys.path.insert(0, "claude/examples")
from common import DRAFT

streaming_draft = copy.deepcopy(DRAFT)
streaming_draft["eager_input_streaming"] = True
```

Use the declaration in `client.messages.stream(...)`, and consume the stream's
final message before executing the draft handler. **When:** a large generated
file or argument should begin arriving early. **Limits:** chunks may not be
valid JSON and a truncated response may never form a complete argument. Never
execute a partial command or send a partial document just because bytes arrived;
validate the assembled argument and final stop reason.
[Fine-grained tool streaming](https://platform.claude.com/docs/en/agents-and-tools/tool-use/fine-grained-tool-streaming).

## 4.9 Exercises

**Exercise 4-1.** Build a synthetic long history and observe an actual clearing
event. Preserve the client archive and compare the reported usage.

**Exercise 4-2.** Delegate a context-heavy lookup and compare the parent transcript
with the subagent's working record.

**Exercise 4-3.** Design an aggregation tool for many excerpts. State which data
must remain retrievable after only the aggregate enters context.

---

[← Chapter 3: Execution](03-execution.md) · [Book contents](README.md) · [Chapter 5: Output That Steers the Next Step →](05-output-that-steers.md)
