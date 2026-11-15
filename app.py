from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from gerar_prova import montar_prova
from gerar_pdf import criar_pdf

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Banco de Provas</title>
<style>
body{font-family:'Segoe UI',Arial;background:#f1f5f9;margin:0;padding:20px;display:flex;justify-content:center;min-height:100vh}
.container{max-width:520px;width:100%}
.card{background:white;border-radius:20px;padding:30px;box-shadow:0 10px 30px rgba(0,0,0,0.08)}
h1{text-align:center;color:#0f172a;margin:0;font-size:28px}
.sub{text-align:center;color:#475569;font-size:14px;margin:10px 0 20px;line-height:1.5}
.btn{width:100%;padding:16px;border:none;border-radius:12px;font-size:16px;font-weight:800;cursor:pointer;margin-top:12px}
.btn-prof{background:#0f172a;color:white}
.btn-aluno{background:#2563eb;color:white}
.btn-conc{background:#7c3aed;color:white}
.footer{text-align:center;color:#94a3b8;font-size:11px;margin-top:20px;line-height:1.4}
label{display:block;margin-top:14px;font-size:14px;font-weight:500}
select,input{width:100%;padding:12px;margin-top:6px;border-radius:10px;border:1.5px solid #e2e8f0;box-sizing:border-box;font-size:14px}
select:focus,input:focus{outline:none;border-color:#f59e0b}
.dica{font-size:12px;color:#64748b;margin-top:5px}
.adaptada{background:#fef9c3;padding:12px;border-radius:10px;margin-top:15px;display:flex;align-items:center;gap:8px;font-weight:600;font-size:14px}
.voltar{background:#e2e8f0;border:none;padding:8px 12px;border-radius:8px;cursor:pointer;margin-bottom:10px}
#gerador{display:none}
#home{display:block}
.gerarBtn{width:100%;background:#0f172a;color:white;padding:14px;border:none;border-radius:12px;font-weight:800;margin-top:20px;cursor:pointer;font-size:15px}
</style>
</head>
<body>
<div class="container">

<div id="home" class="card">
  <h1>📚 Banco de Provas</h1>
  <div class="sub">Fundamental 1, Fundamental 2 e Ensino Médio<br>15 matérias - Prova Normal e Adaptada</div>
  <button class="btn btn-prof" onclick="abrir('professor')">👨‍🏫 Área do Professor</button>
  <button class="btn btn-aluno" onclick="abrir('aluno')">🧑‍🎓 Área do Aluno</button>
  <button class="btn btn-conc" onclick="abrir('concurso')">🏛️ Área de Concurso</button>
  <div class="footer">Sistema com turma e tema aberto<br>Prova com gabarito no final para edição com logo da escola</div>
</div>

<div id="gerador" class="card">
  <button class="voltar" onclick="voltar()">← Voltar</button>
  <h2 style="margin:5px 0 15px">🧑‍🏫 Gerar Prova</h2>
  
  <label>Turma:</label>
  <select id="turma">
    <option>-- Escolha --</option>
    <option>3º ano - Fundamental 1</option>
    <option>4º ano - Fundamental 1</option>
    <option>5º ano - Fundamental 1</option>
    <option>6º ano - Fundamental 2</option>
    <option>7º ano - Fundamental 2</option>
    <option>8º ano - Fundamental 2</option>
    <option>9º ano - Fundamental 2</option>
    <option>1º ano - Ensino Médio</option>
    <option>2º ano - Ensino Médio</option>
    <option>3º ano - Ensino Médio / ENEM</option>
  </select>

  <label>Matéria (15):</label>
  <select id="materia">
    <option>1 - Português</option>
    <option>2 - Matemática</option>
    <option>3 - História</option>
    <option>4 - Geografia</option>
    <option>5 - Ciências / Biologia</option>
    <option>6 - Física</option>
    <option>7 - Química</option>
    <option>8 - Inglês</option>
    <option>9 - Espanhol</option>
    <option>10 - Sociologia</option>
    <option>11 - Filosofia</option>
    <option>12 - Artes</option>
    <option>13 - Educação Física</option>
    <option>14 - Ensino Religioso</option>
    <option>15 - Concurso / Geral</option>
  </select>

  <label>Tema (digite o que você está trabalhando):</label>
  <input id="tema" placeholder="Ex: Arte Barroca, Fração, Revolução Francesa...">
  <div class="dica">💡 Você digita livre, cada escola trabalha um tema diferente.</div>

  <div class="adaptada">
    <input type="checkbox" id="adaptada" style="width:20px;height:20px">
    <label for="adaptada" style="margin:0">Prova Adaptada / Leve (texto curto para TDAH e inclusão)</label>
  </div>

  <label>Quantidade (1 a 10):</label>
  <input id="qtd" type="number" value="5" min="1" max="10">

  <button class="gerarBtn" onclick="gerar()">GERAR PROVA EM PDF</button>
  <p id="msg" style="font-size:13px;color:#64748b;text-align:center;margin-top:10px"></p>
</div>

</div>
<script>
function abrir(t){
  document.getElementById("home").style.display="none";
  document.getElementById("gerador").style.display="block";
}
function voltar(){
  document.getElementById("home").style.display="block";
  document.getElementById("gerador").style.display="none";
}
async function gerar(){
  const materia=document.getElementById("materia").value;
  const tema=document.getElementById("tema").value || "tema geral";
  const qtd=document.getElementById("qtd").value;
  const adaptada=document.getElementById("adaptada").checked ? "adaptada" : "normal";
  if(document.getElementById("turma").value=="-- Escolha --"){alert("Escolha a turma!");return}
  if(!tema){alert("Digite o tema!");return}
  document.getElementById("msg").innerText="Gerando... aguarde";
  try{
    const res=await fetch(`/gerar-prova?materia=${materia}&tema=${tema}&quantidade=${qtd}&tipo=${adaptada}`,{method:"POST"});
    const blob=await res.blob();
    const url=URL.createObjectURL(blob);
    const a=document.createElement("a");a.href=url;a.download="prova.pdf";a.click();
    document.getElementById("msg").innerText="Pronto! PDF baixado.";
  }catch(e){document.getElementById("msg").innerText="Erro: "+e}
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/gerar-prova")
def gerar(materia: str, tema: str, quantidade: int = 5, tipo: str = "normal"):
    perguntas = montar_prova(materia, tema, quantidade, tipo)
    caminho_pdf = criar_pdf(perguntas, materia, "Geral", tema)
    return FileResponse(caminho_pdf, filename="prova.pdf")
