# Exemplos LangGraph - Para Referência Futura

> ⚠️ Esta seção será preenchida quando iniciarmos o ÉPICO 5
> O objetivo é ter exemplos concretos de código, não só descrições

---

## Estado (State) - Exemplo Concreto

```python
# TODO: Adicionar exemplo real quando começarmos ÉPICO 5
#
# Exemplo do que esperamos documentar:
# - TypedDict ou Pydantic model representando o State
# - Campos necessários: messages, current_agent, history, last_decision
# - Como inicializar o estado
# - Como atualizar o estado durante transições
```

---

## Criação de Nós e Arestas

```python
# TODO: Adicionar exemplo real quando começarmos ÉPICO 5
#
# Exemplo do que esperamos documentar:
# - Como definir nós (orchestrator, methodologist, user_response)
# - Como criar arestas condicionais baseadas em decisões
# - Como conectar os nós no grafo
# - Como visualizar o grafo para debug
```

---

## Estratégia de Fallback

**Status**: A definir em discussão antes da implementação

### Questões a Resolver:
- [ ] Como lidar com falhas na API do Claude?
- [ ] Retry logic: quantas tentativas? backoff exponencial?
- [ ] Mensagem ao usuário quando agente falha?
- [ ] Fallback para resposta direta se orquestrador falhar?
- [ ] Como persistir estado em caso de crash?

**Importante**: Algumas decisões não podem ser tomadas antecipadamente.
Serão definidas quando estivermos implementando o ÉPICO 5.

---

## Integração com CLI

```python
# TODO: Adicionar exemplo real quando começarmos ÉPICO 5
#
# Exemplo do que esperamos documentar:
# - Como integrar LangGraph workflow com CLI
# - Como exibir transições de estado no terminal
# - Como executar o workflow de forma assíncrona
# - Logs formatados mostrando o reasoning
```

---

## Notas para Implementação Futura

- Priorizar **exemplos concretos** sobre descrições abstratas
- Código de referência funcional, não pseudocódigo
- Casos de teste para validar cada componente
- Documentar decisões de arquitetura tomadas

**Este documento será o guia principal quando começarmos o ÉPICO 5**
