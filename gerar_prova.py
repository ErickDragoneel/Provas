import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BANCO_PATH = "banco_perguntas.json"

def gerar_questoes_com_ia(materia: str, nivel: str, tema: str, dificuldade: str, quantidade: int = 5):
    """
    Gera questões no padrão ENEM e salva no banco_perguntas.json
    """
    prompt = f"""
    Você é um elaborador de questões do INEP/ENEM, especialista em {materia}.
    
    TAREFA: Crie {quantidade} questões INÉDITAS sobre:
    - Matéria: {materia}
    - Série: {nivel}
    - Tema específico: {tema}
    - Dificuldade: {dificuldade}

    REGRAS OBRIGATÓRIAS - SIGA 100%:
    1. Cada questão DEVE ter um TEXTO BASE (mínimo 3 linhas) com contexto real: notícia, gráfico, experimento, situação do cotidiano.
    2. Enunciado interpretativo. PROIBIDO questões de cálculo direto tipo "quanto é 2+2".
    3. 4 alternativas (A, B, C, D), todas plausíveis. Apenas uma correta.
    4. Ao final de cada questão, em linha separada, coloque: GABARITO: X
    5. No final de tudo, crie uma seção GABARITO GERAL listando todas.
    6. Linguagem acessível para aluno de escola pública.

    FORMATO DE SAÍDA:
    TEXTO BASE 1: [seu texto aqui]
    QUESTÃO 1: [enunciado]
    A) ...
    B) ...
    C) ...
    D) ...
    GABARITO: C

    (repita até {quantidade})

    GABARITO GERAL: 1-C, 2-A, 3-D...
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um professor criativo e rigoroso do ENEM."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )

        conteudo = response.choices[0].message.content
        
        # Separa prova e gabarito
        prova_texto = conteudo
        gabarito_texto = "Ver no final do texto"
        if "GABARITO GERAL" in conteudo:
            partes = conteudo.split("GABARITO GERAL")
            prova_texto = partes[0]
            gabarito_texto = partes[1]

        # Salva no banco
        salvar_no_banco(materia, nivel, tema, dificuldade, conteudo)

        return {
            "prova": prova_texto.strip(),
            "gabarito": gabarito_texto.strip(),
            "conteudo_completo": conteudo
        }

    except Exception as e:
        return {"erro": str(e), "prova": "", "gabarito": ""}

def salvar_no_banco(materia, nivel, tema, dificuldade, conteudo):
    """Salva cada geração no banco_perguntas.json"""
    novo_registro = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "materia": materia,
        "nivel": nivel,
        "tema": tema,
        "dificuldade": dificuldade,
        "conteudo": conteudo
    }
    
    try:
        if os.path.exists(BANCO_PATH):
            with open(BANCO_PATH, "r", encoding="utf-8") as f:
                banco = json.load(f)
        else:
            banco = []
        
        banco.append(novo_registro)
        
        with open(BANCO_PATH, "w", encoding="utf-8") as f:
            json.dump(banco, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

# Teste direto: python gerar_prova.py
if __name__ == "__main__":
    print("Testando IA...")
    resultado = gerar_questoes_com_ia("matematica", "3 ano", "função quadrática", "media", 2)
    
    if "erro" in resultado and resultado["erro"]:
        print(f"ERRO: {resultado['erro']}")
    else:
        print("--- PROVA GERADA ---")
        print(resultado["prova"])
        print("--- GABARITO ---")
        print(resultado["gabarito"])