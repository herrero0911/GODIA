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
    numero = data.get("from")
    mensaje = data.get("message", {}).get("text", {}).get("body", "")
    boton = data.get("message", {}).get("interactive", {}).get("button_reply", {}).get("id")

    if not numero:
        return {"status": "error", "detail": "No hay número de cliente"}

    if numero not in clientes:
        clientes[numero] = {}

    # Paso 1: el cliente pulsa un botón
    if boton:
        clientes[numero]["servicio"] = boton
        enviar_mensaje(numero, "Perfecto. Por favor, indíqueme su nombre completo y la matrícula de su coche.")
        return {"status": "ok"}

    # Paso 2: el cliente envía nombre y matrícula
    if "nombre" not in clientes[numero]:
        # Simple: suponemos que envía "Nombre Matricula"
        partes = mensaje.split()
        clientes[numero]["nombre"] = partes[0]
        clientes[numero]["matricula"] = partes[-1]
        enviar_mensaje(numero, "Gracias. Ahora indique el día y la hora que desea su cita.")
        return {"status": "ok"}

    # Paso 3: el cliente envía fecha y hora
    if "fecha" not in clientes[numero]:
        clientes[numero]["fecha"] = mensaje
        servicio = clientes[numero]["servicio"]
        nombre = clientes[numero]["nombre"]
        matricula = clientes[numero]["matricula"]
        enviar_mensaje(numero, f"Su cita ha sido registrada: {mensaje}, matrícula {matricula}, servicio {servicio}. Gracias, {nombre}.")
        return {"status": "ok"}

    return {"status": "ok"} 
# -------------------------------
# EJECUCIÓN LOCAL
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)