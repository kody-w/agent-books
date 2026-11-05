import anthropic
from common import MODEL, require_key


def main():
    require_key()
    with anthropic.Anthropic() as client:
        messages = [{"role": "user", "content": "Use code execution to compute sum([2, 3, 5])."}]
        for _ in range(8):
            response = client.messages.create(
                model=MODEL, max_tokens=2048, messages=messages,
                tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
            )
            if response.stop_reason == "end_turn":
                print(response.model_dump_json(indent=2))
                return
            if response.stop_reason != "pause_turn":
                raise RuntimeError(f"incomplete response: {response.stop_reason}")
            messages.append({"role": "assistant", "content": response.content})
    raise RuntimeError("server tool exceeded eight turns")


if __name__ == "__main__":
    main()
