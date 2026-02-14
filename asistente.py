# asistente.py
import requests
from fastapi import FastAPI, Request
import uvicorn

# -------------------------------
# CONFIGURACIÓN WHATSAPP (Whapi.Cloud)
# -------------------------------
WHAPI_TOKEN = "yPp49ofCErBqz8eozhKtz8c1r0ksNFf8AQUI_VA_TU_TOKEN_DE_WHAPI"
WHAPI_URL = "https://gate.whapi.cloud/"

# -------------------------------
# BACKEND FASTAPI
# -------------------------------
app = FastAPI()

# Guardamos información de clientes temporalmente (puedes usar DB después)
clientes = {}

# -------------------------------
# FUNCIONES DE ENVÍO
# -------------------------------
def enviar_mensaje(numero, texto):
    payload = {"to": numero, "type": "text", "text": {"body": texto}}
    headers = {"Authorization": f"Bearer {WHAPI_TOKEN}", "Content-Type": "application/json"}
    requests.post(WHAPI_URL, json=payload, headers=headers)

def enviar_bienvenida(numero):
    payload = {
        "to": numero,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "Muy buenas, soy tu asistente del taller.\n¿Para qué desea su cita?"},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": "mantenimiento", "title": "Mantenimiento"}},
                    {"type": "reply", "reply": {"id": "reparacion", "title": "Reparación / Avería"}},
                    {"type": "reply", "reply": {"id": "otra", "title": "Otra consulta"}}
                ]
            }
        }
    }
    headers = {"Authorization": f"Bearer {WHAPI_TOKEN}", "Content-Type": "application/json"}
    requests.post(WHAPI_URL, json=payload, headers=headers)

# -------------------------------
# WEBHOOK PARA RECIBIR MENSAJES
# -------------------------------
@app.post("/webhook")
async def whatsapp_webhook(req: Request):
    data = await req.json()
    print("DATA RECIBIDA:", data)
    return {"status": "ok"}    
# -------------------------------
# EJECUCIÓN LOCAL
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)