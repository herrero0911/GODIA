# asistente.py
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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
    try:
        requests.post(WHAPI_URL, json=payload, headers=headers)
    except Exception as e:
        print(f"ERROR enviando mensaje a {numero}: {str(e)}")

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
    try:
        requests.post(WHAPI_URL, json=payload, headers=headers)
    except Exception as e:
        print(f"ERROR enviando bienvenida a {numero}: {str(e)}")

# -------------------------------
# WEBHOOK ROBUSTO PARA RECIBIR MENSAJES
# -------------------------------
@app.post("/webhook")
async def whatsapp_webhook(req: Request):
    try:
        # Intentamos leer JSON
        try:
            data = await req.json()
        except Exception:
            return JSONResponse(
                content={"status": "error", "detail": "No se recibió JSON válido"},
                status_code=400
            )

        print("DATA RECIBIDA:", data)  # Depuración

        # Validamos campos obligatorios
        numero = data.get("from")
        message = data.get("message", {})

        if not numero:
            return JSONResponse(
                content={"status": "error", "detail": "No hay número de cliente"},
                status_code=400
            )

        if numero not in clientes:
            clientes[numero] = {}

        # Detectar botón interactivo
        boton = message.get("interactive", {}).get("button_reply", {}).get("id")
        texto = message.get("text", {}).get("body", "")

        # PASO 1: cliente pulsa botón
        if boton:
            clientes[numero]["servicio"] = boton
            enviar_mensaje(numero, "Perfecto. Por favor, indíqueme su nombre completo y la matrícula de su coche.")
            return JSONResponse(content={"status": "ok"}, status_code=200)

        # PASO 2: cliente envía nombre y matrícula
        if "nombre" not in clientes[numero]:
            partes = texto.strip().split()
            if len(partes) < 2:
                return JSONResponse(
                    content={"status": "error", "detail": "Formato de nombre/matrícula incorrecto"},
                    status_code=400
                )
            clientes[numero]["nombre"] = partes[0]
            clientes[numero]["matricula"] = partes[-1]
            enviar_mensaje(numero, "Gracias. Ahora indique el día y la hora que desea su cita.")
            return JSONResponse(content={"status": "ok"}, status_code=200)

        # PASO 3: cliente envía fecha y hora
        if "fecha" not in clientes[numero]:
            clientes[numero]["fecha"] = texto
            servicio = clientes[numero]["servicio"]
            nombre = clientes[numero]["nombre"]
            matricula = clientes[numero]["matricula"]
            enviar_mensaje(numero, f"Su cita ha sido registrada: {texto}, matrícula {matricula}, servicio {servicio}. Gracias, {nombre}.")
            return JSONResponse(content={"status": "ok"}, status_code=200)

        # Si todo ya está completo
        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        print("ERROR WEBHOOK:", str(e))
        return JSONResponse(
            content={"status": "error", "detail": "Error interno del servidor", "exception": str(e)},
            status_code=500
        )

# -------------------------------
# EJECUCIÓN LOCAL
# -------------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)