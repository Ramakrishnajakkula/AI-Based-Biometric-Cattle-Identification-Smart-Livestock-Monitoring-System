"""
Email Alert — Send email notifications via SMTP
Author: Aditi
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "")


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send email via SMTP.
    
    Returns True if sent successfully, False otherwise.
    """
    if not all([SMTP_USER, SMTP_PASS]):
        logger.warning("SMTP credentials not configured — email skipped")
        return False
    
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL or SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        
        logger.info(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Email failed to {to_email}: {e}")
        return False
