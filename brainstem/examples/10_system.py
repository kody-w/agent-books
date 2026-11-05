import argparse
import json
from pathlib import Path
from mini_loop import FIXTURES, system

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat", type=Path,
                        default=FIXTURES / "chat.txt")
    parser.add_argument("--later", type=Path,
                        default=FIXTURES / "later.txt")
    args = parser.parse_args()
    print(json.dumps(system(args.chat, args.later), indent=2))
