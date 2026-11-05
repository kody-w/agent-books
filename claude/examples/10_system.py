import argparse
import copy
import hashlib
import json
from pathlib import Path
from common import FIXTURES, REVIEW, draft_once, execute, run


def replay(archive, later_text):
    source = Path(__file__).with_name("common.py")
    if archive["schema"] != "book-claude-replay/1.0":
        raise ValueError("unsupported replay schema")
    if archive["source_sha256"] != hashlib.sha256(source.read_bytes()).hexdigest():
        raise ValueError("tool source changed; replay refused")
    first = archive["step1"]
    if first["name"] != "draft_follow_up":
        raise ValueError("only the pure draft step can be replayed")
    arguments = copy.deepcopy(first["arguments"])
    arguments["transcript"] += "\nLater evidence:\n" + later_text
    return execute(first["name"], arguments)


def system(chat, later):
    first = draft_once(chat.read_text(encoding="utf-8"))
    draft = first["output"]["data_slush"]["draft"]
    second = run("Call review_draft with this exact draft:\n" + draft,
                 tools=[REVIEW], required="review_draft")
    reviews = [e for e in second["events"] if e["name"] == "review_draft"]
    if not reviews or reviews[0]["arguments"].get("draft") != draft:
        raise RuntimeError("review handoff changed the draft")
    if reviews[0]["output"]["status"] != "success":
        raise RuntimeError("review failed")
    source = Path(__file__).with_name("common.py")
    archive = {
        "schema": "book-claude-replay/1.0",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "step1": first, "step2": reviews[0],
    }
    replayed = replay(archive, later.read_text(encoding="utf-8"))
    return {"archive": archive, "replayed": replayed}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat", type=Path, default=FIXTURES / "chat.txt")
    parser.add_argument("--later", type=Path, default=FIXTURES / "later.txt")
    parser.add_argument("--out", type=Path, default=Path("example-output/claude-system.json"))
    args = parser.parse_args()
    result = system(args.chat, args.later)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
