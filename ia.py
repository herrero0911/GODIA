import ollama

# Memoria simple (luego se mejora)
mensajes = []

def preguntar_ia(texto):
    mensajes.append({"role": "user", "content": texto})

    response = ollama.chat(
        model="llama3",
        messages=mensajes
    )

    respuesta = response["message"]["content"]
    mensajes.append({"role": "assistant", "content": respuesta})

    return respuesta


# --- MODO PRUEBA POR TERMINAL (opcional) ---
def chat_terminal():
    print("🤖 Asistente iniciado. Escribe 'salir' para terminar.\n")

    while True:
        user_input = input("Tú: ")

        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 Asistente detenido.")
            break

        respuesta = preguntar_ia(user_input)
        print(f"Asistente: {respuesta}\n")


if __name__ == "__main__":
    chat_terminal()