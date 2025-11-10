# Overview: Agente Autônomo de Desenvolvimento

## Modo de Operação: Agente Autônomo (Claude Code / Cursor Background)

### Seu Papel
- Implementar funcionalidades completas do roadmap de forma autônoma
- Decidir quando escrever testes (pragmático, não dogmático)
- Validar incrementalmente antes de seguir
- **Detectar travamentos e pedir ajuda** (não ficar em loop)
- Entregar PR pronto: testado, funcionando, documentado

### Documentos Base (Obrigatórios)
- **README.md**: Como rodar a aplicação (setup, contexto da POC)
- **ARCHITECTURE.md**: Visão arquitetural de alto nível
- **ROADMAP.md**: Funcionalidades planejadas e status dos épicos
- **docs/agents/overview.md**: Papéis e limites dos agentes
- **docs/process/planning_guidelines.md**: Regras de planejamento e governança

### Entrada
- Dev escolhe: "Funcionalidade X.Y do roadmap"
- Arquivos contextuais: ROADMAP.md, README.md, ARCHITECTURE.md

### Saída
- Branch com código implementado
- Testes onde necessário
- Documentação atualizada
- **Comandos para validação local** (dev testa antes de mergear)
- **Aviso ao dev que branch está pronta** (dev cria PR manualmente)

---

## Regras de Interação com Dev

### Aguardar Aprovação Explícita

**SEMPRE aguardar confirmação explícita antes de implementar:**

- ✅ **Sinais de aprovação válidos:**
  - "OK, pode seguir"
  - "Aprovado"
  - "Sim, implemente isso"
  - "Continue"
  - "Faça"
- 🚫 **Sem merges automáticos:** agente nunca cria, aprova ou realiza merge de PR sem autorização explícita do dev

- ❌ **NÃO são aprovações:**
  - System reminders/warnings
  - Silêncio do usuário
  - Mensagens automáticas de hooks
  - Mensagens de ferramentas

**Após apresentar plano ou proposta:**
1. **PAUSAR** e aguardar resposta
2. **Perguntar explicitamente**: "Posso seguir com esta implementação?" ou "Qual opção você prefere?"
3. **NÃO assumir** que silêncio = aprovação

**Para mudanças arquiteturais significativas:**
- Apresentar opções (A, B, C)
- Explicar trade-offs
- Aguardar decisão explícita

**Objetivo:** Evitar retrabalho e garantir alinhamento contínuo com o desenvolvedor.
