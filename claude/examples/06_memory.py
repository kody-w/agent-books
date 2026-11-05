from pathlib import Path
import anthropic
from anthropic.tools import BetaLocalFilesystemMemoryTool
from common import MODEL, require_key

if __name__ == "__main__":
    require_key()
    path = Path("example-output/claude-memory")
    path.mkdir(parents=True, exist_ok=True)
    memory = BetaLocalFilesystemMemoryTool(base_path=str(path))
    with anthropic.Anthropic() as client:
        runner = client.beta.messages.tool_runner(
            model=MODEL, max_tokens=1024, max_iterations=8,
            tools=[memory],
            messages=[{"role": "user", "content":
                       "Remember this approved working note: library follow-ups stay drafts."}],
        )
        response = runner.until_done()
        if response.stop_reason != "end_turn":
            raise RuntimeError(f"incomplete memory run: {response.stop_reason}")
        print(response.content)
