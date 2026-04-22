# Delivery Autônomo: Disparo + Validação Final

> **📌 Localização:** `docs/process/autonomous/`
> **📌 Público:** Dev (operador do modo autônomo).
> **📌 Pré-requisito:** funcionalidade pertence a épico em `🔍 Detalhes definidos` no ROADMAP (checklist `docs/process/refinement/autonomous_readiness.md` aplicado).

---

## 1. COMO DISPARAR (PELA MANHÃ)

### Passos
1. **Escolher funcionalidade:** abrir ROADMAP (core ou produto) e identificar `X.Y` em épico `🔍 Detalhes definidos`.
2. **Abrir Claude Code Web:** [claude.ai/code](https://claude.ai/code) no repositório `paper-agent`.
3. **Preencher dispatch:** copiar `docs/process/autonomous/dispatch.md` e substituir placeholders:
   - `[Funcionalidade X.Y]` → identificador real (ex: `11.3`)
   - `feature/X.Y-nome` → nome real da branch (ex: `feature/11.3-snapshot-detection`)
4. **Disparar:** enviar o prompt e fechar a sessão. As skills assumem dali pra frente.

### Critérios para disparar com segurança
- ✅ Funcionalidade tem critérios de aceite claros no ROADMAP
- ✅ Dependências técnicas implementadas e validadas
- ✅ Padrão de implementação conhecido (segue épicos anteriores)
- ✅ Sem decisões arquiteturais em aberto

> Se algum critério acima falhar → use o **fluxo manual** (Claude Web + Cursor).

---

## 2. AO RECEBER NOTIFICAÇÃO DE TASK PRONTA (À NOITE)

A RTE Skill notifica o dev no formato definido em [development/delivery.md](../development/delivery.md):

```
✅ Branch pronta! Você pode criar o PR pela interface do GitHub.

📋 Comandos de validação (copie e cole):
[comandos com nome real da branch]

🔍 Validações esperadas:
[critérios de aceite + comportamentos a observar]
```

### O que fazer
1. **Ler relatório dos gates:** verificar `docs/process/current_implementation.md` (status QA/TL/PO)
2. **Rodar comandos de validação local** (próxima seção)
3. **Validar critérios de aceite** manualmente
4. **Decidir:** aprovar merge OU devolver com feedback

---

## 3. COMANDOS DE VALIDAÇÃO LOCAL

A RTE Skill já entrega os comandos prontos. Estrutura típica:

```bash
# 1. Baixar branch
git fetch origin
git checkout feature/X.Y-nome
git pull origin feature/X.Y-nome

# 2. Preparar ambiente
source venv/bin/activate           # Linux/Mac
# .\venv\Scripts\Activate.ps1     # Windows
pip install -r requirements.txt   # se houver mudanças em deps

# 3. Rodar testes
pytest tests/core/unit/ -v
pytest tests/core/integration/ -v -m integration   # se aplicável

# 4. Rodar aplicação (se mudou interface)
[comando específico do produto: streamlit run ..., python -m core.tools.cli.chat, etc]
```

### O que verificar
- ✅ Testes passam (unit + integration aplicáveis)
- ✅ Aplicação sobe sem erros
- ✅ Comportamento conforme critérios de aceite do ROADMAP
- ✅ Sem warnings críticos no console

---

## 4. CRITÉRIOS PARA APROVAR MERGE

Aprove o merge quando **TODOS** estes critérios forem atendidos:

**Gates automáticos (verificar em `current_implementation.md`):**
- [ ] QA Skill: aprovado
- [ ] TL Skill: aprovado (ou aprovado com observações justificadas)
- [ ] PO Skill: todos os critérios de aceite cobertos

**Validação local do dev:**
- [ ] Comandos de validação rodaram sem erro
- [ ] Critérios de aceite do ROADMAP observados manualmente
- [ ] Comportamentos "não deve" não ocorreram
- [ ] Documentação estrutural atualizada (ARCHITECTURE/ROADMAP/README quando aplicável)

**Caso algum critério falhe:**
- ❌ **Não mergeie.** Devolva com feedback no Claude Code Web (nova rodada autônoma) OU traga para Cursor (fluxo manual) se exigir decisão arquitetural.

---

## 5. CRIAÇÃO DO PR

Mesma regra do fluxo manual:
- ✅ Dev cria PR **manualmente** pela interface do GitHub
- ✅ Template (`.github/PULL_REQUEST_TEMPLATE.md`) é aplicado automaticamente
- ❌ Skills **não** criam PR via `gh pr create`

---

## 6. RETROSPECTIVA (OPCIONAL)

Após mergear, anotar em `.claudecode.md` quando aplicável:
- Bloqueios encontrados pelas skills
- Padrões que precisam ficar mais explícitos no ROADMAP/ARCHITECTURE
- Casos em que o modo autônomo não foi adequado

Esses inputs alimentam refinamentos futuros das skills e dos guidelines.

---

**Ver também:**
- Visão geral do modo autônomo → [overview.md](overview.md)
- Detalhe das skills (Scrum Master/QA/TL/PO/RTE) → [workflow.md](workflow.md)
- Template de dispatch → `docs/process/autonomous/dispatch.md`
- Convenções operacionais (segredos, granularidade de commits) → [session_conventions.md](session_conventions.md)
- Mensagem final padrão (compartilhada com fluxo manual) → [development/delivery.md](../development/delivery.md)
