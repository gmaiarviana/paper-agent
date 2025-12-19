# Modelo Cognitivo - Exemplos Práticos

> **Nota:** Para conceitos fundamentais, consulte `core/docs/vision/cognitive_model/core.md`.  
> Para processo de evolução, consulte `core/docs/vision/cognitive_model/evolution.md`.

Este documento apresenta um exemplo completo e detalhado de como o modelo cognitivo evolui durante uma conversa real.

## Exemplo Completo: "Levantamento de Obra com IA"

### Turno 1: Claim Vago, Proposições de Baixa Solidez Detectadas

**Input do usuário**: "Quero fazer um artigo sobre levantamento de obra com IA"

**Estado cognitivo**:
```python
claim: "Artigo sobre levantamento de obra com IA"
fundamentos: [
  ProposiçãoRef(
    id="prop-1",
    enunciado="Levantamento de obra é um problema relevante",
    solidez=0.30  # Baixa: apenas inferência inicial
  ),
  ProposiçãoRef(
    id="prop-2",
    enunciado="IA pode ajudar em levantamento de obra",
    solidez=0.25  # Baixa: hipótese inicial
  ),
  ProposiçãoRef(
    id="prop-3",
    enunciado="Há contribuição acadêmica possível",
    solidez=0.20  # Muito baixa: hipótese não explorada
  )
]
open_questions: [
  "O que é levantamento de obra?",
  "Como IA pode ajudar?",
  "Qual é o problema específico?",
  "Qual tipo de artigo? (empírico, revisão, teórico)"
]
contradictions: []
evidências: []
context: {
  "domain": "construction",
  "technology": "AI (unclear which)",
  "population": "not specified",
  "article_type": "unclear"
}
```

**Ação do sistema**: Orquestrador explora contexto
- "Interessante! Me conta mais: o que é levantamento de obra para você? E como você imagina que IA pode ajudar?"

### Turno 3: Claim Muda, Fundamentos Adicionados, Sistema Provoca

**Input do usuário**: "Levantamento de obra é medir quantidades de materiais. Quero usar visão computacional para automatizar"

**Estado cognitivo**:
```python
claim: "Usar visão computacional para automatizar levantamento de quantidades de materiais em obras"
fundamentos: [
  ProposiçãoRef(
    id="prop-4",
    enunciado="Levantamento de obra envolve medir quantidades de materiais",
    solidez=0.70  # Média-alta: evidência direta da conversa
  ),
  ProposiçãoRef(
    id="prop-5",
    enunciado="Visão computacional pode identificar materiais em imagens",
    solidez=0.60  # Média: conhecimento técnico geral
  ),
  ProposiçãoRef(
    id="prop-6",
    enunciado="Automatização é desejável",
    solidez=0.50  # Média: inferência do contexto
  ),
  ProposiçãoRef(
    id="prop-7",
    enunciado="Visão computacional é precisa o suficiente para quantificar materiais",
    solidez=0.35  # Baixa: hipótese não verificada
  ),
  ProposiçãoRef(
    id="prop-8",
    enunciado="Automatização reduz tempo/custo sem comprometer precisão",
    solidez=0.30  # Baixa: hipótese não verificada
  ),
  ProposiçãoRef(
    id="prop-9",
    enunciado="Há contribuição acadêmica (não é apenas aplicação direta)",
    solidez=0.25  # Baixa: hipótese não explorada
  )
]
open_questions: [
  "Qual é a precisão atual de métodos manuais?",
  "Qual é o baseline de tempo/custo?",
  "Como validar precisão da IA?",
  "Qual tipo de materiais? (tijolos, concreto, etc.)"
]
contradictions: []
evidências: []
context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, AI",
  "population": "not specified",
  "article_type": "unclear"  # Pode ser empírico (testar) ou metodológico (validar método)
}
```

**Ação do sistema**: Orquestrador provoca reflexão
- "Você mencionou automatização, mas e a PRECISÃO? Como você validaria que a IA é tão precisa quanto métodos manuais?"

### Turno 5: Pesquisador Busca, Evidências Adicionadas, Modelo Amadurece

**Input do usuário**: "Quero testar se visão computacional é mais rápida e precisa que métodos manuais"

**Estado cognitivo** (após Pesquisador buscar literatura):
```python
claim: "Visão computacional é mais rápida e precisa que métodos manuais para levantamento de quantidades de materiais em obras"
fundamentos: [
  ProposiçãoRef(
    id="prop-4",
    enunciado="Levantamento de obra envolve medir quantidades de materiais",
    solidez=0.70  # Mantida: evidência direta
  ),
  ProposiçãoRef(
    id="prop-5",
    enunciado="Visão computacional pode identificar materiais em imagens",
    solidez=0.75  # Aumentou: evidência bibliográfica adicionada
  ),
  ProposiçãoRef(
    id="prop-10",
    enunciado="Métodos manuais existem e têm precisão conhecida",
    solidez=0.80  # Alta: evidência bibliográfica forte
  ),
  ProposiçãoRef(
    id="prop-11",
    enunciado="Comparação de métodos é válida academicamente",
    solidez=0.70  # Média-alta: padrão metodológico
  ),
  ProposiçãoRef(
    id="prop-7",
    enunciado="Visão computacional é precisa o suficiente para quantificar materiais",
    solidez=0.65  # Aumentou: evidência bibliográfica (85% precisão)
  ),
  ProposiçãoRef(
    id="prop-12",
    enunciado="Resultado é generalizável para diferentes tipos de obras",
    solidez=0.40  # Média-baixa: poucas evidências
  ),
  ProposiçãoRef(
    id="prop-13",
    enunciado="Precisão da IA é suficiente para uso prático",
    solidez=0.60  # Média: evidência parcial (85% é alto, mas contexto específico)
  )
]
open_questions: [
  "Qual é o tamanho da amostra necessária?",
  "Como definir 'mais preciso'? (margem de erro aceitável?)",
  "Quais tipos de materiais testar? (tijolos, concreto, aço?)"
]
contradictions: []
evidências: [
  {
    "id": "evid-3",
    "descricao": "Zhang et al. (2022) aplicaram YOLO para detecção de materiais com 85% de precisão",
    "fonte": "doi:10.1234/construction-ai",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-5", "prop-7", "prop-13"]
  },
  {
    "id": "evid-4",
    "descricao": "Revisão sistemática de 20 estudos mostra erro médio de 7.5% em levantamentos manuais",
    "fonte": "doi:10.5678/manual-survey",
    "forca": "forte",
    "tipo": "estudo",
    "apoia": ["prop-10"]
  }
]
# Solidez de prop-5, prop-7 e prop-13 aumentou após adicionar evid-3
# Solidez de prop-10 aumentou após adicionar evid-4
context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, YOLO, deep learning",
  "population": "construction projects (not specified: residential, commercial, etc.)",
  "metrics": "speed (time), accuracy (error margin)",
  "article_type": "empirical"  # Agora claro: quer testar hipótese
}
```

**Ação do sistema**: Orquestrador apresenta resultado
- "Temos uma boa base! Encontrei estudos relevantes. Validei o desenho experimental dessa comparação: [resultado]. Faz sentido?"
[Bastidores: 🔬 Metodologista validou → 🎯 Orquestrador curou]

### Turno 7: Modelo Maduro, Pronto para Estruturação

**Estado cognitivo** (após Metodologista validar):
```python
claim: "Visão computacional (YOLO) é mais rápida (redução de 60% no tempo) e mais precisa (erro de 3% vs 7.5% manual) que métodos manuais para levantamento de quantidades de tijolos em obras residenciais"

fundamentos: [
  ProposiçãoRef(
    id="prop-4",
    enunciado="Levantamento de obra envolve medir quantidades de materiais",
    solidez=0.70  # Mantida
  ),
  ProposiçãoRef(
    id="prop-14",
    enunciado="Visão computacional (YOLO) pode identificar tijolos em imagens",
    solidez=0.80  # Alta: evidências + validação metodológica
  ),
  ProposiçãoRef(
    id="prop-10",
    enunciado="Métodos manuais têm erro médio de 7.5%",
    solidez=0.80  # Alta: evidência bibliográfica forte
  ),
  ProposiçãoRef(
    id="prop-11",
    enunciado="Comparação experimental é válida academicamente",
    solidez=0.75  # Alta: validação metodológica
  ),
  ProposiçãoRef(
    id="prop-15",
    enunciado="Obras residenciais são contexto representativo",
    solidez=0.65  # Média-alta: justificativa metodológica
  ),
  ProposiçãoRef(
    id="prop-16",
    enunciado="Resultado é generalizável para outros materiais",
    solidez=0.35  # Baixa: hipótese futura, poucas evidências
  )
]

open_questions: []  # Todas respondidas

contradictions: []  # Nenhuma detectada

evidências: [
  # ... (mesmo do turno 5, mais evidências adicionadas)
]

context: {
  "domain": "construction, quantity surveying",
  "technology": "computer vision, YOLO, deep learning",
  "population": "residential construction projects",
  "metrics": "speed (time reduction %), accuracy (error margin %)",
  "article_type": "empirical"
}
```

**Ação do sistema**: Apresentação de resultado
- "Hipótese validada! Organizei em uma questão de pesquisa estruturada: [resultado]. Podemos seguir com: 1) definir desenho experimental, 2) pesquisar literatura, ou 3) algo diferente?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]

## Análise do Exemplo

### Evolução do Claim

1. **Turno 1**: Vago e genérico ("Artigo sobre levantamento de obra com IA")
2. **Turno 3**: Mais específico, mas ainda exploratório ("Usar visão computacional para automatizar")
3. **Turno 5**: Hipótese clara com comparação ("Visão computacional é mais rápida e precisa que métodos manuais")
4. **Turno 7**: Claim maduro com métricas específicas ("YOLO é mais rápida (60% redução) e mais precisa (3% vs 7.5%)")

### Evolução dos Fundamentos

- **Início**: Poucas proposições com baixa solidez (0.20-0.30)
- **Meio**: Mais proposições adicionadas, algumas com solidez média (0.50-0.70)
- **Final**: Proposições principais com alta solidez (0.70-0.80), algumas hipóteses futuras mantidas com baixa solidez (0.35)

### Evolução das Evidências

- **Início**: Nenhuma evidência bibliográfica
- **Meio**: Evidências adicionadas pelo Pesquisador, vinculadas a proposições específicas
- **Final**: Evidências suficientes para sustentar proposições principais

### Evolução do Contexto

- **Início**: Domínio genérico ("construction"), tecnologia vaga ("AI")
- **Meio**: Domínio específico ("quantity surveying"), tecnologia específica ("YOLO, deep learning")
- **Final**: Contexto completo com população, métricas e tipo de artigo definidos

## Referências

- `core/docs/vision/cognitive_model/core.md` - Conceitos fundamentais (artefatos, responsabilidades)
- `core/docs/vision/cognitive_model/evolution.md` - Processo de evolução do pensamento
- `core/docs/vision/epistemology.md` - Base filosófica (proposições, solidez, evidências)

