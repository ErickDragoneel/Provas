import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_perguntas(materia, tema, quantidade=10, tipo="multipla escolha"):
    prompt = f"Crie {quantidade} questoes de {tipo} sobre {materia}, tema: {tema}. Para ensino medio. Retorne em JSON."
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        import json
        data = json.loads(resp.choices[0].message.content)
        return data.get("perguntas", data.get("questoes", [])) if isinstance(data, dict) else data
    except Exception as e:
        print(f"Erro OpenAI, usando mock: {e}")
        return [
            {
                "pergunta": f"Exemplo {i+1} sobre {tema} em {materia}?",
                "alternativas": ["A) Opcao 1", "B) Opcao 2", "C) Opcao 3", "D) Opcao 4"],
                "resposta": "A",
                "explicacao": "Exemplo"
            } for i in range(quantidade)
        ]
