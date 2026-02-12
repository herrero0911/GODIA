import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone()  # o usa device_index si tu micrófono no es el primero

def escuchar():
    """
    Escucha un comando desde el micrófono y devuelve el texto transcrito.
    """
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Escuchando...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            comando = r.recognize_google(audio, language="es-ES")
            comando = comando.lower().strip()
            print("✅ Transcripción:", comando)
            return comando
        except sr.WaitTimeoutError:
            print("⌛ No se detectó voz a tiempo")
            return ""
        except sr.UnknownValueError:
            print("❌ No se entendió")
            return ""
        except sr.RequestError as e:
            print("❌ Error con el servicio de reconocimiento:", e)
            return ""