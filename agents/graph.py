from langgraph.graph import StateGraph, END

from .state import EcoOpsState

from .nodes import (
    anomaly_detection_node,
    rag_node,
    historical_analysis_node,
    confidence_scoring_node,
    recommendation_node,
)

from .router import (
    safety_router,
    monitor_node,
    escalation_node,
)


def build_graph():

    graph = StateGraph(EcoOpsState)

    # Register nodes
    graph.add_node(
        "anomaly_detection",
        anomaly_detection_node
    )

    graph.add_node(
        "rag",
        rag_node
    )

    graph.add_node(
        "historical",
        historical_analysis_node
    )

    graph.add_node(
        "confidence",
        confidence_scoring_node
    )

    graph.add_node(
        "recommendation",
        recommendation_node
    )

    graph.add_node(
        "monitor",
        monitor_node
    )

    graph.add_node(
        "escalate",
        escalation_node
    )

    # Start
    graph.set_entry_point("anomaly_detection")

    # Normal processing pipeline
    graph.add_edge(
        "anomaly_detection",
        "rag"
    )

    graph.add_edge(
        "rag",
        "historical"
    )

    graph.add_edge(
        "historical",
        "confidence"
    )

    # Safety routing
    graph.add_conditional_edges(
        "confidence",
        safety_router,
        {
            "recommend": "recommendation",
            "monitor": "monitor",
            "escalate": "escalate"
        }
    )

    # End states
    graph.add_edge(
        "recommendation",
        END
    )

    graph.add_edge(
        "monitor",
        END
    )

    graph.add_edge(
        "escalate",
        END
    )

    return graph.compile()


ecoops_graph = build_graph()