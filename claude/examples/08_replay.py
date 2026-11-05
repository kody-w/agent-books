import asyncio
from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, query
from common import MODEL, require_key


async def checked_query(prompt, options):
    final = None
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            final = message
    if final is None or final.is_error or final.subtype != "success":
        raise RuntimeError(f"Agent SDK failed: {final}")
    return final


async def main():
    require_key()
    first = await checked_query(
        "Draft a follow-up asking for comments by Friday. Do not send.",
        ClaudeAgentOptions(model=MODEL, tools=[], max_turns=3),
    )
    fork = await checked_query(
        "Later evidence: the deadline moved to Monday. Revise the draft. Do not send.",
        ClaudeAgentOptions(model=MODEL, tools=[], max_turns=3,
                           resume=first.session_id, fork_session=True),
    )
    if first.session_id == fork.session_id:
        raise RuntimeError("fork did not create a distinct session")
    print(first.session_id, first.result)
    print(fork.session_id, fork.result)


if __name__ == "__main__":
    asyncio.run(main())
