# Skills

> **📌 Localização:** `skills/` (raiz do repo)
> **📌 Público:** Claude Code Web (executor autônomo) e dev (operador).
> **📌 Pré-requisito de leitura:** `docs/process/autonomous/` (overview, workflow, delivery).

---

## 1. O QUE É UMA SKILL

Skill = bloco reutilizável de instruções que substitui aprovações explícitas do dev no **modo autônomo**. Cada skill tem um papel único e atua como gate dentro do fluxo definido em `docs/process/autonomous/workflow.md`.

**Não confundir:**
- Skills **não são agentes do core** (Orquestrador, Metodologista, etc). Agentes vivem em `core/agents/` e processam conteúdo do usuário.
- Skills atuam sobre o **processo de desenvolvimento** (planejamento, qualidade, entrega).

---

## 2. CATEGORIAS

### Skills de Processo (este diretório)
Conduzem o fluxo autônomo de desenvolvimento. Substituem a interação manual dev ↔ Cursor.

| Skill | Etapa do fluxo | Prompt operacional | Responsabilidade |
|-------|---------------|-------------------|------------------|
| **planning** | Antes do Dev | `skills/planning/skill.md` | Quebra funcionalidade em tasks, clarifica TUDO antes de implementar |
| **qa** | Após Dev | `skills/qa/skill.md` | Valida testes, sintaxe, imports, comportamento — decisão binária |
| **tl** | Após QA | `skills/tl/skill.md` | Valida arquitetura, padrões, aderência ao ROADMAP técnico — decisão binária |
| **po** | Após TL | `skills/po/skill.md` | Valida critérios de aceite e detecta gold plating — decisão binária |
| **validation** | Após PO | `skills/validation/skill.md` | Prepara branch + comandos para o dev validar |

### Protocolo de carregamento (OBRIGATÓRIO no modo autônomo)
1. O dispatch (`docs/process/autonomous/dispatch.md`) lista os 5 skill.md a carregar em sequência.
2. Antes de executar cada gate, Claude Web **abre o `skill.md` correspondente e segue na íntegra** — não resumir, não adaptar.
3. Cada skill registra evidência de carregamento em `docs/process/current_implementation.md` → "Evidências de carregamento de skill" imediatamente ao iniciar.
4. Cada skill (exceto Planning) verifica a evidência do gate anterior como parte do gate de entrada. Falta de evidência = fluxo corrompido → aborta e devolve ao dev.

### Skills de Implementação (não existem ainda)
Eventuais blocos reutilizáveis para tarefas técnicas recorrentes (ex: criar novo agente, adicionar tool LangGraph). Quando surgirem, viverão sob `skills/<dominio>/` e serão indexados aqui.

---

## 3. COMO AS SKILLS SE COMUNICAM

Skills não se invocam diretamente. Elas se comunicam via **artefatos compartilhados**:

- **`docs/process/current_implementation.md`** — plano + status de cada gate. Planning escreve; demais skills leem e atualizam.
- **Branch git `feature/X.Y-nome`** — código + commits. Dev escreve; QA/TL/PO leem; Validation entrega.
- **ROADMAP.md** (core ou produto) — fonte da verdade da funcionalidade. Todas leem; PO confronta com a entrega.

**Regra:** se uma skill precisa de informação que outra produziu, ela busca no artefato — nunca assume estado de memória entre skills.

---

## 4. ESTRUTURA DE UMA SKILL

Cada skill segue o mesmo layout para facilitar reuso:

```
skills/<nome>/
├── README.md           # Quando usar, como funciona, exemplos resumidos
├── skill.md            # Prompt/instruções carregadas pelo executor
├── examples/           # (opcional) Casos concretos de uso
└── templates/          # (opcional) Templates de saída
```

- `README.md` é leitura para humanos (dev entender quando a skill aplica).
- `skill.md` é o **prompt operacional** carregado pelo Claude Code Web durante o fluxo autônomo.
- `examples/` ilustram comportamento esperado em casos reais.
- `templates/` padronizam outputs consumidos por humanos ou outras skills.

---

## 5. SKILLS DISPONÍVEIS

| Skill | Status | Documentação |
|-------|--------|-------------|
| **planning** | ✅ Disponível | [planning/README.md](planning/README.md) |
| **qa** | ✅ Disponível | [qa/README.md](qa/README.md) |
| **tl** | ✅ Disponível | [tl/README.md](tl/README.md) |
| **po** | ✅ Disponível | [po/README.md](po/README.md) |
| **validation** | ✅ Disponível | [validation/README.md](validation/README.md) |

> Fluxo completo do modo autônomo agora habilitado: Planning → Dev → QA → TL → PO → Validation, com gates binários automáticos no meio.

---

## 6. PRINCÍPIOS PARA CRIAR NOVAS SKILLS

- ✅ **Responsabilidade única:** uma skill = um gate ou uma tarefa bem delimitada
- ✅ **Sem duplicação:** referencie `docs/process/`, `docs/ARCHITECTURE.md`, ROADMAPs — não copie
- ✅ **Saída observável:** toda skill produz artefato concreto (arquivo, commit, mensagem padronizada)
- ✅ **Falha ruidosa:** ao reprovar/bloquear, registre motivo em `current_implementation.md` e devolva à etapa anterior
- ✅ **PT-BR + padrões do projeto:** seguir CONSTITUTION e padrões de documentação existentes

---

**Ver também:**
- Visão do modo autônomo → `docs/process/autonomous/overview.md`
- Fluxo entre skills → `docs/process/autonomous/workflow.md`
- Disparo e validação pelo dev → `docs/process/autonomous/delivery.md`
- Template de dispatch → `docs/process/autonomous/dispatch.md`
