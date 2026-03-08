"""
SMS Alert — Send SMS notifications via Twilio
Author: Aditi
"""

import os
import logging

logger = logging.getLogger(__name__)

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER", "")


def send_sms(to_number: str, message: str) -> bool:
    """
    Send SMS via Twilio.
    
    Returns True if sent successfully, False otherwise.
    """
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_FROM]):
        logger.warning("Twilio credentials not configured — SMS skipped")
        return False
    
    try:
        from twilio.rest import Client
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=to_number
        )
        logger.info(f"SMS sent to {to_number}: SID={msg.sid}")
        return True
    except Exception as e:
        logger.error(f"SMS failed to {to_number}: {e}")
        return False
