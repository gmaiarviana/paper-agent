"""
Spike: Valida se Claude usa CognitiveModel naturalmente via prompt
Objetivo: Testar se leitura de estado é suficiente (sem tool)
"""
from anthropic import Anthropic
import os
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Simular cognitive_model atualizado pelo Observador
COGNITIVE_MODEL_EXAMPLE = {
    "claim": "LLMs aumentam produtividade de desenvolvedores Python",
    "proposicoes": [
        {
            "texto": "Existem equipes de desenvolvimento Python no mercado",
            "solidez": 0.85,
            "tipo": "fundamento"
        },
        {
            "texto": "LLMs podem gerar código automaticamente",
            "solidez": 0.70,
            "tipo": "fundamento"
        }
    ],
    "concepts_detected": ["LLMs", "Produtividade", "Python"],
    "contradictions": [
        "Usuário afirma que LLMs aumentam produtividade, mas também disse que código gerado precisa revisão extensa"
    ],
    "open_questions": [
        "Como medir produtividade objetivamente?",
        "Qual baseline de comparação?"
    ],
    "overall_solidez": 0.42,
    "overall_completude": 0.35
}

ORCHESTRATOR_PROMPT = """Você é o Orquestrador Socrático, responsável por guiar o desenvolvimento do argumento.

COGNITIVE MODEL DISPONÍVEL
O Observador analisou o diálogo e extraiu o seguinte modelo cognitivo:

Afirmação atual:
{claim}

Fundamentos identificados:
{proposicoes}

Conceitos detectados:
{concepts}

Contradições detectadas:
{contradictions}

Questões em aberto:
{open_questions}

Métricas:
- Solidez geral: {solidez:.2f} (quão bem fundamentada está a afirmação)
- Completude: {completude:.2f} (quanto do argumento foi desenvolvido)

CONTEXTO DA CONVERSA
Usuário disse: "Acho que LLMs realmente aumentam a produtividade. Equipes Python existem e LLMs geram código. Mas é verdade que o código precisa de muita revisão..."

SUA TAREFA
Analise o Cognitive Model e o contexto. Decida o próximo passo:
- explore: Fazer pergunta socrática para aprofundar
- suggest_agent: Chamar agente especializado
- clarify: Pedir clarificação de ambiguidade

Explique seu raciocínio e decisão.
"""


def test_natural_usage():
    """Testa se Claude usa cognitive_model naturalmente"""
    print("\n" + "="*60)
    print("TESTE: Claude Usa CognitiveModel Naturalmente?")
    print("="*60 + "\n")

    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Formatar prompt
    prompt = ORCHESTRATOR_PROMPT.format(
        claim=COGNITIVE_MODEL_EXAMPLE["claim"],
        proposicoes=json.dumps(COGNITIVE_MODEL_EXAMPLE["proposicoes"], indent=2, ensure_ascii=False),
        concepts=", ".join(COGNITIVE_MODEL_EXAMPLE["concepts_detected"]),
        contradictions="\n".join(f"- {c}" for c in COGNITIVE_MODEL_EXAMPLE["contradictions"]),
        open_questions="\n".join(f"- {q}" for q in COGNITIVE_MODEL_EXAMPLE["open_questions"]),
        solidez=COGNITIVE_MODEL_EXAMPLE["overall_solidez"],
        completude=COGNITIVE_MODEL_EXAMPLE["overall_completude"]
    )

    print("📤 Enviando prompt para Claude...\n")

    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    reasoning = response.content[0].text

    print("="*60)
    print("RESPOSTA DE CLAUDE")
    print("="*60 + "\n")
    print(reasoning)
    print("\n" + "="*60)

    # Análise
    print("\nANÁLISE\n")

    keywords = {
        "solidez": "solidez" in reasoning.lower() or "0.42" in reasoning,
        "completude": "completude" in reasoning.lower() or "0.35" in reasoning,
        "contradição": "contradi" in reasoning.lower(),
        "questões abertas": "questões" in reasoning.lower() or "questões em aberto" in reasoning.lower() or "open" in reasoning.lower(),
        "conceitos": any(c.lower() in reasoning.lower() for c in COGNITIVE_MODEL_EXAMPLE["concepts_detected"])
    }

    for key, found in keywords.items():
        status = "✅" if found else "❌"
        print(f"{status} Mencionou '{key}': {found}")

    usage_score = sum(keywords.values()) / len(keywords)

    print(f"\n📊 Score de uso: {usage_score:.0%}")

    if usage_score >= 0.6:
        print("\n✅ SUCESSO: Claude usa cognitive_model naturalmente")
        print("   Recomendação: Leitura de estado é SUFICIENTE")
        return True
    else:
        print("\n❌ FALHA: Claude ignora cognitive_model")
        print("   Recomendação: Considerar tool explícito")
        return False


if __name__ == "__main__":
    success = test_natural_usage()

    print("\n" + "="*60)
    if success:
        print("CONCLUSÃO: ✅ Proposta VIÁVEL")
    else:
        print("CONCLUSÃO: ❌ Proposta precisa AJUSTE")
    print("="*60 + "\n")

