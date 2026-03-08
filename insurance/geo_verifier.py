"""
Geo Verifier — Checks cattle GPS against farm geofence
Author: Aditi
"""

import math


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance in meters between two GPS coordinates."""
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def verify_location(cattle_gps: dict, farm_center: dict, radius_meters: float = 5000) -> dict:
    """
    Check if cattle is within farm geofence.
    
    Args:
        cattle_gps: {"lat": float, "lng": float}
        farm_center: {"lat": float, "lng": float}
        radius_meters: geofence radius
    
    Returns:
        dict with within_fence (bool), distance
    """
    dist = haversine_distance(
        cattle_gps["lat"], cattle_gps["lng"],
        farm_center["lat"], farm_center["lng"]
    )
    
    return {
        "within_fence": dist <= radius_meters,
        "distance_meters": round(dist, 2),
        "fence_radius": radius_meters
    }
