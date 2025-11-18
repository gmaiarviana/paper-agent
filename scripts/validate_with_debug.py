"""
Validação do Épico 11 com logging DEBUG ativado.
"""
import sys
import logging
from pathlib import Path

# Configurar logging DEBUG ANTES de importar qualquer módulo
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s [%(name)s]: %(message)s',
    stream=sys.stdout
)

# Adicionar o diretório raiz ao PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 70)
print(" VALIDAÇÃO COM DEBUG LOGGING ATIVADO")
print("=" * 70)
print("\nLogs [MATURITY] mostrarão detalhes da detecção de maturidade via LLM\n")

# Importar após configurar logging
from agents.models.cognitive_model import CognitiveModel, SolidGround
from agents.persistence import detect_argument_maturity

if __name__ == "__main__":
    # Criar modelo de teste
    print("Criando modelo cognitivo de teste...")
    model_v1 = CognitiveModel(
        claim="LLMs aumentam produtividade",
        premises=["Reduzem tempo de tarefas repetitivas"],
        assumptions=["Usuários sabem usar LLMs"],
        open_questions=["Quanto aumenta exatamente?"],
    )

    print(f"Modelo criado: claim='{model_v1.claim}'")
    print("\nChamando detect_argument_maturity() com DEBUG ativado...\n")
    print("=" * 70)

    try:
        assessment = detect_argument_maturity(model_v1)

        print("=" * 70)
        print("\n✅ RESULTADO:")
        print(f"   Maduro: {assessment.is_mature}")
        print(f"   Confiança: {assessment.confidence:.2f}")
        print(f"   Justificativa: {assessment.justification}")
        if assessment.missing_elements:
            print(f"   Elementos faltando: {assessment.missing_elements}")

    except Exception as e:
        print("=" * 70)
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
