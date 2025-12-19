Super-Sistema com Core Universal
=================================

## Visão Geral
Super-sistema colaborativo com agentes de IA para apoiar clareza de pensamento e extração de conhecimento. Arquitetura atual: sistema multi-agente conversacional sobre LangGraph com Orquestrador facilitador, Estruturador organizador e Metodologista validador lógico. Sistema mantém diálogo fluido onde usuário e agentes negociam caminho juntos. Interface web conversacional (Streamlit) como principal; CLI mantido para desenvolvimento e automação.

**Produto atual:** Revelar - sistema conversacional para estruturar pensamentos nebulosos em conceitos claros.

Visão do Sistema
----------------

Este repositório implementa um **super-sistema** com core universal que serve múltiplos produtos. O core compartilha ontologia (Conceito, Ideia, Argumento), modelo cognitivo, agentes especializados e infraestrutura vetorial (ChromaDB, embeddings).

**Pipeline de Produtos (visão futura):**
```
Revelar (clareza) → Camadas da Linguagem (estruturação) → Expressão (forma)
     ↑
Prisma Verbal (extração de textos)
```

- **Revelar** (atual): Clareza de pensamento via diálogo socrático
- **Prisma Verbal** (planejado): Extração de conceitos de textos estáticos
- **Camadas da Linguagem** (planejado): Estruturação de ideias em mensagens
- **Expressão** (planejado): Produção de conteúdo em formas diversas
- **Produtor Científico** (planejado): Especialização de Expressão para artigos acadêmicos

**Filosofia Central:** Sistema não julga verdade, mapeia sustentação. Proposições têm solidez (não são "verdadeiras" ou "falsas"). Pesquisa fortalece/enfraquece, não valida/refuta.

> Para detalhes completos: `core/docs/vision/system_philosophy.md` e `core/docs/architecture/vision/super_system.md`

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

Interfaces do Sistema
---------------------

O sistema oferece **duas interfaces web** para diferentes necessidades, além de CLI para desenvolvimento:

### 1. Interface Web Conversacional (Principal)

Interface web como experiência principal com chat fluido e painel "Bastidores" para transparência:
```bash
# Executar interface principal
streamlit run products/revelar/app/chat.py
```

Navegador abre em `http://localhost:8501`.

**O que oferece:**
- 💬 **Chat conversacional**: Input de mensagens, histórico, métricas inline
- 🔍 **Bastidores (opcional)**: Reasoning dos agentes em tempo real
- 📊 **Timeline**: Histórico de decisões dos agentes (colapsado)
- 💰 **Métricas discretas**: Custo e tokens por mensagem
- 💬 **Conversas**: Sidebar com últimas 5 conversas (backend SqliteSaver)
- 📖 **Meus Pensamentos**: Página dedicada com grid de ideias cristalizadas
- 🏷️ **Catálogo**: Biblioteca de conceitos (disponível após Épico 13)
- 💾 **Persistência**: Sessões sobrevivem entre visitas (sem autenticação)

**Uso:**
1. Execute o comando acima
2. Digite sua ideia ou observação no chat
3. Converse naturalmente - sistema faz perguntas para entender contexto
4. Clique no header "📊 Bastidores" para expandir o painel de raciocínio (opcional)
5. Sistema sugere quando chamar agentes especializados
6. Você decide aceitar ou continuar conversando

**Bastidores (quando expandido):**
````
┌─────────────────────────────────────┐
│ 🧠 Orquestrador                     │
│                                     │
│ Usuário tem observação com contexto,│
│ mas falta estruturação formal.      │
│                                     │
│ [📄 Ver raciocínio completo]        │
│                                     │
│ ⏱️ 1.2s | 💰 $0.0012 | 📊 215 tokens│
└─────────────────────────────────────┘
````

### 2. Dashboard (Debug/Monitoring)

Interface de debug mantida para desenvolvedores visualizarem eventos de todas as sessões:
```bash
# Executar dashboard de debug
streamlit run products/revelar/app/dashboard.py
```

Navegador abre em `http://localhost:8501` (mesma porta, app diferente).

**O que oferece:**
- 📋 Lista todas as sessões ativas do sistema
- 🕒 Timeline cronológica de eventos por sessão
- 📊 Status visual dos agentes (executando, concluído, erro)
- 🔄 Auto-refresh configurável (padrão: 2 segundos)
- 📈 Estatísticas: eventos por tipo, agentes executados, total de tokens
- 🗑️ Ações: atualizar manualmente, limpar sessão

**Quando usar:**
- ✅ Debug de problemas em sessões específicas
- ✅ Monitoring de uso geral do sistema
- ✅ Desenvolvimento/validação de novos agentes
- ❌ Uso interativo normal (preferir chat.py)

### 3. CLI (Desenvolvimento)

Interface de linha de comando mantida para desenvolvimento e automação (não para uso interativo):
```bash
# Modo padrao
python -m core.tools.cli.chat

# Modo verbose (exibe raciocinio)
python -m core.tools.cli.chat --verbose
```

**Quando usar CLI:**
- ✅ Testes automatizados (scripts, CI/CD)
- ✅ Debugging de agentes
- ✅ Validação rápida de prompts
- ❌ Uso interativo (preferir interface web)

**Nota:** CLI compartilha mesmo backend da interface web (LangGraph + EventBus). Funcionalidade congelada - novas features vão para web.

---

Documentação
------------

### Estrutura Geral

- **Raiz**: Processo e visão geral
  - `core/ROADMAP.md` - Épicos e melhorias do core
  - `CONSTITUTION.md` - Princípios e processo de trabalho
  - `ARCHITECTURE.md` - Decisões arquiteturais

- **Core**: Sistema universal
  - `core/README.md` - Visão geral do core
  - `products/revelar/ROADMAP.md` - Épicos e melhorias do Revelar
  - `core/docs/vision/` - Filosofia e princípios
  - `core/docs/architecture/` - Estrutura técnica
  - `core/docs/agents/` - Especificações dos agentes

- **Produtos**: Aplicações específicas
  - `products/revelar/` - Chat para clareza de pensamento (atual)
  - `products/prisma-verbal/` - Extração de conceitos de textos (planejado)
  - `products/camadas-da-linguagem/` - Estruturação de mensagens (planejado)
  - `products/expressao/` - Produção de conteúdo (planejado)
  - `products/produtor-cientifico/` - Manuscritos acadêmicos (planejado)

### Documentos Essenciais (Core)

- **Filosofia**: `core/docs/vision/system_philosophy.md`
- **Epistemologia**: `core/docs/vision/epistemology.md`
- **Modelo Cognitivo**: `core/docs/vision/cognitive_model/`
- **Conversação**: `core/docs/vision/conversation_mechanics.md`
- **Ontologia**: `core/docs/architecture/data-models/ontology.md`
- **Super-Sistema**: `core/docs/architecture/vision/super_system.md`

### Para AI Agents (Claude, Cursor, Claude Code)

Consulte os documentos essenciais na raiz:
- **CONSTITUTION.md** - Princípios e processo de trabalho
- **core/ROADMAP.md** - Épicos e melhorias do core
- **products/revelar/ROADMAP.md** - Épicos e melhorias do Revelar
- **ARCHITECTURE.md** - Decisões técnicas
- **planning_guidelines.md** - Processo de refinamento

Ver mapa completo de documentação em CONSTITUTION.md.

