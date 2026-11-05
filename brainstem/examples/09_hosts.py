import json
from mini_loop import MiniLoop

if __name__ == "__main__":
    request = json.loads('{"name":"ReviewDraft","arguments":{"draft":"Library note"}}')
    result = MiniLoop().call(request["name"], request["arguments"])
    print(json.dumps(result))
