---
layout: book
title: Hosts and Portability
book_label: Chapter 9
book_progress: 66
book_order: 90
description: Port the interface without assuming identical runtime facilities
---

[← Chapter 8: Replay and Time Travel](08-replay-and-time-travel.md) · [Book contents](README.md) · [Chapter 10: Building a Real System End to End →](10-building-a-real-system.md)

# Chapter 9 — Hosts and Portability

> **In this chapter:** cross a JSON boundary, identify host responsibilities,
> and distinguish a portable pattern from a verified deployment.

## 9.1 Cross the wire

Run `python3 brainstem/examples/09_hosts.py`.

```python
import json
import sys
sys.path.insert(0, "brainstem/examples")
from mini_loop import MiniLoop

wire = '{"name":"ReviewDraft","arguments":{"draft":"Library follow-up"}}'
request = json.loads(wire)
result = MiniLoop().call(request["name"], request["arguments"])
encoded = json.dumps(result)
assert json.loads(encoded)["data_slush"]["sent"] is False
print(encoded)
```

This is serialization, not a running HTTP endpoint. It establishes that the request
and result can cross a text boundary without depending on Python object identity.
An actual server must also define transport errors, authentication, request limits,
and concurrent execution.

## 9.2 Local Brainstem

The supplied agents import `BasicAgent` from `agents.basic_agent`.
The news agent calls its base constructor with a name and metadata; the memory agents
also depend on `memory_store`. A local host must provide those modules and decide
how agents are discovered and invoked.

The inspected `BasicAgent` exposes `to_tool()` as an OpenAI-style function declaration
(`agents/basic_agent.py:25–34`); its default `system_context()` returns `None`
(lines 20–23). The runtime scans `AGENTS_PATH/*_agent.py`, instantiates classes,
validates their public shape, and quarantines invalid or duplicate registrations
(`brainstem.py:1528–1698,1836–1864`). This is fresh request-time loading, not a
long-lived agent-object registry.

The stdlib examples omit that base class. The live runner supplies adapters around
their unchanged implementations, copies the runtime into a temporary directory,
sets absolute `AGENTS_PATH` and `SOUL_PATH`, and selects an unused loopback port.
`brainstem.py:436–462` defines those settings. Credential files are copied privately
and deleted with the temporary directory; the real installation and its work
endpoint on port 7071 are never imported, started, or called.

Run `python3 scripts/run_brainstem_live.py` in an environment containing `flask`,
`flask-cors`, `python-dotenv`, and `requests`, with existing Copilot access.
The command makes real model requests. It is not part of offline CI.
Its checked-in [fixture](../fixtures/brainstem-live.json) records the observed model,
source hashes, synthetic requests, tool outputs, and exact acceptance assertions.

## 9.3 Pyodide and a browser

The news source documents a Pyodide path and imports `pyodide.http.open_url`
inside its fetch helper. That is evidence of an intended networking adapter.
The browser still controls CORS, network availability, and storage lifetime.
Ordinary CPython file paths and SQLite assumptions do not automatically survive
inside WebAssembly.

A working browser deployment is **(unverified)** here. To verify one, use the actual
browser host, call a real read-only capability, inspect the returned structure,
and reload the page to test persistence separately. Do not claim portability from
Python syntax compilation alone.

## 9.4 Copilot Studio boundary

A studio host would need an adapter from its action schema to the agent declaration,
an execution location for Python, and a result mapping back into conversation.
Those are architectural requirements, not a claim that a particular connector is
already installed.

No Copilot Studio deployment was performed; execution, memory, hot loading, and
replay through that host are **(unverified)**.

## 9.5 Conversation statelessness

The conversation loop keeps no conversation between requests. The evidence is
specific: `brainstem.py:2262–2266` reads `conversation_history` from this request
and creates or accepts a `session_id`; lines 2300–2302 build a new `messages`
list from the current soul, optional context, supplied history, and new input.
Lines 2306–2340 append assistant/tool messages only to that local list.
Lines 2344–2356 return response text and logs, not a server-side conversation handle.
Passing the same `session_id` without history does not resume a hidden conversation.

This makes the caller's transcript the **only carried conversation state**. A caller
can send copies to any number of identically configured Brainstems in parallel,
choose one result, or keep separate branches. It must retain the messages itself;
the endpoint does not return a complete internal tool-call transcript.

This is not a claim that the entire process is stateless. Soul and agent files,
credentials, model selection, diagnostic logs, and optional memory storage persist.
`system_context()` reads those stores before each model turn (lines 2286–2294).
Equivalent history alone cannot guarantee identical output if those inputs differ,
or if a model/network call is nondeterministic. Shared file-writing agents also need
coordination across workers. The core tool loop executes sequentially with three
tool-call rounds and a final tool-less completion (lines 2180–2230,2305–2340).

## 9.6 RAPP/1 frames and distribution

Use [RAPP/1](https://github.com/kody-w/rapp-1), specifically
[SPEC sections 4–8](https://github.com/kody-w/rapp-1/blob/main/SPEC.md), when a
distributed transcript needs verifiable content and order. The fetched specification
defines an eleven-key frame:

```json
{
  "spec": "rapp/1",
  "kind": "memory.tool-call",
  "stream_id": "<registered memory stream>",
  "seq": 0,
  "utc": "2026-11-05T20:00:00.000Z",
  "payload": {"name": "DraftFollowUp", "arguments": {}, "output": {}},
  "payload_hash": "<64 lowercase hex>",
  "frame_hash": "<64 lowercase hex>",
  "prev": null,
  "prev_wave": null,
  "sig": null
}
```

This is a shape illustration, **not a valid frame fixture**: identifiers and hashes
are placeholders. Use the protocol's conforming implementation and tests, not
`json.dumps(sort_keys=True)` as a substitute for RFC 8785 canonicalization.
`payload_hash` addresses the payload in the `rapp/1:particle` domain; `frame_hash`
addresses the frame minus `frame_hash` and `sig` in the `rapp/1:wave` domain.
The next frame's `prev` is the predecessor's **payload_hash**, not its frame hash.
Consumers verify schema, registry/stream binding, both hashes, chain, wire rules,
and any signature, against a trusted checkpoint. Unsigned local memory frames
can show integrity relative to that checkpoint, not author identity.

The current Brainstem `/chat` endpoint does not emit these frames. A caller-side
recorder must capture actual requests, results, implementation hashes, and branches,
then use a conforming frame producer. Our live fixture is ordinary JSON, and the
chapter 8 archive is `book-replay/1.0`; neither is falsely labeled RAPP/1-conformant.

For distribution, ship reviewed agent files plus their imports, pinned runtime
identity, and a host contract. RAPP/1 section 9 specifies an egg for packaging;
sections 7–8 define transportable events and `/chat`. A load balancer can route
stateless conversation requests to compatible workers; a transcript/frame store
stays caller-owned. That design permits horizontal conversation processing without
claiming a built-in scheduler, distributed database, or automatic conflict resolution.

## 9.7 Carry a host contract

For each destination, record Python version, imports, filesystem availability,
network policy, authenticated scope, timeout, result encoding, and how context
is assembled. Add a smoke test for every facility actually used.

The portable part is the described capability with hidden work and useful output.
The nonportable part is often a host convenience that no one wrote down.
Keep that convenience out of the agent's semantic contract when possible, and
make it explicit when it is unavoidable.

## 9.8 Exercises

**Exercise 9-1.** Round-trip a result containing non-ASCII text through UTF-8 JSON.
Assert that its evidence and digest remain consistent.

**Exercise 9-2.** Write a host capability checklist for a read-only tool and for a
persistent memory tool. Identify the additional requirements of the latter.

**Exercise 9-3.** Propose a studio adapter with a real failure response. State what
must be observed before you would remove its unverified label.

---

[← Chapter 8: Replay and Time Travel](08-replay-and-time-travel.md) · [Book contents](README.md) · [Chapter 10: Building a Real System End to End →](10-building-a-real-system.md)
