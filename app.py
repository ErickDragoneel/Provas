from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fpdf import FPDF
import os

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Banco de Provas Brasil</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-slate-50 min-h-screen flex flex-col">
<header class="bg-white border-b sticky top-0 z-50">
<div class="max-w-6xl mx-auto px-6 py-4 flex items-center gap-3">
<div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white"><i class="fa-solid fa-book-open"></i></div>
<div><h1 class="font-black text-slate-900 leading-none">BANCO DE PROVAS BRASIL</h1><p class="text-[11px] text-slate-500 font-bold">bancodeprovasbrasil.com.br • FASE TESTES • 17 MATÉRIAS</p></div>
<span class="ml-auto bg-green-100 text-green-700 px-3 py-1 rounded-full text-xs font-black">OFICIAL</span>
</div>
</header>

<main class="flex-1 max-w-5xl w-full mx-auto px-4 py-8">
<div class="bg-white rounded-[20px] shadow-sm border p-2 flex gap-2 mb-6">
<button onclick="setArea('Professor')" id="bP" class="flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white">PROFESSOR (PDF com gabarito)</button>
<button onclick="setArea('Aluno')" id="bA" class="flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500">ALUNO (Online)</button>
<button onclick="setArea('Concurso')" id="bC" class="flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500">CONCURSO (Banca)</button>
</div>

<div class="bg-white rounded-[24px] shadow-sm border p-8">
<form action="/gerar-prova" method="post" id="form">
<input type="hidden" name="area" id="area" value="Professor">

<div id="hP"><h2 class="text-2xl font-black">Área do Professor</h2><p class="text-sm text-slate-500 mb-4">Normal, Adaptada (TDAH ou transtornos), Não adaptada • PDF com gabarito no final</p></div>
<div id="hA" class="hidden"><h2 class="text-2xl font-black">Área do Aluno</h2><p class="text-sm text-slate-500 mb-4">Fund I, II, Médio e ENEM • Prova online com corrigir na hora • SEM gabarito</p></div>
<div id="hC" class="hidden"><h2 class="text-2xl font-black">Área de Concurso</h2><p class="text-sm text-slate-500 mb-4">Escolhe a banca primeiro • Prova online com corrigir</p></div>

<div class="grid md:grid-cols-2 gap-4">
<div>
<label class="text-xs font-black uppercase">Turma</label>
<select name="turma" class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-blue-200 bg-blue-50 font-bold">
<optgroup label="Fundamental I"><option>1º Ano Fund I</option><option>2º Ano Fund I</option><option>3º Ano Fund I</option><option>4º Ano Fund I</option><option>5º Ano Fund I</option></optgroup>
<optgroup label="Fundamental II"><option>6º Ano Fund II</option><option>7º Ano Fund II</option><option>8º Ano Fund II</option><option>9º Ano Fund II</option></optgroup>
<optgroup label="Ensino Médio"><option>1º Ano Médio</option><option>2º Ano Médio</option><option>3º Ano Médio</option></optgroup>
<optgroup label="ENEM / Outros"><option>ENEM - Simulado Completo (60 questões nível ENEM)</option><option>Turma Geral</option></optgroup>
</select>
</div>
<div id="tipoProf">
<label class="text-xs font-black uppercase">Tipo de Prova (Professor)</label>
<select name="tipo_prof" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold">
<option>Normal</option><option>Adaptada - TDAH ou Transtornos</option><option>Não Adaptada</option>
</select>
</div>
<div id="tipoAluno" class="hidden">
<label class="text-xs font-black uppercase">Dificuldade (Aluno)</label>
<select name="tipo_aluno" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold">
<option>Fácil</option><option selected>Médio</option><option>Difícil</option>
</select>
</div>
</div>

<div class="mt-4">
<label class="text-xs font-black uppercase">Matéria (17 oficiais)</label>
<select name="materia" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold">
<option>Português</option><option>Matemática</option><option>História</option><option>Geografia</option><option>Ciências</option><option>Biologia</option><option>Química</option><option>Física</option><option>Redação (em breve - fase paga)</option><option>Literatura</option><option>Inglês</option><option>Espanhol</option><option>Filosofia</option><option>Sociologia</option><option>Artes</option><option>Educação Física</option><option>Ensino Religioso</option><option>ENEM - Todas as áreas</option>
</select>
</div>

<div id="bancaBox" class="hidden mt-4">
<label class="text-xs font-black uppercase">Banca do Concurso (escolhe primeiro)</label>
<select name="banca" class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-amber-200 bg-amber-50 font-bold">
<option>CESPE / Cebraspe</option><option>FGV</option><option>FCC</option><option>Vunesp</option><option>Cesgranrio</option><option>IBFC</option><option>AOCP</option><option>Quadrix</option><option>IDECAN</option><option>Outro</option>
</select>
</div>

<div class="mt-4">
<label class="text-xs font-black uppercase">Tema da Prova</label>
<input name="tema" placeholder="Ex: Frações, Crase, Revolução Industrial, Fotossíntese, Equação do 2º grau..." class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold" required>
</div>

<div class="mt-4">
<label class="text-xs font-black uppercase">Quantidade de Questões</label>
<select name="qtd" class="w-full mt-2 px-4 py-3.5 rounded-xl border bg-slate-50 font-bold">
<option>5</option><option selected>10</option><option>15</option><option>20</option><option>60 - Simulado ENEM</option>
</select>
</div>

<button type="submit" class="w-full mt-6 py-4 bg-blue-600 text-white rounded-xl font-black text-lg hover:bg-blue-700"><i class="fa-solid fa-bolt"></i> GERAR PROVA OFICIAL</button>
<p class="text-[11px] text-slate-400 mt-2 text-center" id="infoBtn">Professor = PDF com gabarito | Aluno/Concurso = Prova online com botão Corrigir</p>
</form>
</div>
</main>
<script>
function setArea(a){
 document.getElementById('area').value=a;
 document.getElementById('bP').className='flex-1 py-3.5 rounded-xl font-black text-sm '+(a=='Professor'?'bg-slate-900 text-white':'text-slate-500');
 document.getElementById('bA').className='flex-1 py-3.5 rounded-xl font-black text-sm '+(a=='Aluno'?'bg-slate-900 text-white':'text-slate-500');
 document.getElementById('bC').className='flex-1 py-3.5 rounded-xl font-black text-sm '+(a=='Concurso'?'bg-slate-900 text-white':'text-slate-500');
 document.getElementById('hP').classList.toggle('hidden',a!='Professor');
 document.getElementById('hA').classList.toggle('hidden',a!='Aluno');
 document.getElementById('hC').classList.toggle('hidden',a!='Concurso');
 document.getElementById('tipoProf').classList.toggle('hidden',a=='Concurso');
 document.getElementById('tipoAluno').classList.toggle('hidden',a=='Professor');
 document.getElementById('bancaBox').classList.toggle('hidden',a!='Concurso');
 document.getElementById('infoBtn').innerText = a=='Professor' ? 'Vai gerar PDF COM GABARITO no final' : 'Vai gerar PROVA ONLINE com botão CORRIGIR (sem gabarito)';
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML

@app.post("/gerar-prova")
def gerar(area: str = Form(...), turma: str = Form(...), materia: str = Form(...), tema: str = Form(...), qtd: str = Form(...), tipo_prof: str = Form("Normal"), tipo_aluno: str = Form("Médio"), banca: str = Form("FGV")):
    # Se for ALUNO ou CONCURSO -> gera prova ONLINE (HTML com corrigir)
    if area in ["Aluno", "Concurso"]:
        num = 60 if "60" in qtd or "ENEM" in turma else int(qtd.split()[0]) if qtd[0].isdigit() else 10
        # 10 questões fake pra demonstração (depois troca por IA)
        questoes_html = ""
        gabarito = []
        import random
        for i in range(1, num+1):
            correta = random.choice(["A","B","C","D","E"])
            gabarito.append(correta)
            questoes_html += f"""
            <div class="bg-white border rounded-xl p-5 mb-4">
            <p class="font-bold">{i}. ({area} - {materia} - {tema}) - Qual alternativa correta sobre {tema}?</p>
            <div class="mt-3 space-y-2">
                <label class="flex gap-2"><input type="radio" name="q{i}" value="A"> A) Alternativa A sobre {tema}</label>
                <label class="flex gap-2"><input type="radio" name="q{i}" value="B"> B) Alternativa B sobre {tema}</label>
                <label class="flex gap-2"><input type="radio" name="q{i}" value="C"> C) Alternativa C sobre {tema}</label>
                <label class="flex gap-2"><input type="radio" name="q{i}" value="D"> D) Alternativa D sobre {tema}</label>
                <label class="flex gap-2"><input type="radio" name="q{i}" value="E"> E) Alternativa E sobre {tema}</label>
            </div>
            </div>
            """
        gab_str = ",".join(gabarito)
        page = f"""
        <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-100 p-6"><div class="max-w-3xl mx-auto">
        <div class="bg-blue-600 text-white rounded-xl p-6 mb-6"><h1 class="font-black text-xl">{area} - {turma} - {materia} - {tema}</h1><p class="text-sm opacity-80">Banca: {banca} | {num} questões | SEM gabarito (correção automática)</p></div>
        <form id="prova">{questoes_html}
        <button type="button" onclick="corrigir()" class="w-full py-4 bg-green-600 text-white rounded-xl font-black text-lg">CORRIGIR AGORA</button>
        </form>
        <div id="resultado" class="hidden mt-6 bg-white border-2 border-green-300 rounded-xl p-6 text-center"></div>
        </div>
        <script>
        const gab = "{gab_str}".split(",");
        function corrigir(){{
            let acertos=0;
            for(let i=1;i<={num};i++){{
                let sel=document.querySelector('input[name="+'q'+i+':checked"]');
                if(sel && sel.value==gab[i-1]) acertos++;
            }}
            document.getElementById('resultado').classList.remove('hidden');
            document.getElementById('resultado').innerHTML = '<h2 class="text-3xl font-black">Você acertou '+acertos+' de {num}</h2><p class="mt-2">Nota: '+((acertos/{num})*10).toFixed(1)+'</p><p class="text-sm text-slate-500 mt-2">Fase testes - correção automática grátis</p>';
            window.scrollTo(0,document.body.scrollHeight);
        }}
        </script>
        </body></html>
        """
        path="/tmp/prova_online.html"
        open(path,"w",encoding="utf-8").write(page)
        return FileResponse(path, media_type="text/html", filename="prova_online.html")

    # PROFESSOR -> PDF COM GABARITO
    else:
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Arial","B",16)
        pdf.cell(0,10,f"BANCO DE PROVAS BRASIL - {area.upper()}",ln=True,align="C")
        pdf.set_font("Arial","",11)
        pdf.cell(0,8,f"Turma: {turma} | Materia: {materia} | Tema: {tema} | Tipo: {tipo_prof}",ln=True)
        pdf.cell(0,8,f"17 materias oficiais - com Espanhol e Ensino Religioso",ln=True)
        pdf.ln(5)
        import random
        gab=[]
        qtd_num = 60 if "60" in qtd else int(qtd.split()[0]) if qtd[0].isdigit() else 10
        for i in range(1,qtd_num+1):
            corr=random.choice(["A","B","C","D","E"])
            gab.append(corr)
            pdf.set_font("Arial","B",11)
            pdf.multi_cell(0,7,f"{i}. ({materia} - {tema}) - Questao sobre {tema} - Turma {turma}")
            pdf.set_font("Arial","",10)
            for l in ["A","B","C","D","E"]:
                pdf.cell(0,6,f" {l}) Alternativa {l} sobre {tema}",ln=True)
            pdf.ln(3)
        pdf.add_page()
        pdf.set_font("Arial","B",14)
        pdf.cell(0,10,"GABARITO - USO EXCLUSIVO DO PROFESSOR",ln=True,align="C")
        pdf.set_font("Arial","",12)
        for i,c in enumerate(gab,1):
            pdf.cell(0,7,f"Questao {i}: {c}",ln=True)
        out="/tmp/prova_professor.pdf"
        pdf.output(out)
        return FileResponse(out, media_type="application/pdf", filename=f"prova_{materia}_{tema}.pdf")
