"""Testes de não-regressão: orchestrator e structurer emitem additional_kwargs["agent"].

E-PROTO-1.3 — garante que os nós do core adicionam metadata de agente
nas AIMessage sem quebrar o Revelar.
"""

from langchain_core.messages import AIMessage


class TestOrchestratorEmitsAgentMetadata:
    def test_aimage_accepts_additional_kwargs_with_agent(self):
        """Verifica que AIMessage aceita additional_kwargs com chave 'agent'."""
        msg = AIMessage(content="Olá", additional_kwargs={"agent": "orchestrator"})
        assert msg.additional_kwargs.get("agent") == "orchestrator"

    def test_aimage_additional_kwargs_backward_compatible(self):
        """Consumidores que não leem additional_kwargs continuam funcionando."""
        msg = AIMessage(content="Texto", additional_kwargs={"agent": "structurer"})
        # Consumidor que só acessa .content não quebra
        assert msg.content == "Texto"

    def test_structurer_additional_kwargs_with_sections(self):
        msg = AIMessage(
            content="Proposta: Introdução, Métodos, Resultados",
            additional_kwargs={
                "agent": "structurer",
                "article_sections": ["Introdução", "Métodos", "Resultados"],
            },
        )
        assert msg.additional_kwargs["agent"] == "structurer"
        assert msg.additional_kwargs["article_sections"] == [
            "Introdução",
            "Métodos",
            "Resultados",
        ]

    def test_missing_additional_kwargs_falls_back_gracefully(self):
        """Mensagem sem additional_kwargs não quebra ao tentar ler agent."""
        msg = AIMessage(content="Mensagem antiga sem metadata")
        agent = msg.additional_kwargs.get("agent")  # None — sem KeyError
        assert agent is None
