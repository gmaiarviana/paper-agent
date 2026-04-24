# Ensaio

Sistema conversacional para transformar experimentos de código em artigos técnico-científicos publicáveis.

## O que é

Laboratório de escrita onde experimentos (PoCs, protótipos, estudos em TRL 3–6) viram artigos. O experimento acontece no código; o artigo emerge da conversa entre pesquisador e sistema.

**Para quem:** pesquisadores de ICT que produzem PoCs em desenvolvimento de software, IA agêntica e tecnologias correlatas.

**Diferencial:** sistema proativo — identifica lacunas no argumento e solicita métricas, evidências e informações que o artigo precisará.

## Posição no Super-Sistema

```
┌─────────────┐     ┌─────────────┐
│   REVELAR   │     │   ENSAIO    │
│  (diálogo)  │     │(experimentos)│
└─────────────┘     └─────────────┘
        │                   │
        └─────── core ──────┘
```

Ensaio é **produto próprio com app próprio**, paralelo ao Revelar. Compartilha os agentes do core (Orquestrador, Estruturador, Metodologista, Writer), não a UI.

## Status

POC ✅ implementada e validada manualmente (milestone POC-ENSAIO — C-ENSAIO-2, E-POC-1, E-POC-2, E-POC-3).

Executar localmente:

```bash
python -m streamlit run products/ensaio/app/chat.py
```

Requer apenas `ANTHROPIC_API_KEY` no `.env`. Modelo padrão pode ser trocado via `LLM_MODEL` no `.env`.

## Documentação

- `products/ensaio/docs/vision.md` - Visão do produto (POC / Protótipo / MVP, casos de uso, filosofia)
- `products/ensaio/ROADMAP.md` - Épicos planejados
- `products/ensaio/docs/poc_validation.md` - Checklist de validação manual da POC (usado pelo dev ao revisar a PR final)
- `core/docs/agents/writer/design.md` - Decisões arquiteturais do Writer (agente core motivado pelo Ensaio)
- `core/docs/vision/super_system.md` - Desacoplamento core ↔ produto
