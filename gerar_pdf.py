from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def criar_pdf(perguntas, materia, serie, tema):
    caminho = "/tmp/prova.pdf"
    if os.name == "nt":
        caminho = "prova.pdf"
    
    c = canvas.Canvas(caminho, pagesize=A4)
    width, height = A4
    
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, f"PROVA - {materia.upper()} - {serie}")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Tema: {tema}")
    y -= 40
    
    c.setFont("Helvetica", 11)
    for i, q in enumerate(perguntas, 1):
        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)
        
        texto_pergunta = q.get("pergunta", str(q))
        c.drawString(50, y, f"{i}. {texto_pergunta[:90]}")
        y -= 15
        
        for alt in q.get("alternativas", []):
            c.drawString(70, y, str(alt)[:85])
            y -= 15
        y -= 10
    
    c.save()
    return caminho
