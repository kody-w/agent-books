import argparse
import anthropic
from common import MODEL, check_server_results, require_key

TOOLS = {
    "code": {"type": "code_execution_20260521", "name": "code_execution"},
    "search": {
        "type": "web_search_20260318", "name": "web_search",
        "allowed_callers": ["direct"], "max_uses": 2,
        "allowed_domains": ["platform.claude.com"],
    },
    "fetch": {
        "type": "web_fetch_20260318", "name": "web_fetch",
        "allowed_callers": ["direct"], "max_uses": 2,
        "max_content_tokens": 12000, "allowed_domains": ["platform.claude.com"],
        "citations": {"enabled": True},
    },
}
PROMPTS = {
    "code": "Use code execution to compute sum([2, 3, 5]).",
    "search": "Search the official Claude documentation for tool result IDs. Cite your sources.",
    "fetch": (
        "Fetch https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview "
        "and explain the client tool lifecycle with citations."
    ),
}


def main(tool="code"):
    require_key()
    with anthropic.Anthropic() as client:
        messages = [{"role": "user", "content": PROMPTS[tool]}]
        container = None
        server_calls = []
        for _ in range(8):
            response = client.messages.create(
                model=MODEL, max_tokens=2048, messages=messages,
                tools=[TOOLS[tool]],
                **({"container": container} if container else {}),
            )
            check_server_results(response.model_dump())
            server_calls.extend(
                block.name for block in response.content if block.type == "server_tool_use"
            )
            if response.container is not None:
                container = response.container.id
            if response.stop_reason == "end_turn":
                expected = (
                    {"code_execution", "bash_code_execution"}
                    if tool == "code" else {TOOLS[tool]["name"]}
                )
                if not expected.intersection(server_calls):
                    raise RuntimeError("model completed without invoking the requested server tool")
                print(response.model_dump_json(indent=2))
                return
            if response.stop_reason != "pause_turn":
                raise RuntimeError(f"incomplete response: {response.stop_reason}")
            messages.append({"role": "assistant", "content": response.content})
    raise RuntimeError("server tool exceeded eight turns")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real server-tool requests; API key required.")
    parser.add_argument("--tool", choices=TOOLS, default="code")
    main(parser.parse_args().tool)
