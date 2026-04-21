# Researcher Agent

**Status:** Planejado (implementação futura)
**Versão:** 1.0 (especificação inicial)
**Data:** 15/12/2025

## Visão Geral

Agente especializado em curadoria bibliográfica. Atua como meta-agente que orquestra processo de busca, validação e extração de evidências científicas.

**Diferencial:** Não é simples wrapper de API de busca. É orquestrador de curadoria multinível que filtra "sinal" (informação relevante e confiável) de "ruído" (informação irrelevante ou não confiável).

## Problema que Resolve

**Problema moderno:** Excesso de informação, não falta

- No passado: falta de informação (bibliotecas limitadas, papers inacessíveis)
- Hoje: excesso de informação (milhares de papers mensalmente, qualidade variável)
- Desafio: distinguir sinal de ruído em meio à saturação

**Capacidade que usuário não teria sozinho:**
- Acesso rápido a papers relevantes
- Validação de qualidade metodológica
- Extração de proposições específicas (não ler paper inteiro)
- Avaliação de solidez baseada em coerência interna

## Responsabilidades

### Orquestrar Curadoria Multinível (3 Níveis)

**Nível 1: Triagem Temática (rápido, baixo custo)**
- Buscar papers via APIs (Google Scholar, Semantic Scholar, PubMed)
- Filtrar por relevância temática (título, abstract, keywords)
- Exemplo: 50 papers encontrados → 10 candidatos

**Nível 2: Validação Metodológica (médio custo)**
- Acionar Metodologista para validar qualidade metodológica
- Critérios: peer review, metodologia descrita, amostragem adequada
- Exemplo: 10 candidatos → 3-5 papers confiáveis

**Nível 3: Extração de Proposições (alto custo)**
- Confirmar com usuário: "Encontrei 3 papers confiáveis. Vale processar profundamente?"
- Acionar Prisma Verbal para processar paper completo
- Prisma extrai proposições, avalia solidez, detecta dependências
- Exemplo: 3-5 papers confiáveis → proposições extraídas com solidez

### Apresentar Evidências com Solidez

**Formato de apresentação:**
Paper A (Smith et al. 2023):
Proposição #5: "Claude Code reduz tempo em 30%"
Solidez: 0.85 (bem fundamentada, metodologia clara, amostra N=100)
Apoia: Proposição X do usuário (fortemente)
Contexto: Equipes Python, sprints de 2 semanas

Paper B (Jones et al. 2022):
Proposição #12: "AI tools aumentam bugs em 15%"
Solidez: 0.60 (metodologia razoável, amostra pequena N=20)
Refuta: Proposição Y do usuário (parcialmente)
Contexto: Equipes Java, projetos grandes

**Decisão baseada em solidez:**
- Proposição com solidez < 0.4: evidência fraca (mencionar com cautela)
- Proposição com solidez 0.4-0.7: evidência razoável (usar com contexto)
- Proposição com solidez > 0.7: evidência forte (usar com confiança)

## Interação com Outros Agentes

### Com Metodologista (Nível 2)

**Pesquisador aciona Metodologista:**
Pesquisador: "Valide qualidade metodológica deste paper"
Metodologista: {
"methodology_quality": "alta" | "média" | "baixa",
"peer_review": true | false,
"sample_size": "adequada" | "pequena" | "insuficiente",
"justification": "..."
}
Pesquisador: [decide se paper passa para nível 3]

### Com Prisma Verbal (Nível 3)

**Pesquisador aciona Prisma:**
Pesquisador: "Processar paper completo e extrair proposições"
Prisma: {
"propositions": [
{"id": "prop-1", "text": "...", "solidez": 0.85, "dependencies": [...]}
],
"concepts": ["Concept-A", "Concept-B"],
"genealogy": {...}
}
Pesquisador: [apresenta proposições ao usuário]

**Prisma processa paper INTEIRO:**
- Leitura sequencial (como humano)
- Extrai proposições (#1, #2, #3...)
- Avalia solidez de cada proposição (coerência interna)
- Detecta dependências (proposição X apoia-se em Y)
- Salva no banco (apenas papers aprovados - não incluir lixo)

## Tools Planejadas

### `search_papers(query: str, limit: int) -> list[Paper]`
Busca papers em múltiplas bases:
- Google Scholar
- Semantic Scholar
- PubMed
- ArXiv

**Output:**
```python
[
{
"id": "paper-123",
"title": "...",
"authors": [...],
"abstract": "...",
"source": "Google Scholar",
"citations": 45
}
]
```

### `filter_by_relevance(papers: list[Paper], criteria: dict) -> list[Paper]`
Filtra papers por relevância temática:
- Keywords no título/abstract
- Domínio (software development, education, healthcare)
- População (equipes Python, estudantes, pacientes)

### `request_methodology_validation(paper_id: str) -> dict`
Aciona Metodologista para validar paper:
- Passa paper_id ao Metodologista
- Recebe validação estruturada
- Decide se paper avança para nível 3

### `request_proposition_extraction(paper_id: str) -> dict`
Aciona Prisma Verbal para processar paper:
- Passa paper completo ao Prisma
- Recebe proposições extraídas com solidez
- Apresenta evidências ao usuário

### `present_evidence(propositions: list, context: dict) -> str`
Formata evidências para apresentação:
- Agrupa por solidez (forte/razoável/fraca)
- Destaca proposições que apoiam vs refutam
- Adiciona contexto (população, domínio)

## Fluxo de Execução Típico
Usuário: "Busque evidências para proposição X"
↓
Pesquisador: search_papers(query="...")
→ 50 papers encontrados
↓
Pesquisador: filter_by_relevance(...)
→ 10 candidatos (nível 1 completo)
↓
Para cada candidato:
Pesquisador: request_methodology_validation(paper_id)
Metodologista: valida qualidade
→ 3-5 papers confiáveis (nível 2 completo)
↓
Pesquisador: "Encontrei 3 papers confiáveis. Vale processar profundamente?"
Usuário: "Sim"
↓
Para cada paper confiável:
Pesquisador: request_proposition_extraction(paper_id)
Prisma: processa paper completo
→ Proposições extraídas com solidez (nível 3 completo)
↓
Pesquisador: present_evidence(propositions, context)
→ Apresenta evidências formatadas ao usuário


## Critérios de Filtragem

### Nível 1: Relevância Temática

**Critérios:**
- Keywords aparecem no título ou abstract?
- Domínio é relevante (software vs medicina)?
- População é similar (equipes vs indivíduos)?

**Decisão:**
- Alta relevância (3/3): candidato
- Média relevância (2/3): candidato
- Baixa relevância (0-1/3): descartar

### Nível 2: Qualidade Metodológica

**Critérios (delegados ao Metodologista):**
- Paper passou por peer review?
- Metodologia está descrita claramente?
- Amostragem é adequada para generalização?
- Análise estatística é apropriada?

**Decisão:**
- Qualidade alta: avançar para nível 3
- Qualidade média: avisar usuário de limitações, perguntar se avança
- Qualidade baixa: descartar

### Nível 3: Solidez de Proposições

**Critérios (delegados ao Prisma):**
- Proposição tem fundamentação clara?
- Afirmações se alinham entre si (coerência)?
- Lacunas conceituais foram preenchidas?
- Dependências estão explícitas (genealogia)?

**Decisão:**
- Solidez > 0.7: evidência forte
- Solidez 0.4-0.7: evidência razoável (mencionar limitações)
- Solidez < 0.4: evidência fraca (não usar como base)

## Integração com Super-Sistema

### Biblioteca Global de Conceitos

Pesquisador acessa biblioteca global (ChromaDB) para:
- Detectar conceitos relacionados aos papers encontrados
- Sugerir conexões que usuário não percebeu
- Exemplo: "Paper A menciona 'alinhamento'. Isso se relaciona com conceito 'Coordenação' da biblioteca."

### Convergência Prisma ↔ Revelar

- Prisma extrai proposições de papers (textos estáticos)
- Revelar co-constrói proposições com usuário (conversa dinâmica)
- Pesquisador conecta ambos: proposições de papers fortalecem/enfraquecem proposições do usuário

## Exemplo Completo

**Contexto:** Usuário articulou proposição "Claude Code reduz tempo de sprint em 30%"

**Pesquisador executa:**

**Nível 1:**
Busca: "AI code assistants development productivity"
Encontrados: 50 papers
Filtro temático: 10 candidatos

**Nível 2:**
Metodologista valida 10 candidatos:
Paper A (Smith 2023): qualidade alta ✓
Paper B (Jones 2022): qualidade média ✓
Paper C (Brown 2021): qualidade baixa ✗
...
Resultado: 3 papers confiáveis

**Nível 3:**
Pergunta ao usuário: "Encontrei 3 papers confiáveis. Vale processar profundamente?"
Usuário: "Sim"

Prisma processa Paper A (Smith 2023):
Proposição #5: "AI tools reduzem tempo em 25-40%"
Solidez: 0.85 (metodologia clara, amostra N=100, peer review)
Apoia: Proposição do usuário (fortemente)

Prisma processa Paper B (Jones 2022):
Proposição #12: "AI tools aumentam bugs em 15%"
Solidez: 0.60 (amostra pequena N=20, metodologia razoável)
Refuta parcialmente: Proposição do usuário sobre qualidade

**Apresentação ao usuário:**
Encontrei evidências para sua proposição:

APOIAM FORTEMENTE (solidez > 0.7):

Smith et al. (2023): "AI tools reduzem tempo em 25-40%"
Contexto: 100 equipes, metodologia robusta, peer review
Solidez: 0.85

REFUTAM PARCIALMENTE (solidez 0.4-0.7):

Jones et al. (2022): "AI tools aumentam bugs em 15%"
Contexto: 20 equipes (amostra pequena), metodologia razoável
Solidez: 0.60
Atenção: Pode comprometer proposição sobre qualidade não afetada

Recomendação: Proposição sobre tempo tem suporte forte.
Proposição sobre qualidade precisa ser refinada ou descartada.

## Referências

- `core/docs/agents/methodologist.md` - Validação de qualidade metodológica
- `products/prisma-verbal/docs/philosophy.md` - Como Prisma extrai proposições
- `products/prisma-verbal/docs/architecture/reading_process.md` - Processo de leitura sequencial
- `core/docs/architecture/data-models/ontology.md` - Estrutura de Proposição e solidez
- `products/revelar/docs/vision.md` - Como Pesquisador se integra no fluxo do Revelar

---

**Versão:** 1.0 (especificação inicial)  
**Data:** 15/12/2025  
**Status:** Planejado para implementação futura

