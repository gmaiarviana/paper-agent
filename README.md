Paper Agent
===========

Visão Geral
-----------
- Plataforma colaborativa com agentes de IA pensada para apoiar todo o ciclo de produção de artigos, combinando especialistas virtuais e orquestração automatizada.
- POC atual valida a primeira etapa dessa visão: análise de hipóteses com um agente Metodologista coordenado por um Orquestrador construído sobre LangGraph.
- Interface web conversacional (Streamlit) como experiência principal; CLI mantido como ferramenta auxiliar para desenvolvimento.
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
python scripts/health_checks/validate_api.py
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

### Interface Web Conversacional (Épico 9)

Interface web como experiência principal com chat fluido e painel "Bastidores" para transparência:
```bash
# Executar interface web
streamlit run app/chat.py
```

**O que a Interface Web oferece:**
- 💬 **Chat conversacional**: Input de mensagens, histórico, métricas inline
- 🔍 **Bastidores (opcional)**: Reasoning dos agentes em tempo real
- 📊 **Timeline**: Histórico de decisões dos agentes (colapsado)
- 💰 **Métricas discretas**: Custo e tokens por mensagem
- 📂 **Sessões**: Sidebar com lista de conversas

**Uso:**
1. Execute o comando acima
2. Navegador abre em `http://localhost:8501`
3. Digite sua ideia ou observação no chat
4. Converse naturalmente - sistema faz perguntas para entender contexto
5. Clique "🔍 Ver raciocínio" para ver bastidores (opcional)
6. Sistema sugere quando chamar agentes especializados
7. Você decide aceitar ou continuar conversando

**Exemplo de sessão conversacional:**
```
Você: "Observei que TDD reduz bugs"

Sistema: "Interessante! Em que contexto você observou isso?"
💰 $0.0012 · 215 tokens · 1.2s

Você: "Na minha equipe Python"

Sistema: "E como você mediu essa redução de bugs?"
💰 $0.0008 · 180 tokens · 0.9s

Você: "Impressão geral, mas bugs caíram bastante"

Sistema: "Posso chamar o Estruturador para transformar isso em 
         uma questão de pesquisa estruturada?"

Você: "Sim"

🤖 Estruturando questão de pesquisa...
[Sistema processa e estrutura V1]
```

**Bastidores (quando aberto):**
```
┌─────────────────────────────────────┐
│ 🧠 Orquestrador                     │
│                                     │
│ Usuário tem observação com contexto,│
│ mas falta estruturação formal.      │
│ Estruturador pode ajudar.           │
│                                     │
│ [📄 Ver raciocínio completo]        │
│                                     │
│ ⏱️ 1.2s | 💰 $0.0012 | 📊 215 tokens│
└─────────────────────────────────────┘
```

**Validação da Interface Web:**
```bash
# Backend deve estar funcionando
python scripts/flows/validate_multi_agent_flow.py

# Validar SSE (streaming)
python scripts/flows/validate_sse_endpoint.py
```

---

### CLI: Ferramenta de Desenvolvimento

Interface de linha de comando mantida para desenvolvimento e automação (não para uso interativo):
```bash
# Modo padrão (CLI limpa)
python cli/chat.py

# Modo verbose (exibe raciocínio)
python cli/chat.py --verbose
```

**Quando usar CLI:**
- ✅ Testes automatizados (scripts, CI/CD)
- ✅ Debugging de agentes
- ✅ Validação rápida de prompts
- ❌ Uso interativo (preferir interface web)

**Uso:**
1. Execute o comando acima
2. Sistema pergunta sobre sua ideia
3. Converse via terminal
4. Digite `exit` ou `sair` para encerrar

**Nota:** CLI compartilha mesmo backend da interface web (LangGraph + EventBus). Funcionalidade congelada - novas features vão para web.

---

### Dashboard Streamlit (Épico 5.1)

> **⚠️ DEPRECATED:** Dashboard de visualização foi substituído pela interface web conversacional (Épico 9). Documentação mantida para referência histórica.

Interface web para visualização de sessões e eventos em tempo real:

```bash
# Executar o dashboard
streamlit run app/dashboard.py
```

**O Dashboard exibe:**
- 📋 Lista de sessões ativas
- 🕒 Timeline cronológica de eventos por sessão
- 📊 Status visual dos agentes (executando, concluído, erro)
- 🔄 Auto-refresh configurável (padrão: 2 segundos)
- 📈 Estatísticas de tokens por agente

**Como usar:**
1. Execute o Dashboard em um terminal: `streamlit run app/dashboard.py`
2. Execute o CLI em outro terminal: `python cli/chat.py`
3. Digite uma hipótese no CLI
4. Veja os eventos aparecerem em tempo real no Dashboard!

**Validação do Dashboard:**
```bash
python scripts/flows/validate_dashboard.py
```

**Resultado esperado:**
- ✅ EventBus publica e consome eventos corretamente
- ✅ Resumo de sessão funciona
- ✅ Timeline mantém ordem cronológica
- ✅ Auto-refresh atualiza em tempo real

---

### Validação de Configurações e Memória (Épico 6)

Validar arquivos YAML de configuração de agentes e funcionalidade de memória:

```bash
# Validação completa de configs (inclui MemoryManager)
python scripts/health_checks/validate_agent_config.py

# Validação de configs YAML e carregamento (mais rápida, sem deps)
python scripts/health_checks/validate_runtime_config_simple.py

# Validação de sintaxe Python dos módulos modificados
python scripts/health_checks/validate_syntax.py

# Validação end-to-end da integração de MemoryManager (Épico 6.2)
python scripts/flows/validate_memory_integration.py
```

**O que é validado:**
- Estrutura de diretórios (`config/agents/`, `agents/memory/`)
- Arquivos YAML de configuração (orchestrator, structurer, methodologist)
- Schema de configurações (campos obrigatórios, tipos)
- Config Loader (carregamento e validação)
- Memory Manager (histórico, metadados, reset)
- Integração runtime nos nós (carregamento de prompts/modelos)
- **Registro de tokens e custos** (Épico 6.2)
- **Integração com CostTracker** (Épico 6.2)
- **Fluxo completo multi-agente** (orchestrator → structurer → methodologist)
- Fallback automático quando YAML não está disponível
- Mensagens de erro em PT-BR

**Resultado esperado:**
- ✅ Todas as validações passando
- 🎉 Confirmação de implementação do Épico 6.1 (Configuração Externa)
- 🎉 Confirmação de implementação do Épico 6.2 (Registro de Memória)

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

