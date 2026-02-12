import subprocess
import speech_recognition as sr
import ollama

# Inicializar el motor de voz
def hablar(texto):
    """
    Función para que el asistente hable usando la voz de macOS.
    """
    subprocess.run(["say", "-v", "Monica", "-r", "180", texto])

def escuchar():
    recognizer = sr.Recognizer()

    # 🔧 AJUSTES CLAVE PARA QUE NO CORTE FRASES
    recognizer.pause_threshold = 1.2        # segundos de silencio para parar
    recognizer.phrase_threshold = 0.3
    recognizer.non_speaking_duration = 0.5
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:
        print("🎤 Escuchando...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)  # escucha hasta que detecta silencio

    try:
        texto = recognizer.recognize_google(audio, language="es-ES")
        print("🗣️ Dijiste:", texto)
        return texto.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""

# -------- IA (Ollama) --------
mensajes = []

def ask_ai(texto):
    global mensajes

    mensajes.append({"role": "user", "content": texto})

    response = ollama.chat(
        model="llama3",
        messages=mensajes
    )

    respuesta = response["message"]["content"]
    mensajes.append({"role": "assistant", "content": respuesta})

    return respuesta

# -------- PROGRAMA PRINCIPAL --------
hablar("Hola, soy tu asistente virtual. ¿En qué puedo ayudarte?")

while True:
    # 1️⃣ Escuchar al usuario
    comando = escuchar()

    # Si no escuchó nada, vuelve a intentar
    if not comando:
        continue

    print("Usuario:", comando)

    # 2️⃣ Salida del asistente
    if "salir" in comando.lower() or "adiós" in comando.lower():
        hablar("Hasta luego")
        break

    # 3️⃣ Procesar la respuesta del modelo
    respuesta = ask_ai(comando)
    print("Asistente:", respuesta)

    # 4️⃣ Hablar la respuesta (mientras habla, no escuchamos)
    hablar(respuesta)