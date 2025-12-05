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
    - Modelo recomendado: claude-3-5-haiku-20241022 (custo-efetivo)
"""

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
# CONSTANTES DE CONFIGURACAO
# =============================================================================

# Modelo recomendado para extracao (custo-efetivo e rapido)
RECOMMENDED_MODEL = "claude-3-5-haiku-20241022"

# Temperature para extracao (deterministica)
EXTRACTION_TEMPERATURE = 0

# Maximo de tokens para resposta de extracao
MAX_EXTRACTION_TOKENS = 500

# Threshold de confianca para reportar contradicoes
CONTRADICTION_CONFIDENCE_THRESHOLD = 0.80
