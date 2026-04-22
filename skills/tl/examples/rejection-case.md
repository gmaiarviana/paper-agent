# Exemplo: TL Rejeitou

> **Contexto:** caso típico (anonimizado) onde a TL Skill rejeitou apesar de QA ter aprovado, por dois desvios arquiteturais.

---

## Funcionalidade

`14.2 - Exportação de Pensamentos para Markdown` (já aprovada por QA)

## Diff Resumido

```
core/utils/markdown_exporter.py                  | +110 -0
products/revelar/app/components/export_button.py |  +45 -0
products/revelar/app/utils/format_helpers.py     |  +38 -0
core/agents/orchestrator/nodes.py                |  +12 -0
tests/core/unit/test_markdown_exporter.py             |  +85 -0
```

(QA aprovou: testes verdes, sintaxe OK, lógica nova coberta.)

---

## Verificações Feitas e Desvios Detectados

### 3.1 Estrutura e Nomenclatura — ⚠️ DESVIO #1
- ❌ `products/revelar/app/utils/format_helpers.py` duplica funções de formatação de markdown que **já existem** em `core/utils/markdown_exporter.py`
- Padrão esperado: util genérico vive em `core/utils/`; produto importa de lá
- Referência: `docs/ARCHITECTURE.md` (seção "Separação core vs produto") + `.claudecode.md` (Princípio de Responsabilidade Única)

### 3.2 Contratos e Dependências
- ✅ Sem ciclo
- ✅ Pydantic usado conforme convenção

### 3.3 Aderência ao ROADMAP — ⚠️ DESVIO #2
- ❌ `core/agents/orchestrator/nodes.py` recebeu mudança nova (+12 linhas) para acoplar exportação ao fluxo conversacional
- Mas o ROADMAP da 14.2 só pede **botão na interface** + utilitário de exportação — **não** menciona integração ao orquestrador
- Padrão esperado: orquestrador não muda fora do escopo do épico; nova integração exige refinamento prévio
- Referência: `docs/ROADMAP.md` (funcionalidade 14.2) + CONSTITUTION §1 ("Funcionalidades detalhadas aceleram implementação")

### 3.4 Documentação Estrutural
- ✅ `README.md` do produto atualizado com novo botão
- ✅ Sem mudança em docs/ARCHITECTURE.md (não havia decisão arquitetural nova legítima)

### 3.5 Anti-duplicação
- ❌ Já contemplado no Desvio #1

### 3.6 Débito Técnico
- ⚠️ TODO em `nodes.py:88`: `# TODO: simplificar quando export virar evento`
  - Vago, sem issue, sem prazo, sem critério de "simplificação"
- (não conta como desvio próprio porque o desvio raiz é o #2 — remover a mudança em `nodes.py` elimina o TODO)

---

## Decisão Registrada em `current_implementation.md`

```
TL ❌ 2026-04-15 (rejeição #1)

Desvios encontrados:

1. [DUPLICAÇÃO + DOMÍNIO ERRADO] products/revelar/app/utils/format_helpers.py
   Funções de formatação duplicam core/utils/markdown_exporter.py.
   Padrão esperado: produto importa do core; sem reimplementar util genérico.
   Referência: docs/ARCHITECTURE.md "Separação core vs produto"

2. [ESCOPO EXTRAPOLADO] core/agents/orchestrator/nodes.py (+12 linhas)
   Mudança no orquestrador não está no escopo da 14.2 (ROADMAP pede botão + util).
   Padrão esperado: orquestrador não muda fora do escopo; nova integração exige refinamento.
   Referência: docs/ROADMAP.md (14.2) + CONSTITUTION §1

Ação: devolver ao Dev. NÃO seguir para PO.
```

---

## Como o Dev Resolveu

1. Removeu `products/revelar/app/utils/format_helpers.py` e fez o componente importar de `core/utils/markdown_exporter`
2. Reverteu mudanças em `core/agents/orchestrator/nodes.py` (e o TODO que vinha junto)
3. Re-disparou o ciclo

QA voltou a aprovar (seguia passando), TL aprovou na 2ª rodada. Custo de 1 ciclo extra — mas evitou push de débito real para o repo.

---

## O QUE ESTE EXEMPLO ENSINA

- ✅ **QA verde ≠ pronto.** TL é gate independente: testes podem passar e arquitetura ainda estar errada.
- ✅ **Toda rejeição tem padrão de referência.** A TL não diz "feio" — diz "viola padrão X documentado em Y".
- ✅ **Escopo é um padrão também.** Mexer fora do escopo do ROADMAP é desvio arquitetural, não só de produto.
- ✅ **Débito segue o desvio.** O TODO vago caiu junto com a mudança que o introduziu — não foi necessário rejeitar separadamente.
