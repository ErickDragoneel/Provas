import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAIsk-proj-gpLZBNtSTCR9bGhBFtBJs_6_aC9q0VBzTdGtwRfevsWvfp21yBfQO_-gwJIFw1kUmJQHpuPyyAT3BlbkFJPecl-s-MJMi5qrM6WwlW--5YPLjYr4i1hcomz4lFeVN7l-5rWo2GiwHmj8tRONml02yTdZ8ccA_API_KEY"))

def gerar_perguntas_ia(materia, nivel, tema, dificuldade, quantidade):
    try:
        prompt = f"""
Crie {quantidade} questões de {materia} para nível {nivel}.

Tema: {tema}
Dificuldade: {dificuldade}

Formato:
1. Pergunta
A) ...
B) ...
C) ...
D) ...

Resposta correta: A/B/C/D
"""

        resposta = client.responses.create(
            model="gpt-4o-mini",
            input=f"Você é um professor especialista.\n{prompt}",
            temperature=0.7
        )

        texto = resposta.output[0].content[0].text

        linhas = texto.split("\n")
        gabarito = []
        perguntas = []

        for linha in linhas:
            if "Resposta correta" in linha:
                letra = linha.split(":")[-1].strip()
                gabarito.append(letra)
            else:
                perguntas.append(linha)

        return "\n".join(perguntas), gabarito

    except Exception as e:
        return f"Erro: {str(e)}", []