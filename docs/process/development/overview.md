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
- **planning_guidelines.md**: Regras de planejamento e governança

### Entrada
- Dev escolhe: "Funcionalidade X.Y do roadmap"
- Arquivos contextuais: ROADMAP.md, README.md, ARCHITECTURE.md

### Saída
- Branch com código implementado
- Testes onde necessário
- Documentação atualizada
- **Comandos para validação local** (dev testa antes de mergear)
- **Aviso ao dev que branch está pronta** (dev cria PR manualmente)

## Modo de Operação: Validação Híbrida

### Seu Papel na Validação
- **Sintaxe e imports:** Validar automaticamente (Python parser)
- **Busca de impactos:** Identificar arquivos que usam funções modificadas
- **Comandos de teste:** Fornecer comandos prontos para dev rodar
- **NÃO rodar testes:** Ambiente não tem dependências completas instaladas
- **NÃO instalar requirements.txt:** Demorado (~2-5min) e desnecessário

### Validação ao Fim de Checkpoint
Ao finalizar checkpoint (conjunto de funcionalidades), fornecer:
1. ✅ Status de validação automática (sintaxe, imports)
2. ⚠️ Arquivos impactados (busca por chamadas a funções modificadas)
3. 📋 Comandos de validação prontos (copiar e colar)
4. 🔍 Validações esperadas (o que dev deve verificar)
5. 📄 Atualizar `docs/process/current_implementation.md` (marcar checkpoint ✅)

**Exemplo de mensagem ao fim de checkpoint:**
```
✅ Checkpoint 1 concluído (Features 11.1 + 11.2)
Branch pronta: feature/11.1-11.2

✅ Validação automática:
- Sintaxe Python: OK (5 arquivos)
- Imports: OK

⚠️ Impactos detectados:
- agents/orchestrator/nodes.py usa fundamentos (linha 45)
- agents/structurer/nodes.py usa fundamentos (linha 23)

📋 Comandos de validação (copie e cole):
pytest tests/unit/test_proposition.py -v
pytest tests/unit/test_cognitive_model.py -v

🔍 Validações esperadas:
- ✅ Testes devem passar
- ✅ Imports não devem quebrar
- ✅ Sistema deve rodar sem erros

📄 Atualizei docs/process/current_implementation.md
   (Checkpoint 1 marcado como concluído)

Aguardando sua validação para prosseguir ao Checkpoint 2.
```

**Exemplo de mensagem ao fim do ÚLTIMO checkpoint:**
```
✅ Checkpoint 3 concluído (Features 11.6 + 11.7 + 11.8)
Branch pronta: feature/11.6-11.8

[... validações automáticas ...]

📄 Deletei docs/process/current_implementation.md
   (Épico 11 finalizado)

Aguardando sua validação final.
```

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
