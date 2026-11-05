---
layout: book
title: Building a Real System End to End
book_label: Chapter 10
book_progress: 73
book_order: 100
description: Build the same file-to-draft-to-review-to-replay workflow through real Claude tools
---

[← Chapter 9: Hosts and Portability](09-hosts-and-portability.md) · [Book contents](README.md) · [Appendix A: Reference Manual →](A-reference-manual.md)

# Chapter 10 — Building a Real System End to End

> **In this chapter:** call real tools over real files, verify the handoff, replay
> one pure step with later evidence, and preserve the original result.

## 10.1 Run the system

With the dependencies installed and a key available, run
`python3 claude/examples/10_system.py`. It prints the result and saves
`example-output/claude-system.json`. This book-level entry point also runs the flow:

```python
import importlib.util
import sys
sys.path.insert(0, "claude/examples")
from common import FIXTURES

spec = importlib.util.spec_from_file_location("book_claude_system", "claude/examples/10_system.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
result = module.system(FIXTURES / "chat.txt", FIXTURES / "later.txt")
assert "Monday" in result["replayed"]["summary"]
assert result["archive"]["step2"]["output"]["data_slush"]["sent"] is False
print(result["replayed"]["summary"])
```

The live part uses client tools through the official Messages API. The application
runs the handlers and returns their results, as in the documented tool lifecycle.
[Client tool execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## 10.2 Trace the four boundaries

Application design: first, read the synthetic chat file into text. Second, require
a draft tool call and verify that its transcript argument matches the file exactly.
Third, require the reviewer tool and verify that its draft argument matches the
returned artifact exactly. Fourth, copy the recorded draft arguments, append the
later file, and invoke only the pure draft handler locally.

The last step is application-owned replay, not an SDK session fork. It runs the
same local operation on more evidence without asking Claude to choose the operation
again. The SDK's distinct session-fork behavior is demonstrated in chapter 8.
[Tool execution](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[session forks](https://code.claude.com/docs/en/agent-sdk/sessions).

The tool draft remains an evidence-preserving template in both books. It contains
the original Friday date and the later Monday correction so the conflict is visible.
No claim of semantic resolution is hidden behind a mechanical equality test.

## 10.3 What the archive establishes

The saved record contains first-step and second-step calls and outputs, a replay
schema identifier, and the SHA-256 of `common.py`. It also stores the revised result.
This is a book format, not a Claude session serialization format.

For persisted replay, the example's `replay()` function checks the schema and source
digest before executing the saved step. A mismatch fails explicitly.
Keep the corresponding repository revision if the archive must remain replayable
after code changes. A hash identifies implementation bytes but does not restore them.

SDK sessions separately preserve conversation and tool history on disk.
That facility is useful for model continuation but does not replace the exact
application input and implementation record.
[SDK persistence](https://code.claude.com/docs/en/agent-sdk/sessions).

## 10.4 Evaluate the right property

The offline suite compiles and imports examples and tests the pure handler and
archive behavior. The opt-in live test calls the complete system with the key and
checks actual tool events, the exact draft transfer, and later evidence.
A skipped authenticated test is printed as skipped, never substituted with a fake
response.

The shared helper uses `auto` selection and strict tool schemas, then rejects a
workflow missing the required successful event. This is intentional for
`claude-opus-5-5`, which rejects forced `tool_choice` types `tool` and `any`.
Exact-source assertions remain necessary even with a schema-valid argument.
[Model-specific selection rules](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools).

For a future model-generated drafting implementation, add semantic evaluations:
preserved commitments, explicit uncertainty, accurate deadline handling, and no
invented sending claim. Keep those separate from transport, provenance, and replay
checks.

Application guidance: never publish real chat archives through this repository's
static book API. The site indexes manuscripts and synthetic examples, not private
conversation data.

## 10.5 Thinking and effort: spend reasoning where it helps

```python
import anthropic

with anthropic.Anthropic() as client:
    response = client.messages.create(
        model="claude-opus-5-5", max_tokens=8192,
        thinking={"type": "adaptive", "display": "summarized"},
        output_config={"effort": "medium"},
        messages=[{"role": "user", "content":
                   "Review a plan for exact-source drafting, review handoff, and pure replay. "
                   "Identify which checks belong in deterministic code. Never send."}],
    )
    print(response.model_dump_json(indent=2))
```

**What:** adaptive thinking lets Claude allocate reasoning, while effort
controls the requested reasoning intensity. **When:** architecture review,
ambiguous evidence, or multi-step recovery deserves more consideration than
formatting a known result. Keep the actual hashes and equality checks in code;
reasoning should not replace deterministic validation.
[Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking),
[effort](https://platform.claude.com/docs/en/build-with-claude/effort).

**Limits:** effort is not a correctness guarantee or exact token budget.
`max_tokens` covers the whole generated response, including thinking. Returned
thinking can be summarized or otherwise restricted; preserve returned blocks
when continuing a tool conversation instead of inventing or editing them.
Raise effort based on measured task quality, not because every step is labeled
“agentic.”
[Thinking with tools](https://platform.claude.com/docs/en/build-with-claude/thinking).

## 10.6 Task budgets: give a multi-turn job a resource target

```python
import anthropic

with anthropic.Anthropic() as client:
    with client.beta.messages.stream(
        model="claude-opus-5-5", max_tokens=8192,
        betas=["task-budgets-2026-03-13"],
        output_config={
            "effort": "medium",
            "task_budget": {"type": "tokens", "total": 12000},
        },
        messages=[{"role": "user", "content":
                   "Review the failure cases of a draft-only library follow-up pipeline."}],
    ) as stream:
        response = stream.get_final_message()
    print(response.usage)
```

**What:** a beta task budget gives the model a cross-turn resource target for
planning its work, rather than only limiting one response.
**When:** a long-running task needs cost-aware reasoning and tool-use choices.
**Limits:** this guidance does not replace a client iteration limit, timeout,
or billing guard. Preserve the documented budget state through a multi-turn
workflow; do not treat a fresh request with the original total as proof that
the whole job stayed within it. Managed session budgets are a separate hosted
resource control.
[Task budgets](https://platform.claude.com/docs/en/build-with-claude/task-budgets).

## 10.7 Advisor tool: consult a specialist model mid-generation

**What:** an executor can invoke a server-side advisor to obtain strategic
guidance within an agentic turn. **Exact tool declaration and beta:**

```python
advisor = {
    "type": "advisor_20260301", "name": "advisor",
    "model": "claude-opus-5-5", "max_uses": 1, "max_tokens": 4096,
}
betas = ["advisor-tool-2026-03-01"]
```

Add it to a compatible executor's `client.beta.messages.create()` request.
The official page lists supported executor/advisor pairings; choose a supported
pair rather than assuming any two models work. **When:** mostly mechanical
multi-step work occasionally needs a stronger strategic review. For this
book's tiny template operation the additional inference is unnecessary, but a
large evidence-review workflow can benefit from a deliberate planning boundary.
[Advisor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool).

**Limits:** advisor inference is separately billed and uses the advisor model's
rate limits. Inspect `usage.iterations`, not only executor totals. The newest
Opus advisor returns encrypted `advisor_redacted_result`; round-trip it
unchanged rather than claiming that advice text is available to your client.
Pending calls can cause `pause_turn`; retain the tool and beta while resuming.
An advisor is not an independent authorization system and does not run your
application's client tools.
[Advisor results and costs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool).

## 10.8 Token counting: estimate before a large request

```python
import anthropic

with anthropic.Anthropic() as client:
    count = client.messages.count_tokens(
        model="claude-opus-5-5",
        system="Review-only library workflow. Preserve evidence conflicts.",
        messages=[{"role": "user", "content":
                   "Original deadline Friday; later note Monday."}],
    )
    print(count.input_tokens)
```

**What:** count request input tokens without generating an answer.
**When:** choose chunk sizes, plan a context policy, or reject an unexpectedly
large upload before starting a job. **Limits:** input estimates do not include
unknown future output, future tool results, or the full cost of advisor
sub-inferences. Runtime usage remains the measurement of what was actually
billed. Count the same tools and system content you will submit.
[Token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting).

## 10.9 Message Batches: independent jobs without an interactive loop

```python
import anthropic

with anthropic.Anthropic() as client:
    batch = client.messages.batches.create(requests=[{
        "custom_id": "synthetic-library-review-1",
        "params": {
            "model": "claude-opus-5-5", "max_tokens": 1024,
            "messages": [{"role": "user", "content":
                          "Draft a library review request. Never send it."}],
        },
    }])
    print(batch.id, batch.processing_status)
```

**What:** submit independent Messages requests for asynchronous batch processing.
**When:** evaluate many synthetic drafting prompts or process a backlog whose
items do not need immediate interaction. **Limits:** creation only accepts the
job; retrieve its processing status and consume
`client.messages.batches.results(batch.id)` after completion, checking each
item's result type by `custom_id`. A batch does not automatically execute
client tools or order dependent steps. Our draft→review workflow still needs
an application orchestrator; do not submit its dependent steps as independent
batch items and hope ordering works.
[Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing).

## 10.10 Exercises

**Exercise 10-1.** Run the live system with your own synthetic temporary files.
Check the source digest and both exact-value handoffs.

**Exercise 10-2.** Modify the archive's implementation digest and verify that
persisted replay refuses before invoking a handler.

**Exercise 10-3.** Replace the template with a semantic drafting tool. Keep the
original mechanical tests and add an independent quality evaluation.

---

[← Chapter 9: Hosts and Portability](09-hosts-and-portability.md) · [Book contents](README.md) · [Appendix A: Reference Manual →](A-reference-manual.md)
