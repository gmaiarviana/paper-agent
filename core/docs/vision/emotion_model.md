# Modelo de Embedding Emocional - Visão

## 1. Visão Geral

**O Que É:**
Modelo que mapeia textos (argumentos, evidências) para espaço vetorial emocional contínuo, capturando essências emocionais que transcendem categorias racionais.

**Por Que É Diferencial:**
- Sistemas tradicionais: categorizam emoções ("alegria", "tristeza", "raiva")
- Este sistema: captura essência emocional em espaço latente sem rótulos
- Analogia: Word2Vec para emoções

**Conexão Filosófica:**
Extensão natural de "Essências transcendem palavras" (ver `system_philosophy.md`):
- Conceitos: "cooperação", "dharma", "harmonia" → mesma essência semântica
- Emoções: "empatia visceral", "compaixão silenciosa", "identificação" → mesma essência emocional

---

## 2. Problema com Categorias Fixas

### Limitações de Categorização Racional

**Abordagem tradicional:**
```python
emocoes = ["alegria", "tristeza", "raiva", "medo", "surpresa", "nojo"]
# ou variações mais sofisticadas:
emocoes = ["empatia", "urgência", "esperança", "nostalgia", "confiança"]
```

**Problemas:**
1. **Reducionismo:** Emoções complexas não cabem em rótulos
2. **Fronteiras artificiais:** Onde termina "empatia" e começa "compaixão"?
3. **Subjetividade cultural:** "Saudade" não tem tradução direta
4. **Combinações:** "Alegria melancólica" - como categorizar?

### Solução: Espaço Latente

```python
# Em vez de:
emocao = "empatia"

# Temos:
emocao_vetor = [0.23, -0.87, 0.45, 0.12, ..., -0.34]  # 128-512 dimensões
# Cada dimensão captura aspecto da essência emocional
# Dimensões NÃO têm rótulos
# Emoções similares ficam próximas no espaço
```

**Benefícios:**
1. **Gradações naturais:** Espectro contínuo, não bins discretos
2. **Combinações:** Vetores podem representar emoções complexas
3. **Similaridade:** Cosseno captura proximidade emocional
4. **Universalidade:** Transcende barreiras linguísticas/culturais

---

## 3. Metodologia de Treino

### Fase 1: Coleta Manual (Fundação)

**Processo:**
1. Humanos leem textos (argumentos, parágrafos)
2. Descrevem SUBJETIVAMENTE que emoção o texto desperta
3. Descrição é em linguagem natural, não categorias

**Exemplo de anotação:**
```
Texto: "Mudei de São Paulo pro interior. A ansiedade que me
acompanhava há 5 anos simplesmente... sumiu."

Anotação humana: "Desperta esperança silenciosa, identificação
com sofrimento passado, vontade de transformação.
Sensação de alívio vicário."
```

**Características:**
- Alto custo (tempo humano)
- Alta qualidade (nuances capturadas)
- Fundação para próximas fases

### Fase 2: Semi-Automatizado (Escala)

**Processo:**
1. Modelo inicial treinado com dados da Fase 1
2. Modelo sugere vetores emocionais para textos novos
3. Humanos validam/corrigem sugestões
4. Loop de feedback refina modelo

**Exemplo:**
```
Texto novo: "Depois de 3 meses meditando, percebi que o problema
não era a cidade - era eu correndo de mim mesmo."

Modelo sugere: vetor [0.45, -0.23, 0.78, ...]
Tradução aproximada: "reflexão profunda, vulnerabilidade, insight"

Humano valida: "Sim, mas falta capturar a coragem de admitir erro"
Modelo ajusta: vetor [0.45, -0.23, 0.78, 0.31, ...]  # dimensão ajustada
```

**Características:**
- Custo médio (humano valida, não cria do zero)
- Qualidade alta (feedback humano preservado)
- Escala 10-100x maior que Fase 1

### Fase 3: Automatizado (Produção)

**Processo:**
1. Modelo generaliza padrões de abstração
2. Detecta essências emocionais sem supervisão
3. Humano audita amostragens (não 100%)
4. Modelo auto-melhora com uso

**Exemplo:**
```
Usuário descreve: "Quero que leitor sinta um incômodo
silencioso que cresce devagar"

Modelo:
1. Gera vetor emocional da descrição
2. Busca argumentos com vetores similares
3. Rankeia por similaridade cosseno
4. Apresenta top 5 para usuário

Usuário aceita 3, rejeita 2
Modelo aprende: ajusta mapeamento
```

**Características:**
- Baixo custo (automático com auditoria)
- Qualidade monitorada (métricas de satisfação)
- Escala ilimitada

---

## 4. Arquitetura Conceitual

### Componentes

```
┌─────────────────────────────────────────────────────┐
│                  Emotion Model                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐      ┌─────────────┐              │
│  │   Encoder   │      │   Decoder   │              │
│  │   (texto →  │      │   (vetor →  │              │
│  │    vetor)   │      │   descrição)│              │
│  └──────┬──────┘      └──────┬──────┘              │
│         │                    │                      │
│         ▼                    ▼                      │
│  ┌─────────────────────────────────────┐           │
│  │      Espaço Latente Emocional       │           │
│  │      (128-512 dimensões)            │           │
│  │                                     │           │
│  │   [vetor A] ●────────● [vetor B]   │           │
│  │              \      /               │           │
│  │               \    /                │           │
│  │                ●                    │           │
│  │            [vetor C]                │           │
│  │                                     │           │
│  └─────────────────────────────────────┘           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Encoder (Texto → Vetor)

**Input:** Texto do argumento/evidência
**Output:** Vetor no espaço latente emocional

**Processo conceitual:**
1. Tokenização do texto
2. Encoding semântico (transformer-based)
3. Projeção para espaço emocional (camada específica)
4. Normalização do vetor

### Decoder (Vetor → Descrição) - Opcional

**Input:** Vetor no espaço latente
**Output:** Descrição em linguagem natural

**Uso:** Debugging, explicabilidade, validação

### Similarity Search

**Input:** Vetor da mensagem (intenção do usuário)
**Output:** Top-K argumentos mais similares

**Processo:**
1. Recebe vetor emocional da mensagem
2. Calcula similaridade cosseno com todos argumentos
3. Rankeia por similaridade
4. Retorna top-K

---

## 5. Coleta de Dados

### Fonte 1: Anotações Diretas

Humanos anotam textos com descrições emocionais.

**Formato:**
```json
{
  "texto": "Mudei de SP pro interior...",
  "anotacao": "Esperança silenciosa, identificação com sofrimento...",
  "anotador_id": "user_123",
  "confianca": 0.85
}
```

### Fonte 2: Feedback Implícito

Usuários aceitam/rejeitam sugestões do sistema.

**Formato:**
```json
{
  "mensagem_vetor": [0.23, -0.87, ...],
  "argumento_id": "arg_456",
  "argumento_vetor": [0.21, -0.82, ...],
  "acao": "aceito",  // ou "rejeitado"
  "usuario_id": "user_789"
}
```

### Fonte 3: Comparações Pareadas

Humanos comparam pares de textos.

**Formato:**
```json
{
  "texto_a": "Mudei de SP pro interior...",
  "texto_b": "Larguei emprego corporativo...",
  "pergunta": "Qual desperta mais esperança?",
  "resposta": "texto_a",
  "anotador_id": "user_123"
}
```

---

## 6. Métricas de Qualidade

### Métricas Quantitativas

1. **Satisfação do usuário:** % de sugestões aceitas vs rejeitadas
2. **Consistência:** Vetores similares para textos similares
3. **Separabilidade:** Vetores distintos para textos distintos emocionalmente

### Métricas Qualitativas

1. **Auditoria humana:** Amostragem de sugestões avaliadas
2. **Casos difíceis:** Performance em emoções complexas/combinadas
3. **Cross-cultural:** Consistência entre anotadores de culturas diferentes

---

## 7. Diferencial Competitivo

### Por Que Ninguém Faz Isso

1. **Complexidade:** Requer visão de longo prazo + investimento
2. **Dados:** Anotações subjetivas são caras de coletar
3. **Expertise:** Requer entendimento filosófico + técnico
4. **Paciência:** Fases 1 e 2 são lentas antes de escalar

### Por Que Vale a Pena

1. **Moat defensável:** Dados proprietários + modelo treinado
2. **UX única:** "Descreva como quer que pessoa sinta" > "Escolha categoria"
3. **Qualidade superior:** Sugestões mais alinhadas com intenção real
4. **Escalabilidade:** Uma vez treinado, custo marginal baixo

### Conexão com Visão do Super-Sistema

Este modelo é peça central da visão de longo prazo:

```
Revelar: Clareza de ideia
    ↓
Produtor Científico: Mensagem + Vetor Emocional
    ↓
Emotion Model: Busca argumentos por similaridade
    ↓
Conteúdo gerado alinhado com intenção emocional
```

---

## 8. MVP vs Visão

### MVP (Categorias Fixas)

```python
# Temporário
EMOCOES = ["empatia", "urgência", "confiança", "reflexão", "esperança"]

def encode_emotion(descricao: str) -> dict:
    # LLM extrai categorias da descrição
    return {"empatia": 0.8, "reflexão": 0.6, ...}

def similarity(msg_vetor: dict, arg_vetor: dict) -> float:
    # Overlap ponderado
    return weighted_overlap(msg_vetor, arg_vetor)
```

### Visão (Espaço Latente)

```python
# Futuro
class EmotionEncoder:
    def encode(self, texto: str) -> np.array:
        # Modelo treinado
        return self.model.encode(texto)  # [0.23, -0.87, ...]

def similarity(msg_vetor: np.array, arg_vetor: np.array) -> float:
    return cosine_similarity(msg_vetor, arg_vetor)
```

### Arquitetura Escalável

Interface e lógica de negócio NÃO mudam:
- MVP: `EmotionEncoder` retorna dict com categorias
- Visão: `EmotionEncoder` retorna vetor latente
- Código cliente usa mesma API

---

## 9. Roadmap Conceitual

| Fase | Foco | Dados | Modelo |
|------|------|-------|--------|
| MVP | Validar UX | Nenhum | Categorias fixas (LLM) |
| v1 | Coletar dados | ~1000 anotações | Fine-tuned encoder |
| v2 | Escalar coleta | ~10000 anotações | Modelo próprio |
| v3 | Automatizar | Feedback implícito | Auto-melhoria |

---

## 10. Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Viés cultural | Modelo reflete cultura dos anotadores | Diversificar anotadores |
| Overfitting | Modelo memoriza, não generaliza | Validação cross-domain |
| Subjetividade | Anotadores discordam | Múltiplos anotadores, consenso |
| Custo | Anotação é cara | Fase 2 (semi-auto) reduz custo |

---

## Referências

- `core/docs/vision/system_philosophy.md` - Essências transcendem palavras
- `core/docs/vision/communication_philosophy.md` - Emoção como espaço latente
- `core/docs/architecture/data-models/message_model.md` - Schema de Mensagem

