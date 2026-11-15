import os
import json

def gerar_perguntas(materia, tema, quantidade, tipo):
    # Versão de teste sem precisar de chave ainda
    perguntas = []
    for i in range(int(quantidade)):
        perguntas.append({
            "pergunta": f"[{materia} - {tema}] Pergunta exemplo {i+1} sobre {tema} ({tipo})?",
            "alternativas": ["A) Alternativa 1", "B) Alternativa 2", "C) Alternativa 3", "D) Alternativa 4"],
            "correta": "A"
        })
    return perguntas
