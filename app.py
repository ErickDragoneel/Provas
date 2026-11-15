from fastapi import FastAPI
from gerar_prova import montar_prova
from gerar_pdf import criar_pdf
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return {"status": "ok", "mensagem": "Banco de Provas no ar!"}

@app.post("/gerar-prova")
def gerar(materia: str, tema: str, quantidade: int = 5, tipo: str = "multipla escolha"):
    perguntas = montar_prova(materia, tema, quantidade, tipo)
    caminho_pdf = criar_pdf(perguntas, materia, "Geral", tema)
    return FileResponse(caminho_pdf, filename="prova.pdf")
