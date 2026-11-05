from agent import DraftFollowUp

if __name__ == "__main__":
    result = DraftFollowUp().perform(transcript="")
    assert result["status"] == "error"
    print(result["message"])
