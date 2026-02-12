import subprocess

def hablar(texto):
    """
    Función para que el asistente hable usando la voz de macOS.
    """
    # Cambia 'Monica' por la voz que prefieras
    # '-r 200' es la velocidad (palabras por minuto)
    subprocess.run(["say", "-v", "Monica", "-r", "200", texto])