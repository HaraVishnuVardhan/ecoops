from agents.graph import ecoops_graph


sample_data = {
    "metric": "energy",
    "location": "Academic Block A",
    "current_value": 12500,
    "baseline_value": 10870,
    "timestamp": "2026-09-10T14:30:00",
    "event_today": False,
    "sensor_recently_replaced": False,
}


initial_state = {
    "query": "Analyze abnormal energy consumption.",
    "metric_data": sample_data,
    "trace_log": [],
}


result = ecoops_graph.invoke(initial_state)


print("\n========== ECOOPS 2.0 ==========\n")

print("Location:", result["anomaly_result"]["location"])

print("Metric:", result["anomaly_result"]["metric"])

print(
    "Change:",
    f'{result["anomaly_result"]["change_percent"]}%'
)

print("Severity:", result["anomaly_result"]["severity"])

print(
    "Overall Confidence:",
    result["overall_confidence"]
)

print("Decision:", result["decision"])

print("\nRecommendation:")

for recommendation in result.get(
    "recommendations",
    []
):
    print("-", recommendation)

print(
    "\nRAG Source:",
    result["rag_result"]["source"]
)

print(
    "Possible Cause:",
    result["historical_result"]["possible_cause"]
)
print("Historical Tool:", result["historical_result"].get("tool"))
print(
    "Historical Similarity:",
    result["historical_result"].get("historical_similarity")
)

print("\nAudit Trail:")

for event in result["trace_log"]:
    print(
        "-",
        event.get("event")
    )

print("\n===============================\n")