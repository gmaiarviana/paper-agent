# Análise de Riscos e Mitigações - Migração Monorepo

**Data:** 2025-01-XX  
**Escopo:** Migração de estrutura plana para monorepo (`core/` + `products/revelar/`)  
**Arquivos Afetados:** ~344 arquivos (35k código + 20k docs)  
**Timeline Estimado:** ~15 horas

---

## Riscos Identificados

### 1. Risco: Imports Relativos Quebrados
- **Descrição:** `from .state import MultiAgentState` pode quebrar após mover diretórios
- **Probabilidade:** Alta
- **Impacto:** Médio (testes detectam)
- **Arquivos Afetados:** ~16 arquivos com imports relativos em `agents/`
- **Mitigação:** 
  - Converter para imports absolutos ANTES de mover
  - Script de validação: `grep -r "from \." agents/`
  - Testar imports após cada fase: `python -c "from core.agents.orchestrator.state import MultiAgentState"`

### 2. Risco: Testes Não Detectam Quebras
- **Descrição:** Testes podem não cobrir todos os caminhos de execução
- **Probabilidade:** Média
- **Impacto:** Alto (bugs em produção)
- **Mitigação:** 
  - Rodar suite completa após cada fase: `pytest tests/ -v`
  - Executar testes de integração: `pytest tests/integration/ -v`
  - Validar smoke tests: `pytest -m smoke -v`
  - Manter cobertura: `pytest --cov=core --cov=products tests/`

### 3. Risco: Documentação Desatualizada
- **Descrição:** 144 arquivos de docs com referências a caminhos antigos
- **Probabilidade:** Alta
- **Impacto:** Baixo (não quebra código, mas confunde desenvolvedores)
- **Mitigação:** 
  - Migrar docs por último (Fase 7)
  - Script de validação de links: `grep -r "agents/" docs/`
  - Atualizar referências em lote com find/replace
  - Validar links após migração: `find docs/ -name "*.md" -exec grep -l "agents/" {} \;`

### 4. Risco: Perda de Histórico Git
- **Descrição:** `mv` simples perde histórico de arquivos
- **Probabilidade:** Alta se não usar `git mv`
- **Impacto:** Alto (perde rastreabilidade, dificulta debugging)
- **Mitigação:** 
  - **SEMPRE usar `git mv`** ao invés de `mv`
  - Validar histórico: `git log --follow core/agents/orchestrator/nodes.py`
  - Se esquecer, usar: `git add -A` + `git commit --amend` para preservar

### 5. Risco: Fadiga do Desenvolvedor
- **Descrição:** 344 arquivos é muito para revisar manualmente
- **Probabilidade:** Alta
- **Impacto:** Alto (erros por cansaço, revisões incompletas)
- **Mitigação:** 
  - Automatizar o máximo possível (scripts de migração)
  - Fazer pausas entre fases (não tentar fazer tudo de uma vez)
  - Commits pequenos e incrementais (uma fase por commit)
  - Validar automaticamente após cada fase

### 6. Risco: Dependências Circulares Não Detectadas
- **Descrição:** Imports circulares podem quebrar silenciosamente
- **Probabilidade:** Média
- **Impacto:** Alto (erros em runtime, difícil debugar)
- **Mitigação:** 
  - Validar imports após cada fase: `python -c "import core.agents.orchestrator.nodes"`
  - Usar ferramenta de detecção: `pylint --disable=all --enable=import-error`
  - Testar importação de todos os módulos principais

### 7. Risco: Configurações de Caminhos Quebradas
- **Descrição:** `config_loader.py` e paths de YAML podem quebrar
- **Probabilidade:** Alta
- **Impacto:** Alto (sistema não inicia)
- **Arquivos Afetados:** 
  - `agents/memory/config_loader.py`
  - `utils/config.py`
  - Todos os arquivos que carregam `config/agents/*.yaml`
- **Mitigação:** 
  - Ajustar `config_loader.py` imediatamente após mover `config/`
  - Validar: `python -c "from core.agents.memory.config_loader import load_all_agent_configs"`
  - Testar carregamento de configs: `python scripts/health_checks/validate_config_loading.py`

### 8. Risco: Entry Points Quebrados (Streamlit/CLI)
- **Descrição:** `streamlit run app/chat.py` e `python -m cli.chat` podem quebrar
- **Probabilidade:** Alta
- **Impacto:** Alto (usuário não consegue usar sistema)
- **Mitigação:** 
  - Atualizar entry points após mover `app/` e `cli/`
  - Testar: `streamlit run products/revelar/app/chat.py`
  - Testar: `python -m core.tools.cli.chat`
  - Atualizar README.md com novos comandos

### 9. Risco: PYTHONPATH e Imports Dinâmicos
- **Descrição:** Scripts que usam `sys.path.insert()` podem quebrar
- **Probabilidade:** Média
- **Impacto:** Médio (scripts de validação/teste quebram)
- **Arquivos Afetados:** 
  - `scripts/validate_*.py`
  - `scripts/health_checks/*.py`
- **Mitigação:** 
  - Revisar todos os scripts que modificam `sys.path`
  - Atualizar paths relativos: `Path(__file__).parent.parent.parent`
  - Testar scripts após mover: `python scripts/health_checks/validate_config_loading.py`

### 10. Risco: Paths de Banco de Dados Quebrados
- **Descrição:** Referências a `data/checkpoints.db`, `data/concepts.db` podem quebrar
- **Probabilidade:** Baixa (paths relativos geralmente funcionam)
- **Impacto:** Alto (perda de dados, sistema não funciona)
- **Mitigação:** 
  - Validar que `data/` permanece na raiz (não muda)
  - Testar acesso a DBs: `python -c "import sqlite3; sqlite3.connect('data/checkpoints.db')"`
  - Verificar `SqliteSaver.from_conn_string()` em `multi_agent_graph.py`

### 11. Risco: ChromaDB Paths Quebrados
- **Descrição:** ChromaDB armazena paths absolutos, pode quebrar após mover
- **Probabilidade:** Média
- **Impacto:** Alto (Observer não funciona, conceitos perdidos)
- **Mitigação:** 
  - Validar que `data/chroma/` permanece na raiz
  - Testar Observer após migração: `python scripts/validate_observer_integration.py`
  - Se necessário, recriar coleção ChromaDB (dados podem ser perdidos)

### 12. Risco: EventBus e Callbacks Quebrados
- **Descrição:** Callbacks assíncronos do Observer podem quebrar
- **Probabilidade:** Média
- **Impacto:** Médio (Observer não processa, mas sistema continua)
- **Mitigação:** 
  - Validar imports do EventBus: `from utils.event_bus import get_event_bus`
  - Testar callback do Observer: `python scripts/validate_observer_integration.py`
  - Verificar que `multi_agent_graph.py` mantém callback funcionando

### 13. Risco: Testes de Integração Dependentes de Estrutura
- **Descrição:** Testes que importam `from app.` ou `from agents.` diretamente
- **Probabilidade:** Alta
- **Impacto:** Alto (suite de testes quebra)
- **Arquivos Afetados:** 
  - `tests/integration/behavior/test_cli_integration.py`
  - `tests/integration/behavior/test_system_maturity.py`
- **Mitigação:** 
  - Atualizar imports em testes imediatamente após mover código
  - Rodar testes após cada fase: `pytest tests/integration/ -v`
  - Usar `conftest.py` para centralizar imports de fixtures

### 14. Risco: pytest.ini e Test Paths Quebrados
- **Descrição:** `pytest.ini` pode precisar ajustes para novos paths
- **Probabilidade:** Baixa (testpaths relativos geralmente funcionam)
- **Impacto:** Médio (testes não rodam corretamente)
- **Mitigação:** 
  - Validar `pytest.ini` após reorganizar testes (Fase 5)
  - Testar: `pytest tests/core/ -v` e `pytest tests/products/revelar/ -v`
  - Ajustar `testpaths` se necessário

### 15. Risco: Checkpoints do LangGraph Invalidados
- **Descrição:** Checkpoints podem referenciar módulos antigos
- **Probabilidade:** Baixa (LangGraph serializa por nome, não path)
- **Impacto:** Alto (sessões antigas não podem ser retomadas)
- **Mitigação:** 
  - Testar retomada de sessão após migração
  - Documentar breaking change: "Sessões antigas precisam ser recriadas"
  - Considerar script de migração de checkpoints (se necessário)

### 16. Risco: Imports de Utils Quebrados
- **Descrição:** `from utils.prompts.` → `from core.prompts.` pode quebrar
- **Probabilidade:** Alta
- **Impacto:** Alto (agentes não funcionam)
- **Arquivos Afetados:** ~20 arquivos que importam `utils.prompts.*`
- **Mitigação:** 
  - Converter imports em lote: `sed -i 's/from utils\.prompts/from core.prompts/g' **/*.py`
  - Validar: `grep -r "from utils.prompts" . --exclude-dir=venv`
  - Testar após conversão: `python -c "from core.prompts.orchestrator import build_prompt"`

### 17. Risco: Multi-Agent Graph Quebrado
- **Descrição:** `multi_agent_graph.py` importa de múltiplos lugares
- **Probabilidade:** Alta
- **Impacto:** Crítico (sistema não inicia)
- **Arquivos Afetados:** `agents/multi_agent_graph.py`
- **Mitigação:** 
  - Atualizar TODOS os imports em `multi_agent_graph.py` imediatamente após Fase 2
  - Validar: `python -c "from core.agents.multi_agent_graph import build_graph"`
  - Testar criação do grafo: `python -c "from core.agents.multi_agent_graph import build_graph; g = build_graph()"`

### 18. Risco: Scripts de Validação Quebrados
- **Descrição:** Scripts em `scripts/health_checks/` podem ter imports quebrados
- **Probabilidade:** Alta
- **Impacto:** Médio (validações não funcionam, mas sistema pode funcionar)
- **Mitigação:** 
  - Atualizar imports em scripts após mover código (Fase 6)
  - Testar scripts manualmente: `python scripts/health_checks/validate_config_loading.py`
  - Manter scripts funcionando para validação contínua

### 19. Risco: README e Documentação de Instalação Desatualizada
- **Descrição:** README.md pode ter comandos/exemplos com paths antigos
- **Probabilidade:** Alta
- **Impacto:** Baixo (não quebra código, mas confunde novos desenvolvedores)
- **Mitigação:** 
  - Atualizar README.md na Fase 9 (Limpeza Final)
  - Validar todos os comandos no README
  - Atualizar exemplos de código

### 20. Risco: CI/CD Quebrado (se existir)
- **Descrição:** Pipelines podem ter paths hardcoded
- **Probabilidade:** Média (se CI/CD existir)
- **Impacto:** Alto (deploy quebra)
- **Mitigação:** 
  - Revisar `.github/workflows/` ou `.gitlab-ci.yml` se existir
  - Atualizar paths em scripts de CI/CD
  - Testar pipeline após migração

---

## Matriz de Priorização de Riscos

| Risco | Probabilidade | Impacto | Prioridade | Fase Crítica |
|-------|---------------|---------|------------|--------------|
| Imports Relativos Quebrados | Alta | Médio | Alta | Fase 2 |
| Configurações de Caminhos | Alta | Alto | Crítica | Fase 2 |
| Multi-Agent Graph Quebrado | Alta | Crítico | Crítica | Fase 2 |
| Entry Points Quebrados | Alta | Alto | Alta | Fase 3-4 |
| Testes Não Detectam Quebras | Média | Alto | Alta | Todas |
| Dependências Circulares | Média | Alto | Alta | Fase 2 |
| Testes Dependentes de Estrutura | Alta | Alto | Alta | Fase 5 |
| ChromaDB Paths | Média | Alto | Média | Fase 2 |
| Checkpoints Invalidados | Baixa | Alto | Média | Fase 2 |
| Documentação Desatualizada | Alta | Baixo | Baixa | Fase 7 |
| Fadiga do Desenvolvedor | Alta | Alto | Alta | Todas |

---

## Plano de Mitigação por Fase

### Fase 0: Preparação
- ✅ Criar branch `refactor/monorepo-structure`
- ✅ Analisar estrutura atual
- ✅ Criar MIGRATION.md
- ✅ **Criar este documento (risk_assessment.md)**

### Fase 1: Estrutura Base
- ✅ Criar diretórios vazios
- ✅ Validar que testes continuam passando

### Fase 2: Core Essencial (CRÍTICA)
**Riscos Principais:**
- Imports relativos quebrados
- Configurações de caminhos
- Multi-agent graph quebrado
- Dependências circulares

**Mitigações:**
1. Converter imports relativos para absolutos ANTES de mover
2. Atualizar `config_loader.py` imediatamente após mover `config/`
3. Atualizar TODOS os imports em `multi_agent_graph.py`
4. Validar imports: `python -c "import core.agents.multi_agent_graph"`
5. Rodar suite completa de testes: `pytest tests/ -v`

### Fase 3: CLI
**Riscos Principais:**
- Entry points quebrados

**Mitigações:**
1. Testar: `python -m core.tools.cli.chat`
2. Atualizar scripts que usam CLI

### Fase 4: Produto Revelar
**Riscos Principais:**
- Entry points Streamlit quebrados
- Imports de app quebrados

**Mitigações:**
1. Testar: `streamlit run products/revelar/app/chat.py`
2. Validar todos os imports em `app/`
3. Rodar testes de integração

### Fase 5: Testes
**Riscos Principais:**
- Testes dependentes de estrutura
- pytest.ini quebrado

**Mitigações:**
1. Atualizar imports em todos os testes
2. Validar `pytest.ini`
3. Rodar: `pytest tests/core/ -v` e `pytest tests/products/revelar/ -v`

### Fase 6: Scripts
**Riscos Principais:**
- Scripts de validação quebrados
- PYTHONPATH quebrado

**Mitigações:**
1. Atualizar `sys.path` em scripts
2. Testar scripts manualmente
3. Validar health checks

### Fase 7: Documentação
**Riscos Principais:**
- Documentação desatualizada
- Links quebrados

**Mitigações:**
1. Atualizar referências em lote
2. Validar links: `find docs/ -name "*.md" -exec grep -l "agents/" {} \;`
3. Revisar manualmente seções críticas

### Fase 8: ROADMAPs
**Riscos Principais:**
- Referências desatualizadas

**Mitigações:**
1. Atualizar referências em ROADMAPs
2. Validar links internos

### Fase 9: Limpeza Final
**Riscos Principais:**
- README desatualizado
- Comandos quebrados

**Mitigações:**
1. Atualizar README.md
2. Validar todos os comandos
3. Teste final completo: `pytest tests/ -v`

---

## Checklist de Validação Pós-Migração

Após cada fase, validar:

- [ ] Imports funcionam: `python -c "import core.agents.orchestrator.nodes"`
- [ ] Testes passam: `pytest tests/ -v`
- [ ] Configs carregam: `python scripts/health_checks/validate_config_loading.py`
- [ ] Entry points funcionam: `streamlit run products/revelar/app/chat.py`
- [ ] Observer funciona: `python scripts/validate_observer_integration.py`
- [ ] CLI funciona: `python -m core.tools.cli.chat`
- [ ] Histórico Git preservado: `git log --follow core/agents/orchestrator/nodes.py`
- [ ] Sem imports circulares: `pylint --disable=all --enable=import-error`
- [ ] Documentação atualizada: `grep -r "agents/" docs/` (deve retornar vazio ou apenas referências históricas)

---

## Estratégias de Rollback

Se algo quebrar gravemente:

1. **Rollback Git:** `git reset --hard <commit-anterior>`
2. **Branch de Backup:** Manter branch `main` intacta, trabalhar apenas em `refactor/monorepo-structure`
3. **Commits Incrementais:** Cada fase = commit separado, fácil de reverter
4. **Validação Contínua:** Não avançar para próxima fase se atual está quebrada

---

## Notas Finais

- **Não tentar fazer tudo de uma vez:** Migração de 15h deve ser feita em múltiplas sessões
- **Automatizar o máximo possível:** Scripts de migração reduzem erros humanos
- **Validar constantemente:** Após cada fase, rodar suite completa de testes
- **Documentar breaking changes:** Se checkpoints antigos não funcionarem, documentar claramente
- **Comunicar mudanças:** Atualizar README e documentação para novos desenvolvedores

---

**Versão:** 1.0  
**Última Atualização:** 2025-01-XX  
**Status:** Documento vivo - atualizar conforme riscos são identificados/mitigados

