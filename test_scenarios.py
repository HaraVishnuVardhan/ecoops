from agents.graph import ecoops_graph


def run_scenario(name: str, data: dict):
    print("\n" + "=" * 60)
    print(f"SCENARIO: {name}")
    print("=" * 60)

    state = {
        "query": f"Analyze abnormal {data['metric']} consumption.",
        "metric_data": data,
        "trace_log": [],
    }

    result = ecoops_graph.invoke(state)

    anomaly = result["anomaly_result"]

    print(f"Metric:       {anomaly['metric']}")
    print(f"Location:     {anomaly['location']}")
    print(f"Change:       {anomaly['change_percent']}%")
    print(f"Severity:     {anomaly['severity']}")
    print(f"Confidence:   {result['overall_confidence']}")
    print(f"Decision:     {result['decision']}")

    print("\nTrace events:")

    for event in result.get("trace_log", []):
        print(f"  - {event['event']}")

    return result


def assert_safety_invariants(
    result: dict,
    expected_decision: str
):
    decision = result["decision"]
    severity = result["anomaly_result"]["severity"]

    assert decision == expected_decision, (
        f"Expected {expected_decision}, "
        f"but got {decision}"
    )

    if severity == "EXTREME":
        assert decision == "ESCALATE", (
            "EXTREME anomaly was not escalated."
        )

    if decision == "ESCALATE":
        assert result["should_escalate"] is True

        escalation_events = [
            event
            for event in result.get("trace_log", [])
            if event["event"] == "mcp_escalation_alert"
        ]

        assert escalation_events, (
            "ESCALATE decision did not create "
            "an MCP escalation trace."
        )

    if decision == "MONITOR":
        assert result["should_escalate"] is False

        monitor_events = [
            event
            for event in result.get("trace_log", [])
            if event["event"]
            == "llm_monitoring_guidance_generated"
        ]

        assert monitor_events, (
            "MONITOR decision did not generate "
            "LLM monitoring guidance."
        )


def test_academic_block():
    result = run_scenario(
        "Academic Block A",
        {
            "metric": "energy",
            "location": "Academic Block A",
            "current_value": 12500,
            "baseline_value": 10870,
            "timestamp": "2026-06-15T14:00:00",
            "event_today": False,
            "sensor_recently_replaced": False,
        },
    )

    assert_safety_invariants(
        result,
        "MONITOR"
    )


def test_hostel_c():
    result = run_scenario(
        "Hostel C",
        {
            "metric": "water",
            "location": "Hostel C",
            "current_value": 15000,
            "baseline_value": 11100,
            "timestamp": "2026-06-15T18:00:00",
            "event_today": True,
            "sensor_recently_replaced": False,
        },
    )

    assert_safety_invariants(
        result,
        "MONITOR"
    )

    policy = result["rag_result"]

    assert policy["policy_source"] == "water_policy.txt"

    for item in policy["retrieved_documents"]:
        assert item["source"] == "water_policy.txt"


def test_chemistry_lab():
    result = run_scenario(
        "Chemistry Lab",
        {
            "metric": "energy",
            "location": "Chemistry Lab",
            "current_value": 28000,
            "baseline_value": 5800,
            "timestamp": "2026-06-15T02:47:00",
            "event_today": False,
            "sensor_recently_replaced": False,
        },
    )

    assert_safety_invariants(
        result,
        "ESCALATE"
    )

    assert result["overall_confidence"] <= 0.45


if __name__ == "__main__":

    print("\n")
    print("ECOOPS 2.0 EVALUATION SUITE")
    print("Confidence-Aware Safety Evaluation")
    print("\n")

    academic = run_scenario(
        "Academic Block A",
        {
            "metric": "energy",
            "location": "Academic Block A",
            "current_value": 12500,
            "baseline_value": 10870,
            "timestamp": "2026-06-15T14:00:00",
            "event_today": False,
            "sensor_recently_replaced": False,
        },
    )

    assert_safety_invariants(
        academic,
        "MONITOR"
    )

    hostel = run_scenario(
        "Hostel C",
        {
            "metric": "water",
            "location": "Hostel C",
            "current_value": 15000,
            "baseline_value": 11100,
            "timestamp": "2026-06-15T18:00:00",
            "event_today": True,
            "sensor_recently_replaced": False,
        },
    )

    assert_safety_invariants(
        hostel,
        "MONITOR"
    )

    chemistry = run_scenario(
        "Chemistry Lab",
        {
            "metric": "energy",
            "location": "Chemistry Lab",
            "current_value": 28000,
            "baseline_value": 5800,
            "timestamp": "2026-06-15T02:47:00",
            "event_today": False,
            "sensor_recently_replaced": False,
        },
    )

    assert_safety_invariants(
        chemistry,
        "ESCALATE"
    )

    print("\n" + "=" * 60)
    print("ALL SAFETY EVALUATIONS PASSED")
    print("=" * 60)