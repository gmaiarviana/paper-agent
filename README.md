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

Estrutura do Projeto
--------------------
```
paper-agent/
├── agents/          # Agentes especializados (Metodologista, etc.)
├── orchestrator/    # Lógica de orquestração e decisão
├── utils/           # Utilitários e helpers
├── app/             # Interface Streamlit (futura)
├── docs/            # Documentação detalhada
├── requirements.txt # Dependências do projeto
└── .env.example     # Template de variáveis de ambiente
```

Primeiros Passos
----------------
1. Clone o repositório
2. (Recomendado) Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY
   ```

Status Atual
------------
🚧 **Em Desenvolvimento**

O projeto está sendo construído incrementalmente seguindo o `ROADMAP.MD`:
- ✅ ÉPICO 1.1: Configuração de Ambiente - **CONCLUÍDO**
- ⏳ ÉPICO 1.2: Teste de Conexão com Claude API - Próximo passo
- ⏳ ÉPICO 2: Agente Metodologista Standalone
- ⏳ ÉPICO 3: Orquestrador com Reasoning
- ⏳ ÉPICO 4: Interface CLI e Streamlit

Como Rodar (Disponível em Breve)
---------------------------------
- CLI principal: `python cli.py`
- Streamlit (visualização local): `streamlit run app.py`

Testes (Disponíveis em Breve)
------------------------------
- Conexão com Claude: `python test_api.py`
- Metodologista isolado: `python test_methodologist.py`
- Orquestração completa: `python test_orchestration.py`

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

