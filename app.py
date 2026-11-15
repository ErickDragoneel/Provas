from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from gerar_prova import montar_prova
from gerar_pdf import criar_pdf

app = FastAPI()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Banco de Provas</title>
<style>
body{font-family:Arial;background:#f0f2f5;padding:30px}
.card{background:white;max-width:600px;margin:auto;padding:30px;border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.1)}
input,select{width:100%;padding:10px;margin:8px 0;border-radius:8px;border:1px solid #ccc}
button{background:#7c3aed;color:white;padding:12px;width:100%;border:none;border-radius:8px;font-size:16px;cursor:pointer}
button:hover{background:#5b21b6}
h1{text-align:center;color:#7c3aed}
</style>
</head>
<body>
<div class="card">
<h1>📚 Banco de Provas</h1>
<label>Matéria</label><input id="materia" placeholder="Ex: Matemática">
<label>Tema</label><input id="tema" placeholder="Ex: Frações">
<label>Quantidade</label><input id="qtd" type="number" value="5">
<label>Tipo</label><select id="tipo"><option>multipla escolha</option><option>verdadeiro ou falso</option><option>dissertativa</option></select>
<br><br>
<button onclick="gerar()">Gerar Prova em PDF</button>
<p id="msg"></p>
</div>
<script>
async function gerar(){
  const materia=document.getElementById('materia').value;
  const tema=document.getElementById('tema').value;
  const quantidade=document.getElementById('qtd').value;
  const tipo=document.getElementById('tipo').value;
  if(!materia||!tema){alert('Preencha matéria e tema');return;}
  document.getElementById('msg').innerText='Gerando... aguarde 5s';
  const res=await fetch(`/gerar-prova?materia=${materia}&tema=${tema}&quantidade=${quantidade}&tipo=${tipo}`,{method:'POST'});
  if(res.ok){
    const blob=await res.blob();
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a');a.href=url;a.download='prova.pdf';a.click();
    document.getElementById('msg').innerText='Pronto! PDF baixado.';
  } else {
    document.getElementById('msg').innerText='Erro ao gerar';
  }
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.post("/gerar-prova")
def gerar(materia: str, tema: str, quantidade: int = 5, tipo: str = "multipla escolha"):
    perguntas = montar_prova(materia, tema, quantidade, tipo)
    caminho_pdf = criar_pdf(perguntas, materia, "Geral", tema)
    return FileResponse(caminho_pdf, filename="prova.pdf")
