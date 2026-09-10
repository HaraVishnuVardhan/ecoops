import ollama


MODEL_NAME = "llama3.2:3b"


def generate_recommendation(
    anomaly: dict,
    policy: dict,
    historical: dict
) -> str:
    """
    Generate an operational recommendation using
    the local Llama model.

    The LLM provides the recommendation text.
    The safety router remains responsible for
    the final RECOMMEND / MONITOR / ESCALATE decision.
    """

    metric = anomaly.get("metric", "resource")
    location = anomaly.get("location", "Unknown")
    current_value = anomaly.get("current_value", 0)
    baseline_value = anomaly.get("baseline_value", 0)
    change_percent = anomaly.get("change_percent", 0)
    severity = anomaly.get("severity", "UNKNOWN")

    possible_cause = historical.get(
        "possible_cause",
        "Unknown"
    )

    policy_guidance = policy.get(
        "guidance",
        []
    )

    policy_text = "\n".join(
        policy_guidance
    )

    prompt = f"""
You are the recommendation agent for EcoOps 2.0,
a confidence-aware campus sustainability system.

Analyze this operational anomaly.

Metric: {metric}
Location: {location}
Current value: {current_value}
Baseline value: {baseline_value}
Change: {change_percent}%
Severity: {severity}

Possible cause:
{possible_cause}

Retrieved campus policy guidance:
{policy_text}

Generate a concise recommendation for the campus
facilities team.

Rules:
1. Base the recommendation only on the supplied evidence
   and retrieved policy.
2. Do not invent sensor readings, events, causes, or facts.
3. Do not claim that an operational change is definitely safe.
4. Human approval is required before operational changes.
5. If the anomaly is extreme or unexplained, emphasize
   investigation and human review.
6. Keep the answer under 80 words.

Return only the recommendation.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()