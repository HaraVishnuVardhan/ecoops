import asyncio
from fastmcp import Client

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"


async def call_mcp_tool(
    tool_name: str,
    arguments: dict
):
    """Call an EcoOps tool through MCP."""

    client = Client(MCP_SERVER_URL)

    async with client:
        result = await client.call_tool(
            tool_name,
            arguments,
        )

        return result.data


def call_tool(
    tool_name: str,
    arguments: dict
):
    """
    Synchronous MCP wrapper.

    If an MCP service fails, return a safe
    failure response instead of crashing the
    entire agent pipeline.
    """

    try:
        return asyncio.run(
            call_mcp_tool(
                tool_name,
                arguments
            )
        )

    except Exception as error:

        return {
            "success": False,
            "tool": tool_name,
            "error": str(error),
            "status": "TOOL_FAILURE",
            "requires_human_review": True,
        }