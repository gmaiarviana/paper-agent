"""Testes unitários para E-PROTO2-1.1 e 1.3 — co-decisão da estrutura.

Cobre os event handlers de ``EnsaioState`` que substituem o auto-commit do
Estruturador por proposta pendente + aceite/recusa/edição leve.

Nota: testes não instanciam ``rx.State`` (depende de runtime Reflex). Em vez
disso, exercitam os métodos diretamente em uma instância simulada que tem os
atributos esperados. As funções unbound são copiadas para a instância para
preservar o ``self`` esperado.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from products.ensaio.app.state import EnsaioState


def _make_state() -> SimpleNamespace:
    """Instância simulada de EnsaioState com os atributos relevantes."""
    obj = SimpleNamespace(
        messages=[],
        langchain_history=[],
        focal_argument={},
        current_article=[],
        editing_section_index=-1,
        pending_structure_proposal={},
        editing_proposal=False,
        proposal_draft=[],
        proposal_rationale_draft="",
        proposal_edit_error="",
    )
    # Vincular event handlers do EnsaioState à instância simulada.
    # Funcionam porque os handlers só usam ``self.<atributo>`` e nunca
    # chamam APIs de rx.State.
    method_names = (
        "_commit_proposal",
        "accept_structure_proposal",
        "reject_structure_proposal",
        "start_editing_proposal",
        "update_proposal_section",
        "move_proposal_section",
        "remove_proposal_section",
        "add_proposal_section",
        "confirm_proposal_edit",
        "cancel_proposal_edit",
    )
    for name in method_names:
        attr = getattr(EnsaioState, name)
        # Reflex envolve event handlers em EventHandler; o método raw vive
        # em ``.fn``. Métodos privados (começando com _) seguem como
        # função normal, sem wrapper.
        fn = getattr(attr, "fn", attr)
        setattr(obj, name, fn.__get__(obj, type(obj)))
    return obj


def test_accept_structure_proposal_commits_to_current_article():
    s = _make_state()
    s.pending_structure_proposal = {
        "sections": ["Introdução", "Métodos", "Resultados"],
        "rationale": "Ordem padrão IMRaD.",
    }

    s.accept_structure_proposal()

    assert len(s.current_article) == 3
    assert [sec["title"] for sec in s.current_article] == [
        "Introdução", "Métodos", "Resultados"
    ]
    assert all(sec["status"] == "empty" and sec["body"] == "" for sec in s.current_article)
    assert [sec["index"] for sec in s.current_article] == [0, 1, 2]
    # Pendente é zerado no aceite.
    assert s.pending_structure_proposal == {}


def test_accept_without_pending_does_nothing():
    s = _make_state()
    s.accept_structure_proposal()
    assert s.current_article == []


def test_reject_clears_pending_without_touching_current_article():
    s = _make_state()
    s.current_article = [
        {"title": "Velha", "body": "x", "status": "draft", "index": 0}
    ]
    s.pending_structure_proposal = {
        "sections": ["Nova"],
        "rationale": "...",
    }

    s.reject_structure_proposal()

    assert s.pending_structure_proposal == {}
    # current_article preservado.
    assert s.current_article == [
        {"title": "Velha", "body": "x", "status": "draft", "index": 0}
    ]
    # Recusa deixa nota no histórico.
    assert any("recusada" in m.get("content", "").lower() for m in s.messages)


def test_start_editing_copies_proposal_into_draft():
    s = _make_state()
    s.pending_structure_proposal = {
        "sections": ["A", "B", "C"],
        "rationale": "ABC.",
    }

    s.start_editing_proposal()

    assert s.editing_proposal is True
    assert s.proposal_draft == ["A", "B", "C"]
    assert s.proposal_rationale_draft == "ABC."


def test_update_proposal_section_renames():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A", "B"], "rationale": ""}
    s.start_editing_proposal()

    s.update_proposal_section(1, "B-renomeada")

    assert s.proposal_draft == ["A", "B-renomeada"]


def test_move_proposal_section_swaps():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A", "B", "C"], "rationale": ""}
    s.start_editing_proposal()

    s.move_proposal_section(0, 1)
    assert s.proposal_draft == ["B", "A", "C"]

    # Borda: tentar mover além do limite não muda nada.
    s.move_proposal_section(2, 1)
    assert s.proposal_draft == ["B", "A", "C"]


def test_remove_proposal_section():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A", "B", "C"], "rationale": ""}
    s.start_editing_proposal()

    s.remove_proposal_section(1)
    assert s.proposal_draft == ["A", "C"]


def test_add_proposal_section_appends():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A"], "rationale": ""}
    s.start_editing_proposal()

    s.add_proposal_section()
    assert s.proposal_draft == ["A", "Nova seção"]


def test_confirm_proposal_edit_commits_cleaned_draft():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A", "B"], "rationale": ""}
    s.start_editing_proposal()
    s.update_proposal_section(0, "  Introdução  ")
    s.update_proposal_section(1, "")  # vazia será descartada no commit

    s.confirm_proposal_edit()

    assert [sec["title"] for sec in s.current_article] == ["Introdução"]
    assert s.editing_proposal is False
    assert s.proposal_draft == []
    assert s.pending_structure_proposal == {}


def test_confirm_proposal_edit_blocks_when_all_empty():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A"], "rationale": ""}
    s.start_editing_proposal()
    s.update_proposal_section(0, "")

    s.confirm_proposal_edit()

    assert s.current_article == []  # nada comitado
    assert s.editing_proposal is True  # ainda em edição
    assert s.proposal_edit_error  # mensagem inline presente


def test_cancel_proposal_edit_returns_to_view_mode():
    s = _make_state()
    s.pending_structure_proposal = {"sections": ["A"], "rationale": "X"}
    s.start_editing_proposal()
    s.update_proposal_section(0, "Modificada")

    s.cancel_proposal_edit()

    assert s.editing_proposal is False
    assert s.proposal_draft == []
    assert s.proposal_rationale_draft == ""
    # Proposta original preservada.
    assert s.pending_structure_proposal["sections"] == ["A"]
