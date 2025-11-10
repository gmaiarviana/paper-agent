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

Setup Inicial
-------------

> **⚠️ IMPORTANTE**: Este projeto **REQUER** um ambiente virtual Python. Todos os comandos devem ser executados com o ambiente virtual ativado.

**1. Clone o repositório**
```bash
git clone <repository-url>
cd paper-agent
```

**2. Crie e ative um ambiente virtual**

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Você deve ver `(venv)` no início do seu prompt, indicando que o ambiente está ativo.

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

**Linux/Mac:**
```bash
cp .env.example .env
# Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
# Edite o arquivo .env e adicione sua ANTHROPIC_API_KEY
```

**Verificação do Setup:**
```bash
# Verifique se as dependências foram instaladas corretamente
python -c "import langgraph; print('✅ LangGraph instalado com sucesso!')"
```

Validação e Testes
------------------

### Health Check da API

Valide a conexão com a API Anthropic:

```bash
python scripts/validate_api.py
```

**Resultado esperado:**
- ✅ Mensagem de sucesso do Claude
- 📊 Estatísticas de uso de tokens
- 💰 Custo estimado

---

### Testes Automatizados

```bash
# Testes unitários (rápidos, sem API)
python -m pytest tests/unit/ -v

# Testes de integração (requer API key)
python -m pytest tests/integration/ -v

# Todos os testes
python -m pytest tests/ -v

# Com coverage
python -m pytest tests/unit/ --cov=utils --cov=agents --cov=orchestrator
```

**Nota:** Para validação de funcionalidades específicas, consulte `ROADMAP.md`

Documentação
------------
- **Status de desenvolvimento**: `ROADMAP.md`
- **Estrutura técnica**: `ARCHITECTURE.md`
- **Processo de desenvolvimento**: `development_guidelines.md`
- **Especificações detalhadas**: `docs/`
  - Agentes: `docs/agents/`
  - Interface: `docs/interface/`
  - Orquestração: `docs/orchestration/`
  - Planejamento: `docs/process/`

