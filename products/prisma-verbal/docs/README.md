# Documentação - Prisma Verbal

Sistema que lê textos como humano, extraindo conceitos/ideias centrais e permitindo descoberta de cosmovisões compartilhadas.

---

## 📖 Documentos Principais

### [Philosophy](./philosophy.md)
Fundamentos filosóficos do sistema. Explica **POR QUE** fazemos assim:
- Palavras como escolhas contextuais → essências
- Separação: Leitura vs Contextualização
- Genealogia de crenças
- Checkpoint multinível

### [Vision](./vision.md)
Visão do produto. Explica **O QUE** fazemos:
- Entidades (Book, Chapter, BaseFichamento, UserFichamento)
- Fluxos (Upload → Processamento → Navegação)
- Catálogo público + textos pessoais
- Integração com Core

---

## 🏗️ Arquitetura

### [Reading Process](./architecture/reading_process.md)
Como sistema lê textos sequencialmente:
- Leitura progressiva (ordem importa)
- Respeitar o que foi dito literalmente
- Acumulação de contexto
- Checkpoints dinâmicos

---

## 📚 Exemplos

### [Sapiens - Introdução](./examples/sapiens_intro.md)
Exemplo de processamento de texto filosófico/científico (Yuval Noah Harari)

---

## 🔗 Relacionados

- [Core - Ontologia](../../../core/docs/architecture/data-models/ontology.md) - Conceito, Ideia, Argumento (compartilhado entre produtos)
- [Core - Super Sistema](../../../core/docs/vision/super_system.md) - Como Prisma Verbal consome o core universal

