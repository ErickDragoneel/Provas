from gerador_perguntas import gerar_perguntas
import json
import os

CAMINHO_BANCO = "banco_perguntas.json"

def montar_prova(materia, tema, quantidade, tipo):
    perguntas = gerar_perguntas(materia, tema, quantidade, tipo)
    
    banco = []
    if os.path.exists(CAMINHO_BANCO):
        try:
            with open(CAMINHO_BANCO, "r", encoding="utf-8") as f:
                banco = json.load(f)
        except:
            banco = []
    
    banco.extend(perguntas)
    with open(CAMINHO_BANCO, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
    
    return perguntas
