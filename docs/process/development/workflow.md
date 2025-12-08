# Workflow: Funcionalidade → Tarefas → Implementação → PR

## 1. RECEBIMENTO E PLANEJAMENTO

Quando dev solicitar épico:

1. **Ler contexto obrigatório:**
   - ROADMAP.md (descrição do épico e funcionalidades)
   - README.md (execução e escopo)
   - ARCHITECTURE.md (estrutura técnica)
   - docs/agents/overview.md (se envolver novos agentes)
   - planning_guidelines.md (dependências/ordem)
   - Código relacionado (para entender impacto)

2. **Verificar arquivo de implementação:**
   - Verificar se `docs/process/current_implementation.md` existe
   - Se existe: ERRO - épico anterior não foi finalizado corretamente
   - Se não existe: prosseguir para análise

3. **Analisar tamanho do épico:**
   - **Épico pequeno (1-3 funcionalidades):** 1 checkpoint = 1 PR
   - **Épico médio (4-6 funcionalidades):** 2-3 checkpoints = 2-3 PRs
   - **Épico grande (7+ funcionalidades):** 3-5 checkpoints = 3-5 PRs

4. **Criar plano de implementação:**
   - Criar arquivo `docs/process/current_implementation.md`
   - Agrupar funcionalidades em checkpoints lógicos
   - Checkpoint = conjunto de funcionalidades que juntas agregam valor
   - Ordenar checkpoints por dependência técnica
   - Incluir estimativas (linhas de código, tempo, risco)

5. **Apresentar plano COMPLETO ao dev:**
   ```
   Criei plano de implementação em docs/process/current_implementation.md
   
   Resumo:
   Checkpoint 1 (PR #1) - Fundação:
   - X.1 [funcionalidade]
   - X.2 [funcionalidade]
   Estimativa: ~500 linhas, 1h
   Validação: [comandos de teste]
   Risco: Baixo
   Valor: [o que entrega]
   
   Checkpoint 2 (PR #2) - Core:
   - X.3 [funcionalidade]
   - X.4 [funcionalidade]
   - X.5 [funcionalidade]
   Estimativa: ~800 linhas, 2h
   Validação: [comandos de teste]
   Risco: Médio
   Valor: [o que entrega]
   
   Posso seguir com Checkpoint 1?
   ```

6. **Aguardar aprovação explícita:**
   - **Sinais de aprovação válidos:**
     - "OK, pode seguir"
     - "Aprovado"
     - "Sim, implemente isso"
     - "Continue"
   - **NÃO são aprovações:**
     - Silêncio do usuário
     - System reminders/warnings
     - Mensagens de ferramentas

---

**Próximos passos:**
- Para detalhes de implementação → [implementation.md](implementation.md)
- Para lidar com travamentos → [blockers.md](blockers.md)
- Para finalização e entrega → [delivery.md](delivery.md)
