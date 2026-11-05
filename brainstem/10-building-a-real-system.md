---
layout: book
title: Building a Real System End to End
book_label: Chapter 10
book_progress: 73
book_order: 100
description: Read a chat, draft a follow-up, hand it off, and replay with a later file
---

[← Chapter 9: Hosts and Portability](09-hosts-and-portability.md) · [Book contents](README.md) · [Appendix A: Reference Manual →](A-reference-manual.md)

# Chapter 10 — Building a Real System End to End

> **In this chapter:** compose two capabilities over real files, replay only
> step 1 with later evidence, and check exact data movement rather than prose plausibility.

## 10.1 Run the system

Run `python3 brainstem/examples/10_system.py`. It prints an archive and both draft
versions. This shorter executable form makes the acceptance checks visible:

```python
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import FIXTURES, system

result = system(FIXTURES / "chat.txt", FIXTURES / "later.txt")
assert result["review"]["data_slush"]["draft"] == result["original"]["data_slush"]["draft"]
assert result["review"]["data_slush"]["sent"] is False
assert "Monday" not in result["original"]["summary"]
assert "Monday" in result["replayed"]["summary"]
assert result["events_after_replay"] == 3
print(result["replayed"]["summary"])
```

The same task appears in the companion chapter: read a chat transcript, draft a
follow-up, hand its result to a second step, and replay step 1 with a later file.
Both use the same synthetic library discussion and deadline correction.

## 10.2 Trace the four boundaries

First, file I/O reads the chat into a string. The agent receives text, not a
machine-specific path. That makes the call independently recordable.

Second, `DraftFollowUp` produces a draft and source digest. The system checks
success before accessing `data_slush`. It does not report an empty draft as success.

Third, `ReviewDraft` receives the exact draft field. It returns a review-ready
artifact with `sent: false`; no mail integration exists.

Fourth, replay copies only the first call's arguments and appends the later file's
contents. It adds one new draft event. The reviewer is not re-executed, and the old
review continues to refer to the old draft. If a human accepts the revised draft,
a new review should be recorded rather than silently updating the earlier one.

## 10.3 The draft is intentionally modest

The output preserves evidence verbatim. It does not write an elegant message or
decide which deadline is authoritative. This lets deterministic tests establish
what actually crossed the boundary.

For a semantic drafting tool, replace the template behind `perform()` and evaluate
it separately: does it preserve commitments, identify conflicting dates, omit
unsupported promises, and remain a draft? Keep the interface and handoff tests,
but do not confuse them with a quality evaluation.

Likewise, a deterministic caller selecting known names is not a test of description-
driven model behavior. It isolates the mechanics so a later model-based evaluation
can identify selection errors rather than rediscovering basic data loss.

## 10.4 Make the archive durable

The command prints the archive; redirect its JSON output to a chosen file if you
want a durable run record. `MiniLoop.save()` is also available for recording events
with their implementation digest. Store the matching repository revision beside it.

Do not put real transcripts in a public static book repository. In a deployed
system, retain archives under appropriate access control and deletion policy.
The JSON endpoint that publishes this book is not a suitable store for private
conversation data.

The local tests additionally run all ten programs, check replay immutability and
source mismatch refusal, and exercise the complete flow with independent temporary
files. These checks cover mechanics, not the unavailable production hosts.

## 10.5 Exercises

**Exercise 10-1.** Use two files you create in a temporary directory. Change the
later deadline and verify that only the replayed draft changes.

**Exercise 10-2.** Add a review of the revised draft as a fourth event. Preserve
both review versions and make their source identities explicit.

**Exercise 10-3.** Replace the drafting template with a model-backed implementation.
Keep mechanical checks separate from semantic quality and live-access checks.

---

[← Chapter 9: Hosts and Portability](09-hosts-and-portability.md) · [Book contents](README.md) · [Appendix A: Reference Manual →](A-reference-manual.md)
