from mini_loop import MiniLoop, SOURCE, load_trusted_file

if __name__ == "__main__":
    loop = MiniLoop()
    del loop.tools["ReviewDraft"]
    loop.register(load_trusted_file(SOURCE))
    print(loop.call("ReviewDraft", {"draft": "Draft for review"})["summary"])
