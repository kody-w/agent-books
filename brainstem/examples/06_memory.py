from pathlib import Path
from tempfile import TemporaryDirectory
from agent import MemoryAgent

if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        memory = MemoryAgent(Path(directory) / "memory.json")
        print(memory.perform(content="Use a draft; never send automatically.")["summary"])
        print(memory.system_context())
