# DEVELOPMENT_GUIDELINES.md

## 📚 Guia Modular de Desenvolvimento

Este documento é o índice principal das diretrizes de desenvolvimento. Cada seção está organizada em módulos separados para facilitar navegação e manutenção.

---

## 📖 Módulos

### 1. [Overview: Agente Autônomo](docs/process/implementation/overview.md)
**O que contém:**
- Papel do agente autônomo (Claude Code / Cursor Background)
- Documentos base obrigatórios (README, ARCHITECTURE, ROADMAP, etc.)
- Entrada e saída esperada do agente
- Regras de interação com o dev (aprovação explícita obrigatória)

**Quando ler:** Início de cada sessão, para entender o contexto e papel do agente.

---

### 2. [Workflow: Funcionalidade → Tarefas](docs/process/implementation/workflow.md)
**O que contém:**
- Recebimento da funcionalidade do roadmap
- Leitura do contexto obrigatório
- Quebra em tarefas ordenadas por dependência
- Validação do plano com o dev

**Quando ler:** Ao receber uma nova funcionalidade para implementar.

---

### 3. [Implementação Detalhada](docs/process/implementation/implementation.md)
**O que contém:**
- Heurística de TDD (quando aplicar testes antes/depois)
- Ciclo de implementação (Red-Green-Refactor)
- Scripts de validação (`scripts/validate_*.py`) - estrutura e boas práticas
- Commits estratégicos (opcionais)

**Relacionado:**
- Estratégia de testes, pirâmide, markers (`integration`, `slow`) e política de uso da API real: ver [`docs/testing/strategy.md`](docs/testing/strategy.md)

**Quando ler:** Durante a implementação de cada tarefa.

---

### 4. [Bloqueios e Travamentos](docs/process/implementation/blockers.md)
**O que contém:**
- Critérios de travamento (regra das 3 tentativas)
- Protocolo de reporte ao dev
- Tratamento de erros comuns (testes, dependências, complexidade)
- Opções de desbloqueio

**Quando ler:** Quando encontrar dificuldades ou erros persistentes.

---

### 5. [Fechamento e Entrega](docs/process/implementation/delivery.md)
**O que contém:**
- Mensagem final obrigatória ao dev
- Template de PR (referência - o oficial é em `.github/PULL_REQUEST_TEMPLATE.md`)
- Checklist de finalização (testes, código, documentação, git)
- Comandos de validação local

**Quando ler:** Ao finalizar todas as tarefas e preparar entrega.

---

### 6. [Regras de Qualidade](docs/process/implementation/quality_rules.md)
**O que contém:**
- Princípios gerais (incremental, TDD pragmático, transparente)
- Anti-redundância: tabela de responsabilidades de cada documento
- Comandos e validação (PowerShell, scripts, template)
- Exemplo de fluxo completo
- Observações finais para dev e agente

**Quando ler:** Periodicamente, para revisar princípios e garantir qualidade.

---

## 🚀 Início Rápido

**Fluxo típico de trabalho:**

1. **Dev solicita funcionalidade** → Leia [overview.md](docs/process/implementation/overview.md) para entender seu papel
2. **Planeje as tarefas** → Leia [workflow.md](docs/process/implementation/workflow.md) e quebre a funcionalidade
3. **Implemente cada tarefa** → Siga [implementation.md](docs/process/implementation/implementation.md) (TDD, validação, commits)
4. **Se encontrar bloqueio** → Consulte [blockers.md](docs/process/implementation/blockers.md) e reporte após 3 tentativas
5. **Finalize e entregue** → Use [delivery.md](docs/process/implementation/delivery.md) para mensagem final e PR
6. **Mantenha qualidade** → Revise [quality_rules.md](docs/process/implementation/quality_rules.md) periodicamente

---

## 🎯 Regras de Ouro

- ✅ **Aguardar aprovação explícita** antes de implementar
- ✅ **Parar após 3 tentativas falhas** e reportar travamento
- ✅ **Validar incrementalmente** (testes, scripts, app rodando)
- ✅ **Documentar incrementalmente** (não deixar pro final)
- ✅ **Fornecer comandos de validação** prontos para copiar/colar
- ❌ **Nunca criar PR automaticamente** - dev cria pela interface do GitHub
- ❌ **Nunca duplicar informações** entre documentos - sempre referenciar

---

## 📝 Compatibilidade

Este documento foi modularizado para facilitar manutenção. Links existentes que apontam para `development_guidelines.md` continuam funcionando, mas agora você tem acesso granular a cada seção.

**Última atualização:** 2025-11-10
