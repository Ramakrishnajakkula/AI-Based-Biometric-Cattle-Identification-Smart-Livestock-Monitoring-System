"""
Notification Manager — Routes alerts to SMS/Email/Dashboard
Author: Aditi

Severity routing:
    HIGH   → SMS + Email + Dashboard
    MEDIUM → Email + Dashboard
    LOW    → Dashboard only
"""

import logging
from .sms_alert import send_sms
from .email_alert import send_email

logger = logging.getLogger(__name__)


def route_alert(alert: dict):
    """
    Route an alert based on severity.
    
    Args:
        alert: dict with keys: cattle_id, type, severity, message, owner_contact
    """
    severity = alert.get("severity", "low").lower()
    cattle_id = alert.get("cattle_id", "unknown")
    message = alert.get("message", "Health alert")
    
    logger.info(f"Routing {severity} alert for {cattle_id}: {message}")
    
    # Dashboard notification is always stored in DB (handled by backend)
    
    if severity == "high":
        # SMS + Email
        phone = alert.get("owner_phone")
        email = alert.get("owner_email")
        
        if phone:
            send_sms(phone, f"URGENT: {message} for cattle {cattle_id}")
        if email:
            send_email(email, f"Health Alert: {cattle_id}", message)
        
        logger.warning(f"HIGH alert dispatched via SMS+Email for {cattle_id}")
    
    elif severity == "medium":
        # Email only
        email = alert.get("owner_email")
        if email:
            send_email(email, f"Health Alert: {cattle_id}", message)
        
        logger.info(f"MEDIUM alert dispatched via Email for {cattle_id}")
    
    else:
        logger.info(f"LOW alert for {cattle_id} — dashboard only")
