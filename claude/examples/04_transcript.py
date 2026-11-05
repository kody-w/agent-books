import argparse
import json
import anthropic
from common import MODEL, check_server_results, require_key

EXECUTION_TOOL = {"type": "code_execution_20260521", "name": "code_execution"}
CATALOG_TOOL = {
    "name": "list_review_items",
    "description": "Return synthetic review items with page counts.",
    "input_schema": {
        "type": "object", "properties": {}, "additionalProperties": False,
    },
    "allowed_callers": ["code_execution_20260521"],
}


def programmatic(client):
    messages = [{"role": "user", "content": (
        "Use code execution to call list_review_items, filter items with more than "
        "10 pages, and print only their titles. Do not invent the catalog."
    )}]
    container = None
    observed = False
    for _ in range(8):
        response = client.messages.create(
            model=MODEL, max_tokens=4096, messages=messages,
            tools=[EXECUTION_TOOL, CATALOG_TOOL],
            **({"container": container} if container else {}),
        )
        check_server_results(response.model_dump())
        messages.append({"role": "assistant", "content": response.content})
        if response.container is not None:
            container = response.container.id
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            caller = getattr(block, "caller", None)
            if (block.name != "list_review_items" or block.input != {}
                    or getattr(caller, "type", None) != "code_execution_20260120"):
                raise RuntimeError(f"unexpected programmatic tool call: {block}")
            observed = True
            results.append({
                "type": "tool_result", "tool_use_id": block.id,
                "content": json.dumps([
                    {"title": "Library design", "pages": 18},
                    {"title": "Short agenda", "pages": 2},
                    {"title": "Library evidence review", "pages": 14},
                ]),
            })
        if results:
            messages.append({"role": "user", "content": results})
            continue
        if response.stop_reason == "pause_turn":
            continue
        if response.stop_reason != "end_turn" or not observed:
            raise RuntimeError(f"no completed programmatic call: {response.stop_reason}")
        print(response.model_dump_json(indent=2))
        return
    raise RuntimeError("programmatic tool loop exceeded eight turns")


def main(mode="context"):
    require_key()
    with anthropic.Anthropic() as client:
        if mode == "programmatic":
            programmatic(client)
            return
        messages = [{"role": "user", "content": "Explain why an old tool result may be cleared."}]
        response = client.beta.messages.create(
            model=MODEL, max_tokens=1024, messages=messages,
            betas=["context-management-2025-06-27"],
            context_management={"edits": [{"type": "clear_tool_uses_20250919"}]},
        )
        if response.stop_reason != "end_turn":
            raise RuntimeError(f"incomplete response: {response.stop_reason}")
        print(response.model_dump_json(indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Context policy or real programmatic calling.")
    parser.add_argument("--mode", choices=["context", "programmatic"], default="context")
    main(parser.parse_args().mode)
