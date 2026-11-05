from mini_loop import FIXTURES, MiniLoop

if __name__ == "__main__":
    result = MiniLoop().call(
        "DraftFollowUp", {"transcript": (FIXTURES / "chat.txt").read_text()}
    )
    print(result["summary"])
