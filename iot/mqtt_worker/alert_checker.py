"""
Alert Checker - Check sensor values against thresholds
Author: Jaswanth
"""

from typing import List, Dict


# Cattle vital sign thresholds
THRESHOLDS = {
    "temperature": {"min": 37.5, "max": 39.5},
    "heartrate": {"min": 40, "max": 80},
}


def check_thresholds(cattle_id: str, sensor_type: str, payload: dict) -> List[Dict]:
    """
    Check if sensor values exceed thresholds.
    
    Returns list of alert dicts if anomalies found, empty list otherwise.
    """
    alerts = []
    
    if sensor_type == "temperature":
        value = payload.get("value")
        if value and value > THRESHOLDS["temperature"]["max"]:
            alerts.append({
                "cattle_id": cattle_id,
                "type": "fever",
                "severity": "high",
                "message": f"Temperature {value}°C exceeds threshold {THRESHOLDS['temperature']['max']}°C",
                "value": value
            })
        elif value and value < THRESHOLDS["temperature"]["min"]:
            alerts.append({
                "cattle_id": cattle_id,
                "type": "hypothermia",
                "severity": "medium",
                "message": f"Temperature {value}°C below threshold {THRESHOLDS['temperature']['min']}°C",
                "value": value
            })
    
    elif sensor_type == "heartrate":
        bpm = payload.get("bpm")
        if bpm and bpm > THRESHOLDS["heartrate"]["max"]:
            alerts.append({
                "cattle_id": cattle_id,
                "type": "elevated_heartrate",
                "severity": "medium",
                "message": f"Heart rate {bpm} bpm exceeds threshold {THRESHOLDS['heartrate']['max']} bpm",
                "value": bpm
            })
    
    return alerts
