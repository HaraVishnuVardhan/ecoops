from datetime import datetime
from typing import Any

from mcp_tools.client import call_tool
from rag.retriever import retrieve_policy
from rag.llm import generate_recommendation

from .state import EcoOpsState


def add_trace(
    state: EcoOpsState,
    event: str,
    details: Any
) -> None:
    """
    Add a structured event to the EcoOps audit trail.
    """

    trace = state.setdefault(
        "trace_log",
        []
    )

    trace.append({
        "event": event,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })


def anomaly_detection_node(
    state: EcoOpsState
) -> dict[str, Any]:

    data = state.get(
        "metric_data",
        {}
    )

    current = float(
        data.get(
            "current_value",
            0
        )
    )

    baseline = float(
        data.get(
            "baseline_value",
            1
        )
    )

    mcp_result = call_tool(
        "anomaly_detector",
        {
            "current_value": current,
            "baseline_value": baseline,
        },
    )

    # MCP failure must fail safely.
    if mcp_result.get("success") is False:

        result = {
            "metric": data.get(
                "metric",
                "unknown"
            ),
            "location": data.get(
                "location",
                "Unknown"
            ),
            "current_value": current,
            "baseline_value": baseline,
            "change_percent": 0,
            "severity": "EXTREME",
            "confidence": 0.0,
            "timestamp": data.get(
                "timestamp",
                datetime.now().isoformat()
            ),
            "tool": "MCP: anomaly_detector",
            "tool_failure": True,
            "error": mcp_result.get(
                "error",
                "Unknown MCP failure"
            ),
        }

        add_trace(
            state,
            "mcp_tool_failure",
            result
        )

        return {
            "anomaly_result": result,
            "data_confidence": 0.0,
            "trace_log": state["trace_log"],
        }

    change_percent = mcp_result[
        "change_percent"
    ]

    severity = mcp_result[
        "severity"
    ]

    if severity == "EXTREME":
        confidence = 0.96
    elif severity == "HIGH":
        confidence = 0.90
    elif severity == "MEDIUM":
        confidence = 0.78
    else:
        confidence = 0.92

    result = {
        "metric": data.get(
            "metric",
            "unknown"
        ),
        "location": data.get(
            "location",
            "Unknown"
        ),
        "current_value": current,
        "baseline_value": baseline,
        "change_percent": change_percent,
        "severity": severity,
        "confidence": confidence,
        "timestamp": data.get(
            "timestamp",
            datetime.now().isoformat()
        ),
        "tool": "MCP: anomaly_detector",
    }

    add_trace(
        state,
        "anomaly_detected",
        result
    )

    return {
        "anomaly_result": result,
        "data_confidence": confidence,
        "trace_log": state["trace_log"],
    }


def rag_node(
    state: EcoOpsState
) -> dict[str, Any]:

    anomaly = state.get(
        "anomaly_result",
        {}
    )

    metric = anomaly.get(
        "metric",
        "resource"
    )

    severity = anomaly.get(
        "severity",
        "UNKNOWN"
    )

    location = anomaly.get(
        "location",
        "Unknown"
    )

    change_percent = anomaly.get(
        "change_percent",
        0
    )

    metric_data = state.get(
        "metric_data",
        {}
    )

    event_today = metric_data.get(
        "event_today",
        False
    )

    sensor_recently_replaced = metric_data.get(
        "sensor_recently_replaced",
        False
    )

    query = (
        f"{metric} consumption anomaly at "
        f"{location}. "
        f"Change is {change_percent} percent. "
        f"Severity is {severity}. "
        f"Campus event today: {event_today}. "
        f"Sensor recently replaced: "
        f"{sensor_recently_replaced}. "
        f"Determine investigation, validation, "
        f"human review, escalation, and safe "
        f"operational guidance."
    )

    try:

        retrieval = retrieve_policy(
            metric=metric,
            query=query,
            n_results=2
        )

    except Exception as error:

        result = {
            "source": "RAG unavailable",
            "guidance": [],
            "retrieved_documents": [],
            "query": query,
            "grounded": False,
            "retrieval_confidence": 0.0,
            "tool": "ChromaDB: policy_retriever",
            "error": str(error),
        }

        add_trace(
            state,
            "rag_failure",
            result
        )

        return {
            "rag_result": result,
            "rag_confidence": 0.0,
            "trace_log": state["trace_log"],
        }

    retrieved_results = retrieval.get(
        "results",
        []
    )

    sources = []

    for item in retrieved_results:

        source = item.get(
            "source",
            "unknown"
        )

        if source not in sources:
            sources.append(source)

    guidance = []

    for item in retrieved_results:

        document = item.get(
            "document",
            ""
        )

        if document:
            guidance.append(
                document
            )

    result = {
        "source": ", ".join(
            sources
        ) if sources else "No policy retrieved",

        "guidance": guidance,

        "retrieved_documents":
            retrieved_results,

        "query": query,

        "grounded":
            retrieval.get(
                "grounded",
                False
            ),

        "retrieval_confidence":
            retrieval.get(
                "retrieval_confidence",
                0.0
            ),

        "tool":
            "ChromaDB: policy_retriever"
    }

    add_trace(
        state,
        "policy_retrieved",
        result
    )

    return {
        "rag_result": result,
        "rag_confidence":
            result[
                "retrieval_confidence"
            ],
        "trace_log": state["trace_log"]
    }


def historical_analysis_node(
    state: EcoOpsState
) -> dict[str, Any]:

    data = state.get(
        "metric_data",
        {}
    )

    anomaly = state.get(
        "anomaly_result",
        {}
    )

    metric = data.get(
        "metric",
        "unknown"
    )

    location = data.get(
        "location",
        "Unknown"
    )

    mcp_result = call_tool(
        "historical_matcher",
        {
            "metric": metric,
            "location": location,
        },
    )

    if mcp_result.get("success") is False:

        result = {
            "possible_cause":
                "Historical analysis unavailable. "
                "Human validation is required.",

            "event_today":
                data.get(
                    "event_today",
                    False
                ),

            "sensor_recently_replaced":
                data.get(
                    "sensor_recently_replaced",
                    False
                ),

            "historical_similarity":
                0.0,

            "confidence":
                0.0,

            "tool":
                "MCP: historical_matcher",

            "tool_failure":
                True,
        }

        add_trace(
            state,
            "historical_tool_failure",
            result
        )

        return {
            "historical_result": result,
            "historical_confidence": 0.0,
            "trace_log": state["trace_log"],
        }

    event_today = data.get(
        "event_today",
        False
    )

    sensor_recently_replaced = data.get(
        "sensor_recently_replaced",
        False
    )

    similarity = mcp_result.get(
        "similarity",
        0.0
    )

    if event_today:

        possible_cause = (
            "A recent campus event may "
            "explain the increase."
        )

        confidence = 0.62

    elif sensor_recently_replaced:

        possible_cause = (
            "Recent sensor replacement may "
            "affect the reading."
        )

        confidence = 0.55

    elif anomaly.get(
        "severity"
    ) == "EXTREME":

        possible_cause = (
            "No normal contextual explanation "
            "was found."
        )

        confidence = 0.90

    else:

        possible_cause = (
            "The pattern is reasonably "
            "consistent with normal "
            "operational conditions."
        )

        confidence = similarity

    result = {
        "possible_cause":
            possible_cause,

        "event_today":
            event_today,

        "sensor_recently_replaced":
            sensor_recently_replaced,

        "historical_similarity":
            similarity,

        "confidence":
            confidence,

        "tool":
            "MCP: historical_matcher",
    }

    add_trace(
        state,
        "historical_analysis",
        result
    )

    return {
        "historical_result": result,
        "historical_confidence":
            confidence,
        "trace_log":
            state["trace_log"],
    }


def confidence_scoring_node(
    state: EcoOpsState
) -> dict[str, Any]:

    data_confidence = state.get(
        "data_confidence",
        0.0
    )

    rag_confidence = state.get(
        "rag_confidence",
        0.0
    )

    historical_confidence = state.get(
        "historical_confidence",
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

    overall = (
        data_confidence * 0.40
        + rag_confidence * 0.25
        + historical_confidence * 0.35
    )

    if severity == "EXTREME":

        overall = min(
            overall,
            0.45
        )

    overall = round(
        overall,
        2
    )

    result = {
        "data_confidence":
            data_confidence,

        "rag_confidence":
            rag_confidence,

        "historical_confidence":
            historical_confidence,

        "overall_confidence":
            overall
    }

    add_trace(
        state,
        "confidence_scored",
        result
    )

    return {
        "overall_confidence":
            overall,

        "trace_log":
            state["trace_log"]
    }


def recommendation_node(
    state: EcoOpsState
) -> dict[str, Any]:

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

        ai_recommendation = (
            generate_recommendation(
                anomaly=anomaly,
                policy=rag,
                historical=historical
            )
        )

    except Exception as error:

        ai_recommendation = (
            "Recommendation generation is "
            "currently unavailable. "
            "Continue with human review and "
            "do not make automatic operational "
            "changes."
        )

        add_trace(
            state,
            "llm_failure",
            {
                "error": str(error),
                "safe_fallback": True
            }
        )

    recommendation = {
        "action":
            ai_recommendation,

        "status":
            "RECOMMEND",

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

        "possible_cause":
            historical.get(
                "possible_cause",
                "Unknown"
            ),

        "safety_note":
            "Human approval is required "
            "before operational changes.",

        "generated_by":
            "Llama 3.2 3B via Ollama"
    }

    add_trace(
        state,
        "llm_recommendation_generated",
        recommendation
    )

    return {
        "decision":
            "RECOMMEND",

        "should_escalate":
            False,

        "recommendations":
            [recommendation],

        "trace_log":
            state["trace_log"]
    }