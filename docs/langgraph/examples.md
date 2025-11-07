Exemplos LangGraph
==================

> ⚠️ Documento de referência para o Épico 5 (Integração com LangGraph State)
> Priorize exemplos concretos de código quando iniciar a implementação.

Estado (State)
-------------
```python
# TODO: Adicionar exemplo real quando começarmos ÉPICO 5
# - TypedDict ou Pydantic representando o State
# - Campos: messages, current_agent, history, last_decision
# - Inicialização do estado
# - Atualização do estado durante transições
```

Nós e Arestas
-------------
```python
# TODO: Adicionar exemplo real quando começarmos ÉPICO 5
# - Definição dos nós (orchestrator, methodologist, user_response)
# - Arestas condicionais baseadas em decisões
# - Conexão dos nós no grafo
# - Visualização para debug
```

Estratégia de Fallback
----------------------
- [ ] Como lidar com falhas na API do Claude?
- [ ] Retry logic (quantas tentativas? backoff?)
- [ ] Mensagem ao usuário quando agente falha?
- [ ] Fallback para resposta direta se o Orquestrador falhar?
- [ ] Persistência do estado em caso de crash?

Integração com CLI
------------------
```python
# TODO: Adicionar exemplo real quando começarmos ÉPICO 5
# - Integração do workflow LangGraph com a CLI
# - Exibição das transições de estado no terminal
# - Execução assíncrona quando necessário
# - Logs formatados mostrando reasoning
```

Notas Futuras
------------
- Priorize código executável em vez de descrições abstratas
- Documente decisões de arquitetura assim que forem tomadas
- Adicione casos de teste de referência para cada componente do grafo

