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

Our examples use no `BasicAgent` import because they must run with Python alone.
They preserve the metadata/method/result pattern but are not drop-in demonstrations
of a particular installed package. The installed package's loader, invocation
transport, and lifecycle remain **(unverified)** because its source was inaccessible.

That is a material portability distinction. Carrying one Python file does not
carry the modules it imports or the credentials and permissions it expects.

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
replay through that host are **(unverified)**. This chapter includes the host because
the requested portability map includes it, not to advertise an unobserved integration.

## 9.5 Carry a host contract

For each destination, record Python version, imports, filesystem availability,
network policy, authenticated scope, timeout, result encoding, and how context
is assembled. Add a smoke test for every facility actually used.

The portable part is the described capability with hidden work and useful output.
The nonportable part is often a host convenience that no one wrote down.
Keep that convenience out of the agent's semantic contract when possible, and
make it explicit when it is unavoidable.

## 9.6 Exercises

**Exercise 9-1.** Round-trip a result containing non-ASCII text through UTF-8 JSON.
Assert that its evidence and digest remain consistent.

**Exercise 9-2.** Write a host capability checklist for a read-only tool and for a
persistent memory tool. Identify the additional requirements of the latter.

**Exercise 9-3.** Propose a studio adapter with a real failure response. State what
must be observed before you would remove its unverified label.

---

[← Chapter 8: Replay and Time Travel](08-replay-and-time-travel.md) · [Book contents](README.md) · [Chapter 10: Building a Real System End to End →](10-building-a-real-system.md)
