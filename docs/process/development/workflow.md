# Workflow: Funcionalidade → Tarefas → Implementação → PR

## 1. RECEBIMENTO E PLANEJAMENTO

Quando dev solicitar funcionalidade:

1. **Ler contexto obrigatório:**
   - ROADMAP.md (descrição da funcionalidade)
   - README.md (execução e escopo da POC)
   - ARCHITECTURE.md (estrutura técnica)
   - docs/agents/overview.md (se envolver novos agentes)
   - planning_guidelines.md (para entender dependências/ordem)
   - Código relacionado (para entender dependências)

2. **Quebrar em tarefas:**
   - Ordenar por dependência técnica
   - Identificar onde TDD faz sentido (ver [implementation.md](implementation.md))
   - Estimar complexidade realista
   - Mostrar plano COMPLETO

3. **Validar plano com dev:**
   - Listar tarefas com indicação de testes
   - Aguardar OK antes de começar
   - Dev pode ir para reunião/outra atividade após aprovar

---

**Próximos passos:**
- Para detalhes de implementação → [implementation.md](implementation.md)
- Para lidar com travamentos → [blockers.md](blockers.md)
- Para finalização e entrega → [delivery.md](delivery.md)
