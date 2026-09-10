from datetime import datetime

from mcp_tools.client import call_tool
from rag.llm import generate_recommendation

from .state import EcoOpsState


def add_router_trace(
    state: EcoOpsState,
    event: str,
    details: dict
):
    trace = state.setdefault(
        "trace_log",
        []
    )

    trace.append({
        "event": event,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })


def safety_router(
    state: EcoOpsState
) -> str:

    confidence = state.get(
        "overall_confidence",
        0.0
    )

    anomaly = state.get(
        "anomaly_result",
        {}
    )

    severity = anomaly.get(
        "severity",
        "LOW"
    )

    if anomaly.get(
        "tool_failure",
        False
    ):

        reason = (
            "Required anomaly detection tool "
            "failed. The system cannot safely "
            "validate the operational condition."
        )

        state["escalation_reason"] = reason

        add_router_trace(
            state,
            "safety_decision",
            {
                "decision": "ESCALATE",
                "confidence": confidence,
                "reason": reason
            }
        )

        return "escalate"

    if severity == "EXTREME":

        reason = (
            "Extreme anomaly detected. "
            "Automatic optimization is blocked. "
            "Human investigation is required."
        )

        state["escalation_reason"] = reason

        add_router_trace(
            state,
            "safety_decision",
            {
                "decision": "ESCALATE",
                "confidence": confidence,
                "severity": severity,
                "reason": reason
            }
        )

        return "escalate"

    if confidence >= 0.80:

        add_router_trace(
            state,
            "safety_decision",
            {
                "decision": "RECOMMEND",
                "confidence": confidence,
                "threshold": 0.80
            }
        )

        return "recommend"

    if confidence >= 0.50:

        add_router_trace(
            state,
            "safety_decision",
            {
                "decision": "MONITOR",
                "confidence": confidence,
                "threshold": 0.50
            }
        )

        return "monitor"

    reason = (
        "Confidence is below the safety "
        "threshold. Human investigation "
        "is required."
    )

    state["escalation_reason"] = reason

    add_router_trace(
        state,
        "safety_decision",
        {
            "decision": "ESCALATE",
            "confidence": confidence,
            "reason": reason
        }
    )

    return "escalate"


def monitor_node(
    state: EcoOpsState
) -> dict:

    anomaly = state.get(
        "anomaly_result",
        {}
    )

    rag = state.get(
        "rag_result",
        {}
    )

    historical = state.get(
        "historical_result",
        {}
    )

    try:

        ai_guidance = (
            generate_recommendation(
                anomaly=anomaly,
                policy=rag,
                historical=historical
            )
        )

    except Exception:

        ai_guidance = (
            "Continue monitoring the anomaly "
            "and validate the sensor and "
            "operational context before making "
            "any changes."
        )

        add_router_trace(
            state,
            "llm_failure",
            {
                "safe_fallback": True
            }
        )

    recommendation = {
        "action":
            ai_guidance,

        "status":
            "MONITOR",

        "policy_source":
            rag.get(
                "source",
                "Unknown"
            ),

        "policy_grounded":
            rag.get(
                "grounded",
                False
            ),

        "generated_by":
            "Llama 3.2 3B via Ollama",

        "safety_note":
            "No automatic operational change "
            "will be applied while confidence "
            "remains below the recommendation "
            "threshold."
    }

    add_router_trace(
        state,
        "llm_monitoring_guidance_generated",
        recommendation
    )

    return {
        "decision":
            "MONITOR",

        "should_escalate":
            False,

        "recommendations":
            [recommendation],

        "trace_log":
            state["trace_log"]
    }


def escalation_node(
    state: EcoOpsState
) -> dict:

    anomaly = state.get(
        "anomaly_result",
        {}
    )

    location = anomaly.get(
        "location",
        "Unknown"
    )

    severity = anomaly.get(
        "severity",
        "UNKNOWN"
    )

    reason = state.get(
        "escalation_reason",
        "Human investigation is required."
    )

    alert = call_tool(
        "facilities_alerter",
        {
            "location":
                location,

            "severity":
                severity,

            "reason":
                reason,
        },
    )

    add_router_trace(
        state,
        "mcp_escalation_alert",
        {
            "decision":
                "ESCALATE",

            "reason":
                reason,

            "tool":
                "MCP: facilities_alerter",

            "alert":
                alert
        }
    )

    return {
        "decision":
            "ESCALATE",

        "should_escalate":
            True,

        "escalation_reason":
            reason,

        "recommendations": [{
            "action":
                "Escalate to the campus "
                "facilities team.",

            "status":
                "ESCALATE",

            "reason":
                reason,

            "alert_status":
                alert.get(
                    "status",
                    "HUMAN_REVIEW_REQUIRED"
                ),
        }],

        "trace_log":
            state["trace_log"],
    }