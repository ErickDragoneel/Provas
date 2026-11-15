from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fpdf import FPDF

app = FastAPI()

HTML = """
<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Banco de Provas Brasil - 4 Areas</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"></head>
<body class="bg-slate-50 min-h-screen flex flex-col">
<header class="bg-white border-b sticky top-0 z-50"><div class="max-w-6xl mx-auto px-6 py-4 flex items-center gap-3">
<div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white"><i class="fa-solid fa-book-open"></i></div>
<div><h1 class="font-black text-slate-900">BANCO DE PROVAS BRASIL</h1><p class="text-[11px] text-slate-500 font-bold">4 AREAS • 17 materias + Base Tecnica 11 eixos</p></div>
<span class="ml-auto bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-black">4 AREAS OFICIAL</span></div></header>
<main class="flex-1 max-w-5xl w-full mx-auto px-4 py-8">
<div class="bg-white rounded-[20px] shadow-sm border p-2 grid grid-cols-2 md:grid-cols-4 gap-2 mb-6">
<button onclick="setArea('Professor')" id="bP" class="py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white">PROFESSOR</button>
<button onclick="setArea('Aluno')" id="bA" class="py-3.5 rounded-xl font-black text-sm text-slate-500">ALUNO</button>
<button onclick="setArea('Concurso')" id="bC" class="py-3.5 rounded-xl font-black text-sm text-slate-500">CONCURSO</button>
<button onclick="setArea('BaseTecnica')" id="bT" class="py-3.5 rounded-xl font-black text-sm text-slate-500 bg-amber-100">BASE TECNICA</button>
</div>
<div class="bg-white rounded-[24px] shadow-sm border p-8">
<form action="/gerar-prova" method="post">
<input type="hidden" name="area" id="area" value="Professor">
<div id="boxBase" class="hidden mb-4 p-4 bg-amber-50 border-2 border-amber-200 rounded-xl">
<label class="text-xs font-black uppercase">EIXO DA BASE TECNICA (11 eixos oficiais PB)</label>
<select name="eixo" class="w-full mt-2 px-4 py-3.5 rounded-xl border font-bold">
<option>Turismo, Hospitalidade e Lazer - Eventos</option>
<option>Turismo, Hospitalidade e Lazer - Gastronomia</option>
<option>Turismo, Hospitalidade e Lazer - Hospedagem</option>
<option>Informacao e Comunicacao - Informatica / Redes</option>
<option>Gestao e Negocios - Administracao</option>
<option>Gestao e Negocios - Vendas / Comercio</option>
<option>Gestao e Negocios - Contabilidade</option>
<option>Ambiente e Saude - Enfermagem / Saude</option>
<option>Seguranca - Seguranca do Trabalho</option>
<option>Producao Alimenticia - Agroindustria</option>
<option>Infraestrutura - Edificacoes / Eletrotecnica</option>
</select>
<p class="text-[11px] text-amber-700 mt-1">Conforme Genilson: base pega varios cursos, 11 eixos, 43 cursos tecnicos nas ECITs PB</p>
</div>
<div class="grid md:grid-cols-2 gap-4">
<div><label class="text-xs font-black uppercase">Turma</label>
<select name="turma" class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-blue-200 bg-blue-50 font-bold">
<optgroup label="Fund I"><option>1º Ano Fund I</option><option>5º Ano Fund I</option></optgroup>
<optgroup label="Fund II"><option>6º Ano Fund II</option><option>9º Ano Fund II</option></optgroup>
<optgroup label="Medio"><option>1º Ano Medio</option><option>3º Ano Medio</option></optgroup>
<optgroup label="Base Tecnica"><option>1º Ano Base Tecnica</option><option>2º Ano Base Tecnica</option><option>3º Ano Base Tecnica</option></optgroup>
<optgroup label="ENEM"><option>ENEM - Simulado Completo</option></optgroup>
</select></div>
<div><label class="text-xs font-black uppercase">Materia / Curso Tecnico</label>
<select name="materia" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold">
<optgroup label="17 materias oficiais"><option>Portugues</option><option>Matematica</option><option>Historia</option><option>Geografia</option><option>Ciencias</option><option>Biologia</option><option>Quimica</option><option>Fisica</option><option>Literatura</option><option>Ingles</option><option>Espanhol</option><option>Filosofia</option><option>Sociologia</option><option>Artes</option><option>Educacao Fisica</option><option>Ensino Religioso</option></optgroup>
<optgroup label="Cursos Tecnicos (Base)"><option>Eventos</option><option>Gastronomia</option><option>Hospedagem</option><option>Informatica</option><option>Administracao</option><option>Vendas</option><option>Enfermagem</option><option>Seguranca do Trabalho</option></optgroup>
</select></div>
</div>
<div class="mt-4"><label class="text-xs font-black uppercase">Tema da Prova</label>
<input name="tema" placeholder="Ex: Gestao de Eventos, Higiene na Gastronomia, Atendimento em Hospedagem..." class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold" required></div>
<div class="mt-4 grid md:grid-cols-2 gap-4">
<div><label class="text-xs font-black uppercase">Tipo</label><select name="tipo" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold"><option>Normal</option><option>Adaptada - TDAH</option><option>Nao Adaptada</option></select></div>
<div><label class="text-xs font-black uppercase">Qtd</label><select name="qtd" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold"><option>10</option><option>20</option><option>60 - ENEM</option></select></div>
</div>
<div id="bancaBox" class="hidden mt-4"><label class="text-xs font-black uppercase">Banca (Concurso)</label><select name="banca" class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-amber-200 bg-amber-50 font-bold"><option>CESPE</option><option>FGV</option><option>FCC</option><option>Vunesp</option></select></div>
<button type="submit" class="w-full mt-6 py-4 bg-blue-600 text-white rounded-xl font-black text-lg">GERAR PROVA - 4 AREAS OFICIAL</button>
</form></div></main>
<script>
function setArea(a){document.getElementById('area').value=a;
document.getElementById('bP').className='py-3.5 rounded-xl font-black text-sm '+(a=='Professor'?'bg-slate-900 text-white':'text-slate-500');
document.getElementById('bA').className='py-3.5 rounded-xl font-black text-sm '+(a=='Aluno'?'bg-slate-900 text-white':'text-slate-500');
document.getElementById('bC').className='py-3.5 rounded-xl font-black text-sm '+(a=='Concurso'?'bg-slate-900 text-white':'text-slate-500');
document.getElementById('bT').className='py-3.5 rounded-xl font-black text-sm '+(a=='BaseTecnica'?'bg-slate-900 text-white':'text-slate-500 bg-amber-100');
document.getElementById('boxBase').classList.toggle('hidden',a!='BaseTecnica');
document.getElementById('bancaBox').classList.toggle('hidden',a!='Concurso');
}
</script></body></html>
"""
@app.get("/", response_class=HTMLResponse)
def home(): return HTML
@app.post("/gerar-prova")
def gerar(area: str=Form(...), turma: str=Form(...), materia: str=Form(...), tema: str=Form(...), qtd: str=Form(...), tipo: str=Form(...), eixo: str=Form(""), banca: str=Form("")):
    if area in ["Aluno","Concurso"]:
        num = 60 if "60" in qtd else 10
        import random; questoes=""; gab=[]
        for i in range(1,num+1):
            c=random.choice(["A","B","C","D","E"]); gab.append(c)
            questoes+=f'<div class="bg-white border rounded-xl p-5 mb-4"><p class="font-bold">{i}. ({eixo} - {materia} - {tema})</p><div class="mt-3 space-y-2"><label class="flex gap-2"><input type="radio" name="q{i}" value="A"> A) Alternativa A</label><label class="flex gap-2"><input type="radio" name="q{i}" value="B"> B) Alternativa B</label><label class="flex gap-2"><input type="radio" name="q{i}" value="C"> C) Alternativa C</label><label class="flex gap-2"><input type="radio" name="q{i}" value="D"> D) Alternativa D</label><label class="flex gap-2"><input type="radio" name="q{i}" value="E"> E) Alternativa E</label></div></div>'
        page=f"<!DOCTYPE html><html><head><meta charset='UTF-8'><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-slate-100 p-6'><div class='max-w-3xl mx-auto'><div class='bg-blue-600 text-white rounded-xl p-6 mb-6'><h1 class='font-black'>{area} - {eixo} - {materia}</h1><p>{turma} - {tema}</p></div><form id='prova'>{questoes}<button type='button' onclick='corrigir()' class='w-full py-4 bg-green-600 text-white rounded-xl font-black'>CORRIGIR</button></form><div id='res' class='hidden mt-6 bg-white border-2 border-green-300 rounded-xl p-6 text-center'></div></div><script>const gab='{','.join(gab)}'.split(',');function corrigir(){{let ac=0;for(let i=1;i<={num};i++){{let s=document.querySelector('input[name=q'+i+']:checked');if(s&&s.value==gab[i-1])ac++;}}document.getElementById('res').classList.remove('hidden');document.getElementById('res').innerHTML='<h2 class=text-3xl font-black>Você acertou '+ac+' de {num}</h2>';}}</script></body></html>"
        open("/tmp/p.html","w",encoding="utf-8").write(page); return FileResponse("/tmp/p.html",media_type="text/html")
    else:
        pdf=FPDF();pdf.add_page();pdf.set_font("Arial","B",16);pdf.cell(0,10,f"BANCO PROVAS BRASIL - {area} - {eixo}",ln=True,align="C");pdf.set_font("Arial","",11);pdf.cell(0,8,f"Turma: {turma} | {materia} | {tema} | {tipo}",ln=True);pdf.ln(5)
        import random; gab=[]
        qtdn=60 if "60" in qtd else 10
        for i in range(1,qtdn+1):
            c=random.choice(["A","B","C","D","E"]);gab.append(c);pdf.set_font("Arial","B",11);pdf.multi_cell(0,7,f"{i}. {tema} - {materia} - {eixo}");pdf.set_font("Arial","",10)
            for l in ["A","B","C","D","E"]:pdf.cell(0,6,f" {l}) Alternativa {l}",ln=True)
            pdf.ln(3)
        pdf.add_page();pdf.set_font("Arial","B",14);pdf.cell(0,10,"GABARITO PROFESSOR - BASE TECNICA",ln=True,align="C")
        for i,c in enumerate(gab,1):pdf.cell(0,7,f"{i}: {c}",ln=True)
        pdf.output("/tmp/prof.pdf"); return FileResponse("/tmp/prof.pdf",media_type="application/pdf",filename="prova_base_tecnica.pdf")
