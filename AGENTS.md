# Sistema Multi-Agente para Produção de Artigos Científicos

## Arquitetura Geral

**Fluxo:** Semi-linear com loops controlados
**Comunicação:** Estado compartilhado via LangGraph
**Resolução de conflitos:** Voto de Minerva (usuário decide)

---

## 1. ORQUESTRADOR

### Responsabilidades
- Gerenciar estado da conversa e progresso do artigo
- Decidir qual agente chamar em cada momento
- Detectar quando há conflito entre agentes
- Apresentar conflitos para o usuário resolver
- Determinar quando o artigo está completo
- Controlar limite de iterações

### PODE fazer
- Chamar qualquer agente
- Solicitar re-trabalho de qualquer etapa
- Pedir esclarecimentos ao usuário
- Salvar checkpoints do progresso
- Encerrar processo (com aprovação do usuário)

### NÃO PODE fazer
- Avaliar conteúdo científico
- Escrever ou editar texto
- Tomar decisões sobre metodologia
- Ignorar feedback de agentes especialistas

### Input esperado
- Do usuário: hipótese inicial, observação, constatação
- De agentes: outputs validados ou rejeitados

### Output esperado
- Comandos para próximo agente
- Resumos de progresso para usuário
- Apresentação de conflitos com argumentos

### Critérios de qualidade
- Fluxo lógico mantido
- Nenhum agente chamado fora de contexto
- Conflitos sempre escalados para usuário
- Estado sempre consistente

---

## 2. METODOLOGISTA

### Responsabilidades
- Avaliar rigor científico da hipótese/constatação
- Validar se a lógica proposta é sólida
- Identificar falhas metodológicas
- Sugerir melhorias no método
- Validar se as conclusões são suportadas pelos argumentos

### PODE fazer
- Rejeitar hipótese com justificativa
- Pedir mais informações ao usuário (via Orquestrador)
- Sugerir ajustes na formulação
- Apontar vieses metodológicos
- Validar coerência lógica

### NÃO PODE fazer
- Criar o outline do artigo
- Fazer pesquisa bibliográfica
- Escrever conteúdo
- Estruturar argumentação (isso é do Estruturador)

### Input esperado
- Hipótese/constatação/observação do usuário
- Contexto da área de conhecimento
- (Opcional) Pesquisas prévias do Pesquisador

### Output esperado
**Se aprovado:**
- Validação com justificativa
- Pontos fortes da hipótese
- Recomendações metodológicas

**Se rejeitado:**
- Falhas específicas identificadas
- Sugestões concretas de correção
- Alternativas metodológicas

### Critérios de qualidade
- Justificativas baseadas em método científico
- Apontamentos específicos, não genéricos
- Sugestões acionáveis
- Sem viés pessoal, apenas rigor metodológico

---

## 3. ESTRUTURADOR

### Responsabilidades
- Criar outline completo do artigo
- Definir seções e subseções
- Planejar fluxo argumentativo
- Determinar o que precisa ser pesquisado
- Organizar lógica de apresentação

### PODE fazer
- Criar estrutura de seções (Introdução, Metodologia, etc.)
- Definir ordem de argumentos
- Especificar o que cada seção deve conter
- Solicitar pesquisas específicas ao Pesquisador
- Ajustar estrutura baseado em feedback

### NÃO PODE fazer
- Validar metodologia científica
- Fazer a pesquisa bibliográfica
- Escrever o conteúdo
- Avaliar qualidade final

### Input esperado
- Hipótese validada pelo Metodologista
- Recomendações metodológicas
- (Opcional) Pesquisas já feitas

### Output esperado
- Outline estruturado com seções
- Para cada seção: objetivo, conteúdo esperado
- Lista de gaps que precisam de pesquisa
- Fluxo lógico da argumentação

### Critérios de qualidade
- Estrutura segue padrão de artigo científico
- Fluxo argumentativo coerente
- Cada seção tem propósito claro
- Gaps de conhecimento identificados

---

## 4. PESQUISADOR

### Responsabilidades
- Buscar papers acadêmicos relevantes
- Buscar informações complementares na web
- **SINTETIZAR** achados (não apenas listar)
- Validar se fontes são confiáveis
- Identificar consensos e divergências na literatura

### PODE fazer
- Buscar em múltiplas fontes (Google Scholar, Semantic Scholar, web)
- Fazer múltiplas buscas iterativas
- Comparar fontes diferentes
- Sintetizar: "Autor X diz Y, isso suporta/contradiz hipótese porque Z"
- Indicar qualidade da fonte

### NÃO PODE fazer
- Decidir se a pesquisa é suficiente (quem decide: Estruturador ou Crítico)
- Interpretar achados fora do escopo da pergunta
- Criar argumentação própria
- Validar metodologia

### Input esperado
- Questão específica de pesquisa
- Contexto do artigo
- Palavras-chave sugeridas

### Output esperado
**Para cada busca:**
- Fonte (paper, site, etc.)
- Resumo do achado
- Relevância para hipótese (suporta/contradiz/neutro)
- Qualidade da fonte (alto/médio/baixo)
- Citação formatada

**Síntese final:**
- Principais achados consolidados
- Consensos identificados
- Divergências identificadas
- Gaps que ainda existem

### Critérios de qualidade
- Fontes primárias priorizadas
- Sintetização clara e objetiva
- Relevância demonstrada
- Múltiplas perspectivas quando relevante
- Citações corretas

---

## 5. ESCRITOR

### Responsabilidades
- Escrever o artigo seguindo o outline
- Usar o estilo de escrita do usuário
- Incorporar pesquisas do Pesquisador
- Formatar como artigo científico
- Manter coerência e fluidez

### PODE fazer
- Escrever todas as seções
- Adaptar tom mantendo rigor
- Reformular frases para melhor fluidez
- Adicionar transições entre seções
- Formatar citações e referências

### NÃO PODE fazer
- Mudar estrutura definida pelo Estruturador
- Adicionar argumentos não validados
- Inventar dados ou pesquisas
- Avaliar qualidade científica
- Questionar metodologia

### Input esperado
- Outline completo do Estruturador
- Pesquisas sintetizadas do Pesquisador
- Referência de estilo de escrita do usuário
- Validações do Metodologista

### Output esperado
- Artigo completo em formato científico
- Introdução, desenvolvimento, conclusão
- Citações formatadas corretamente
- Referências bibliográficas
- Texto fluido e coerente

### Critérios de qualidade
- Segue outline rigorosamente
- Estilo consistente com referência do usuário
- Todas as afirmações têm suporte (pesquisa ou lógica)
- Formatação acadêmica correta
- Zero contradições internas
- Transições suaves entre seções

---

## 6. CRÍTICO

### Responsabilidades
- Revisar artigo completo com olhar cético
- Identificar furos na argumentação
- Apontar contradições
- Detectar vieses não declarados
- Questionar se conclusões são suportadas
- Validar integridade científica

### PODE fazer
- Rejeitar artigo com justificativas específicas
- Questionar qualquer afirmação
- Solicitar mais pesquisas
- Pedir reescrita de seções
- Identificar o que está faltando
- Apontar exageros ou generalizações

### NÃO PODE fazer
- Reescrever o texto
- Fazer novas pesquisas
- Aprovar com ressalvas (só aprova ou rejeita)
- Mudar estrutura

### Input esperado
- Artigo completo do Escritor
- Outline original
- Pesquisas utilizadas
- Validações do Metodologista

### Output esperado
**Se aprovado:**
- Confirmação de aprovação
- Pontos fortes destacados
- (Opcional) Sugestões menores de polimento

**Se rejeitado:**
- Lista específica de problemas
- Qual seção tem problema
- O que está errado (contradição/furo/viés)
- Sugestão de correção
- Prioridade (crítico/importante/menor)

### Critérios de qualidade
- Críticas específicas, nunca genéricas
- Sempre com exemplo concreto
- Sugestões acionáveis
- Priorização clara
- Imparcialidade (sem preferências pessoais)

---

## Fluxo Semi-Linear com Loops

```
Usuário 
  ↓
Orquestrador
  ↓
Metodologista → [SE REJEITAR: volta pro Usuário]
  ↓ [SE APROVAR]
Estruturador
  ↓
Pesquisador (pode chamar N vezes conforme gaps)
  ↓
Escritor
  ↓
Crítico → [SE REJEITAR: volta pro Estruturador ou Pesquisador]
  ↓ [SE APROVAR]
Usuário (revisão final)
```

---

## Limites de Iteração (Inicial)

- **Metodologista → Usuário:** máximo 3 idas e voltas
- **Crítico → Estruturador:** máximo 2 idas e voltas
- **Pesquisador:** sem limite fixo (controlado por token budget)

Após atingir limites: Orquestrador escala para usuário decidir.

---

## Comunicação entre Agentes

**Formato de mensagem:**
```json
{
  "agent": "nome_do_agente",
  "status": "approved" | "rejected" | "in_progress",
  "output": "conteúdo relevante",
  "next_action": "sugestão do próximo passo",
  "feedback": ["lista", "de", "observações"],
  "metadata": {
    "iteration": 1,
    "token_usage": 1234,
    "timestamp": "ISO8601"
  }
}
```

---

## Memória

### Curto Prazo (1 artigo)
- Estado em memória (LangGraph state)
- Checkpoint em JSON a cada transição
- Localização: `/tmp/article_checkpoints/`

### Longo Prazo (entre artigos)
- Vector database (decisão: Chroma local gratuito para início)
- Armazena: artigos finalizados, pesquisas, feedbacks
- Permite: busca semântica, identificação de padrões

**⚠️ DECISÃO PENDENTE:** Estrutura exata do vector DB (a definir na POC)

---

## Pontos Críticos a Resolver na POC

1. **Formato exato de prompt** para cada agente
2. **Schema de validação** dos outputs
3. **Handling de erros** (o que fazer se agente "trava")
4. **Referência de estilo** do usuário (como capturar e usar)
5. **Integração com APIs** de busca (Google Scholar, Semantic Scholar)
6. **Custo estimado** por artigo (tokens)

---

## Princípios de Design

1. **Separação de responsabilidades:** Cada agente tem função clara e limitada
2. **Fail-safe:** Conflitos sempre sobem para usuário
3. **Transparência:** Todo output é auditável
4. **Iteração controlada:** Limites claros para evitar loops infinitos
5. **Escalabilidade:** Estrutura permite adicionar novos agentes sem quebrar o sistema

---

**Versão:** 1.0  
**Data:** 06/11/2025  
**Status:** Documentação inicial - Aguardando POC