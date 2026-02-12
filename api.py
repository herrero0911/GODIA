from fastapi import FastAPI
from pydantic import BaseModel
from ia import preguntar_ia

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Mensaje(BaseModel):
    texto: str

@app.post("/chat")
def chat(mensaje: Mensaje):
    respuesta = preguntar_ia(mensaje.texto)
    return {"respuesta": respuesta}