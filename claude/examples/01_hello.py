from common import FIXTURES, draft_once

if __name__ == "__main__":
    print(draft_once((FIXTURES / "chat.txt").read_text())["output"]["summary"])
