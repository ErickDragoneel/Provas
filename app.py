<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Banco de Provas Brasil - Gerador Oficial</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-[#f8fafc] min-h-screen">
<header class="bg-white border-b sticky top-0 z-50">
<div class="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
<div class="flex items-center gap-3"><div class="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white"><i class="fa-solid fa-book-open"></i></div><div><h1 class="font-black text-slate-800">BANCO DE PROVAS BRASIL</h1><p class="text-xs text-slate-500 -mt-1">Plataforma Oficial de Geração</p></div></div>
<div class="hidden md:flex gap-2 text-xs font-bold text-slate-500"><span class="bg-green-100 text-green-700 px-3 py-1 rounded-full"><i class="fa-solid fa-circle-check"></i> OFICIAL NO AR</span></div>
</div>
</header>

<main class="max-w-5xl mx-auto px-4 py-8">
<div class="bg-white rounded-[20px] shadow-sm border p-2 flex gap-2 mb-8">
<button onclick="setArea('Professor')" id="tabProfessor" class="tab-btn flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white"><i class="fa-solid fa-chalkboard-teacher mr-2"></i> PROFESSOR</button>
<button onclick="setArea('Aluno')" id="tabAluno" class="tab-btn flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500"><i class="fa-solid fa-graduation-cap mr-2"></i> ALUNO</button>
<button onclick="setArea('Concurso')" id="tabConcurso" class="tab-btn flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500"><i class="fa-solid fa-building-columns mr-2"></i> CONCURSO</button>
</div>

<div class="grid md:grid-cols-[1.2fr_0.8fr] gap-6">
<div class="bg-white rounded-[24px] shadow-sm border p-8">
<form action="/gerar-prova" method="post">
<input type="hidden" name="area" id="areaInput" value="Professor">

<div id="headerProfessor"><h2 class="text-2xl font-black text-slate-800">Área do Professor</h2><p class="text-sm text-slate-500 mb-6">Crie provas adaptadas e regulares em segundos</p></div>
<div id="headerAluno" class="hidden"><h2 class="text-2xl font-black text-slate-800">Área do Aluno</h2><p class="text-sm text-slate-500 mb-6">Treine no formato ENEM e vestibulares</p></div>
<div id="headerConcurso" class="hidden"><h2 class="text-2xl font-black text-slate-800">Área de Concursos</h2><p class="text-sm text-slate-500 mb-6">Gere questões no padrão da banca que quiser</p></div>

<label class="text-xs font-black text-slate-700 uppercase tracking-widest">Matéria</label>
<select name="materia" class="w-full mt-2 mb-5 px-4 py-3.5 rounded-xl border border-slate-200 bg-slate-50 font-bold">
<option>Matemática</option><option>Português</option><option>História</option><option>Geografia</option><option>Ciências</option><option>Biologia</option><option>Física</option><option>Química</option><option>Inglês</option><option>Redação</option>
</select>

<label class="text-xs font-black text-slate-700 uppercase tracking-widest">Tema / Conteúdo Específico</label>
<input name="tema" required placeholder="Ex: Análise combinatória, Crase, Revolução Industrial..." class="w-full mt-2 mb-5 px-4 py-3.5 rounded-xl border border-slate-200 bg-slate-50 font-bold placeholder:font-normal">

<div class="grid grid-cols-2 gap-4 mb-5">
<div><label class="text-xs font-black text-slate-700 uppercase tracking-widest">Qtd. Questões</label><select name="quantidade" class="w-full mt-2 px-4 py-3.5 rounded-xl border border-slate-200 bg-slate-50 font-bold"><option value="5">5</option><option value="10" selected>10</option><option value="15">15</option><option value="20">20</option></select></div>
<div><label class="text-xs font-black text-slate-700 uppercase tracking-widest">Dificuldade</label><select class="w-full mt-2 px-4 py-3.5 rounded-xl border border-slate-200 bg-slate-50 font-bold"><option>Fácil</option><option selected>Médio</option><option>Difícil</option></select></div>
</div>

<div id="boxProfessor" class="">
<div class="bg-blue-50 border border-blue-100 rounded-xl p-4 mb-2"><label class="text-xs font-black text-blue-700 uppercase">Tipo de Prova</label><select name="tipo" class="w-full mt-2 px-3 py-3 rounded-lg border bg-white font-bold text-sm"><option value="normal">Prova Regular - Padrão Escola</option><option value="adaptada">Prova Adaptada - TDAH / Dislexia / Autismo (Fonte maior, espaçada)</option></select></div>
</div>

<div id="boxAluno" class="hidden">
<div class="bg-emerald-50 border border-emerald-100 rounded-xl p-4 mb-2"><label class="text-xs font-black text-emerald-700 uppercase">Formato do Aluno</label><select name="tipo" class="w-full mt-2 px-3 py-3 rounded-lg border bg-white font-bold text-sm"><option value="enem">ENEM - Texto base + 5 alternativas</option><option value="vestibular">Vestibular Tradicional</option><option value="revisao">Revisão Rápida com Gabarito Explicado</option></select></div>
</div>

<div id="boxConcurso" class="hidden">
<div class="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-2"><label class="text-xs font-black text-amber-800 uppercase"><i class="fa-solid fa-pen-to-square"></i> Digite a Banca (Campo Aberto)</label><input name="banca" id="bancaInput" placeholder="Digite: CESPE / Cebraspe, FGV, FCC, VUNESP, IBFC, AOCP..." class="w-full mt-2 px-4 py-3.5 rounded-xl border-2 border-amber-200 bg-white font-black placeholder:font-bold"><p class="text-[11px] text-amber-800 mt-2 font-bold">✓ Sistema aberto: você digita qualquer banca. O IA gera no padrão exato da banca.</p></div>
</div>

<button type="submit" class="w-full mt-6 bg-slate-900 hover:bg-black text-white py-4 rounded-xl font-black tracking-widest transition"><i class="fa-solid fa-bolt mr-2"></i> GERAR PROVA EM PDF - OFICIAL</button>
<p class="text-center text-[11px] text-slate-400 mt-3 font-bold">PDF profissional pronto para impressão • Cabeçalho com nome, turma e nota</p>
</form>
</div>

<div class="space-y-4">
<div class="bg-slate-900 text-white rounded-[24px] p-6"><h3 class="font-black"><i class="fa-solid fa-shield-check text-green-400"></i> No Ar</h3><p class="text-sm text-slate-300 mt-2">Domínio oficial: <b>bancodeprovasbrasil.com.br</b> configurado. Interface profissional validada.</p><div class="mt-4 grid grid-cols-3 text-center text-[10px] font-black"><div class="bg-white/10 p-3 rounded-xl">PROFESSOR<br>ADAPTADA</div><div class="bg-white/10 p-3 rounded-xl">ALUNO<br>ENEM</div><div class="bg-white/10 p-3 rounded-xl">BANCA<br>ABERTA</div></div></div>
<div class="bg-white rounded-[24px] border p-6"><h4 class="font-black text-sm">O que vai gerar:</h4><ul class="text-sm text-slate-600 mt-3 space-y-2"><li><i class="fa-solid fa-check text-green-500"></i> 10 questões inéditas com 4 alternativas</li><li><i class="fa-solid fa-check text-green-500"></i> Gabarito separado na última página</li><li><i class="fa-solid fa-check text-green-500"></i> Padrão da banca que você digitou</li><li><i class="fa-solid fa-check text-green-500"></i> PDF pronto A4</li></ul></div>
</div>
</div>
</main>
<script>
function setArea(a){
document.getElementById('areaInput').value=a;
['Professor','Aluno','Concurso'].forEach(x=>{
document.getElementById('tab'+x).className = x===a ? 'tab-btn flex-1 py-3.5 rounded-xl font-black text-sm bg-slate-900 text-white' : 'tab-btn flex-1 py-3.5 rounded-xl font-black text-sm text-slate-500';
document.getElementById('header'+x).classList.toggle('hidden', x!==a);
document.getElementById('box'+x).classList.toggle('hidden', x!==a);
});
}
</script>
</body>
</html>
