from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def gerar_pdf(texto, gabarito, nome_arquivo):
    pdf = canvas.Canvas(nome_arquivo, pagesize=letter)
    largura, altura = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(220, altura - 50, "PROVA")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, altura - 80, "Nome: ____________________________")
    pdf.drawString(350, altura - 80, "Data: ____/____/______")

    y = altura - 120

    pdf.setFont("Helvetica", 11)

    for linha in texto.split("\n"):
        pdf.drawString(50, y, linha)
        y -= 15

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = altura - 50

    pdf.showPage()

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(200, altura - 50, "GABARITO")

    pdf.setFont("Helvetica", 12)
    y = altura - 100

    for i, resposta in enumerate(gabarito, start=1):
        pdf.drawString(50, y, f"{i} - {resposta}")
        y -= 20

    pdf.save()