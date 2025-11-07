Paper Agent
===========

Visão Geral
-----------
- Plataforma colaborativa com agentes de IA pensada para apoiar todo o ciclo de produção de artigos, combinando especialistas virtuais e orquestração automatizada.
- POC atual valida a primeira etapa dessa visão: análise de hipóteses com um agente Metodologista coordenado por um Orquestrador construído sobre LangGraph.
- Fluxo principal acontece via CLI; Streamlit serve como visualização opcional para uso humano.
- Projeto orientado para colaboração com agentes de IA (Claude Code, Cursor background), com documentação enxuta e responsabilidades bem separadas.

Pré-requisitos
--------------
- Python 3.11+
- Chave da API Anthropic (`ANTHROPIC_API_KEY`)

Primeiros Passos
----------------
1. Instale dependências: `pip install -r requirements.txt`
2. Configure variáveis: copie `.env.example` para `.env` e defina `ANTHROPIC_API_KEY`
3. (Opcional) Ative seu ambiente virtual preferido antes de instalar dependências

Como Rodar
----------
- CLI principal: `python cli/chat.py`
- Streamlit (visualização local): `streamlit run app.py`

Testes Disponíveis
------------------
- Conexão com Claude: `python tests/test_api.py`
- Metodologista isolado: `python tests/test_methodologist.py`
- Orquestração completa: `python tests/test_orchestration.py`

O que Esperar
-------------
- Inputs casuais recebem resposta direta do Orquestrador
- Hipóteses são encaminhadas ao agente Metodologista, que devolve JSON estruturado com status, justificativa e sugestões
- Logs no terminal destacam decisões tomadas (use `--verbose` na CLI conforme configurado)

Documentação
------------
- Visão arquitetural: `ARCHITECTURE.md`
- Visão dos agentes: `docs/agents/overview.md`
- Detalhes do Metodologista: `docs/agents/methodologist.md`
- Orquestração e LangGraph: `docs/orchestration/orchestrator.md`
- Interface CLI/Streamlit: `docs/interface/cli.md`
- Planejamento e processo: `docs/process/`

