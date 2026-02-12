# core/assistant.py

def responder(texto):
    texto = texto.lower()

    if "hola" in texto:
        return "Hola, soy el asistente virtual de la empresa. ¿En qué puedo ayudarte?"

    if "servicios" in texto:
        return "Ofrecemos soluciones digitales y automatización para empresas."

    if "contacto" in texto:
        return "Puedes contactarnos por correo o a través de nuestra web."

    if "adiós" in texto or "salir" in texto:
        return "Gracias por tu tiempo. Hasta luego."

    return "Lo siento, todavía estoy aprendiendo. ¿Puedes reformular?"