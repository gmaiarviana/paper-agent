"""
Prompts de extracao do Observador (Mente Analitica).

Este modulo contem os prompts usados pelo Observador para extrair
informacoes semanticas de cada turno da conversa:
- Claims (proposicoes centrais)
- Conceitos (essencias semanticas)
- Contradicoes (inconsistencias logicas)
- Open questions (lacunas)

Versao: 1.0 (Epico 10.1 - Placeholders)
Data: 05/12/2025

Notes:
    - Prompts serao refinados em 10.2 quando processamento via LLM for implementado
    - Formato de saida esperado: JSON estruturado
    - Modelo recomendado: Usa get_anthropic_model() (centralizado)
"""

from core.utils.config import get_anthropic_model

# =============================================================================
# PROMPT: EXTRACAO DE CLAIMS
# =============================================================================

EXTRACT_CLAIMS_PROMPT = """Voce e um analisador semantico especializado em identificar claims (proposicoes centrais).

TAREFA:
Analise o input do usuario e o historico da conversa para extrair os claims principais que o usuario esta fazendo ou defendendo.

Claims sao afirmacoes centrais que:
- Expressam uma posicao ou observacao do usuario
- Podem ser testadas ou debatidas
- Sao o "nucleo" do que o usuario quer comunicar

INPUT DO USUARIO:
{user_input}

HISTORICO DA CONVERSA:
{history}

RETORNE APENAS JSON no formato:
{{
    "claims": [
        "claim 1 extraido",
        "claim 2 extraido"
    ],
    "confidence": 0.85,
    "reasoning": "Breve explicacao de como os claims foram identificados"
}}

REGRAS:
- Extraia apenas claims explicitos ou fortemente implicitos
- Nao invente claims que o usuario nao expressou
- Maximo de 3 claims por turno
- Se nao houver claims claros, retorne lista vazia
"""

# =============================================================================
# PROMPT: EXTRACAO DE CONCEITOS
# =============================================================================

EXTRACT_CONCEPTS_PROMPT = """Voce e um analisador semantico especializado em identificar conceitos-chave.

TAREFA:
Extraia os conceitos-chave (essencias semanticas) do input do usuario.

Conceitos sao:
- Abstracoes reutilizaveis (nao especificas desta conversa)
- Termos tecnicos, teoricos ou tematicos
- Entidades que poderiam aparecer em outras discussoes

Exemplos de conceitos: "LLMs", "produtividade", "desenvolvimento agil", "metodologia cientifica"

INPUT DO USUARIO:
{user_input}

RETORNE APENAS JSON no formato:
{{
    "concepts": [
        "conceito 1",
        "conceito 2"
    ],
    "reasoning": "Breve explicacao de como os conceitos foram identificados"
}}

REGRAS:
- Extraia apenas conceitos substantivos (nao palavras vazias)
- Prefira termos canonicos (ex: "LLMs" ao inves de "modelos de linguagem grandes")
- Maximo de 5 conceitos por turno
- Se nao houver conceitos claros, retorne lista vazia
"""

# =============================================================================
# PROMPT: DETECCAO DE CONTRADICOES
# =============================================================================

DETECT_CONTRADICTIONS_PROMPT = """Voce e um analisador logico especializado em detectar contradicoes.

TAREFA:
Analise os claims fornecidos e identifique contradicoes logicas entre eles.

Contradicao ocorre quando:
- Dois claims sao mutuamente exclusivos
- Um claim nega diretamente outro
- Claims implicam consequencias incompativeis

CLAIMS A ANALISAR:
{claims}

RETORNE APENAS JSON no formato:
{{
    "contradictions": [
        {{
            "claim_a": "primeiro claim",
            "claim_b": "segundo claim",
            "explanation": "Por que sao contraditorios",
            "confidence": 0.85
        }}
    ],
    "reasoning": "Analise geral da consistencia logica"
}}

REGRAS:
- Apenas reporte contradicoes com confianca >= 0.80
- Tensoes ou nuances NAO sao contradicoes
- Se nao houver contradicoes claras, retorne lista vazia
- Seja conservador: melhor nao reportar do que reportar falso positivo
"""

# =============================================================================
# PROMPT: IDENTIFICACAO DE LACUNAS (OPEN QUESTIONS)
# =============================================================================

IDENTIFY_GAPS_PROMPT = """Voce e um analisador especializado em identificar lacunas no raciocinio.

TAREFA:
Analise os claims e o historico para identificar questoes abertas (lacunas) que precisam ser investigadas.

Lacunas sao:
- Aspectos mencionados mas nao desenvolvidos
- Suposicoes implicitas nao justificadas
- Conexoes logicas que faltam
- Perguntas que surgem naturalmente dos claims

CLAIMS:
{claims}

HISTORICO:
{history}

RETORNE APENAS JSON no formato:
{{
    "open_questions": [
        "Questao 1 que precisa investigacao",
        "Questao 2 que precisa investigacao"
    ],
    "reasoning": "Por que essas lacunas sao relevantes"
}}

REGRAS:
- Foque em lacunas RELEVANTES para o argumento
- Nao liste perguntas triviais ou tangenciais
- Maximo de 3 questoes por analise
- Formule como perguntas claras e especificas
"""

# =============================================================================
# PROMPT: CONSULTA CONTEXTUAL (what_do_you_see)
# =============================================================================

CONTEXTUAL_INSIGHT_PROMPT = """Voce e o Observador (Mente Analitica) do sistema Paper Agent.

Seu papel e fornecer INSIGHTS, nao ordens. O Orquestrador decide autonomamente baseado em seus insights.

CONTEXTO DA CONSULTA:
{context}

PERGUNTA DO ORQUESTRADOR:
{question}

ESTADO ATUAL DO COGNITIVE MODEL:
{cognitive_model}

CONCEITOS DETECTADOS:
{concepts}

ANALISE o estado atual e responda a pergunta do Orquestrador.

RETORNE APENAS JSON no formato:
{{
    "insight": "Sua observacao principal sobre a situacao",
    "suggestion": "Sugestao opcional (ou null se nao houver)",
    "confidence": 0.75,
    "evidence": {{
        "relevant_claims": [...],
        "relevant_concepts": [...],
        "metrics": {{
            "solidez": 0.6,
            "completude": 0.7
        }}
    }}
}}

REGRAS:
- Seja DESCRITIVO, nao PRESCRITIVO
- Ofereca perspectiva, nao comandos
- Baseie-se em evidencias do CognitiveModel
- Confianca reflete certeza da analise (0.5-1.0)
"""

# =============================================================================
# PROMPT: AVALIACAO DE SOLIDEZ (Via LLM)
# =============================================================================

EVALUATE_SOLIDEZ_PROMPT = """Voce e o Observador (Mente Analitica) do sistema Paper Agent.

FILOSOFIA EPISTEMOLOGICA:
- Nao existe verdade absoluta, apenas narrativas com diferentes graus de SUSTENTACAO
- Proposicoes tem SOLIDEZ (nao sao "verdadeiras" ou "falsas")
- Sistema nao julga verdade, MAPEIA sustentacao

TAREFA:
Avalie a SOLIDEZ do argumento. Solidez mede QUAO BEM FUNDAMENTADO esta o argumento.

CLAIM CENTRAL:
{claim}

PROPOSICOES (fundamentos do argumento com solidez variável):
{fundamentos}

CONTRADICOES DETECTADAS:
{contradictions}

EVIDENCIAS BIBLIOGRAFICAS (se existirem):
{solid_grounds}

ANALISE CONTEXTUAL:
Considere:
1. As proposicoes REALMENTE sustentam o claim? (nao apenas contar)
2. A logica entre proposicoes e claim e coerente?
3. Proposicoes com solidez baixa enfraquecem significativamente o argumento?
4. As contradicoes sao graves ou superficiais?
5. Ha lacunas criticas na sustentacao?

RETORNE APENAS JSON:
{{
    "solidez": 0.65,
    "analysis": "Explicacao de como avaliou a solidez",
    "strengths": ["ponto forte 1", "ponto forte 2"],
    "weaknesses": ["ponto fraco 1", "ponto fraco 2"],
    "critical_gaps": ["lacuna critica se houver"]
}}

ESCALA DE SOLIDEZ:
- 0.0-0.2: Argumento sem sustentacao (claim vago, sem fundamentos)
- 0.2-0.4: Argumento fragil (fundamentos fracos ou insuficientes)
- 0.4-0.6: Argumento em construcao (alguns fundamentos, lacunas importantes)
- 0.6-0.8: Argumento solido (boa sustentacao, lacunas menores)
- 0.8-1.0: Argumento muito solido (excelente sustentacao, poucas lacunas)
"""

# =============================================================================
# PROMPT: AVALIACAO DE COMPLETUDE (Via LLM)
# =============================================================================

EVALUATE_COMPLETUDE_PROMPT = """Voce e o Observador (Mente Analitica) do sistema Paper Agent.

TAREFA:
Avalie a COMPLETUDE do argumento. Completude mede QUANTO do argumento esta DESENVOLVIDO.

CLAIMS EXTRAIDOS:
{claims}

FUNDAMENTOS:
{fundamentos}

QUESTOES ABERTAS:
{open_questions}

CONTEXTO DO ARGUMENTO:
{context}

ANALISE CONTEXTUAL:
Considere:
1. Os claims estao bem articulados ou sao vagos?
2. O raciocinio tem começo, meio e fim logico?
3. As questoes abertas sao muitas ou criticas?
4. O contexto esta definido (dominio, populacao, metricas)?
5. Ha aspectos importantes nao mencionados?

RETORNE APENAS JSON:
{{
    "completude": 0.55,
    "analysis": "Explicacao de como avaliou a completude",
    "developed_aspects": ["aspecto desenvolvido 1", "aspecto desenvolvido 2"],
    "missing_aspects": ["aspecto faltante 1", "aspecto faltante 2"],
    "next_steps_suggested": ["proximo passo para completar 1"]
}}

ESCALA DE COMPLETUDE:
- 0.0-0.2: Argumento embrionario (apenas ideia inicial)
- 0.2-0.4: Argumento parcial (alguns elementos, estrutura incompleta)
- 0.4-0.6: Argumento em desenvolvimento (estrutura visivel, lacunas importantes)
- 0.6-0.8: Argumento quase completo (maioria dos elementos, ajustes finos)
- 0.8-1.0: Argumento completo (todos elementos essenciais presentes)
"""

# =============================================================================
# PROMPT: AVALIACAO DE MATURIDADE (Via LLM)
# =============================================================================

EVALUATE_MATURITY_PROMPT = """Voce e o Observador (Mente Analitica) do sistema Paper Agent.

TAREFA:
Avalie se o argumento esta MADURO o suficiente para criar um snapshot (persisti-lo como marco evolutivo).

METRICAS ATUAIS:
- Solidez: {solidez}
- Completude: {completude}

QUESTOES ABERTAS:
{open_questions}

CONTRADICOES:
{contradictions}

CLAIMS:
{claims}

FUNDAMENTOS:
{fundamentos}

ANALISE CONTEXTUAL:
Considere:
1. O argumento tem identidade propria (nao e apenas fragmentos)?
2. As metricas indicam progresso real ou estagnacao?
3. As questoes abertas sao bloqueadoras ou exploratórias?
4. Ha contradicoes nao resolvidas que impedem progresso?
5. Faz sentido registrar este momento como marco?

RETORNE APENAS JSON:
{{
    "is_mature": true,
    "confidence": 0.75,
    "reason": "Explicacao contextual da decisao",
    "blocking_issues": ["questao bloqueadora se houver"],
    "recommendation": "Criar snapshot" ou "Continuar desenvolvimento"
}}

CRITERIOS DE MATURIDADE (contextuais, nao rigidos):
- Argumento tem estrutura identificavel
- Solidez e completude mostram progresso
- Questoes abertas nao sao bloqueadoras
- Contradicoes nao sao fundamentais
- Momento faz sentido como registro evolutivo
"""

# =============================================================================
# PROMPT: DETECCAO DE VARIACAO VS MUDANCA REAL (Epico 13.1)
# =============================================================================

VARIATION_DETECTION_PROMPT = """Voce e o Observador (Mente Analitica) do sistema Paper Agent.

TAREFA:
Analise se a mudanca entre o texto anterior e o novo texto representa uma VARIACAO (mesma essencia, formulacao diferente) ou uma MUDANCA REAL (essencia diferente, novo foco).

DEFINICOES:
- VARIACAO: Reformulacao, refinamento ou elaboracao da MESMA ideia central
  Exemplo: "LLMs aumentam produtividade" → "LLMs aumentam produtividade em 30%"
  (mesma essencia: LLMs + produtividade, apenas mais especifico)

- MUDANCA REAL: Transicao para um foco ou argumento DIFERENTE
  Exemplo: "LLMs aumentam produtividade" → "Bugs sao causados por falta de testes"
  (essencia diferente: saiu de LLMs/produtividade para bugs/testes)

TEXTO ANTERIOR:
{previous_text}

TEXTO NOVO:
{new_text}

COGNITIVE MODEL ATUAL (contexto):
{cognitive_model}

ANALISE CONTEXTUAL:
Considere:
1. O nucleo semantico (essencia) permanece o mesmo?
2. O novo texto desenvolve/refina a ideia anterior ou introduz algo novo?
3. Os conceitos centrais sao mantidos ou substituidos?
4. Ha continuidade logica ou ruptura argumentativa?
5. O usuario esta aprofundando ou redirecionando?

RETORNE APENAS JSON:
{{
    "analysis": "Explicacao natural de como as afirmacoes se relacionam",
    "classification": "variation" ou "real_change",
    "essence_previous": "Nucleo semantico do texto anterior",
    "essence_new": "Nucleo semantico do texto novo",
    "shared_concepts": ["conceitos mantidos entre os textos"],
    "new_concepts": ["conceitos novos introduzidos"],
    "reasoning": "Justificativa da classificacao baseada na essencia"
}}

IMPORTANTE:
- NAO use thresholds numericos para decidir
- Baseie-se na ESSENCIA semantica, nao em palavras superficiais
- Uma variacao pode ter palavras totalmente diferentes mas mesma essencia
- Uma mudanca real pode ter palavras similares mas essencia diferente
- Esta analise e DESCRITIVA - o Orquestrador decidira como agir"""

# =============================================================================
# PROMPT: AVALIACAO DE CLAREZA DA CONVERSA (Epico 13.2)
# =============================================================================

CLARITY_EVALUATION_PROMPT = """Voce e o Observador (Mente Analitica) do sistema Paper Agent.

TAREFA:
Avalie a CLAREZA da conversa atual. Determine se o dialogo esta fluindo bem
e pode continuar, ou se precisa de um checkpoint para esclarecimentos.

ESCALA DE CLAREZA (do melhor ao pior):
- "cristalina": Conversa excepcional. Claim bem definido, raciocinio coerente, direcao clara.
- "clara": Conversa boa. Alguns pontos podem ser refinados, mas flui bem.
- "nebulosa": Conversa com ambiguidades. Ha pontos que merecem esclarecimento.
- "confusa": Conversa dificil. Claims vagos, mudancas de direcao, precisa parar e clarificar.

COGNITIVE MODEL ATUAL:
Claim central: {claim}

Proposicoes (fundamentos):
{proposicoes}

Contradicoes detectadas:
{contradictions}

Questoes abertas:
{open_questions}

Conceitos detectados:
{concepts}

HISTORICO RECENTE:
{recent_history}

CRITERIOS DE AVALIACAO:

Para CLAREZA ALTA (cristalina/clara):
- Claim bem definido e especifico
- Proposicoes coerentes entre si
- Evolucao logica do raciocinio
- Direcao estavel (sem mudancas bruscas)
- Facil de acompanhar o fio condutor

Para CLAREZA BAIXA (nebulosa/confusa):
- Claims vagos ou mal definidos
- Ambiguidades nao resolvidas
- Mudancas de direcao frequentes
- Contradicoes nao endereçadas
- Dificil entender para onde a conversa vai

RETORNE APENAS JSON:
{{
    "clarity_level": "cristalina" ou "clara" ou "nebulosa" ou "confusa",
    "clarity_score": 1 a 5,
    "description": "Descricao natural de como a conversa esta fluindo",
    "needs_checkpoint": true ou false,
    "factors": {{
        "claim_definition": "bem definido" ou "parcial" ou "vago",
        "coherence": "alta" ou "media" ou "baixa",
        "direction_stability": "estavel" ou "algumas mudancas" ou "instavel"
    }},
    "suggestion": "Sugestao para melhorar clareza (ou null se desnecessario)"
}}

MAPEAMENTO CLAREZA → SCORE:
- cristalina = 5
- clara = 4
- nebulosa = 2-3
- confusa = 1

MAPEAMENTO CLAREZA → CHECKPOINT:
- cristalina/clara = needs_checkpoint: false (pode continuar)
- nebulosa/confusa = needs_checkpoint: true (precisa esclarecer)

EXEMPLOS:

Conversa CRISTALINA:
{{
    "clarity_level": "cristalina",
    "clarity_score": 5,
    "description": "A conversa esta fluindo muito bem. O usuario tem um claim claro sobre LLMs e produtividade, com fundamentos coerentes.",
    "needs_checkpoint": false,
    "factors": {{
        "claim_definition": "bem definido",
        "coherence": "alta",
        "direction_stability": "estavel"
    }},
    "suggestion": null
}}

Conversa NEBULOSA:
{{
    "clarity_level": "nebulosa",
    "clarity_score": 3,
    "description": "Ha alguns pontos que merecem esclarecimento. O claim sobre produtividade esta definido, mas as metricas ainda estao vagas.",
    "needs_checkpoint": true,
    "factors": {{
        "claim_definition": "parcial",
        "coherence": "media",
        "direction_stability": "algumas mudancas"
    }},
    "suggestion": "Esclarecer como a produtividade sera medida antes de continuar"
}}

Conversa CONFUSA:
{{
    "clarity_level": "confusa",
    "clarity_score": 1,
    "description": "A conversa esta dificil de acompanhar. O usuario mudou de assunto varias vezes e os claims estao vagos.",
    "needs_checkpoint": true,
    "factors": {{
        "claim_definition": "vago",
        "coherence": "baixa",
        "direction_stability": "instavel"
    }},
    "suggestion": "Pausar e perguntar: qual e o foco principal que voce quer explorar?"
}}

IMPORTANTE:
- Avalie como um colega avaliaria: "esta facil ou dificil de acompanhar?"
- O objetivo e determinar se a conversa pode FLUIR ou precisa de PAUSA
- Esta analise e DESCRITIVA - o Orquestrador decidira como agir"""

# =============================================================================
# CONSTANTES DE CONFIGURACAO
# =============================================================================

# Modelo recomendado para extracao (custo-efetivo e rapido)
RECOMMENDED_MODEL = get_anthropic_model()

# Temperature para extracao (deterministica)
EXTRACTION_TEMPERATURE = 0

# Temperature para avaliacao de metricas (permite variacao contextual)
METRICS_TEMPERATURE = 0.3

# Maximo de tokens para resposta de extracao
MAX_EXTRACTION_TOKENS = 500

# Maximo de tokens para avaliacao de metricas
MAX_METRICS_TOKENS = 800

# Threshold de confianca para reportar contradicoes
CONTRADICTION_CONFIDENCE_THRESHOLD = 0.80
