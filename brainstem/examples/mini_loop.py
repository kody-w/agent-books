"""Deterministic name-selected test caller, not an LLM or the Brainstem runtime."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

from agent import DraftFollowUp, ReviewDraft

SOURCE = Path(__file__).with_name("agent.py")
FIXTURES = Path(__file__).resolve().parents[2] / "fixtures"


def source_hash():
    return hashlib.sha256(SOURCE.read_bytes()).hexdigest()


class MiniLoop:
    def __init__(self):
        self.tools = {}
        self.transcript = []
        self.register(DraftFollowUp())
        self.register(ReviewDraft())

    def register(self, agent):
        name = agent.metadata["name"]
        if name in self.tools:
            raise ValueError(f"duplicate tool: {name}")
        self.tools[name] = agent

    def call(self, name, arguments):
        if name not in self.tools:
            raise ValueError(f"unknown tool: {name}")
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be an object")
        agent = self.tools[name]
        schema = agent.metadata["parameters"]
        props = schema["properties"]
        if set(arguments) - set(props):
            raise ValueError("unexpected argument")
        if set(schema["required"]) - set(arguments):
            raise ValueError("missing argument")
        for key, value in arguments.items():
            if props[key]["type"] == "string" and not isinstance(value, str):
                raise ValueError(f"{key} must be a string")
        result = agent.perform(**arguments)
        event = {
            "name": name,
            "arguments": copy.deepcopy(arguments),
            "output": copy.deepcopy(result),
        }
        self.transcript.append(event)
        return result

    def save(self, path):
        path.write_text(
            json.dumps(
                {"schema": "book-replay/1.0", "source_sha256": source_hash(),
                 "events": self.transcript},
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

    def replay(self, archive, index, later=""):
        if archive["schema"] != "book-replay/1.0":
            raise ValueError("unsupported replay schema")
        if archive["source_sha256"] != source_hash():
            raise ValueError("agent source changed; replay refused")
        event = archive["events"][index]
        if event["name"] != "DraftFollowUp":
            raise ValueError("this replay profile allows only the pure draft step")
        arguments = copy.deepcopy(event["arguments"])
        if later:
            arguments["transcript"] += "\nLater evidence:\n" + later
        return self.call(event["name"], arguments)


def load_trusted_file(path):
    """Only call with reviewed local code; importing Python is execution."""
    spec = importlib.util.spec_from_file_location("book_trusted_agent", path)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load agent")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.ReviewDraft()


def system(path, later_path):
    loop = MiniLoop()
    draft = loop.call("DraftFollowUp", {"transcript": path.read_text(encoding="utf-8")})
    if draft["status"] != "success":
        raise RuntimeError(draft["message"])
    review = loop.call("ReviewDraft", {"draft": draft["data_slush"]["draft"]})
    archive = {
        "schema": "book-replay/1.0",
        "source_sha256": source_hash(),
        "events": copy.deepcopy(loop.transcript),
    }
    replayed = loop.replay(archive, 0, later_path.read_text(encoding="utf-8"))
    return {"original": draft, "review": review, "replayed": replayed,
            "archive": archive, "events_after_replay": len(loop.transcript)}
