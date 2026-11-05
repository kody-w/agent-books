import copy
from common import DRAFT, run

if __name__ == "__main__":
    deferred = copy.deepcopy(DRAFT)
    deferred["defer_loading"] = True
    search = {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"}
    result = run(
        "Find the drafting tool and draft a follow-up from: Please review the library plan.",
        tools=[search, deferred],
    )
    if not any(e["name"] == "draft_follow_up" for e in result["events"]):
        raise RuntimeError("tool search did not lead to a draft call")
    print(result["text"])
