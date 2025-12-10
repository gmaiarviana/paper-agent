# ANÁLISE 6: Estimativa Realista de Tempo - Migração Monorepo

**Data:** 2025-01-XX  
**Contexto:** Migração de estrutura plana para monorepo (core/products)  
**Escopo:** ~191 arquivos Python + 131 arquivos Markdown + ~500 referências

---

## 1. Tempo por Fase (Detalhado)

### Dados Reais Coletados
- **agents/**: 45 arquivos Python
- **utils/**: 24 arquivos Python  
- **app/**: 21 arquivos Python
- **tests/**: 73 arquivos Python
- **scripts/**: 28 arquivos Python
- **docs/**: 131 arquivos Markdown
- **Imports afetados**: 238 linhas em 109 arquivos
- **Referências em docs**: ~500 (estimado)

---

| Fase | Atividade | Arquivos | Tempo Min | Tempo Máx | Observações |
|------|-----------|----------|-----------|-----------|-------------|
| **0** | Preparação | 0 | 1h | 2h | ✅ Já concluída (branch, análise, MIGRATION.md) |
| **1** | Estrutura vazia | 0 | 30min | 1h | Criar dirs + `__init__.py` (~15 dirs) |
| **2** | Mover agents/ | 45 | 2h | 4h | `git mv` + ajustar 238 imports em 109 arquivos |
| **2.1** | Mover utils/ | 24 | 1h | 2h | + ajustar imports restantes |
| **2.2** | Mover prompts/ | ~5 | 30min | 1h | Subdiretório de utils, ajustar imports |
| **2.3** | Mover config/ | ~5 | 30min | 1h | Ajustar paths em config_loader.py |
| **2.4** | Testar Core | - | 1h | 2h | Rodar testes, corrigir quebras |
| **3** | Mover CLI | ~2 | 30min | 1h | + ajustar imports em scripts |
| **4** | Mover app/ | 21 | 1.5h | 3h | + ajustar imports em app/ e testes |
| **4.1** | Testar App | - | 1h | 2h | Streamlit + testes de integração |
| **5** | Reorganizar tests/ | 73 | 2h | 4h | Mover + ajustar imports + pytest.ini |
| **5.1** | Validar Testes | - | 1h | 2h | Rodar suite completa, corrigir quebras |
| **6** | Reorganizar scripts/ | 28 | 1h | 2h | Separar core/revelar + ajustar imports |
| **7** | Reorganizar docs/ | 131 | 3h | 6h | Mover + atualizar ~500 referências internas |
| **7.1** | Validar Links | - | 1h | 2h | Revisar links quebrados, corrigir |
| **8** | ROADMAPs | 3 | 30min | 1h | Criar + mover épicos + atualizar índice |
| **9** | Limpeza Final | ~10 | 1h | 2h | Remover dirs vazios + atualizar README/ARCHITECTURE |

---

## 2. Tempo Total por Cenário

### Cenário Otimista (Tudo funciona na primeira tentativa)
**Assumindo:**
- Imports ajustados automaticamente sem erros
- Testes passam sem correções
- Documentação sem links quebrados
- Sem necessidade de revisão extensa

| Fase | Tempo Otimista |
|------|----------------|
| 0 | 0h (já feito) |
| 1 | 30min |
| 2-2.4 | 4h |
| 3 | 30min |
| 4-4.1 | 2.5h |
| 5-5.1 | 3h |
| 6 | 1h |
| 7-7.1 | 4h |
| 8 | 30min |
| 9 | 1h |
| **TOTAL** | **~17 horas** |

---

### Cenário Realista (Alguns problemas, mas resolvíveis)
**Assumindo:**
- 20-30% dos imports precisam ajuste manual (casos complexos)
- 10-15% dos testes quebram e precisam correção
- 5-10% dos links em docs quebram
- Revisão manual necessária em pontos críticos

| Fase | Tempo Realista |
|------|----------------|
| 0 | 0h (já feito) |
| 1 | 45min |
| 2-2.4 | 6h |
| 3 | 45min |
| 4-4.1 | 4h |
| 5-5.1 | 5h |
| 6 | 1.5h |
| 7-7.1 | 7h |
| 8 | 45min |
| 9 | 1.5h |
| **TOTAL** | **~27 horas** |

---

### Cenário Pessimista (Vários problemas, revisão extensa)
**Assumindo:**
- 40-50% dos imports precisam ajuste manual
- 25-30% dos testes quebram
- 15-20% dos links quebram
- Revisão extensa necessária
- Problemas de compatibilidade com ferramentas (pytest, streamlit)
- Necessidade de refatoração adicional

| Fase | Tempo Pessimista |
|------|------------------|
| 0 | 0h (já feito) |
| 1 | 1h |
| 2-2.4 | 9h |
| 3 | 1h |
| 4-4.1 | 6h |
| 5-5.1 | 8h |
| 6 | 2h |
| 7-7.1 | 10h |
| 8 | 1h |
| 9 | 2h |
| **TOTAL** | **~40 horas** |

---

## 3. Fatores de Ajuste

### Fatores que Reduzem Tempo (-)

| Fator | Redução | Observações |
|-------|---------|-------------|
| **Automação de Imports** | -20% a -30% | Script para buscar/substituir imports (risco: falsos positivos) |
| **Testes Automatizados** | -15% a -25% | CI/CD detecta quebras rapidamente |
| **Git mv Preserva Histórico** | -5% | Não precisa rastrear arquivos manualmente |
| **Estrutura Simples** | -10% | Poucos imports circulares, dependências claras |

**Redução Máxima Estimada:** -40% (cenário ideal com automação completa)

---

### Fatores que Aumentam Tempo (+)

| Fator | Aumento | Observações |
|-------|---------|-------------|
| **Testes Quebrados** | +30% a +50% | Correção de imports, ajuste de paths, debugging |
| **Revisão Manual** | +20% a +40% | Validar cada mudança, garantir consistência |
| **Imports Complexos** | +15% a +25% | Imports relativos, imports circulares, sys.path hacks |
| **Documentação Quebrada** | +10% a +20% | Links internos, referências em múltiplos arquivos |
| **Ferramentas (pytest/streamlit)** | +10% a +15% | Ajustar PYTHONPATH, configs, paths de execução |
| **Imprevistos** | +10% a +20% | Problemas não mapeados, dependências ocultas |

**Aumento Máximo Estimado:** +100% (cenário pessimista com múltiplos problemas)

---

## 4. Recomendações

### ✅ Estratégia Recomendada

#### 1. **Fazer em Múltiplas Sessões (NÃO Sprint)**
- **Sessão 1 (4-6h):** Fases 1-2 (Estrutura + Core Essencial)
- **Pausa:** Validar sistema funcional
- **Sessão 2 (3-4h):** Fases 3-4 (CLI + Produto)
- **Pausa:** Validar app funcionando
- **Sessão 3 (4-6h):** Fases 5-6 (Testes + Scripts)
- **Pausa:** Validar testes passando
- **Sessão 4 (4-6h):** Fases 7-9 (Docs + ROADMAPs + Limpeza)
- **Total:** 4-5 sessões de trabalho focado

#### 2. **Pausar Entre Fases para Validar**
- Após cada fase crítica (2, 4, 5): rodar testes completos
- Após Fase 4: testar Streamlit manualmente
- Após Fase 5: rodar suite completa de testes
- Commits incrementais após cada validação bem-sucedida

#### 3. **Não Fazer Tudo de Uma Vez**
- **Risco:** Overwhelming, erros acumulados, difícil debugar
- **Benefício de pausar:** Problemas detectados cedo, menos retrabalho

#### 4. **Automação Parcial (Recomendado)**
- Script para buscar/substituir imports principais (`from agents.` → `from core.agents.`)
- **MAS:** Revisar manualmente casos complexos
- **NÃO automatizar:** Documentação (muitos falsos positivos)

#### 5. **Priorização**
- **Prioridade 1 (Fases 1-4):** Sistema funcional → **~12-18h realista**
- **Prioridade 2 (Fases 5-6):** Estrutura completa → **+6-8h**
- **Prioridade 3 (Fases 7-9):** Polimento → **+6-8h**

---

## 5. Riscos Identificados

### 🔴 Alto Risco
1. **Imports Circulares:** Dependências entre agents/ podem quebrar
2. **Testes Quebrados:** 73 arquivos de teste, muitos podem falhar
3. **Streamlit Paths:** App pode não encontrar módulos após mover
4. **Config Loader:** Paths hardcoded podem quebrar

### 🟡 Médio Risco
1. **Documentação:** 131 arquivos, fácil perder referências
2. **Scripts:** 28 scripts podem ter paths hardcoded
3. **pytest.ini:** Configuração pode precisar ajuste

### 🟢 Baixo Risco
1. **CLI:** Apenas 2 arquivos, baixa complexidade
2. **ROADMAPs:** 3 arquivos, baixo impacto

---

## 6. Checklist de Validação por Fase

### Após Fase 2 (Core Essencial)
- [ ] `pytest tests/unit/ -v` → Todos passando
- [ ] `pytest tests/integration/smoke/ -v` → Todos passando
- [ ] `python -m core.agents.orchestrator.router` → Import funciona
- [ ] Verificar imports: `grep -r "from agents\." .` → Nenhum resultado

### Após Fase 4 (Produto Revelar)
- [ ] `streamlit run products/revelar/app/chat.py` → App inicia
- [ ] `pytest tests/ -v` → Todos passando
- [ ] Verificar imports: `grep -r "from app\." .` → Apenas em tests/

### Após Fase 5 (Testes)
- [ ] `pytest tests/core/ -v` → Todos passando
- [ ] `pytest tests/products/revelar/ -v` → Todos passando
- [ ] Cobertura mantida (não diminuiu)

### Após Fase 7 (Documentação)
- [ ] Buscar links quebrados: `grep -r "docs/agents/" docs/` → Nenhum
- [ ] Validar links principais manualmente
- [ ] README.md atualizado

---

## 7. Conclusão

### Estimativa Final (Cenário Realista)
**Tempo Total:** **~27 horas** de trabalho focado

**Distribuição:**
- **Core (Fases 1-3):** ~7-8h
- **Produto (Fase 4):** ~4h
- **Testes (Fase 5):** ~5h
- **Scripts (Fase 6):** ~1.5h
- **Documentação (Fase 7):** ~7h
- **Polimento (Fases 8-9):** ~2h

### Recomendação Final
**Fazer em 4-5 sessões de 4-6 horas cada, com pausas entre fases críticas.**

**Não tentar fazer em sprint único.** Risco de burnout e erros acumulados.

---

**Versão:** 1.0  
**Última Atualização:** 2025-01-XX  
**Próxima Revisão:** Após conclusão da Fase 2 (ajustar estimativas baseado em experiência real)

