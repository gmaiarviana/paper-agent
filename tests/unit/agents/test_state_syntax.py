"""
Script de validação de sintaxe para MultiAgentState (Épico 7, Task 7.1.5).

Valida a estrutura do arquivo state.py sem importar as dependências.
Útil para ambientes sem venv configurado.

"""

import sys
import ast
from pathlib import Path

# Caminho do arquivo state.py
STATE_FILE = Path(__file__).parent.parent.parent / "agents" / "orchestrator" / "state.py"

def validate_state_syntax():
    """Valida sintaxe e estrutura do arquivo state.py."""
    print("=" * 70)
    print("VALIDAÇÃO DE SINTAXE DO MULTIAGENTSTATE (ÉPICO 7, TASK 7.1.5)")
    print("=" * 70)

    # Ler arquivo
    print(f"\n1. Lendo arquivo: {STATE_FILE}")
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    print("   ✅ Arquivo lido com sucesso")

    # Parsear AST
    print("\n2. Parseando AST do arquivo...")
    try:
        tree = ast.parse(content)
        print("   ✅ Sintaxe Python válida")
    except SyntaxError as e:
        print(f"   ❌ Erro de sintaxe: {e}")
        sys.exit(1)

    # Encontrar classe MultiAgentState
    print("\n3. Buscando classe MultiAgentState...")
    multi_agent_state_class = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "MultiAgentState":
            multi_agent_state_class = node
            break

    assert multi_agent_state_class is not None, "Classe MultiAgentState não encontrada"
    print("   ✅ Classe MultiAgentState encontrada")

    # Extrair anotações de campos
    print("\n4. Extraindo anotações de campos...")
    field_annotations = {}
    for node in multi_agent_state_class.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            field_name = node.target.id
            field_annotations[field_name] = ast.unparse(node.annotation)

    print(f"   ✅ {len(field_annotations)} campos encontrados")

    # Validar novos campos (Épico 7)
    print("\n5. Validando NOVOS campos do Orquestrador (Épico 7)...")
    new_fields = {
        "orchestrator_analysis": "Optional[str]",
        "next_step": 'Optional[Literal["explore", "suggest_agent", "clarify"]]',
        "agent_suggestion": "Optional[dict]"
    }

    for field, expected_type in new_fields.items():
        assert field in field_annotations, f"Campo '{field}' não encontrado"
        print(f"   ✅ Campo '{field}' presente ({field_annotations[field]})")

    # Validar remoção de campos obsoletos
    print("\n6. Validando REMOÇÃO de campos obsoletos...")
    obsolete_fields = ["orchestrator_classification", "orchestrator_reasoning"]

    for field in obsolete_fields:
        assert field not in field_annotations, f"Campo obsoleto '{field}' ainda existe"
        print(f"   ✅ Campo obsoleto '{field}' foi removido")

    # Validar campos compartilhados
    print("\n7. Validando campos compartilhados...")
    shared_fields = [
        "user_input",
        "session_id",
        "conversation_history",
        "current_stage",
        "hypothesis_versions"
    ]

    for field in shared_fields:
        assert field in field_annotations, f"Campo compartilhado '{field}' não encontrado"
        print(f"   ✅ Campo compartilhado '{field}' presente")

    # Validar campos de outros agentes
    print("\n8. Validando campos de outros agentes...")
    other_fields = [
        "structurer_output",
        "methodologist_output",
        "messages"
    ]

    for field in other_fields:
        assert field in field_annotations, f"Campo '{field}' não encontrado"
        print(f"   ✅ Campo '{field}' presente")

    # Encontrar função create_initial_multi_agent_state
    print("\n9. Validando função create_initial_multi_agent_state...")
    create_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "create_initial_multi_agent_state":
            create_func = node
            break

    assert create_func is not None, "Função create_initial_multi_agent_state não encontrada"
    print("   ✅ Função create_initial_multi_agent_state encontrada")

    # Validar que função retorna os novos campos
    print("\n10. Validando inicialização dos campos na função...")
    func_body = ast.unparse(create_func)

    # Novos campos devem estar sendo inicializados
    for field in new_fields.keys():
        assert field in func_body, f"Campo '{field}' não está sendo inicializado na função"
        print(f"   ✅ Campo '{field}' está sendo inicializado")

    # Campos obsoletos NÃO devem estar sendo inicializados
    for field in obsolete_fields:
        assert field not in func_body, f"Campo obsoleto '{field}' ainda está sendo inicializado"
        print(f"   ✅ Campo obsoleto '{field}' NÃO está sendo inicializado")

    # Validar versão atualizada
    print("\n11. Validando atualização de versão...")
    assert "2.1" in content, "Versão não foi atualizada para 2.1"
    assert "Épico 7" in content, "Referência ao Épico 7 não encontrada"
    assert "Task 7.1.5" in content, "Referência à Task 7.1.5 não encontrada"
    print("   ✅ Versão atualizada para 2.1 (Épico 7, Task 7.1.5)")

    # Exibir estrutura final
    print("\n12. Estrutura final dos campos:")
    print("\n    CAMPOS DO ORQUESTRADOR (ÉPICO 7):")
    for field in new_fields.keys():
        print(f"      - {field}: {field_annotations[field]}")

    print("\n    CAMPOS COMPARTILHADOS:")
    for field in shared_fields:
        print(f"      - {field}: {field_annotations[field]}")

    print("\n    CAMPOS DE OUTROS AGENTES:")
    for field in other_fields:
        print(f"      - {field}: {field_annotations[field]}")

    print("\n" + "=" * 70)
    print("VALIDAÇÃO DE SINTAXE CONCLUÍDA COM SUCESSO! ✅")
    print("=" * 70)
    print("\n📝 RESUMO DAS MUDANÇAS (TASK 7.1.5):")
    print("   ✅ Adicionados: orchestrator_analysis, next_step, agent_suggestion")
    print("   ✅ Removidos: orchestrator_classification, orchestrator_reasoning")
    print("   ✅ Versão atualizada: 2.1 (Épico 7, Task 7.1.5)")
    print("   ✅ Estado pronto para Orquestrador Conversacional (Épico 7 POC)")
    print("=" * 70)

if __name__ == "__main__":
    try:
        validate_state_syntax()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
