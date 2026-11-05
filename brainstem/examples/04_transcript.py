import json
from mini_loop import MiniLoop

if __name__ == "__main__":
    loop = MiniLoop()
    loop.call("DraftFollowUp", {"transcript": "Please request a library review."})
    print(json.dumps(loop.transcript, indent=2))
