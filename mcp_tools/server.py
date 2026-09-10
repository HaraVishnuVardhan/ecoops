from fastmcp import FastMCP

from mcp_tools.tools import (
    anomaly_detector,
    historical_matcher,
    emission_calculator,
    facilities_alerter,
)

# Create MCP server
mcp = FastMCP("EcoOps Tools")

# Register tools
mcp.tool()(anomaly_detector)
mcp.tool()(historical_matcher)
mcp.tool()(emission_calculator)
mcp.tool()(facilities_alerter)


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
    )