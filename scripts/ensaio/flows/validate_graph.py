"""
Script de validação manual do grafo do Ensaio (E-POC-1.3).

Valida, SEM chamar a API real da Anthropic:
- product_config.load_product_context() devolve string não-vazia
- create_ensaio_graph() compila um grafo LangGraph com os nós esperados
- writer_node aceita o contrato declarado e devolve dict com chave `article`
  (LLM mockado, para não incorrer em custo)

Para validação que usa API real (smoke test de conversa + geração de artigo),
consultar scripts separados no futuro - fora do escopo desta validação rápida.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

# Garantir que a raiz do projeto está no PYTHONPATH
_project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))


def _validate_product_context() -> None:
    from products.ensaio.app.product_config import load_product_context

    ctx = load_product_context()
    assert isinstance(ctx, str) and ctx.strip(), "product_context vazio"
    assert "pesquisador" in ctx.lower(), "product_context não menciona pesquisador"
    assert "imrad" in ctx.lower(), "product_context não menciona IMRaD"
    print(f"  product_context carregado ({len(ctx)} chars)")


def _validate_graph_compiles() -> None:
    from products.ensaio.app.graph import create_ensaio_graph

    graph = create_ensaio_graph()
    node_names = set(graph.get_graph().nodes.keys())
    assert "orchestrator" in node_names, f"nó 'orchestrator' ausente: {node_names}"
    assert "structurer" in node_names, f"nó 'structurer' ausente: {node_names}"
    # Writer NÃO deve estar no grafo conversacional da POC.
    assert "writer" not in node_names, (
        "Writer não deveria estar no grafo conversacional nesta POC"
    )
    assert "methodologist" not in node_names, (
        "Methodologist fora do escopo da POC, não deveria estar no grafo"
    )
    print(f"  grafo compilado com nós: {sorted(node_names)}")


def _validate_writer_contract() -> None:
    from langchain_core.messages import AIMessage, HumanMessage

    from core.agents.writer import writer_node

    fake_response = AIMessage(content="# Artigo\n\nMarkdown válido gerado pelo mock.")

    class _FakeLLM:
        def invoke(self, _messages):
            return fake_response

    with patch(
        "core.agents.writer.nodes.create_anthropic_client", return_value=_FakeLLM()
    ):
        result = writer_node(
            {
                "messages": [HumanMessage(content="Observei X.")],
                "focal_argument": None,
                "previous_article": None,
                "product_context": None,
            }
        )

    assert isinstance(result, dict), "writer_node deve retornar dict"
    assert "article" in result, "writer_node deve retornar chave 'article'"
    assert result["article"].startswith("#"), (
        "Writer deve retornar markdown (começando com título #)"
    )
    print(f"  writer_node contrato OK ({len(result['article'])} chars no artigo)")


def _validate_yaml_writer_config() -> None:
    from core.agents.memory.config_loader import (
        get_agent_model,
        get_agent_prompt,
    )

    model = get_agent_model("writer")
    prompt_ref = get_agent_prompt("writer")
    assert model == "claude-3-5-haiku-20241022", f"modelo inesperado: {model}"
    assert isinstance(prompt_ref, str) and prompt_ref.strip(), (
        "YAML do Writer deve ter prompt (referência)"
    )
    print(f"  config YAML do Writer OK (model={model})")


def main() -> int:
    steps = [
        ("product_context carrega do YAML", _validate_product_context),
        ("config YAML do Writer é válido", _validate_yaml_writer_config),
        ("writer_node respeita contrato", _validate_writer_contract),
        ("grafo do Ensaio compila", _validate_graph_compiles),
    ]

    print("=" * 60)
    print("Validação manual do grafo do Ensaio (POC)")
    print("=" * 60)

    failed = 0
    for label, fn in steps:
        print(f"\n[ ] {label}")
        try:
            fn()
            print(f"[x] {label}")
        except AssertionError as exc:
            failed += 1
            print(f"[!] {label} FALHOU: {exc}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"[!] {label} ERRO: {type(exc).__name__}: {exc}")

    print("\n" + "=" * 60)
    if failed == 0:
        print("TODOS OS CHECKS PASSARAM")
        return 0
    print(f"{failed} CHECK(S) FALHOU/FALHARAM")
    return 1


if __name__ == "__main__":
    sys.exit(main())
