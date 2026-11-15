from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from gerar_prova import montar_prova
from gerar_pdf import criar_pdf
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    with open("app.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/gerar-prova")
def gerar(materia: str, tema: str, quantidade: int = 5, tipo: str = "normal"):
    perguntas = montar_prova(materia, tema, quantidade, tipo)
    caminho = criar_pdf(perguntas, materia, "Geral", tema)
    return FileResponse(caminho, filename="prova.pdf")
