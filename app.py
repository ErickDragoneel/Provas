from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from gerar_prova import montar_prova
from gerar_pdf import criar_pdf
app = FastAPI()

HTML_PAGE = """<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Banco de Provas</title><style>body{font-family:Segoe UI,Arial;background:#f1f5f9;margin:0;padding:20px;display:flex;justify-content:center} .container{max-width:560px;width:100%} .card{background:white;border-radius:20px;padding:30px;box-shadow:0 10px 30px rgba(0,0,0,.08)} h1{text-align:center;color:#0f172a;margin:0} .sub{text-align:center;color:#475569;font-size:14px;margin:10px 0 20px} .btn{width:100%;padding:16px;border:none;border-radius:12px;font-size:16px;font-weight:800;cursor:pointer;margin-top:12px} .btn-prof{background:#0f172a;color:white} .btn-aluno{background:#2563eb;color:white} .btn-conc{background:#7c3aed;color:white} .footer{text-align:center;color:#64748b;font-size:12px;margin-top:25px;line-height:1.5} label{display:block;margin-top:14px;font-size:14px;font-weight:600} select,input{width:100%;padding:12px;margin-top:6px;border-radius:10px;border:1.5px solid #e2e8f0;box-sizing:border-box} .adaptada{background:#fef9c3;padding:12px;border-radius:10px;margin-top:15px;display:flex;gap:8px;font-weight:600;font-size:14px} .voltar{background:#e2e8f0;border:none;padding:8px 12px;border-radius:8px;cursor:pointer;margin-bottom:10px} #gerador{display:none} .gerarBtn{width:100%;background:#0f172a;color:white;padding:14px;border:none;border-radius:12px;font-weight:800;margin-top:20px;cursor:pointer} .badge{display:inline-block;padding:4px 10px;border-radius:12px;font-size:11px;font-weight:bold;color:white;margin-bottom:8px} .bancaBox{background:#f5f3ff;border:1.5px solid #ddd6fe;padding:12px;border-radius:10px;margin-top:10px} </style></head><body><div class="container"><div id="home" class="card"><h1>📚 Banco de Provas</h1><div class="sub">Fundamental 1, 2 e Médio - 15 matérias<br>Prova Normal e Adaptada</div><div style="text-align:left;background:#f8fafc;padding:15px;border-radius:12px;margin:15px 0;font-size:13px;color:#334155"><b>👨‍🏫 Professor:</b> Crie provas com turma e tema aberto.<br><b>🎓 Aluno:</b> Simulado por série, incluindo ENEM. Em breve Redação.<br><b>🏛️ Concurso:</b> Digite a banca e a IA busca questões no estilo da banca.</div><button class="btn btn-prof" onclick="abrir('professor')">👨‍🏫 Área do Professor</button><button class="btn btn-aluno" onclick="abrir('aluno')">🧑‍🎓 Área do Aluno</button><button class="btn btn-conc" onclick="abrir('concurso')">🏛️ Área de Concurso</button><div class="footer">contato@bancodeprovas.com.br<br>Sistema com turma e tema aberto - Gabarito no final</div></div><div id="gerador" class="card"><button class="voltar" onclick="voltar()">← Voltar</button><h2 id="titulo"></h2><div id="bad"></div><div id="campos"></div><button class="gerarBtn" onclick="gerar()">GERAR PROVA EM PDF</button><p id="msg" style="font-size:13px;color:#64748b;text-align:center;margin-top:10px"></p></div></div><script>
let perfil=""
function abrir(p){
 perfil=p
 document.getElementById("home").style.display="none"
 document.getElementById("gerador").style.display="block"
 let html="", titulo="", badge=""
 if(p=="professor"){
  titulo="👨‍🏫 Área do Professor - Gerar Prova"; badge="<span class='badge' style='background:#0f172a'>PROFESSOR</span>"
  html=`<label>Turma:</label><select id="turma"><option>-- Escolha --</option><option>3º ano Fund 1</option><option>6º ano Fund 2</option><option>9º ano Fund 2</option><option>1º Médio</option><option>3º Médio / ENEM</option></select><label>Matéria (15):</label><select id="materia"><option>1 - Português</option><option>2 - Matemática</option><option>3 - História</option><option>5 - Biologia</option><option>15 - Geral</option></select><label>Tema (o que está trabalhando):</label><input id="tema" placeholder="Ex: Fração, Arte Barroca"><div class="adaptada"><input type="checkbox" id="adaptada" style="width:18px"><label for="adaptada" style="margin:0">Prova Adaptada / Leve (TDAH e inclusão)</label></div><label>Quantidade:</label><input id="qtd" type="number" value="5" min="1" max="10">`
 }else if(p=="aluno"){
  titulo="🎓 Área do Aluno - Meu Simulado"; badge="<span class='badge' style='background:#2563eb'>ALUNO - ENEM</span>"
  html=`<label>Sua Série:</label><select id="turma"><option>-- Escolha --</option><option>6º ano</option><option>9º ano</option><option>1º Médio</option><option>2º Médio</option><option>3º Médio / ENEM</option></select><label>Matéria:</label><select id="materia"><option>Português - ENEM</option><option>Matemática - ENEM</option><option>História</option><option>Biologia - ENEM</option><option>Redação (em breve)</option></select><label>O que quer revisar?</label><input id="tema" placeholder="Ex: Função, Interpretação, Genética"><label>Quantidade:</label><input id="qtd" type="number" value="5">`
 }else{
  titulo="🏛️ Área de Concurso"; badge="<span class='badge' style='background:#7c3aed'>CONCURSO - BANCA ABERTA</span>"
  html=`<div class="bancaBox"><label>🏛️ Digite a Banca (aberto):</label><input id="banca" placeholder="Ex: CESPE, FCC, Vunesp, IBFC, FGV, Cebraspe..."><div style="font-size:11px;color:#6d28d9;margin-top:4px">💡 Deixe aberto, a IA busca no estilo da banca que você digitar.</div></div><label>Nível:</label><select id="turma"><option>Superior</option><option>Médio</option><option>Fundamental</option></select><label>Matéria de Concurso:</label><select id="materia"><option>Português para Concurso</option><option>Matemática / Raciocínio Lógico</option><option>Informática</option><option>Direito Constitucional</option><option>Atualidades</option></select><label>Tema / Cargo:</label><input id="tema" placeholder="Ex: Agente da PF, INSS, Banco do Brasil"><label>Quantidade:</label><input id="qtd" type="number" value="5">`
 }
 document.getElementById("titulo").innerText=titulo
 document.getElementById("bad").innerHTML=badge
 document.getElementById("campos").innerHTML=html
}
function voltar(){document.getElementById("home").style.display="block";document.getElementById("gerador").style.display="none"}
async function gerar(){
 const materia=document.getElementById("materia")?.value||"Geral"
 let tema=document.getElementById("tema")?.value||"geral"
 const qtd=document.getElementById("qtd")?.value||5
 const banca=document.getElementById("banca")?.value||""
 if(banca){tema = `Banca ${banca} - ${tema}`}
 const adapt=document.getElementById("adaptada")?.checked ? "adaptada" : "normal"
 document.getElementById("msg").innerText="Gerando no estilo da banca..."
 try{const r=await fetch(`/gerar-prova?materia=${materia}&tema=${tema}&quantidade=${qtd}&tipo=${adapt}`,{method:"POST"});const b=await r.blob();const u=URL.createObjectURL(b);const a=document.createElement("a");a.href=u;a.download="prova.pdf";a.click();document.getElementById("msg").innerText="Pronto! PDF baixado."}catch(e){document.getElementById("msg").innerText="Erro: "+e}
}
</script></body></html>
"""
@app.get("/", response_class=HTMLResponse)
def home(): return HTML_PAGE
@app.post("/gerar-prova")
def gerar(materia: str, tema: str, quantidade: int = 5, tipo: str = "normal"):
    perguntas = montar_prova(materia, tema, quantidade, tipo)
    caminho_pdf = criar_pdf(perguntas, materia, "Geral", tema)
    return FileResponse(caminho_pdf, filename="prova.pdf")
