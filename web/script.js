// Inicializar reconocimiento de voz
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
if (!SpeechRecognition) {
    alert("Tu navegador no soporta reconocimiento de voz");
}
recognition.lang = "es-ES"; // Español
recognition.interimResults = false;

recognition.onresult = function(event) {
    const texto = event.results[0][0].transcript;
    document.getElementById("mensaje").value = texto; // pone el texto en el input
    enviarMensaje(); // lo envía automáticamente
};
const chatDiv = document.getElementById("chat");
const input = document.getElementById("mensaje");

async function enviarMensaje() {
    const texto = input.value;
    if (!texto) return;

    // Mostrar mensaje del usuario
    const pUser = document.createElement("p");
    pUser.className = "user";
    pUser.textContent = "Tú: " + texto;
    chatDiv.appendChild(pUser);

    input.value = "";

    // Llamar a la API
    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto })
    });

    const data = await response.json();

    // Mostrar respuesta del bot
    const pBot = document.createElement("p");
    pBot.className = "bot";
    pBot.textContent = "IA: " + data.respuesta;
    chatDiv.appendChild(pBot);
    // Reproducir voz de la IA
    const utterance = new SpeechSynthesisUtterance(data.respuesta);
    utterance.lang = "es-ES";
    speechSynthesis.speak(utterance);

    chatDiv.scrollTop = chatDiv.scrollHeight;
}
function hablarIA() {
    recognition.start(); // empieza a escuchar
}