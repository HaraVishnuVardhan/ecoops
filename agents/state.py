from typing import TypedDict


class EcoOpsState(TypedDict, total=False):
    # Input
    query: str
    metric_data: dict

    # Agent outputs
    anomaly_result: dict
    rag_result: dict
    historical_result: dict

    # Confidence
    data_confidence: float
    rag_confidence: float
    historical_confidence: float
    overall_confidence: float

    # Final output
    recommendations: list
    decision: str
    should_escalate: bool
    escalation_reason: str

    # Audit trail
    trace_log: list