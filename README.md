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

Como Rodar
----------

### Validar Conexão com API (Health Check)

Valide que a conexão com a API Anthropic está funcionando:

```powershell
# Execute o script de validação
python scripts/validate_api.py
```

**Resultado esperado:**
- ✅ Mensagem de sucesso do Claude
- 📊 Estatísticas de uso de tokens (input/output/total)
- 💰 Custo estimado da chamada

**Se houver erro:**
- Verifique se o arquivo `.env` existe e contém `ANTHROPIC_API_KEY=sua-chave-aqui`
- Confirme que a chave API é válida no painel da Anthropic

---

### Validar Estado do Metodologista

Valide que o estado do agente Metodologista está configurado corretamente:

```powershell
# 1. Ativar ambiente virtual (se ainda não estiver ativo)
.\venv\Scripts\Activate.ps1

# 2. Instalar/atualizar dependências
pip install -r requirements.txt

# 3. Executar script de validação
$env:PYTHONPATH="."; python scripts/validate_state.py
```

**Resultado esperado:**
- ✅ TypedDict MethodologistState validado
- ✅ Função create_initial_state funcionando
- ✅ Checkpointer MemorySaver configurado

---

### Validar Tool ask_user

Valide que a tool ask_user do Metodologista está implementada corretamente:

```bash
# 1. Ativar ambiente virtual (se ainda não estiver ativo)
source venv/bin/activate  # Linux/Mac
# OU
.\venv\Scripts\Activate.ps1  # Windows

# 2. Testes unitários da tool ask_user
python -m pytest tests/unit/test_ask_user_tool.py -v

# 3. Validação manual completa
PYTHONPATH=/home/user/paper-agent python scripts/validate_ask_user.py
```

**Resultado esperado:**
- ✅ 10/10 testes unitários passando
- ✅ Tool implementada com decorator @tool
- ✅ Type hints corretos
- ✅ Docstring completa com Args, Returns e Example
- ✅ Usa interrupt() do LangGraph

---

### Rodar Testes Automatizados

```bash
# 1. Ativar ambiente virtual (se ainda não estiver ativo)
source venv/bin/activate  # Linux/Mac
# OU
.\venv\Scripts\Activate.ps1  # Windows

# 2. Testes unitários (rápidos, sem API)
python -m pytest tests/unit/ -v

# 3. Testes de integração (requer API key)
python -m pytest tests/integration/ -m integration -v

# 4. Todos os testes
python -m pytest tests/ -v

# 5. Com coverage
python -m pytest tests/unit/ --cov=utils --cov=agents --cov=orchestrator

# 6. Teste específico (exemplo: tool ask_user)
python -m pytest tests/unit/test_ask_user_tool.py -v
```

**Mais informações:** Ver `docs/testing_guidelines.md`

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

