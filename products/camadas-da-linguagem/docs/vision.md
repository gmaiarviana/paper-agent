# Visão de Produto - Camadas da Linguagem

> **Nota:** Para filosofia universal do sistema, consulte `core/docs/vision/system_philosophy.md`.

## 1. Visão Geral

**O que é:** Sistema para estruturar ideias em mensagens comunicáveis  
**Para quem:** Usuários que têm clareza da ideia e querem comunicá-la  
**Problema resolvido:** Distância entre "ter uma ideia clara" e "saber como comunicá-la"  
**Input:** Ideia (conjunto de argumentos)  
**Output:** Mensagem (argumentos organizados + intenção comunicativa)

## 2. Posição no Pipeline

```
┌─────────────┐     ┌─────────────────────────┐     ┌───────────┐
│   Revelar   │     │  Camadas da Linguagem   │     │ Expressão │
│ Prisma Verb.│────▶│    (estruturação)       │────▶│  (forma)  │
└─────────────┘     └─────────────────────────┘     └───────────┘
      │                        │                          │
      ▼                        ▼                          ▼
    IDEIA                  MENSAGEM                   CONTEÚDO
```

**Entradas Possíveis:**
- Via Revelar: Usuário chegou na clareza via diálogo
- Via Prisma Verbal: Sistema extraiu argumentos de texto estático
- Argumentos existentes: Reusar argumentos de sessões anteriores

## 3. O Que Faz

### Organização de Argumentos

- **Seleção:** Quais argumentos usar, quais omitir
- **Priorização:** Ordem lógica mais eficaz
- **Evidências:** Quais são mais relevantes para a intenção

### Definição de Intenção

Usuário define a intenção comunicativa:
- "Quero convencer" → argumentos mais fortes primeiro
- "Quero provocar reflexão" → perguntas e contra-exemplos
- "Quero informar" → estrutura didática

### Vetor Emocional

- Usuário descreve o tom/emoção desejada
- Sistema organiza argumentos alinhados com essa intenção
- Resultado: mensagem coerente emocionalmente

## 4. O Que NÃO Faz

❌ **Não produz conteúdo final:** Isso é Expressão  
❌ **Não define formato:** Artigo, post, email são escolhas do Expressão  
❌ **Não cria clareza:** Se usuário está confuso, deve usar Revelar  
❌ **Não extrai conceitos:** Isso é Prisma Verbal

## 5. Relação com Outros Produtos

| De | Para | O que passa |
|----|------|-------------|
| Revelar | Camadas | Ideia (argumentos estruturados) |
| Prisma Verbal | Camadas | Argumentos extraídos de textos |
| Camadas | Expressão | Mensagem (estrutura + intenção) |
| Camadas | Produtor Científico | Mensagem (para artigo acadêmico) |

## 6. Nome do Produto

"Camadas da Linguagem" reflete:
- O espectro matéria ↔ espírito do sistema
- Transição entre camadas de abstração
- De argumentos (abstrato) para mensagem (mais concreto)

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/architecture/vision/super_system.md` - Arquitetura do super-sistema
- `products/expressao/docs/vision.md` - Produto seguinte no pipeline

