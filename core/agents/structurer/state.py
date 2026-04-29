"""
Modelos de output do agente Estruturador.

Schemas Pydantic usados para validar e tipar o `structurer_output` em
`MultiAgentState`. O TypedDict do estado compartilhado vive em
`core/agents/orchestrator/state.py`; aqui ficam apenas os modelos de
saída específicos deste agente.
"""

from pydantic import BaseModel, Field, ConfigDict


class StructurerElementsModel(BaseModel):
    """Elementos estruturados retornados pelo Estruturador."""

    context: str = Field(..., description="Contexto da observação")
    problem: str = Field(..., description="Problema ou gap identificado")
    contribution: str = Field(..., description="Possível contribuição acadêmica ou prática")


class StructurerOutputModel(BaseModel):
    """
    Output estruturado do agente Estruturador.

    Este modelo reflete a estrutura esperada em MultiAgentState.structurer_output.
    """

    structured_question: str = Field(..., description="Questão de pesquisa estruturada")
    elements: StructurerElementsModel

    model_config = ConfigDict(extra="ignore")
