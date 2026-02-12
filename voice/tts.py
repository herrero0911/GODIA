import pyttsx3

def hablar(texto):
    # Crear un motor nuevo cada vez
    engine = pyttsx3.init(driverName='nsss')  # nsss funciona en Mac
    engine.setProperty("rate", 170)
    engine.say(texto)
    engine.runAndWait()