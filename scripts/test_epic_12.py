"""
Script de teste para validar funcionalidades do Épico 12.

Este script testa:
- Criação de ideias
- Criação de argumentos versionados
- Busca e listagem de ideias
- Filtros por status e título
- Alternância entre ideias

Uso:
    python scripts/test_epic_12.py
"""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.database.manager import get_database_manager
from agents.models.cognitive_model import CognitiveModel


def test_create_ideas():
    """Testa criação de ideias no database."""
    print("\n=== Teste 1: Criar Ideias ===")

    db = get_database_manager()

    # Criar 3 ideias de teste
    idea1_id = db.create_idea("LLMs em produtividade", "exploring")
    print(f"✅ Ideia 1 criada: {idea1_id}")

    idea2_id = db.create_idea("Semana de 4 dias", "structured")
    print(f"✅ Ideia 2 criada: {idea2_id}")

    idea3_id = db.create_idea("Drones em obras", "validated")
    print(f"✅ Ideia 3 criada: {idea3_id}")

    return [idea1_id, idea2_id, idea3_id]


def test_create_arguments(idea_ids):
    """Testa criação de argumentos versionados."""
    print("\n=== Teste 2: Criar Argumentos Versionados ===")

    db = get_database_manager()

    # Criar argumentos para ideia 1 (3 versões)
    for i in range(1, 4):
        model = CognitiveModel(
            claim=f"LLMs aumentam produtividade em {i*10}%",
            premises=[f"Premissa {i}", f"Premissa {i+1}"],
            assumptions=[f"Suposição {i}"],
            open_questions=[f"Pergunta {i}?"],
            contradictions=[],
            solid_grounds=[],
            context={"version": i}
        )
        arg_id = db.create_argument(idea_ids[0], model)
        print(f"✅ Argumento V{i} criado para ideia 1: {arg_id}")

    # Criar argumentos para ideia 2 (2 versões)
    for i in range(1, 3):
        model = CognitiveModel(
            claim=f"Semana de 4 dias reduz turnover em {i*20}%",
            premises=[f"Estudo {i}", f"Empresa X implementou"],
            assumptions=[],
            open_questions=[],
            contradictions=[],
            solid_grounds=[],
            context={}
        )
        arg_id = db.create_argument(idea_ids[1], model)
        print(f"✅ Argumento V{i} criado para ideia 2: {arg_id}")

    # Criar argumento para ideia 3 (1 versão)
    model = CognitiveModel(
        claim="Drones podem medir volumes com precisão < 2%",
        premises=["Tecnologia LiDAR", "Validação em campo"],
        assumptions=["Condições climáticas favoráveis"],
        open_questions=["Custo viável?"],
        contradictions=[],
        solid_grounds=[],
        context={}
    )
    arg_id = db.create_argument(idea_ids[2], model)
    print(f"✅ Argumento V1 criado para ideia 3: {arg_id}")


def test_set_focal_arguments(idea_ids):
    """Testa configuração de argumento focal."""
    print("\n=== Teste 3: Configurar Argumento Focal ===")

    db = get_database_manager()

    # Para ideia 1, definir V3 como focal
    args_idea1 = db.get_arguments_by_idea(idea_ids[0])
    focal_arg = args_idea1[0]  # V3 (mais recente)
    db.update_idea_current_argument(idea_ids[0], focal_arg["id"])
    print(f"✅ Argumento focal da ideia 1: V{focal_arg['version']}")

    # Para ideia 2, definir V2 como focal
    args_idea2 = db.get_arguments_by_idea(idea_ids[1])
    focal_arg = args_idea2[0]  # V2 (mais recente)
    db.update_idea_current_argument(idea_ids[1], focal_arg["id"])
    print(f"✅ Argumento focal da ideia 2: V{focal_arg['version']}")

    # Para ideia 3, definir V1 como focal
    args_idea3 = db.get_arguments_by_idea(idea_ids[2])
    focal_arg = args_idea3[0]  # V1 (único)
    db.update_idea_current_argument(idea_ids[2], focal_arg["id"])
    print(f"✅ Argumento focal da ideia 3: V{focal_arg['version']}")


def test_list_ideas():
    """Testa listagem de ideias."""
    print("\n=== Teste 4: Listar Ideias ===")

    db = get_database_manager()

    # Listar todas
    all_ideas = db.list_ideas(limit=10)
    print(f"✅ Total de ideias: {len(all_ideas)}")

    for idea in all_ideas:
        print(f"   - {idea['title']} ({idea['status']})")

    # Listar apenas exploring
    exploring = db.list_ideas(status="exploring", limit=10)
    print(f"✅ Ideias 'exploring': {len(exploring)}")

    # Listar apenas structured
    structured = db.list_ideas(status="structured", limit=10)
    print(f"✅ Ideias 'structured': {len(structured)}")

    # Listar apenas validated
    validated = db.list_ideas(status="validated", limit=10)
    print(f"✅ Ideias 'validated': {len(validated)}")


def test_search_ideas():
    """Testa busca de ideias por título."""
    print("\n=== Teste 5: Buscar Ideias por Título ===")

    db = get_database_manager()

    # Buscar todas
    all_ideas = db.list_ideas(limit=10)

    # Filtrar por "LLMs" (case-insensitive)
    search_term = "llms"
    filtered = [
        idea for idea in all_ideas
        if search_term.lower() in idea["title"].lower()
    ]
    print(f"✅ Busca por '{search_term}': {len(filtered)} resultado(s)")
    for idea in filtered:
        print(f"   - {idea['title']}")

    # Filtrar por "semana"
    search_term = "semana"
    filtered = [
        idea for idea in all_ideas
        if search_term.lower() in idea["title"].lower()
    ]
    print(f"✅ Busca por '{search_term}': {len(filtered)} resultado(s)")
    for idea in filtered:
        print(f"   - {idea['title']}")


def test_get_idea_with_arguments():
    """Testa carregamento de ideia com argumentos."""
    print("\n=== Teste 6: Carregar Ideia com Argumentos ===")

    db = get_database_manager()

    # Pegar primeira ideia
    ideas = db.list_ideas(limit=1)
    if not ideas:
        print("❌ Nenhuma ideia encontrada")
        return

    idea = ideas[0]
    print(f"✅ Ideia: {idea['title']}")
    print(f"   Status: {idea['status']}")
    print(f"   Criada em: {idea['created_at']}")
    print(f"   Atualizada em: {idea['updated_at']}")

    # Carregar argumentos
    arguments = db.get_arguments_by_idea(idea["id"])
    print(f"✅ Argumentos: {len(arguments)} versão(ões)")

    for arg in arguments:
        focal = " [FOCAL]" if arg["id"] == idea["current_argument_id"] else ""
        print(f"   - V{arg['version']}{focal}: {arg['claim'][:50]}...")


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("TESTE DO ÉPICO 12: GESTÃO DE IDEIAS")
    print("=" * 60)

    try:
        # Criar ideias
        idea_ids = test_create_ideas()

        # Criar argumentos
        test_create_arguments(idea_ids)

        # Configurar focais
        test_set_focal_arguments(idea_ids)

        # Listar ideias
        test_list_ideas()

        # Buscar ideias
        test_search_ideas()

        # Carregar com argumentos
        test_get_idea_with_arguments()

        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("=" * 60)

        print("\n💡 Próximo passo: Executar a interface web")
        print("   cd /home/user/paper-agent")
        print("   streamlit run app/chat.py")

    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
