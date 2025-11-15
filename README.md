Paper Agent
===========

Visão Geral
-----------
Plataforma colaborativa com agentes de IA pensada para apoiar todo o ciclo de produção de artigos, combinando especialistas virtuais e orquestração automatizada. A POC atual valida a primeira etapa dessa visão: análise de hipóteses com um agente Metodologista coordenado por um Orquestrador construído sobre LangGraph.

Interface web conversacional (Streamlit) como experiência principal; CLI mantido como ferramenta auxiliar para desenvolvimento.

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

> **💡 Nota sobre `python` vs `python3`:**
> - **Windows (PowerShell):** Use `python` quando o ambiente virtual estiver ativado. O comando `python3` pode invocar o Python do sistema em vez do ambiente virtual.
> - **Linux/Mac:** Use `python3` para garantir que está usando Python 3.x, ou `python` se estiver com venv ativado.
> - **Regra geral:** Com venv ativado, `python` sempre aponta para o Python do ambiente virtual, independentemente do sistema operacional.

Comandos Básicos
----------------

### Interface Web

> **⚠️ NOTA:** Interface web conversacional (`app/chat.py`) será implementada no Épico 9. Atualmente disponível apenas o Dashboard (`app/dashboard.py`) para visualização de eventos.

```bash
# Executar dashboard de visualização
streamlit run app/dashboard.py
```

Dashboard exibe eventos e reasoning dos agentes em tempo real.

### CLI (Desenvolvimento)

```bash
# Modo padrão
python cli/chat.py

# Modo verbose (exibe raciocínio)
python cli/chat.py --verbose
```

### Validação e Testes

```bash
# Health check da API
python scripts/health_checks/validate_api.py

# Testes unitários (rápidos, sem API)
python -m pytest tests/unit/ -v

# Testes de integração (requer API key)
python -m pytest tests/integration/ -v

# Validação de configurações
python scripts/health_checks/validate_agent_config.py
```

---

Documentação
------------
- **Status de desenvolvimento**: `ROADMAP.md`
- **Estrutura técnica**: `ARCHITECTURE.md`
- **Especificações detalhadas**: `docs/`
  - Agentes: `docs/agents/`
  - Interface: `docs/interface/`
  - Orquestração: `docs/orchestration/`
  - Processo: `docs/process/`

### Para AI Agents (Claude, Cursor, Claude Code)

Consulte os documentos essenciais na raiz:
- **CONSTITUTION.md** - Princípios e processo de trabalho
- **ROADMAP.md** - Épicos e funcionalidades
- **ARCHITECTURE.md** - Decisões técnicas
- **planning_guidelines.md** - Processo de refinamento

Ver mapa completo de documentação em CONSTITUTION.md.

