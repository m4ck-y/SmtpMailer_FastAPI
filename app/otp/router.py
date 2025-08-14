from fastapi import APIRouter, HTTPException, status
from app.otp.controller import EmailOTPApplication


controller = EmailOTPApplication()



MODULE_NAME = "email"

router_otp = APIRouter(
    prefix=f"/{MODULE_NAME}",
    tags=[MODULE_NAME])

TAG_OTP = {
    "name": MODULE_NAME,
    "description": """
- 🔐 **Códigos OTP** - Envío de códigos de verificación seguros
- 🎯 **Funcionalidades:** Generación y envío de códigos temporales para 2FA
- 🚀 **Casos de uso:** Registro, login seguro, recuperación de cuenta  
- 📧 **Características:** HTML responsivo, rate limiting, validación RFC
- ⚡ **Seguridad:** Códigos aleatorios, expiración configurable, logging completo
"""
}

@router_otp.post("/send_otp")
def enviar_codigo_otp(email: str, code: str, app_name: str):
    try:
        controller.Send_OTP(email, code, app_name)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))