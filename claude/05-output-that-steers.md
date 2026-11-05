---
layout: book
title: Output That Steers the Next Step
book_label: Chapter 5
book_progress: 38
book_order: 50
description: Shape tool results for presentation, guidance, and exact downstream handoff
---

[← Chapter 4: The Transcript](04-the-transcript.md) · [Book contents](README.md) · [Chapter 6: Memory →](06-memory.md)

# Chapter 5 — Output That Steers the Next Step

> **In this chapter:** give a downstream step an exact artifact, return useful
> guidance, and separate a book result convention from an API requirement.

## 5.1 Hand off a value

Run `python3 claude/examples/05_handoff.py`.

```python
import sys
sys.path.insert(0, "claude/examples")
from common import REVIEW, draft_once, run

draft = draft_once("Please request a library review.")["output"]["data_slush"]["draft"]
result = run("Call review_draft with this exact draft:\n" + draft,
             tools=[REVIEW], required="review_draft")
reviews = [e for e in result["events"] if e["name"] == "review_draft"]
assert reviews and reviews[0]["arguments"]["draft"] == draft
assert reviews[0]["output"]["data_slush"]["sent"] is False
print(reviews[0]["output"]["summary"])
```

The two calls use real SDK requests. The local operations are deliberately pure.
If the model changes the handed-off draft, the assertion fails rather than treating
a paraphrase as exact transfer. Client tools and their paired results are the
documented transport; these exact-value checks are application policy.
[Tool results](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

## 5.2 A convention you can adopt

Our result contains a readable `summary`, an `instruction` for the next reader,
and machine-useful `data_slush`. These are **book conventions**, not reserved
Anthropic fields. JSON text can travel in a normal `tool_result`; an SDK MCP tool
can also return `structuredContent` alongside readable `content`.
[Client results](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[SDK structured results](https://code.claude.com/docs/en/agent-sdk/custom-tools).

Nothing prevents a Claude tool from returning all three jobs together. Managed
Agents likewise exposes custom tools whose results let the agent continue the task.
The choice to make those outputs pleasant to read and easy to pass onward belongs
to the tool author. [Managed Agents tools](https://platform.claude.com/docs/en/managed-agents/tools.md).

Application guidance: put exact identifiers, draft text, provenance, and partial-
success flags in structured fields. Use prose for meaning and next-step guidance.
Do not make another model recover an identifier from a formatted paragraph when
the next operation needs the exact value.

## 5.3 Guidance remains subordinate

A tool result can suggest review, another lookup, or user approval. It should not
be treated as a new system instruction. Retrieved transcripts and web pages may
contain hostile directives. Claude Code's MCP documentation explicitly warns about
prompt-injection risk from connected servers.
[MCP trust boundary](https://code.claude.com/docs/en/mcp).

The book therefore makes no send tool available, checks the exact evidence,
and treats the result instruction as advice. These application constraints are
more concrete than relying only on a sentence saying "do not send."

## 5.4 Failures steer too

An API `tool_result` can mark an error with `is_error`; an SDK MCP handler can
use `isError`. Our client loop translates domain exceptions into explicit error
results so the model can repair the call. It does not swallow authentication or
network failures and invent a successful draft.
[Tool result errors](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview),
[custom-tool errors](https://code.claude.com/docs/en/agent-sdk/custom-tools).

Application guidance: stop the downstream flow when the required artifact is
missing. A polished final model answer is not proof that the intended tool ran.
Inspect the tool event and its success state.

## 5.5 Exercises

**Exercise 5-1.** Add a provenance field and verify that the reviewer receives it
without changing its value.

**Exercise 5-2.** Return an explicit partial result and evaluate whether the next
step asks for the missing evidence rather than inventing it.

**Exercise 5-3.** Place a hostile instruction in the source transcript. Verify that
no sending capability becomes available.

---

[← Chapter 4: The Transcript](04-the-transcript.md) · [Book contents](README.md) · [Chapter 6: Memory →](06-memory.md)
