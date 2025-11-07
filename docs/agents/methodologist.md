Methodologist Agent
===================

Resumo
------
- Especialista responsável por avaliar rigor científico de hipóteses.
- Recebe input estruturado do Orquestrador e responde com JSON padronizado.
- Nunca interage diretamente com o usuário final.

Interface e Contratos
----------------------
- Método público: `Methodologist.analyze(hypothesis: str) -> dict`
- Entrada: texto da hipótese, já sanitizado pelo Orquestrador
- Saída esperada:

```
{
  "status": "approved" | "rejected",
  "justification": "...",
  "suggestions": ["..."]
}
```

- Erros devem ser encapsulados em respostas claras (`{"status": "error", ...}`) para o Orquestrador lidar.

Prompting
---------
- Os prompts residem em `utils/prompts.py` e são versionados (`METHODOLOGIST_PROMPT_V1`, etc.).
- Cada versão inclui: responsabilidades, formato de saída, exemplos de aprovação/rejeição e lembrete explícito para sempre retornar JSON válido.
- Quando atualizar um prompt, registre versão e motivação neste documento.

Tratamento de Respostas
-----------------------
- Valide JSON com Pydantic antes de devolver ao chamador.
- Em caso de formato inválido, tente refazer a chamada (3 tentativas com backoff) antes de propagar erro.
- Logue prompt enviado e resposta recebida em nível `DEBUG` para auditoria.

Boas Práticas
-------------
- Mantenha a responsabilidade do agente limitada a avaliação metodológica; não gerar texto livre além das chaves definidas.
- Evite assumir conhecimento de outros agentes; comunique apenas via dados estruturados.
- Atualize este documento sempre que adicionar novos campos, comportamentos ou regras específicas do Metodologista.

