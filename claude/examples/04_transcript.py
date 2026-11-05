import anthropic
from common import MODEL, require_key


def main():
    require_key()
    with anthropic.Anthropic() as client:
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
    main()
