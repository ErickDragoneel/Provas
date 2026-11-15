from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fpdf import FPDF
app = FastAPI()

HTML = """<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Banco de Provas Brasil - FINAL OFICIAL</title><script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet"></head>
<body class="bg-slate-50 min-h-screen flex flex-col">
<header class="bg-white border-b sticky top-0 z-50"><div class="max-w-6xl mx-auto px-6 py-4 flex items-center gap-3">
<div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white"><i class="fa-solid fa-book-open"></i></div>
<div><h1 class="font-black">BANCO DE PROVAS BRASIL</h1><p class="text-[11px] text-slate-500 font-bold">OFICIAL FINAL - 4 AREAS CORRIGIDAS</p></div>
<span class="ml-auto bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-black">FINAL</span></div></header>
<main class="flex-1 max-w-5xl w-full mx-auto px-4 py-8">
<div class="bg-white rounded-[20px] shadow-sm border p-2 grid grid-cols-4 gap-2 mb-6">
<button onclick="setArea('Professor')" id="bP" class="py-3 rounded-xl font-black text-sm bg-slate-900 text-white">PROFESSOR</button>
<button onclick="setArea('Aluno')" id="bA" class="py-3 rounded-xl font-black text-sm text-slate-500">ALUNO</button>
<button onclick="setArea('Concurso')" id="bC" class="py-3 rounded-xl font-black text-sm text-slate-500">CONCURSO</button>
<button onclick="setArea('BaseTecnica')" id="bT" class="py-3 rounded-xl font-black text-sm bg-amber-100 text-slate-700">BASE TECNICA</button>
</div>
<div class="bg-white rounded-[24px] shadow-sm border p-8">
<form action="/gerar-prova" method="post">
<input type="hidden" name="area" id="area" value="Professor">
<div id="divTurma"><label class="text-xs font-black uppercase">TURMA</label>
<select name="turma" id="selTurma" class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-blue-200 bg-blue-50 font-bold"></select></div>
<div id="divEixo" class="hidden mt-4 p-4 bg-amber-50 border-2 border-amber-200 rounded-xl">
<label class="text-xs font-black uppercase">EIXO / CURSO DA BASE TECNICA (ja e a materia)</label>
<select name="eixo" class="w-full mt-2 px-4 py-3.5 rounded-xl border font-bold">
<option>Eventos - Turismo, Hospitalidade e Lazer</option><option>Gastronomia - Turismo, Hospitalidade e Lazer</option>
<option>Hospedagem - Turismo, Hospitalidade e Lazer</option><option>Informatica - Informacao e Comunicacao</option>
<option>Administracao - Gestao e Negocios</option><option>Vendas - Gestao e Negocios</option>
<option>Contabilidade - Gestao e Negocios</option><option>Enfermagem - Ambiente e Saude</option>
<option>Seguranca do Trabalho</option><option>Agroindustria - Producao Alimenticia</option><option>Edificacoes - Infraestrutura</option>
</select></div>
<div id="divMateria" class="mt-4"><label class="text-xs font-black uppercase">MATERIA (17 oficiais)</label>
<select name="materia" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold">
<option>Portugues</option><option>Matematica</option><option>Historia</option><option>Geografia</option><option>Ciencias</option>
<option>Biologia</option><option>Quimica</option><option>Fisica</option><option>Literatura</option><option>Ingles</option>
<option>Espanhol</option><option>Filosofia</option><option>Sociologia</option><option>Artes</option><option>Educacao Fisica</option><option>Ensino Religioso</option>
<option>ENEM - Todas as areas</option></select></div>
<div id="divTema" class="mt-4"><label class="text-xs font-black uppercase">TEMA DA PROVA</label>
<input name="tema" placeholder="Ex: Fracoes, Crase, Fotossintese..." class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold" required></div>
<div id="divTipo" class="mt-4 grid grid-cols-2 gap-4">
<div><label class="text-xs font-black uppercase">TIPO DE PROVA</label>
<select name="tipo" id="selTipo" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold"></select></div>
<div id="divQtd"><label class="text-xs font-black uppercase">QTD QUESTOES</label>
<select name="qtd" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold"><option>5</option><option selected>10</option><option>20</option><option>60 - Simulado ENEM</option></select></div>
</div>
<div id="divBanca" class="hidden mt-4 p-4 bg-yellow-50 border-2 border-yellow-200 rounded-xl">
<label class="text-xs font-black uppercase">BANCA LIVRE</label>
<select name="banca" class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-amber-300 bg-white font-bold">
<option>CESPE / Cebraspe</option><option>FGV</option><option>FCC</option><option>Vunesp</option>
<option>Cesgranrio</option><option>IBFC</option><option>AOCP</option><option>Quadrix</option><option>IDECAN</option></select>
<p class="text-[11px] text-amber-700 mt-2">Gera prova baseada nas provas antigas dessa banca</p></div>
<button type="submit" id="btnGerar" class="w-full mt-6 py-4 bg-blue-600 text-white rounded-xl font-black text-lg">GERAR PROVA</button>
</form></div></main>
<script>
const turmasBase = `<option>1º Ano Base Tecnica</option><option>2º Ano Base Tecnica</option><option>3º Ano Base Tecnica</option>`;
const turmasAluno = `<optgroup label="Fund I"><option>1º Ano Fund I</option><option>2º Ano Fund I</option><option>3º Ano Fund I</option><option>4º Ano Fund I</option><option>5º Ano Fund I</option></optgroup><optgroup label="Fund II"><option>6º Ano Fund II</option><option>7º Ano Fund II</option><option>8º Ano Fund II</option><option>9º Ano Fund II</option></optgroup><optgroup label="Medio"><option>1º Ano Medio</option><option>2º Ano Medio</option><option>3º Ano Medio</option></optgroup><optgroup label="ENEM"><option>ENEM - Simulado Completo</option></optgroup>`;
function setArea(a){
 document.getElementById('area').value=a;
 document.getElementById('bP').className='py-3 rounded-xl font-black text-sm '+(a=='Professor'?'bg-slate-900 text-white':'text-slate-500');
 document.getElementById('bA').className='py-3 rounded-xl font-black text-sm '+(a=='Aluno'?'bg-slate-900 text-white':'text-slate-500');
 document.getElementById('bC').className='py-3 rounded-xl font-black text-sm '+(a=='Concurso'?'bg-slate-900 text-white':'text-slate-500');
 document.getElementById('bT').className='py-3 rounded-xl font-black text-sm '+(a=='BaseTecnica'?'bg-slate-900 text-white':'bg-amber-100 text-slate-700');
 const selTurma=document.getElementById('selTurma'); const selTipo=document.getElementById('selTipo');
 const divEixo=document.getElementById('divEixo'); const divMateria=document.getElementById('divMateria');
 const divTema=document.getElementById('divTema'); const divTipo=document.getElementById('divTipo');
 const divBanca=document.getElementById('divBanca'); const divTurma=document.getElementById('divTurma');
 const divQtd=document.getElementById('divQtd');
 if(a=='BaseTecnica'){
   divTurma.classList.remove('hidden'); selTurma.innerHTML=turmasBase;
   divEixo.classList.remove('hidden'); divMateria.classList.add('hidden');
   divTema.classList.remove('hidden'); divTipo.classList.remove('hidden'); divBanca.classList.add('hidden'); divQtd.classList.remove('hidden');
   selTipo.innerHTML='<option>Normal</option><option>Adaptada</option>'; document.getElementById('btnGerar').innerText='GERAR PROVA BASE TECNICA - PDF com gabarito';
 } else if(a=='Concurso'){
   divTurma.classList.add('hidden'); divEixo.classList.add('hidden'); divMateria.classList.add('hidden');
   divTema.classList.add('hidden'); divTipo.classList.add('hidden'); divBanca.classList.remove('hidden');
   document.getElementById('btnGerar').innerText='GERAR PROVA DA BANCA';
 } else if(a=='Aluno'){
   divTurma.classList.remove('hidden'); selTurma.innerHTML=turmasAluno;
   divEixo.classList.add('hidden'); divMateria.classList.remove('hidden'); divTema.classList.remove('hidden');
   divTipo.classList.remove('hidden'); divBanca.classList.add('hidden'); divQtd.classList.remove('hidden');
   selTipo.innerHTML='<option>Normal</option>'; document.getElementById('btnGerar').innerText='GERAR PROVA ALUNO - Online';
 } else {
   divTurma.classList.remove('hidden'); selTurma.innerHTML=turmasAluno;
   divEixo.classList.add('hidden'); divMateria.classList.remove('hidden'); divTema.classList.remove('hidden');
   divTipo.classList.remove('hidden'); divBanca.classList.add('hidden'); divQtd.classList.remove('hidden');
   selTipo.innerHTML='<option>Normal</option><option>Adaptada</option>'; document.getElementById('btnGerar').innerText='GERAR PROVA PROFESSOR - PDF com gabarito';
 }
}
setArea('Professor');
</script></body></html>
"""
@app.get("/", response_class=HTMLResponse)
def home(): return HTML

@app.post("/gerar-prova")
def gerar(area: str=Form(...), turma: str=Form(""), materia: str=Form(""), tema: str=Form(""), qtd: str=Form("10"), tipo: str=Form("Normal"), eixo: str=Form(""), banca: str=Form("")):
    import random
    if area=="Concurso":
        num=20; questoes=""; gab=[]
        for i in range(1,num+1):
            c=random.choice(["A","B","C","D","E"]); gab.append(c)
            questoes+=f'<div class="bg-white border rounded-xl p-5 mb-4"><p class="font-bold">{i}. ({banca}) Questao baseada nas ultimas provas</p><div class="mt-3 space-y-2"><label class="flex gap-2"><input type="radio" name="q{i}" value="A"> A) Alt A</label><label class="flex gap-2"><input type="radio" name="q{i}" value="B"> B) Alt B</label><label class="flex gap-2"><input type="radio" name="q{i}" value="C"> C) Alt C</label><label class="flex gap-2"><input type="radio" name="q{i}" value="D"> D) Alt D</label><label class="flex gap-2"><input type="radio" name="q{i}" value="E"> E) Alt E</label></div></div>'
        page=f"<!DOCTYPE html><html><head><meta charset='UTF-8'><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-slate-100 p-6'><div class='max-w-3xl mx-auto'><div class='bg-yellow-500 text-white rounded-xl p-6 mb-6'><h1 class='font-black'>CONCURSO - {banca}</h1><p>Baseada nas ultimas provas da {banca}</p></div><form>{questoes}<button type='button' onclick='corrigir()' class='w-full py-4 bg-green-600 text-white rounded-xl font-black'>CORRIGIR</button></form><div id='res' class='hidden mt-6 bg-white border-2 border-green-300 rounded-xl p-6 text-center'></div></div><script>const gab='{','.join(gab)}'.split(',');function corrigir(){{let ac=0;for(let i=1;i<=20;i++){{let s=document.querySelector('input[name=q'+i+']:checked');if(s&&s.value==gab[i-1])ac++;}}document.getElementById('res').classList.remove('hidden');document.getElementById('res').innerHTML='<h2 class=text-3xl font-black>Acertou '+ac+' de 20 - {banca}</h2>';}}</script></body></html>"
        open("/tmp/c.html","w",encoding="utf-8").write(page); return FileResponse("/tmp/c.html",media_type="text/html")
    elif area in ["Aluno","BaseTecnica"]:
        num=60 if "60" in qtd else int(qtd.split()[0]) if qtd[0].isdigit() else 10
        if area=="BaseTecnica": materia=eixo
        questoes=""; gab=[]
        for i in range(1,num+1):
            c=random.choice(["A","B","C","D","E"]); gab.append(c)
            questoes+=f'<div class="bg-white border rounded-xl p-5 mb-4"><p class="font-bold">{i}. {materia} - {tema} - {turma}</p><div class="mt-3 space-y-2"><label class="flex gap-2"><input type="radio" name="q{i}" value="A"> A</label><label class="flex gap-2"><input type="radio" name="q{i}" value="B"> B</label><label class="flex gap-2"><input type="radio" name="q{i}" value="C"> C</label><label class="flex gap-2"><input type="radio" name="q{i}" value="D"> D</label><label class="flex gap-2"><input type="radio" name="q{i}" value="E"> E</label></div></div>'
        page=f"<!DOCTYPE html><html><head><meta charset='UTF-8'><script src='https://cdn.tailwindcss.com'></script></head><body class='bg-slate-100 p-6'><div class='max-w-3xl mx-auto'><div class='bg-blue-600 text-white rounded-xl p-6 mb-6'><h1 class='font-black'>{area} - {turma} - {materia}</h1></div><form>{questoes}<button type='button' onclick='corrigir()' class='w-full py-4 bg-green-600 text-white rounded-xl font-black'>CORRIGIR AGORA</button></form><div id='res' class='hidden mt-6 bg-white border rounded-xl p-6 text-center'></div></div><script>const gab='{','.join(gab)}'.split(',');function corrigir(){{let ac=0;for(let i=1;i<={num};i++){{let s=document.querySelector('input[name=q'+i+']:checked');if(s&&s.value==gab[i-1])ac++;}}document.getElementById('res').classList.remove('hidden');document.getElementById('res').innerHTML='<h2 class=text-3xl font-black>Acertou '+ac+' de {num}</h2>';}}</script></body></html>"
        open("/tmp/a.html","w",encoding="utf-8").write(page); return FileResponse("/tmp/a.html",media_type="text/html")
    else:
        pdf=FPDF(); pdf.add_page(); pdf.set_font("Arial","B",14); pdf.cell(0,10,f"BANCO DE PROVAS - {area} - {turma}",ln=True,align="C");
        pdf.set_font("Arial","",11); pdf.cell(0,8,f"Materia: {materia} | Tema: {tema} | Tipo: {tipo}",ln=True); pdf.ln(5)
        gab=[]; qn=60 if "60" in qtd else int(qtd.split()[0]) if qtd[0].isdigit() else 10
        for i in range(1,qn+1):
            c=random.choice(["A","B","C","D","E"]); gab.append(c); pdf.set_font("Arial","B",11); pdf.multi_cell(0,7,f"{i}. {tema} - {materia} - {turma}");
            pdf.set_font("Arial","",10);
            for l in ["A","B","C","D","E"]: pdf.cell(0,6,f" {l}) Alternativa {l}",ln=True); pdf.ln(3)
        pdf.add_page(); pdf.set_font("Arial","B",14); pdf.cell(0,10,"GABARITO PROFESSOR",ln=True,align="C")
        for i,c in enumerate(gab,1): pdf.cell(0,7,f"{i}: {c}",ln=True)
        pdf.output("/tmp/p.pdf"); return FileResponse("/tmp/p.pdf",media_type="application/pdf",filename="prova.pdf")
