# Checklist de Execução - Épico 7.2

## 📋 Visão Geral
Este checklist guia a execução manual dos 10 cenários de validação do sistema multi-agente.

**Duração estimada:** 2-3 horas (todos os cenários)  
**Pré-requisitos:**
- [ ] Sistema rodando (`streamlit run app/chat.py`)
- [ ] Ambiente virtual ativado
- [ ] Documentação aberta: `docs/testing/epic7_validation_strategy.md`

---

## 🎯 Preparação Inicial

### Antes de Começar
- [ ] Limpar sessões antigas (opcional):
```powershell
Remove-Item $env:TEMP\paper-agent-events\events-test-*.json -ErrorAction SilentlyContinue
```
- [ ] Fazer backup do checkpoints.db (opcional):
```powershell
Copy-Item data\checkpoints.db data\checkpoints_backup.db
```
- [ ] Abrir 2 terminais: um para Streamlit, outro para coleta de logs

---

## 📝 Cenário 1: Usuário Começa Vago

### 1.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 1)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 1.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 1
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 1.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_01_usuario_vago" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 1.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_01_usuario_vago/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 1.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 2: Usuário Fornece Hipótese Completa

### 2.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 2)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 2.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 2
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 2.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_02_hipotese_completa" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 2.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_02_hipotese_completa/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 2.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 3: Metodologista Sugere Refinamento

### 3.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 3)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 3.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 3
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 3.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_03_refinamento" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 3.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_03_refinamento/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 3.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 4: Provocação Socrática - Métrica Vaga

### 4.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 4)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 4.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 4
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 4.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_04_provocacao_socratica" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 4.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_04_provocacao_socratica/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 4.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 5: Mudança de Direção

### 5.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 5)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 5.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 5
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 5.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_05_mudanca_direcao" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 5.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_05_mudanca_direcao/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 5.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 6: Reasoning Loop do Metodologista

### 6.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 6)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 6.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 6
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 6.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_06_reasoning_loop" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 6.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_06_reasoning_loop/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 6.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 7: Preservação de Contexto em Conversa Longa

### 7.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 7)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 7.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 7
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 7.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_07_preservacao_contexto" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 7.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_07_preservacao_contexto/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 7.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 8: Transição Fluida (Sem "Posso Chamar X?")

### 8.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 8)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 8.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 8
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 8.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_08_transicao_fluida" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 8.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_08_transicao_fluida/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 8.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 9: Validação Científica com Critérios

### 9.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 9)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 9.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 9
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 9.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_09_validacao_cientifica" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 9.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_09_validacao_cientifica/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 9.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 📝 Cenário 10: Bastidores Mostra Reasoning

### 10.1 Preparação
- [ ] Ler cenário completo em `docs/testing/epic7_validation_strategy.md` (CENÁRIO 10)
- [ ] Identificar input esperado
- [ ] Identificar comportamento esperado (checklist)

### 10.2 Execução
- [ ] Iniciar nova conversa no Streamlit
- [ ] Anotar Session ID (aparece na URL ou Bastidores)
- [ ] Fornecer input conforme especificado no CENÁRIO 10
- [ ] Observar comportamento do sistema
- [ ] Anotar problemas encontrados (papel ou bloco de notas)

### 10.3 Coleta de Logs
- [ ] Executar script:
```powershell
python scripts/testing/collect_scenario_logs.py `
  --scenario "cenario_10_bastidores_reasoning" `
  --session-id "[SEU_SESSION_ID]"
```
- [ ] Verificar que logs foram coletados (3 arquivos em logs/)

### 10.4 Análise
- [ ] Abrir `docs/testing/epic7_results/cenario_10_bastidores_reasoning/input.md`
- [ ] Preencher com input fornecido
- [ ] Abrir `output.md` e preencher com output observado
- [ ] Abrir `analysis.md` e preencher análise completa:
  - Comportamento observado (sucesso/parcial/falha)
  - Problemas identificados (crítico/médio/baixo)
  - Observações adicionais

### 10.5 Verificação
- [ ] Todos os arquivos do cenário estão preenchidos?
- [ ] Logs estão completos (events.json, state.json, metadata.txt)?
- [ ] Análise está clara e específica?

---

## 🎯 Finalização

### Após Executar Todos os Cenários
- [ ] Verificar que todos os 10 cenários têm logs coletados
- [ ] Verificar que todos os 10 analysis.md estão preenchidos
- [ ] Executar comando de verificação:
```powershell
Get-ChildItem -Path "docs\testing\epic7_results\*\logs" -File | Measure-Object | Select-Object Count
# Deve mostrar 30 arquivos (3 por cenário × 10 cenários)
```

### Gerar Resumo Executivo
- [ ] Abrir `docs/testing/epic7_results/summary.md`
- [ ] Preencher sumário executivo:
  - Sistema está maduro? (Sim/Não/Parcial)
  - Problemas críticos encontrados (lista)
  - Problemas médios encontrados (lista)
  - Problemas baixos encontrados (lista)
  - Recomendações prioritárias

### Próximos Passos
- [ ] Criar issue/PR com problemas críticos identificados
- [ ] Decidir se sistema está maduro para Épico 8 (automação)
- [ ] Ou: corrigir problemas críticos antes de prosseguir

---

## 💡 Dicas de Execução

### Eficiência
- Execute 2-3 cenários por sessão (não todos de uma vez)
- Faça pausas entre cenários (evita fadiga)
- Anote problemas imediatamente (não confie na memória)

### Qualidade
- Seja específico ao descrever problemas (reprodução clara)
- Inclua trechos de logs relevantes no analysis.md
- Tire screenshots se comportamento visual for relevante
- Compare comportamento observado vs esperado lado a lado

### Organização
- Complete um cenário por vez (não pule etapas)
- Verifique que análise está completa antes de prosseguir
- Mantenha checklist atualizado (marque checkboxes)

---

## 🐛 Troubleshooting

### Script de coleta falha
```powershell
# Verificar se session ID existe
Get-ChildItem $env:TEMP\paper-agent-events\events-*.json
```

### Não consigo encontrar Session ID
- Olhe na URL do Streamlit
- Ou nos Bastidores (EventBus mostra session_id)
- Ou rode: `Get-ChildItem $env:TEMP\paper-agent-events | Sort-Object LastWriteTime -Descending | Select-Object -First 5`

### Sistema não responde como esperado
- Anote como problema no analysis.md
- Continue com próximo cenário (não trave)
- Problemas são esperados (objetivo do Épico 7)

---

**Versão:** 1.0  
**Data:** Dezembro 2025  
**Relacionado:** Épico 7.2 - Executar Cenários e Coletar Logs

