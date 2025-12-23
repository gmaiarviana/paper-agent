# Filosofia de Comunicação

## Visão Geral

Este documento estabelece a filosofia fundamental de comunicação do sistema, explicando como emoção é modelada como espaço latente (não categorias), permitindo capturar essências emocionais que transcendem rótulos racionais.

A abordagem aqui descrita estende o princípio de que "essências transcendem palavras" (ver `system_philosophy.md`) para o domínio emocional, onde essências emocionais são representadas em espaços vetoriais contínuos, não em categorias fixas.

---

## 1. Mensagem vs Forma vs Receptor

### Hierarquia Fundamental

**Mensagem** é a essência do que se quer comunicar. É mais fundamental que qualquer materialização específica. Uma Mensagem contém:
- **O QUE**: O conteúdo semântico (ideias, argumentos, proposições)
- **Vetor emocional**: Como se quer que o receptor se sinta (espaço latente)

**Forma** é a materialização da Mensagem. É o **COMO**:
- Artigo LinkedIn
- Poema
- Thread Twitter
- Vídeo
- Apresentação

**Receptor** é para **QUEM** a comunicação é dirigida. Vem depois da Mensagem, e está ligado à Forma:
- Forma (artigo LinkedIn) → Receptor (profissionais urbanos)
- Forma (poema) → Receptor (sensível a arte)
- Forma (thread Twitter) → Receptor (jovens tech)

### Exemplo: Mesma Mensagem, Múltiplas Formas

**Mensagem:** "Cidades fazem mal à saúde mental"

Esta mesma Mensagem pode materializar-se como:

**Forma 1: Artigo LinkedIn**
- Receptor: Profissionais urbanos
- Estrutura: Tese, evidências, conclusão
- Tom: Profissional, baseado em dados

**Forma 2: Poema**
- Receptor: Sensível a arte
- Estrutura: Versos, imagens, ritmo
- Tom: Lírico, emocional

**Forma 3: Thread Twitter**
- Receptor: Jovens tech
- Estrutura: Tópicos, hooks, dados visuais
- Tom: Direto, provocativo

**O que permanece constante:**
- Conteúdo semântico: ideia sobre cidades e saúde mental
- Vetor emocional: essência emocional que se quer transmitir

**O que varia:**
- Forma de apresentação
- Receptor-alvo
- Tom linguístico

### Implicação Arquitetural

Sistema primeiro identifica a **Mensagem** (essência + vetor emocional), depois sugere **Formas** adequadas ao **Receptor**. Mensagem é primária, Forma e Receptor são derivados.

---

## 2. Emoção como Espaço Latente (Não Categorias)

### Visão (Longo Prazo)

**Emoção NÃO é categórica.** Emoções não são rótulos fixos como "empatia", "urgência", "nostalgia". 

**Emoção é ESPAÇO VETORIAL contínuo** onde essências emocionais vivem.

### Analogia: Word Embeddings (Word2Vec)

Assim como Word2Vec representa palavras em espaço vetorial contínuo:

- Palavras semanticamente similares ficam próximas no espaço
- Dimensões NÃO têm rótulos interpretáveis ("dimensão 1 = sujeito?", não)
- Captura essência semântica que transcende categorias

**Exemplo:**
```
"rei" e "rainha" → próximos no espaço (gênero muda, essência similar)
"rei" e "presidente" → próximos (autoridade compartilhada)
"rei" e "máquina" → distantes (essências distintas)
```

Dimensões do vetor não têm nomes - são aprendidas. Palavras similares apenas tendem a ter vetores similares.

### Sistema com Emoções

Sistema fará o mesmo com **EMOÇÕES**:

- Argumentos com essências emocionais similares ficam próximos no espaço
- Dimensões NÃO têm rótulos ("empatia", "urgência")
- Captura essência emocional que transcende palavras

**Exemplo:**
```
Argumento A: "Pare e questione se a vida que leva faz sentido. Um incômodo silencioso que cresce devagar."
Argumento B: "Reflita sobre suas escolhas. Uma inquietude profunda que não pode ser ignorada."
Argumento C: "Aja agora! Não perca esta oportunidade única!"

A e B → próximos no espaço (essência emocional similar: reflexão silenciosa)
A e C → distantes (essências emocionais distintas: reflexão vs urgência)
```

**Dimensões do vetor emocional:**
- Sem rótulos interpretáveis (não são "empatia", "urgência", "nostalgia")
- Aprendidas via treinamento
- Capturam padrões que humanos reconhecem como similares, mas não necessariamente nomeiam

### Diferencial: Essências Emocionais Transcendem Rótulos

Assim como o sistema detecta que "cooperação", "dharma", "harmonia" apontam para a mesma essência semântica (ver `system_philosophy.md`), ele detectará que:

- "Empatia visceral", "identificação silenciosa", "compaixão ativa" → mesma essência emocional
- "Urgência lancinante", "pressão inescapável", "necessidade imediata" → mesma essência emocional

**AMBOS trabalham em ESPAÇO LATENTE, não categorias.**

---

## 3. Conversação Indeterminística

### Abordagem Não-Determinística

Sistema **NÃO pergunta**: "Escolha emoção: [empatia] [urgência] [nostalgia]"

Sistema **PERGUNTA**: "Como você quer que a pessoa SE SINTA ao ler?"

### Fluxo de Conversação

**1. Usuário descreve subjetivamente:**
```
"Quero que ela pare e questione se a vida que leva faz sentido.
 Um incômodo silencioso que cresce devagar."
```

**2. LLM processa descrição subjetiva:**
- Não busca categoria predefinida
- Interpreta descrição em linguagem natural
- Identifica nuances emocionais descritas

**3. Sistema gera vetor emocional no espaço latente:**
- Encoder emocional converte descrição em vetor (128-512 dimensões)
- Vetor captura essência emocional, não rótulo categórico

**4. Sistema busca argumentos com vetores similares:**
- Calcula similaridade cosseno entre vetor desejado e argumentos na biblioteca
- Argumentos com vetores próximos = essências emocionais similares

**5. Sistema sugere combinação de argumentos:**
- Apresenta argumentos com maior similaridade
- Usuário aceita/rejeita sugestões

**6. Sistema aprende com feedback:**
- Aceitações/rejeições refinam modelo (longo prazo)
- Feedback humano atualiza embeddings emocionais

### Por Que Indeterminístico?

**Determinístico (categorias):**
- Usuário escolhe de lista fixa: ["empatia", "urgência", "nostalgia"]
- Sistema mapeia escolha para categoria
- Limita expressão a rótulos pré-definidos

**Indeterminístico (espaço latente):**
- Usuário descreve subjetivamente em linguagem natural
- Sistema captura nuances que transcendem categorias
- Permite essências emocionais que não têm nome

### Exemplo Completo

**Usuário:**
```
"Quero que ela sinta uma conexão profunda com a solidão urbana,
 mas sem desespero. Algo como melancolia esperançosa."
```

**Sistema:**
1. Processa descrição → gera vetor `[0.23, -0.41, 0.78, ...]` (128 dims)
2. Busca argumentos similares na biblioteca:
   - Argumento A: similaridade 0.89 → "Cidades criam solidão compartilhada"
   - Argumento B: similaridade 0.76 → "Esperança nas pequenas conexões"
   - Argumento C: similaridade 0.34 → "Urgência para mudança imediata"
3. Sugere combinação: A + B
4. Usuário aceita A, rejeita B
5. Sistema ajusta (longo prazo): argumentos com "melancolia esperançosa" tendem a aceitar A

---

## 4. MVP vs Visão (Escalável)

### MVP (Curto Prazo - Determinístico)

**Abordagem categórica:**

- **Categorias fixas:** `["empatia", "urgência", "confiança", "nostalgia", "motivação"]`
- **Interface:** Sliders para cada categoria (0-100)
- **Cálculo de aderência:** Manual, baseado em regras:
  - Se usuário escolhe "empatia: 80, urgência: 20"
  - Sistema busca argumentos com tag "empatia" alta, "urgência" baixa
  - Calcula score de aderência: `score = (emp_match * 0.8) + (urg_match * 0.2)`

**Implementação:**
```python
# MVP: EmotionEncoder mock (categorias)
class EmotionEncoderMock:
    def encode(self, categories: dict) -> np.array:
        # [empatia, urgência, confiança, ...]
        return np.array([categories["empatia"], categories["urgência"], ...])
```

**Limitações:**
- Expressão limitada a categorias pré-definidas
- Não captura nuances emocionais
- Não aprende com feedback

**Objetivo:** Validar conceito, permitir MVP funcional rapidamente.

### Visão (Longo Prazo - Indeterminístico)

**Abordagem em espaço latente:**

- **Espaço latente:** 128-512 dimensões sem rótulos
- **Modelo treinado:** Via anotações humanas subjetivas
- **Busca automática:** Similaridade cosseno no espaço latente

**Implementação:**
```python
# Visão: EmotionEncoder treinado (latente)
class EmotionEncoder:
    def encode(self, description: str) -> np.array:
        # Gera vetor 128-512 dims via modelo treinado
        return self.model.encode(description)  # [0.23, -0.41, 0.78, ...]
    
    def find_similar(self, target_vector: np.array, threshold: float = 0.80):
        # Busca argumentos com vetores similares (cosseno)
        return [arg for arg in arguments 
                if cosine_similarity(target_vector, arg.emotion_vector) > threshold]
```

**Arquitetura escalável:**
- MVP usa `EmotionEncoderMock` (categorias)
- Visão substitui por `EmotionEncoder` treinado (latente)
- **Interface e lógica de negócio NÃO mudam**
- Apenas o encoder interno muda (abstração permite troca)

**Treinamento:**
1. Humanos anotam descrições subjetivas: "Como você quer que a pessoa se sinta?"
2. Sistema gera vetores iniciais (embeddings de descrições)
3. Usuários aceitam/rejeitam sugestões de argumentos
4. Feedback humano refinado atualiza embeddings
5. Modelo aprende padrões: descrições similares → vetores similares → argumentos similares

**Benefícios:**
- Captura essências emocionais que transcendem categorias
- Aprende continuamente com feedback humano
- Escalável para novas nuances emocionais sem redesenhar interface

### Transição MVP → Visão

**Fase 1 (MVP):**
- Interface: sliders de categorias
- Backend: `EmotionEncoderMock`
- Validação: usuários usam sistema, dão feedback

**Fase 2 (Híbrido):**
- Interface mantém sliders (compatibilidade)
- Backend adiciona `EmotionEncoder` treinado
- Sistema oferece ambos: categorias (determinístico) ou descrição livre (indeterminístico)

**Fase 3 (Visão):**
- Interface: apenas descrição livre (indeterminístico)
- Backend: apenas `EmotionEncoder` treinado
- Categorias removidas (obsoletas)

---

## 5. Conexão com Filosofia do Sistema

### Extensão de "Essências Transcendem Palavras"

A modelagem de emoção como espaço latente é extensão natural do princípio fundamental documentado em `system_philosophy.md`:

**Conceitos semânticos:**
- "Cooperação", "dharma", "harmonia" → mesma essência semântica
- Sistema detecta via embedding semântico (ChromaDB, sentence-transformers)
- Similaridade > 0.80 → variations do mesmo conceito

**Emoções (nova proposta):**
- "Empatia visceral", "identificação silenciosa", "compaixão ativa" → mesma essência emocional
- Sistema detectará via embedding emocional (modelo futuro, espaço latente)
- Similaridade > 0.80 → essências emocionais equivalentes

### Abstração Unificada

**AMBOS trabalham em ESPAÇO LATENTE:**

1. **Espaço semântico (conceitos):**
   - Embeddings de palavras/frases
   - Captura essências semânticas que transcendem vocabulário
   - Dimensões não têm rótulos interpretáveis

2. **Espaço emocional (argumentos):**
   - Embeddings de descrições emocionais
   - Captura essências emocionais que transcendem categorias
   - Dimensões não têm rótulos interpretáveis

**Ambos permitem:**
- Detecção de similaridade semântica/emocional
- Transcendência de rótulos linguísticos/categóricos
- Aprendizado contínuo com feedback humano

### Implicação Arquitetural

Sistema já trabalha com espaço latente para conceitos (ChromaDB). Adicionar espaço latente para emoções é evolução natural da mesma arquitetura:

- **Conceitos:** Biblioteca global de conceitos com embeddings semânticos
- **Argumentos:** Biblioteca global de argumentos com embeddings emocionais
- **Busca unificada:** Similaridade semântica + similaridade emocional

---

## Referências

- `core/docs/vision/system_philosophy.md` - "Essências transcendem palavras" (base filosófica)
- `core/docs/vision/epistemology.md` - Base epistemológica (proposições, solidez)
- `core/docs/architecture/data-models/ontology.md` - Será atualizado com Mensagem (futuro)

## Notas de Implementação

**O que NÃO está neste documento:**
- ❌ Detalhes técnicos de implementação (ver `message_model.md` futuro)
- ❌ Definição de dimensões do vetor (mantém indeterminístico)
- ❌ Especificação de modelo de ML (ver `vision/emotion_model.md` futuro)

**Foco deste documento:**
- ✅ Filosofia e princípios orientadores
- ✅ Separação clara entre MVP e Visão
- ✅ Conexão com filosofia existente do sistema


