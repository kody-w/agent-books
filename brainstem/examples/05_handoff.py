from mini_loop import MiniLoop

if __name__ == "__main__":
    loop = MiniLoop()
    first = loop.call("DraftFollowUp", {"transcript": "Please request a library review."})
    second = loop.call("ReviewDraft", {"draft": first["data_slush"]["draft"]})
    print(second["summary"])
