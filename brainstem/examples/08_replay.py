import json
from pathlib import Path
from tempfile import TemporaryDirectory
from mini_loop import MiniLoop

if __name__ == "__main__":
    loop = MiniLoop()
    loop.call("DraftFollowUp", {"transcript": "Comments due Friday."})
    with TemporaryDirectory() as directory:
        path = Path(directory) / "archive.json"
        loop.save(path)
        archive = json.loads(path.read_text())
        print(MiniLoop().replay(archive, 0, "Deadline changed to Monday.")["summary"])
