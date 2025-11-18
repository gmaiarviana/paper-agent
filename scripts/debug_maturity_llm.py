"""
Script para debugar resposta do LLM especificamente na detecção de maturidade.
"""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from agents.models.cognitive_model import CognitiveModel
from agents.persistence import detect_argument_maturity  # Usar mesma função que validação
from agents.persistence.snapshot_manager import MATURITY_DETECTION_PROMPT, SnapshotManager
from utils.config import create_anthropic_client
from langchain_core.messages import HumanMessage

def test_maturity_detection():
    """Testa detecção de maturidade com LLM."""
    print("=" * 70)
    print(" DEBUG: Testando Detecção de Maturidade com LLM")
    print("=" * 70)

    # Criar modelo cognitivo de teste (imaturo)
    model_v1 = CognitiveModel(
        claim="LLMs aumentam produtividade",
        premises=["Reduzem tempo de tarefas repetitivas"],
        assumptions=["Usuários sabem usar LLMs"],
        open_questions=["Quanto aumenta exatamente?"],
    )

    print("\n📊 Modelo Cognitivo V1 (imaturo):")
    print(f"   Claim: {model_v1.claim}")
    print(f"   Premises: {len(model_v1.premises)}")
    print(f"   Assumptions: {len(model_v1.assumptions)}")
    print(f"   Open questions: {len(model_v1.open_questions)}")

    # Preparar dados para LLM
    model_dict = model_v1.to_dict()
    model_json = json.dumps(model_dict, indent=2, ensure_ascii=False)

    print("\n📝 JSON enviado ao LLM:")
    print(model_json[:200] + "..." if len(model_json) > 200 else model_json)

    # Preparar prompt
    prompt = MATURITY_DETECTION_PROMPT.format(cognitive_model_json=model_json)

    print(f"\n📏 Tamanho do prompt: {len(prompt)} caracteres")
    print("\n📝 Prompt (primeiros 500 chars):")
    print(prompt[:500] + "...")

    # Criar cliente LLM
    llm = create_anthropic_client("claude-3-5-haiku-20241022")
    print("\n✅ Cliente LLM criado")

    # Invocar LLM
    try:
        print("\n📞 Invocando LLM...")
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])

        print(f"\n✅ Resposta recebida (tipo: {type(response.content)})")
        print(f"📏 Tamanho da resposta: {len(response.content)} caracteres")
        print("\n📝 Resposta completa:")
        print("=" * 70)
        print(response.content)
        print("=" * 70)

        # Tentar parsear JSON
        response_text = response.content.strip()

        print(f"\n🔍 Resposta após strip: '{response_text[:100]}...'")
        print(f"   Começa com '```': {response_text.startswith('```')}")
        print(f"   Começa com '{{': {response_text.startswith('{')}")

        # Remover markdown code blocks se presentes
        if response_text.startswith("```"):
            print("   → Removendo markdown code block")
            lines = response_text.split("\n")
            response_text = "\n".join(lines[1:-1])
            print(f"   → Após remoção: '{response_text[:100]}...'")

        print("\n🔧 Tentando parsear JSON...")
        assessment_dict = json.loads(response_text)
        print("✅ JSON parseado com sucesso!")
        print(json.dumps(assessment_dict, indent=2, ensure_ascii=False))

    except json.JSONDecodeError as e:
        print(f"\n❌ Erro ao parsear JSON: {e}")
        print(f"   Posição do erro: linha {e.lineno}, coluna {e.colno}")
        print(f"   Mensagem: {e.msg}")
        print(f"\n📝 Texto que tentou parsear:")
        print("=" * 70)
        print(repr(response_text))
        print("=" * 70)
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n" + "=" * 70)
    print("✅ TESTE PASSOU!")
    print("=" * 70)
    return True

def test_via_helper():
    """Testa usando a mesma função helper que o validate_cognitive_model.py usa."""
    print("\n" + "=" * 70)
    print(" TESTE 2: Usando função helper detect_argument_maturity()")
    print("=" * 70)

    # Criar modelo cognitivo de teste (imaturo)
    model_v1 = CognitiveModel(
        claim="LLMs aumentam produtividade",
        premises=["Reduzem tempo de tarefas repetitivas"],
        assumptions=["Usuários sabem usar LLMs"],
        open_questions=["Quanto aumenta exatamente?"],
    )

    print("\n📊 Modelo Cognitivo V1 (imaturo):")
    print(f"   Claim: {model_v1.claim}")
    print(f"   Premises: {len(model_v1.premises)}")

    print("\n📞 Chamando detect_argument_maturity()...")
    try:
        assessment = detect_argument_maturity(model_v1)
        print(f"✅ Avaliação recebida:")
        print(f"   Maduro: {assessment.is_mature}")
        print(f"   Confiança: {assessment.confidence:.2f}")
        print(f"   Justificativa: {assessment.justification[:100]}...")
        if assessment.missing_elements:
            print(f"   Elementos faltando: {', '.join(assessment.missing_elements)}")

        print("\n" + "=" * 70)
        print("✅ TESTE PASSOU! LLM funcionando via helper")
        print("=" * 70)
        return True
    except Exception as e:
        print(f"\n❌ Erro ao chamar helper: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("EXECUTANDO DOIS TESTES:\n")
    print("1. Teste direto com LLM (para ver resposta completa)")
    print("2. Teste via helper detect_argument_maturity() (mesmo que validação usa)")

    success1 = test_maturity_detection()
    success2 = test_via_helper()

    sys.exit(0 if (success1 and success2) else 1)
