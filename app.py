from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gerar_prova import montar_prova
from gerar_pdf import criar_pdf

app = FastAPI(title="Banco de Provas Escola")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PedidoProva(BaseModel):
    materia: str
    serie: str
    tema: str
    quantidade: int = 10
    tipo: str = "multipla escolha"

@app.get("/")
def home():
    return {"status": "online", "mensagem": "Banco de Provas Escola rodando"}

@app.post("/gerar-prova")
def gerar_prova_endpoint(pedido: PedidoProva):
    perguntas = montar_prova(pedido.materia, pedido.tema, pedido.quantidade, pedido.tipo)
    caminho_pdf = criar_pdf(perguntas, pedido.materia, pedido.serie, pedido.tema)
    return FileResponse(caminho_pdf, filename="prova.pdf", media_type="application/pdf")
