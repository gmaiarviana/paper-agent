"""
Script de validação manual para a tool ask_user.

Valida que a tool foi implementada corretamente com:
- Decorator @tool
- Type hints
- Docstring
- Imports corretos

Versão: 1.0
Data: 08/11/2025
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT_STR = str(PROJECT_ROOT)
if PROJECT_ROOT_STR not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_STR)

from scripts.common import setup_project_path

setup_project_path()

from agents.methodologist.tools import ask_user
from langchain_core.tools import BaseTool


def validate_ask_user_tool():
    """Valida a implementação da tool ask_user."""

    print("=" * 70)
    print("VALIDAÇÃO DA TOOL ask_user")
    print("=" * 70)

    # Teste 1: Verificar que ask_user é uma tool do LangChain
    print("\n1. Verificando se ask_user é uma LangChain Tool...")
    assert isinstance(ask_user, BaseTool), "ask_user não é uma BaseTool do LangChain"
    print("   ✅ ask_user é uma LangChain Tool")

    # Teste 2: Verificar nome da tool
    print("\n2. Verificando nome da tool...")
    assert ask_user.name == "ask_user", f"Nome incorreto: {ask_user.name}"
    print(f"   ✅ Nome correto: {ask_user.name}")

    # Teste 3: Verificar descrição
    print("\n3. Verificando descrição da tool...")
    assert ask_user.description is not None, "Tool não tem descrição"
    assert len(ask_user.description) > 50, "Descrição muito curta"
    print(f"   ✅ Descrição presente ({len(ask_user.description)} caracteres)")
    print(f"   Descrição: {ask_user.description[:100]}...")

    # Teste 4: Verificar type hints
    print("\n4. Verificando type hints...")
    annotations = ask_user.func.__annotations__
    assert 'question' in annotations, "Parâmetro 'question' sem type hint"
    assert annotations['question'] == str, "Type hint de 'question' incorreto"
    assert 'return' in annotations, "Return sem type hint"
    assert annotations['return'] == str, "Type hint de return incorreto"
    print(f"   ✅ Type hints corretos: question: {annotations['question'].__name__}, return: {annotations['return'].__name__}")

    # Teste 5: Verificar docstring
    print("\n5. Verificando docstring...")
    docstring = ask_user.func.__doc__
    assert docstring is not None, "Função sem docstring"
    assert len(docstring) > 100, "Docstring muito curta"
    assert "Args:" in docstring, "Docstring sem seção Args"
    assert "Returns:" in docstring, "Docstring sem seção Returns"
    assert "Example:" in docstring, "Docstring sem seção Example"
    print(f"   ✅ Docstring completa ({len(docstring)} caracteres)")
    print(f"   - Contém 'Args': ✅")
    print(f"   - Contém 'Returns': ✅")
    print(f"   - Contém 'Example': ✅")
    print(f"   - Contém 'interrupt': {'✅' if 'interrupt' in docstring else '❌'}")

    # Teste 6: Verificar args schema
    print("\n6. Verificando args schema...")
    assert ask_user.args_schema is not None, "Tool sem args_schema"
    print(f"   ✅ Args schema presente: {ask_user.args_schema}")

    # Teste 7: Verificar estrutura do código fonte
    print("\n7. Verificando estrutura do código fonte...")
    import inspect
    source = inspect.getsource(ask_user.func)
    assert "interrupt" in source, "Código não usa interrupt()"
    assert "logger" in source, "Código não usa logger"
    print("   ✅ Código usa interrupt()")
    print("   ✅ Código usa logger")

    # Teste 8: Verificar que tool pode ser invocada (simulação)
    print("\n8. Verificando que tool pode ser invocada...")
    try:
        # Verificar schema de input
        input_schema = ask_user.get_input_schema()
        print(f"   ✅ Input schema válido: {input_schema.schema()}")
    except Exception as e:
        print(f"   ❌ Erro ao obter input schema: {e}")
        raise

    print("\n" + "=" * 70)
    print("TODOS OS TESTES PASSARAM! ✅")
    print("=" * 70)
    print("\nResumo:")
    print("- Tool implementada com decorator @tool")
    print("- Type hints corretos (question: str) -> str")
    print("- Docstring completa com Args, Returns e Example")
    print("- Usa interrupt() do LangGraph")
    print("- Usa logger para registrar pergunta e resposta")
    print("\nA tool ask_user está pronta para uso! 🎉")


if __name__ == "__main__":
    try:
        validate_ask_user_tool()
    except AssertionError as e:
        print(f"\n❌ ERRO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
