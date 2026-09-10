def anomaly_detector(
    current_value: float,
    baseline_value: float
) -> dict:
    """Detect abnormal resource consumption."""

    if baseline_value == 0:
        baseline_value = 1

    change_percent = (
        (current_value - baseline_value)
        / baseline_value
    ) * 100

    if abs(change_percent) >= 200:
        severity = "EXTREME"
    elif abs(change_percent) >= 50:
        severity = "HIGH"
    elif abs(change_percent) >= 20:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "change_percent": round(change_percent, 2),
        "severity": severity
    }


def historical_matcher(
    metric: str,
    location: str
) -> dict:
    """Compare anomaly with historical patterns."""

    return {
        "metric": metric,
        "location": location,
        "historical_match": True,
        "similarity": 0.85
    }


def emission_calculator(
    energy_kwh: float,
    emission_factor: float = 0.7
) -> dict:
    """Calculate estimated CO2 emissions."""

    emissions = energy_kwh * emission_factor

    return {
        "energy_kwh": energy_kwh,
        "emissions_kg_co2e": round(emissions, 2)
    }


def facilities_alerter(
    location: str,
    severity: str,
    reason: str
) -> dict:
    """Create a human-review alert."""

    return {
        "alert_created": True,
        "location": location,
        "severity": severity,
        "reason": reason,
        "status": "HUMAN_REVIEW_REQUIRED"
    }