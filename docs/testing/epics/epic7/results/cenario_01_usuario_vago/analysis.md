# Análise do Cenário 1: Usuário Começa Vago → Sistema Estrutura

## Comportamento Esperado

- [ ] Orquestrador classifica como vago (`next_step: "explore"`)
- [ ] Sistema pergunta contexto (não estrutura automaticamente)
- [ ] Após usuário responder, Orquestrador chama Estruturador (`next_step: "suggest_agent"`)
- [ ] Estruturador cria V1 com claim correto
- [ ] `focal_argument` é atualizado (intent, subject, population, metrics)

## Logs Necessários

### EventBus
- `agent_started` (orchestrator)
- `agent_completed` (orchestrator)
- `agent_started` (structurer)
- `agent_completed` (structurer)

### MultiAgentState
- `focal_argument`
- `hypothesis_versions`
- `messages`

### Output Final
Mensagem exibida ao usuário

## Critérios de Sucesso

- [ ] Orquestrador explora (não estrutura automaticamente)
- [ ] Estruturador é chamado automaticamente (sem pedir permissão)
- [ ] Contexto preservado (focal_argument atualizado)
- [ ] Mensagem ao usuário é fluida (não burocrática)

## Observações

- **Comportamento esperado foi atingido?** (Sim/Não/Parcial)
- **Problemas identificados?** (Crítico/Médio/Baixo)
- **Notas adicionais:**

