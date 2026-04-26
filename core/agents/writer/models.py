"""Tipos de domínio do Writer — C-ENSAIO-3.1.

Contrato serializável compartilhado entre o core e o produto Ensaio.
Vive no core para que outros produtos (ex.: Produtor Científico) reutilizem
sem depender do Ensaio.
"""

from typing import Literal, TypedDict


class Section(TypedDict):
    title: str
    body: str
    status: Literal["empty", "draft", "edited"]


Article = list[Section]
