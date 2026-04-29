# Lições Aprendidas — Implementação do Revelar

Lições aprendidas implementando o Revelar (sistema conversacional com LLMs). Migrado de `docs/process/implementation/quality_rules.md` em PROTO-WORKFLOW-FAXINA, 2026-04-29.

---

## Sistemas Conversacionais com LLMs

**Debug estruturado > Testes unitários:**
- SEMPRE crie ferramentas de observabilidade (logs detalhados, rastreamento de decisões) ANTES de escrever testes
- Testes unitários não capturam bugs de fluxo multi-turn
- Ferramentas de debug revelam causa raiz em minutos vs horas

**Orientação > Prescrição em prompts:**
- Prompts com 50+ linhas de regras IF-THEN transformam LLM em script
- PREFIRA: código robusto (tolera variações) + prompt minimalista (1-3 parágrafos)
- EVITE: regras rígidas que eliminam autonomia do LLM
- Para sistemas inteligentes: flexibilidade > determinismo

**Preservação de contexto:**
- Reconheça variações naturais do LLM (`"not operationalized"`, `"undefined"`) como valores vagos
- Não dependa apenas do LLM retornar valores padronizados
- Código deve ser resiliente a variações linguísticas

## Validação e Testes

**Validação incremental:**
- Commits separados (infraestrutura → fix parcial → fix completo) aceleram debug
- Facilita rollback e análise histórica
- Cada commit deve ter descrição clara do que resolve

**Cenários de teste:**
- Escreva cenários baseados em hipótese inicial
- Execute e observe comportamento REAL do sistema
- Ajuste cenários OU sistema conforme necessário
- Não tenha medo de ajustar cenários se comportamento real for razoável

## Arquitetura e Design

**Visão do produto define solução técnica:**
- SEMPRE pergunte: "Essa solução está alinhada com a visão do produto?" ANTES de implementar
- Soluções tecnicamente corretas podem conflitar com experiência desejada
- Exemplo: Regras rígidas vs "facilitador inteligente"

**Quando evitar automação completa:**
- Para análise de qualidade conversacional, humano + LLM > automação
- Automação completa perde contexto e qualidade de insights
- PREFIRA: ferramentas que estruturam dados para análise, não que tomam decisões
