from mcp_tools.client import call_tool


result = call_tool(
    "anomaly_detector",
    {
        "current_value": 28000,
        "baseline_value": 5800
    }
)

print("\n========== MCP TEST ==========")
print(result)
print("==============================")
