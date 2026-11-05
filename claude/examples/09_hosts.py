import asyncio
import json
from claude_agent_sdk import (
    ClaudeAgentOptions, ResultMessage, create_sdk_mcp_server, query, tool,
)
from common import MODEL, execute, require_key

EXECUTIONS = []


@tool("review_draft", "Prepare a draft for human review; never send.", {"draft": str})
async def review_draft(args):
    try:
        output = execute("review_draft", args)
    except ValueError as error:
        return {"content": [{"type": "text", "text": str(error)}], "isError": True}
    EXECUTIONS.append(output)
    return {"content": [{"type": "text", "text": json.dumps(output)}],
            "structuredContent": output}


async def main():
    require_key()
    EXECUTIONS.clear()
    server = create_sdk_mcp_server(name="book", tools=[review_draft])
    options = ClaudeAgentOptions(
        model=MODEL, tools=[], mcp_servers={"book": server},
        allowed_tools=["mcp__book__review_draft"], max_turns=5,
    )
    final = None
    async for message in query(
        prompt="Use mcp__book__review_draft on the draft: Library review request.",
        options=options,
    ):
        if isinstance(message, ResultMessage):
            final = message
    if final is None or final.is_error or final.subtype != "success":
        raise RuntimeError(f"Agent SDK failed: {final}")
    if not EXECUTIONS:
        raise RuntimeError("Agent SDK completed without invoking the review tool")
    print(final.result)


if __name__ == "__main__":
    asyncio.run(main())
