# Visão de Produto - Expressão

> **Nota:** Para filosofia universal do sistema, consulte `core/docs/vision/system_philosophy.md`.

## 1. Visão Geral

- **O que é:** Sistema para transformar mensagens em conteúdo
- **Para quem:** Usuários que têm mensagem estruturada e querem produzir conteúdo
- **Problema resolvido:** Distância entre "saber o que comunicar" e "ter o conteúdo pronto"
- **Input:** Mensagem (argumentos organizados + intenção)
- **Output:** Conteúdo em forma específica

## 2. Posição no Pipeline
```
┌─────────────────────────┐     ┌───────────┐
│  Camadas da Linguagem   │────▶│ Expressão │
└─────────────────────────┘     └───────────┘
            │                         │
            ▼                         ▼
        MENSAGEM                  CONTEÚDO
                                      │
                          ┌───────────┼───────────┐
                          ▼           ▼           ▼
                        post        email    apresentação
```

## 3. Formas Disponíveis

- **Post:** LinkedIn, blog, redes sociais
- **Email:** Comunicação direta
- **Apresentação:** Slides, pitch
- **Thread:** Twitter/X
- **(outras formas futuras)**

## 4. Especializações

### Produtor Científico

Fork de Expressão otimizado para artigos acadêmicos:

- Estrutura específica (Introdução, Metodologia, Resultados...)
- Validação metodológica integrada
- Tipos de artigo (empírico, revisão, teórico...)
- Ver: `products/produtor-cientifico/docs/vision.md`

## 5. O Que Faz

- Recebe Mensagem com estrutura e intenção
- Aplica forma específica (post, email, etc.)
- Gera conteúdo final pronto para uso

## 6. O Que NÃO Faz

- ❌ **Não estrutura argumentos:** Isso é Camadas da Linguagem
- ❌ **Não cria clareza:** Isso é Revelar
- ❌ **Não extrai conceitos:** Isso é Prisma Verbal

## 7. Relação com Outros Produtos

| De | Para | O que passa |
|----|------|-------------|
| Camadas da Linguagem | Expressão | Mensagem |
| Expressão | (usuário) | Conteúdo final |

## Referências

- `core/docs/vision/system_philosophy.md` - Filosofia universal
- `core/docs/architecture/vision/super_system.md` - Arquitetura do super-sistema
- `products/camadas-da-linguagem/docs/vision.md` - Produto anterior no pipeline
- `products/produtor-cientifico/docs/vision.md` - Especialização para artigos

