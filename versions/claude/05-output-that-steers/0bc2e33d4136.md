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

## 5.5 Structured outputs: make the final answer machine-readable

```python
import anthropic
from pydantic import BaseModel

class DraftReview(BaseModel):
    draft: str
    deadline_conflict: bool
    sent: bool

with anthropic.Anthropic() as client:
    response = client.messages.parse(
        model="claude-opus-5-5", max_tokens=1024,
        output_format=DraftReview,
        system="Never send. Preserve both dates when evidence conflicts.",
        messages=[{"role": "user", "content":
                   "Draft a review request. Original date Friday; later note Monday."}],
    )
    if response.stop_reason != "end_turn" or response.parsed_output is None:
        raise RuntimeError(f"No complete structured result: {response.stop_reason}")
    review = response.parsed_output
    if review.sent:
        raise RuntimeError("The response incorrectly claims sending")
    print(review.model_dump_json())
```

**What:** constrained JSON output gives the caller a predictable final-answer
shape. Strict tool use in chapter 2 constrains *arguments* instead.
**When:** downstream code needs explicit flags and fields rather than prose
extraction. The typed parser derives its supported JSON Schema from the model.
[Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

**Limits:** schema conformance is not evidence that a draft is accurate.
Refusals and token-limit truncation require handling before consuming parsed
output. Keep semantic assertions and do not treat `sent: false` as proof that no
other component sent mail. This system has no send capability at all.
[Output guarantees and exceptions](https://platform.claude.com/docs/en/build-with-claude/structured-outputs).

## 5.6 Output styles: change Claude Code's working voice

**What:** a Claude Code output style modifies session-level role and response
instructions, unlike a schema on one API response. **Example:** copy
[review-note.md](config/output-styles/review-note.md) to
`.claude/output-styles/review-note.md`:

```yaml
---
name: Review note
description: Concise, evidence-first library review notes.
keep-coding-instructions: true
---
Lead with the draft artifact and unresolved evidence conflicts.
State explicitly that nothing has been sent.
Use short paragraphs; preserve exact dates and identifiers.
```

Select it with `/output-style Review note`. **When:** a team wants a consistent
review voice across a session without rewriting each task prompt.
**Limits:** a style is not JSON validation, a permission policy, or a substitute
for skills that carry a particular procedure. Custom styles replace parts of
Claude Code's default instructions; retaining coding instructions is deliberate
here. The setting is case-sensitive when configured directly in a settings file.
[Output styles](https://code.claude.com/docs/en/output-styles).

## 5.7 Citations and search-result blocks: preserve evidence links

```python
import anthropic

with anthropic.Anthropic() as client:
    response = client.messages.create(
        model="claude-opus-5-5", max_tokens=1024,
        messages=[{"role": "user", "content": [
            {"type": "document", "title": "Synthetic library discussion",
             "source": {"type": "text", "media_type": "text/plain",
                        "data": "Original review: Friday. Later update: Monday."},
             "citations": {"enabled": True}},
            {"type": "text", "text": "State the deadline conflict with citations."},
        ]}],
    )
    print(response.model_dump_json(indent=2))
```

**What:** citation-enabled documents let Claude attach structured source
references to claims. A retrieval tool can return citation-ready `search_result`
blocks rather than flattening every retrieved passage into opaque prose.
**When:** a human reviewer needs to inspect the exact support for a claimed date.
[Citations](https://platform.claude.com/docs/en/build-with-claude/citations),
[search results](https://platform.claude.com/docs/en/build-with-claude/search-results).

**Exact retrieval result configuration:** place this block in the `content`
list of the matching `tool_result`, substituting your authorized source identifier.
The documented `source` field accepts any stable string, including an internal
identifier rather than a URL.
[Source identifiers](https://platform.claude.com/docs/en/build-with-claude/search-results).

```python
retrieved = {
    "type": "search_result", "source": "urn:synthetic:library-policy",
    "title": "Synthetic policy excerpt",
    "content": [{"type": "text", "text": "Library follow-ups remain drafts."}],
    "citations": {"enabled": True},
}
```

**Limits:** the application supplies the provenance; a fabricated source URL
does not become genuine because it is in a citation block. The URN above names
synthetic evidence, not a fetched policy. Preserve actual retrieved
content and surface citation fields in the reader UI. Document citations and
structured JSON output have feature-combination restrictions; do not assume one
response can use every output mode simultaneously.
[Citation support and limitations](https://platform.claude.com/docs/en/build-with-claude/citations).

## 5.8 Exercises

**Exercise 5-1.** Add a provenance field and verify that the reviewer receives it
without changing its value.

**Exercise 5-2.** Return an explicit partial result and evaluate whether the next
step asks for the missing evidence rather than inventing it.

**Exercise 5-3.** Place a hostile instruction in the source transcript. Verify that
no sending capability becomes available.

---

[← Chapter 4: The Transcript](04-the-transcript.md) · [Book contents](README.md) · [Chapter 6: Memory →](06-memory.md)
