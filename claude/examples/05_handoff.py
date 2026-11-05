from common import REVIEW, draft_once, run

if __name__ == "__main__":
    first = draft_once("Please request a library review.")["output"]
    draft = first["data_slush"]["draft"]
    second = run("Call review_draft with this exact draft:\n" + draft,
                 tools=[REVIEW], required="review_draft")
    reviews = [e for e in second["events"] if e["name"] == "review_draft"]
    if not reviews or reviews[0]["arguments"].get("draft") != draft:
        raise RuntimeError("review handoff changed the draft")
    if reviews[0]["output"]["status"] != "success":
        raise RuntimeError("review tool failed")
    print(reviews[0]["output"]["summary"])
