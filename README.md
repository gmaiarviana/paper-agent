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

### CLI Conversacional (Épico 7 Protótipo)

Interface de linha de comando com chat contínuo e múltiplos turnos:

```bash
# Modo padrão (CLI limpa)
python cli/chat.py

# Modo verbose (exibe raciocínio do orquestrador)
python cli/chat.py --verbose
python cli/chat.py -v
```

**Uso:**
1. Sistema inicia conversa perguntando sobre sua ideia
2. Converse naturalmente - sistema faz perguntas para entender contexto
3. Sistema sugere quando chamar agentes especializados
4. Você decide aceitar ou continuar conversando
5. Digite `exit` ou `sair` a qualquer momento para encerrar

**Exemplo de sessão conversacional:**
```
Sistema: Olá! Me conte sobre sua ideia ou observação.

Você: tdd reduz bugs

Sistema: Interessante observação sobre TDD! Poderia me contar um pouco mais?
         Em que contexto você notou que TDD reduz bugs?

Você: na minha equipe Python

Sistema: Entendi! E como você mediu essa redução de bugs? Tem dados
         ou é uma impressão geral?

Você: impressão geral, mas bugs caíram bastante

Sistema: Perfeito! Baseado no que você me contou, posso chamar o
         Estruturador para transformar isso em uma questão de
         pesquisa estruturada?

📌 Agente sugerido: structurer
📝 Justificativa: Usuário tem observação com contexto, mas precisa
   estruturar em questão de pesquisa formal

Você quer que eu chame este agente? (sim/não): sim

🤖 Chamando structurer...
[Sistema processa...]
```

**Modo Verbose (transparência):**
```bash
python cli/chat.py --verbose

# Exibe raciocínio inline:
🧠 Raciocínio: Input vago sobre TDD. Preciso contexto: onde observou,
   como mediu, qual população. Não tenho informação suficiente...

Sistema: Interessante observação sobre TDD! Poderia me contar...
```

**Validação do CLI Conversacional:**
```bash
python scripts/flows/validate_conversational_cli.py
```

---

### Dashboard Streamlit (Épico 5.1)

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

