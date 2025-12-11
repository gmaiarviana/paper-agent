# Filosofia do Sistema - Core Universal

## Visão Geral

Este documento descreve a filosofia e princípios universais do core, aplicáveis a todos os produtos.

## Filosofia Epistemológica

Paper Agent é guiado por uma epistemologia específica: não existe verdade absoluta, apenas narrativas com diferentes graus de sustentação. Isso significa:
- Sistema não julga verdade, mapeia sustentação
- Proposições têm solidez (não são "verdadeiras" ou "falsas")
- Pesquisa fortalece/enfraquece, não valida/refuta
- Ver detalhes em `core/docs/vision/epistemology.md`

## Memory em Camadas

O sistema utiliza uma arquitetura de memória inspirada na memória humana, onde informação recente é mais acessível que informação antiga:

**3 Camadas de Memória:**

- **Superficial (recente):** resumos condensados, busca rápida, últimos dias/semanas. Acesso imediato para contexto conversacional atual.
- **Intermediária:** snapshots de CognitiveModel, evolução da ideia ao longo do tempo. Acesso moderado, útil para revisar progresso.
- **Profunda (antiga):** mensagens literais, acesso mais lento, pode ser compactada periodicamente. Arquivo histórico completo.

**Degradação temporal natural:**
Informação de ontem está mais acessível que de mês passado. O sistema prioriza recência sem perder histórico, seguindo padrão natural de memória humana.

**Futuro:**
Compactação/arquivamento periódico (ex: anual) para manter performance sem perder rastreabilidade completa.

## Super-Sistema: Core Universal

> **Nota:** Para arquitetura completa do super-sistema, consulte `../architecture/vision/super_system.md`.

Paper Agent não é apenas um produto isolado. É a **primeira aplicação** de um super-sistema com core universal que serve múltiplos produtos.

**Produtos planejados:**
- **Paper-agent:** Auxílio em produção científica (atual)
- **Fichamento:** Catálogo de livros com ideias extraídas (futuro próximo)
- **Rede Social:** Conexão por cosmovisões compartilhadas (futuro distante)

**Core compartilhado:**
- Ontologia (Conceito, Ideia, Argumento)
- Modelo cognitivo (claim → fundamentos (com solidez variável))
- Agentes (Orquestrador, Estruturador, Metodologista, Pesquisador)
- Infraestrutura (LangGraph, ChromaDB, embeddings)

Produtos são **serviços desacoplados** que consomem core via APIs.

## Visão Futura: Separação Comunicador/Orquestrador

**Status:** Conceitual, para implementação futura.

**Separação planejada (não implementada ainda):**

- **Orquestrador:** coordenação lógica, decisões, sem linguagem natural. Trabalha com estruturas de dados, estados, fluxos. Neutro e técnico.
- **Comunicador:** interface linguística, tradução para/de usuário, aplicação de personas. Responsável por toda interação em linguagem natural.

**Benefícios:**
- **Neutralidade:** Orquestrador não carrega vieses de comunicação, foca em lógica pura
- **Customização:** Diferentes comunicadores podem aplicar diferentes estilos (Sócrates, Popper, etc.) sem mudar lógica de orquestração
- **Rastreabilidade:** Decisões lógicas separadas de apresentação linguística, facilitando debug e validação

**Relação com Épico 18:**
Personas customizáveis serão implementadas no Comunicador, permitindo que usuários escolham estilos de argumentação sem afetar a coordenação interna do sistema.

**Implementação futura:**
Separação completa permitirá múltiplos canais de comunicação (web, CLI, API) todos consumindo o mesmo Orquestrador neutro.

**Resultado esperado:**
"Flecha penetrante" / "Ideia irresistível" - argumento sólido com respaldo bibliográfico, sem premissas frágeis, sem dúvidas não examinadas. Às vezes o usuário nem sabe onde quer chegar, mas ao elaborar, a clareza aparece.

**Ver detalhes sobre evolução cognitiva em:** `core/docs/vision/cognitive_model/`

## Princípios de Design

- **Inteligente, não determinístico**: adapta fluxos e respostas conforme contexto em vez de seguir roteiros fixos.
- **Colaborativo**: agentes constroem junto ao pesquisador, estimulando coautoria e reflexão crítica.
- **Transparente**: reasoning dos agentes exposto, integrando explicações curtas ou links para aprofundamento.
- **Incremental**: começa com entregáveis mínimos e expande funcionalidades à medida que aprende com o uso.
- **Escalável**: arquitetura previsa integração de novos tipos de artigo, agentes e extensões (ver `ARCHITECTURE.md` para detalhes técnicos).
- **Epistemologicamente honesto**: não existe verdade absoluta; sistema mapeia graus de sustentação baseados em evidências, não julgamentos binários de verdade/falsidade.

## Referências

- `core/docs/vision/epistemology.md` - Base filosófica detalhada
- `../architecture/vision/super_system.md` - Arquitetura do super-sistema
- `core/docs/vision/cognitive_model/` - Como pensamento evolui

