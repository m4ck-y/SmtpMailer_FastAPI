"""
Módulo de waitlist para SmtpMailer FastAPI.

Proporciona funcionalidad para envío de emails de confirmación
cuando los usuarios se registran en la lista de espera.
"""

from app.waitlist.router import router_waitlist, TAG_WAITLIST
from app.waitlist.models import WaitlistEmailRequest, WaitlistEmailResponse
from app.waitlist.controller import EmailWaitlistApplication

__all__ = [
    "router_waitlist", 
    "TAG_WAITLIST", 
    "WaitlistEmailRequest", 
    "WaitlistEmailResponse",
    "EmailWaitlistApplication"
]