---
layout: book
title: Replay and Time Travel
book_label: Chapter 8
book_progress: 59
book_order: 80
description: Use checkpoints, session resume, forks, and application-owned step replay
---

[← Chapter 7: Growing Mid-Session](07-growing-mid-session.md) · [Book contents](README.md) · [Chapter 9: Hosts and Portability →](09-hosts-and-portability.md)

# Chapter 8 — Replay and Time Travel

> **In this chapter:** branch a real SDK session, understand rewind's boundaries,
> and implement exact local step replay without claiming deterministic model output.

## 8.1 Fork a conversation

Run `python3 claude/examples/08_replay.py`. It creates a draft session and forks it
with the deadline correction. The core option construction can be inspected offline:

```python
from claude_agent_sdk import ClaudeAgentOptions

options = ClaudeAgentOptions(
    model="claude-opus-5-5",
    tools=[],
    resume="replace-with-a-real-session-id",
    fork_session=True,
    max_turns=3,
)
print(options.fork_session)
```

The placeholder above is only an offline options demonstration; the numbered program
captures a real `ResultMessage.session_id` and uses it. Resume extends a selected
session; fork copies its history into a new session and leaves the original intact.
[SDK sessions](https://code.claude.com/docs/en/agent-sdk/sessions).

## 8.2 Checkpoints and rewind

Claude Code creates checkpoints for prompts that start turns and tracks file edits.
`/rewind` can restore conversation, code, or both, and can summarize selected portions.
It is a session-level recovery mechanism, not a replacement for version control.
[Checkpointing](https://code.claude.com/docs/en/checkpointing).

The current documentation is nuanced about shell changes: once a file has been
tracked by Claude's editing tools, later Bash changes to that file can be undone;
a file changed only by Bash is not tracked. Most subagent edits to previously
untracked files are not restored. External changes and linked files have further
limits. Do not promise universal filesystem rollback.
[Checkpoint limitations](https://code.claude.com/docs/en/checkpointing).

## 8.3 Conversation state is not filesystem state

SDK sessions preserve prompts, calls, results, and responses. They do not snapshot
the filesystem; the SDK documentation treats file checkpointing separately.
A resumed model can therefore see old conversation context while reading newer
files from disk. [Session persistence boundary](https://code.claude.com/docs/en/agent-sdk/sessions).

Application guidance: record input hashes and the exact file revision used for a
decision. A session identifier alone is not enough to prove which current bytes
will be read after resumption.

The SDK also provides direct session inspection and a `fork_session()` function
that can branch up to a selected message identifier. This is useful when an
application needs explicit branch control rather than only continuing the latest
history. [Python session APIs](https://code.claude.com/docs/en/agent-sdk/python).

## 8.4 Replay a tool operation

There is no need to wait for a special product primitive to replay a pure tool
handler. An application can save the tool name, arguments, implementation identity,
and result, then invoke that same handler with additional evidence.
That is an application convention built on ordinary client tools, not a promise
that an SDK session fork will rerun one fixed operation.
[Client execution boundary](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview).

Chapter 10 implements precisely this distinction: the initial calls go through
Claude, then Python replays the recorded pure draft operation locally.
The archive keeps both results. A separate SDK fork asks the model again and can
produce a different answer; neither session persistence nor prompt caching guarantees
byte-identical model output.
[Sessions](https://code.claude.com/docs/en/agent-sdk/sessions),
[caching semantics](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

Application guidance: never repeat an external side effect under a "replay" label
without an explicit idempotency and approval policy.

## 8.5 Exercises

**Exercise 8-1.** Verify that a fork returns a distinct session identifier and
leaves the original conversation available.

**Exercise 8-2.** Change a source file after a session is saved. Demonstrate why
session history and filesystem history require separate tracking.

**Exercise 8-3.** Replay a pure handler locally, then ask the model again with the
same evidence. State exactly what each experiment proves.

---

[← Chapter 7: Growing Mid-Session](07-growing-mid-session.md) · [Book contents](README.md) · [Chapter 9: Hosts and Portability →](09-hosts-and-portability.md)
