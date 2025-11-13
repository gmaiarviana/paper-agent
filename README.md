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

> **💡 Nota sobre `python` vs `python3`:**
> - **Windows (PowerShell):** Use `python` quando o ambiente virtual estiver ativado. O comando `python3` pode invocar o Python do sistema em vez do ambiente virtual.
> - **Linux/Mac:** Use `python3` para garantir que está usando Python 3.x, ou `python` se estiver com venv ativado.
> - **Regra geral:** Com venv ativado, `python` sempre aponta para o Python do ambiente virtual, independentemente do sistema operacional.

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

---

### CLI Interativo

Interface de linha de comando para testar o agente Metodologista:

```bash
python cli/chat.py
```

**Uso:**
1. Digite sua hipótese quando solicitado
2. Responda perguntas do agente para clarificar aspectos metodológicos
3. Receba a avaliação final (aprovada/rejeitada) com justificativa
4. Cada análise começa com contexto limpo automaticamente (Épico 6)
5. Digite `exit` a qualquer momento para sair

**Exemplo de sessão:**
```
📝 Digite sua hipótese: Café aumenta produtividade
🔬 Analisando hipótese...

❓ Agente pergunta: Qual é a população-alvo do estudo?
💬 Sua resposta: Adultos de 18-40 anos

❓ Agente pergunta: Como a produtividade será medida?
💬 Sua resposta: Número de tarefas completadas por hora

📊 RESULTADO DA ANÁLISE
✅ Status: APROVADA
📝 Justificativa: A hipótese atende aos critérios de testabilidade...
```

**Validação do CLI (sem interação):**
```bash
python scripts/validate_cli.py
```

---

### Validação de Configurações (Épico 6)

Validar arquivos YAML de configuração de agentes e funcionalidade de memória:

```bash
python scripts/validate_agent_config.py
```

**O que é validado:**
- Estrutura de diretórios (`config/agents/`, `agents/memory/`)
- Arquivos YAML de configuração (orchestrator, structurer, methodologist)
- Schema de configurações (campos obrigatórios, tipos)
- Config Loader (carregamento e validação)
- Memory Manager (histórico, metadados, reset)
- Integração entre componentes

**Resultado esperado:**
- ✅ Todas as validações passando
- 🎉 Confirmação de implementação do Épico 6

---

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

