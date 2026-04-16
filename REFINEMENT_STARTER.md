# Refinement Starter Pack

> **📌 Objetivo:** Lista autoritativa de arquivos para arrastar ao Claude Web durante refinamento de épicos.

## 📋 Contexto Base (sempre)

Arraste estes 3 arquivos em qualquer refinamento:

1. **CONSTITUTION.md** - Princípios, responsabilidades, processo
2. **ARCHITECTURE.md** - Estado técnico atual consolidado  
3. **core/ROADMAP.md** - Épicos e melhorias do core compartilhado

## 🎯 + Produto Específico (escolher um)

Adicione o roadmap do produto sendo refinado:

- **Revelar (atual):** products/revelar/ROADMAP.md
- **Ensaio (próximo):** products/ensaio/ROADMAP.md
- **Prisma Verbal (futuro):** products/prisma-verbal/ROADMAP.md

**Total:** 4 arquivos (~1.200 linhas, ~5.000 tokens)

## 📚 Documentos Consultados Sob Demanda

O Claude Web consulta automaticamente via `docs/CONTEXT_INDEX.md`:

- **Visão estratégica:** `docs/product/vision.md`
- **Specs técnicas:** `core/docs/architecture/`, `core/docs/agents/`
- **Processo de implementação:** `docs/process/implementation/`

## ⚠️ Arquivos Removidos do Contexto Inicial

- **README.md** - Útil para setup, não para refinamento estratégico
- **planning_guidelines.md** - Movido para docs/process/refinement/

---

**Versão:** 1.0  
**Data:** 2025-01-27  
**Substitui:** Listas inconsistentes em CONSTITUTION §7, planning_guidelines, CONTEXT_INDEX
