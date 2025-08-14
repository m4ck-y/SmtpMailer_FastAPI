"""
Módulo de configuración para SmtpMailer FastAPI.

Proporciona configuración centralizada basada en variables de entorno
usando Pydantic Settings para validación automática y type hints.
"""

from app.config.env import settings, Settings

__all__ = ["settings", "Settings"]