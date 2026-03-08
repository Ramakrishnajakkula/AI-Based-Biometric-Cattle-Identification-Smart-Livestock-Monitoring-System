"""
Sensor-Based Anomaly Detection for Cattle Health
Author: Aditi
"""

import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Dict, List


# Normal ranges for cattle vital signs
THRESHOLDS = {
    "temperature": {"min": 37.5, "max": 39.5, "unit": "celsius"},
    "heartrate": {"min": 40, "max": 80, "unit": "bpm"},
    "activity_level": {"min": 0.3, "max": 1.0, "unit": "normalized"},
}

ANOMALY_DESCRIPTIONS = {
    "fever": "Body temperature above normal range — possible infection",
    "hypothermia": "Body temperature below normal range",
    "elevated_heartrate": "Heart rate above normal — possible stress or illness",
    "low_heartrate": "Heart rate below normal — possible bradycardia",
    "low_activity": "Significantly reduced movement — possible illness or injury",
    "geofence_breach": "Cattle detected outside farm boundary",
}


def check_sensor_anomaly(cattle_id: str, sensor_data: dict) -> dict:
    """
    Check sensor data for anomalies using threshold rules.
    
    Called by Akash's health_service.py in the backend.
    
    Args:
        cattle_id: Cattle identifier
        sensor_data: {"temperature": 40.1, "heartrate": 95, "activity_level": 0.2}
    
    Returns:
        {
            "is_anomaly": True,
            "anomalies": [...],
            "overall_health_score": 0.35,
            "recommendation": "Veterinary visit recommended"
        }
    """
    anomalies = []
    
    # Temperature check
    temp = sensor_data.get("temperature")
    if temp is not None:
        if temp > THRESHOLDS["temperature"]["max"]:
            anomalies.append({
                "type": "fever",
                "severity": "high" if temp > 40.0 else "medium",
                "value": temp,
                "threshold": THRESHOLDS["temperature"]["max"],
                "description": ANOMALY_DESCRIPTIONS["fever"]
            })
        elif temp < THRESHOLDS["temperature"]["min"]:
            anomalies.append({
                "type": "hypothermia",
                "severity": "high" if temp < 36.5 else "medium",
                "value": temp,
                "threshold": THRESHOLDS["temperature"]["min"],
                "description": ANOMALY_DESCRIPTIONS["hypothermia"]
            })
    
    # Heart rate check
    hr = sensor_data.get("heartrate")
    if hr is not None:
        if hr > THRESHOLDS["heartrate"]["max"]:
            anomalies.append({
                "type": "elevated_heartrate",
                "severity": "high" if hr > 100 else "medium",
                "value": hr,
                "threshold": THRESHOLDS["heartrate"]["max"],
                "description": ANOMALY_DESCRIPTIONS["elevated_heartrate"]
            })
        elif hr < THRESHOLDS["heartrate"]["min"]:
            anomalies.append({
                "type": "low_heartrate",
                "severity": "medium",
                "value": hr,
                "threshold": THRESHOLDS["heartrate"]["min"],
                "description": ANOMALY_DESCRIPTIONS["low_heartrate"]
            })
    
    # Activity check
    activity = sensor_data.get("activity_level")
    if activity is not None:
        if activity < THRESHOLDS["activity_level"]["min"]:
            anomalies.append({
                "type": "low_activity",
                "severity": "medium",
                "value": activity,
                "threshold": THRESHOLDS["activity_level"]["min"],
                "description": ANOMALY_DESCRIPTIONS["low_activity"]
            })
    
    # Calculate overall health score (1.0 = healthy, 0.0 = critical)
    high_count = sum(1 for a in anomalies if a["severity"] == "high")
    med_count = sum(1 for a in anomalies if a["severity"] == "medium")
    health_score = max(0.0, 1.0 - (high_count * 0.3) - (med_count * 0.15))
    
    # Generate recommendation
    if high_count > 0:
        recommendation = "Immediate veterinary attention required"
    elif med_count > 0:
        recommendation = "Monitor closely, consider veterinary check"
    else:
        recommendation = "Cattle appears healthy"
    
    return {
        "cattle_id": cattle_id,
        "is_anomaly": len(anomalies) > 0,
        "anomalies": anomalies,
        "overall_health_score": round(health_score, 2),
        "recommendation": recommendation
    }


if __name__ == "__main__":
    # Test with abnormal values
    result = check_sensor_anomaly("CTL-001", {
        "temperature": 40.1,
        "heartrate": 95,
        "activity_level": 0.2
    })
    print(f"Is anomaly: {result['is_anomaly']}")
    print(f"Health score: {result['overall_health_score']}")
    print(f"Recommendation: {result['recommendation']}")
    for a in result["anomalies"]:
        print(f"  - {a['type']} ({a['severity']}): {a['value']}")
