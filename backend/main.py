from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.graph import ecoops_graph


app = FastAPI(
    title="EcoOps 2.0 API",
    description="Confidence-Aware Campus Sustainability Agent",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request Model
# ---------------------------------------------------------

class AnomalyRequest(BaseModel):
    metric: str
    location: str
    current_value: float
    baseline_value: float
    timestamp: str
    event_today: bool = False
    sensor_recently_replaced: bool = False


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "EcoOps 2.0 API is running"
    }


# ---------------------------------------------------------
# Analyze Endpoint
# ---------------------------------------------------------

@app.post("/analyze")
def analyze(request: AnomalyRequest):

    initial_state = {
        "query": f"Analyze abnormal {request.metric} consumption.",
        "metric_data": request.model_dump(),
        "trace_log": [],
    }

    result = ecoops_graph.invoke(initial_state)

    return {
        "location": result["anomaly_result"]["location"],
        "metric": result["anomaly_result"]["metric"],
        "current_value": result["anomaly_result"]["current_value"],
        "baseline_value": result["anomaly_result"]["baseline_value"],
        "change_percent": result["anomaly_result"]["change_percent"],
        "severity": result["anomaly_result"]["severity"],
        "confidence": result["overall_confidence"],
        "decision": result["decision"],
        "recommendations": result.get(
            "recommendations",
            []
        ),
        "policy": result.get(
            "rag_result",
            {}
        ),
        "historical": result.get(
            "historical_result",
            {}
        ),
        "audit_trail": result.get(
            "trace_log",
            []
        ),
    }