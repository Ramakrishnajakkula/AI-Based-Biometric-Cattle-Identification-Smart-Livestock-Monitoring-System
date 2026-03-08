"""
Fraud Detector — Decision tree logic for insurance fraud detection
Author: Aditi

Decision flow:
    1. Face verification → is the cattle's biometric identity confirmed?
    2. Geo verification → is cattle located within owner's registered farm?
    3. Duplicate check → has a similar claim been filed recently?
    4. Pattern analysis → anomalous claim patterns from same owner?
    5. Decision → approve / flag for review / reject
"""


def detect_fraud(claim: dict, cattle_record: dict, verification_result: dict) -> dict:
    """
    Run fraud detection pipeline on an insurance claim.
    
    Args:
        claim: The insurance claim document
        cattle_record: The cattle document from DB
        verification_result: Output from claim_verifier.verify_claim()
    
    Returns:
        dict with fraud_score (0-100), risk_level, flags list
    """
    fraud_score = 0
    flags = []
    
    # 1. Face verification
    if not verification_result.get("face_verified", True):
        fraud_score += 30
        flags.append("BIOMETRIC_MISMATCH: Muzzle identity could not be verified")
    
    # 2. Geo verification
    if not verification_result.get("geo_verified", True):
        fraud_score += 20
        flags.append("GEO_ANOMALY: Cattle location doesn't match farm boundaries")
    
    # 3. Duplicate check
    if "Duplicate claim" in str(verification_result.get("reasons", [])):
        fraud_score += 25
        flags.append("DUPLICATE: Similar claim already exists")
    
    # 4. Pattern analysis
    if verification_result.get("owner_claim_count", 0) > 3:
        fraud_score += 15
        flags.append("PATTERN: Owner has multiple recent claims")
    
    # 5. Contradicting sensor data
    if "contradicts" in str(verification_result.get("reasons", [])).lower():
        fraud_score += 25
        flags.append("SENSOR_CONTRADICTION: Live sensor data contradicts claim")
    
    # Risk level
    if fraud_score >= 60:
        risk_level = "HIGH"
    elif fraud_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    return {
        "fraud_score": min(fraud_score, 100),
        "risk_level": risk_level,
        "flags": flags,
        "recommendation": "REJECT" if fraud_score >= 70 else "REVIEW" if fraud_score >= 40 else "APPROVE"
    }
