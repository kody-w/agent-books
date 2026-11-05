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

For a future model-generated drafting implementation, add semantic evaluations:
preserved commitments, explicit uncertainty, accurate deadline handling, and no
invented sending claim. Keep those separate from transport, provenance, and replay
checks.

Application guidance: never publish real chat archives through this repository's
static book API. The site indexes manuscripts and synthetic examples, not private
conversation data.

## 10.5 Exercises

**Exercise 10-1.** Run the live system with your own synthetic temporary files.
Check the source digest and both exact-value handoffs.

**Exercise 10-2.** Modify the archive's implementation digest and verify that
persisted replay refuses before invoking a handler.

**Exercise 10-3.** Replace the template with a semantic drafting tool. Keep the
original mechanical tests and add an independent quality evaluation.

---

[← Chapter 9: Hosts and Portability](09-hosts-and-portability.md) · [Book contents](README.md) · [Appendix A: Reference Manual →](A-reference-manual.md)
