# Análise do Cenário 2: Usuário Fornece Hipótese Completa

## Comportamento Esperado

- [ ] Orquestrador reconhece contexto completo (`next_step: "suggest_agent"`)
- [ ] Sistema chama Metodologista diretamente (não pede mais contexto)
- [ ] Metodologista valida hipótese (approved/needs_refinement/rejected)
- [ ] Sistema apresenta feedback de forma fluida

## Logs Necessários

### EventBus
- `agent_started` (orchestrator)
- `agent_completed` (orchestrator)
- `agent_started` (methodologist)
- `agent_completed` (methodologist)

### MultiAgentState
- `focal_argument`
- `methodologist_output`

### Output Final
Mensagem exibida ao usuário

## Critérios de Sucesso

- [ ] Orquestrador não explora (contexto já completo)
- [ ] Metodologista é chamado automaticamente
- [ ] Validação usa critérios científicos (não arbitrária)
- [ ] Feedback é apresentado de forma fluida

## Observações

- **Comportamento esperado foi atingido?** (Sim/Não/Parcial)
- **Problemas identificados?** (Crítico/Médio/Baixo)
- **Notas adicionais:**

