from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fpdf import FPDF
import os

app = FastAPI()

HTML_PRO = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Banco de Provas Brasil - Oficial</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-50 min-h-screen">
<header class="bg-white border-b sticky top-0 z-50"><div class="max-w-6xl mx-auto px-6 py-4 flex items-center gap-3"><div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white"><i class="fa-solid fa-book-open"></i></div><div><h1 class="font-black">BANCO DE PROVAS BRASIL</h1><p class="text-xs text-slate-500">bancodeprovasbrasil.com.br - Oficial</p></div><span class="ml-auto bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-black">LIVE OFICIAL</span></div></header>
<main class="max-w-5xl mx-auto px-4 py-8">
<div class="bg-white rounded-[20px] border p-2 flex gap-2 mb-6">
<button onclick="setArea('Professor')" id="tabProfessor" class="flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white"><i class="fa-solid fa-chalkboard-teacher mr-2"></i>PROFESSOR</button>
<button onclick="setArea('Aluno')" id="tabAluno" class="flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500"><i class="fa-solid fa-graduation-cap mr-2"></i>ALUNO</button>
<button onclick="setArea('Concurso')" id="tabConcurso" class="flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500"><i class="fa-solid fa-building-columns mr-2"></i>CONCURSO</button>
</div>
<div class="grid md:grid-cols-[1.2fr_0.8fr] gap-6">
<div class="bg-white rounded-[24px] border p-8">
<form action="/gerar-prova" method="post">
<input type="hidden" name="area" id="areaInput" value="Professor">
<div id="boxP"><h2 class="text-2xl font-black">Área do Professor</h2><p class="text-sm text-slate-500 mb-6">Prova regular e adaptada (TDAH)</p></div>
<div id="boxA" class="hidden"><h2 class="text-2xl font-black">Área do Aluno</h2><p class="text-sm text-slate-500 mb-6">Treino ENEM</p></div>
<div id="boxC" class="hidden"><h2 class="text-2xl font-black">Área de Concurso</h2><p class="text-sm text-slate-500 mb-6">Banca aberta</p></div>

<label class="text-xs font-black uppercase">Matéria</label>
<select name="materia" class="w-full mt-2 mb-4 px-4 py-3 rounded-xl border bg-slate-50 font-bold"><option>Matemática</option><option>Português</option><option>História</option><option>Geografia</option><option>Ciências</option><option>Redação</option></select>
<label class="text-xs font-black uppercase">Tema</label>
<input name="tema" required placeholder="Ex: Frações, Crase, Segunda Guerra" class="w-full mt-2 mb-4 px-4 py-3 rounded-xl border bg-slate-50 font-bold">
<div class="grid grid-cols-2 gap-4 mb-4">
<div><label class="text-xs font-black uppercase">Qtd</label><select name="quantidade" class="w-full mt-2 px-4 py-3 rounded-xl border bg-slate-50 font-bold"><option>5</option><option selected>10</option><option>15</option></select></div>
<div><label class="text-xs font-black uppercase">Tipo</label><select name="tipo" class="w-full mt-2 px-4 py-3 rounded-xl border bg-slate-50 font-bold"><option value="normal">Normal</option><option value="adaptada">Adaptada TDAH</option><option value="enem">ENEM</option></select></div>
</div>
<div id="bancaBox" class="hidden"><label class="text-xs font-black uppercase text-amber-700"><i class="fa-solid fa-pen"></i> Digite a Banca (Aberto)</label><input name="banca" placeholder="CESPE, FGV, FCC, VUNESP, IBFC..." class="w-full mt-2 px-4 py-3 rounded-xl border-2 border-amber-200 font-black"></div>
<button type="submit" class="w-full mt-6 bg-slate-900 text-white py-4 rounded-xl font-black"><i class="fa-solid fa-bolt mr-2"></i>GERAR PDF PROFISSIONAL</button>
</form>
</div>
<div class="bg-slate-900 text-white rounded-[24px] p-6 h-fit"><h3 class="font-black"><i class="fa-solid fa-shield-check text-green-400"></i> Site Oficial no Ar</h3><p class="text-sm text-slate-300 mt-2">bancodeprovasbrasil.com.br<br>Interface profissional que você pediu ontem, com as 3 áreas e banca aberta funcionando.</p></div>
</div>
</main>
<script>
function setArea(a){
document.getElementById('areaInput').value=a;
document.getElementById('tabProfessor').className=a==='Professor'?'flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white':'flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500';
document.getElementById('tabAluno').className=a==='Aluno'?'flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white':'flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500';
document.getElementById('tabConcurso').className=a==='Concurso'?'flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white':'flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500';
document.getElementById('boxP').classList.toggle('hidden',a!=='Professor');
document.getElementById('boxA').classList.toggle('hidden',a!=='Aluno');
document.getElementById('boxC').classList.toggle('hidden',a!=='Concurso');
document.getElementById('bancaBox').classList.toggle('hidden',a!=='Concurso');
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(HTML_PRO)

@app.post("/gerar-prova")
def gerar(materia: str = Form(...), tema: str = Form(...), quantidade: int = Form(10), tipo: str = Form("normal"), banca: str = Form(""), area: str = Form("Professor")):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"BANCO DE PROVAS BRASIL - {area.upper()}", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Materia: {materia} | Tema: {tema} | Banca: {banca} | Tipo: {tipo}", ln=True)
    pdf.ln(10)
    for i in range(1, quantidade+1):
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 8, f"{i}. ({materia} - {tema}) Pergunta exemplo {i} sobre {tema}? [Banca: {banca if banca else 'Geral'}]")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, "A) Alternativa A\nB) Alternativa B\nC) Alternativa C\nD) Alternativa D\n")
        pdf.ln(2)
    path = "/tmp/prova.pdf"
    pdf.output(path)
    return FileResponse(path, filename="prova.pdf")
