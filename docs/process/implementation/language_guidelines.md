# Language Guidelines

## Estratégia de Idioma

Este projeto adota **bilinguismo estratégico** para otimizar usabilidade e manutenibilidade:

---

## Regras

### 🇧🇷 Português Brasileiro (PT-BR)

**Usar em:**
- ✅ Mensagens ao usuário final (CLI, logs, erros)
- ✅ Docstrings e comentários internos
- ✅ Documentação técnica (`docs/`)
- ✅ Commits e PRs

**Justificativa:**
- Audiência principal é brasileira/acadêmica
- Facilita colaboração local
- Reduz barreira de entrada para novos contribuidores

### 🇬🇧 English (EN)

**Usar em:**
- ✅ Código (variáveis, funções, classes)
- ✅ Nomes de arquivos/pastas
- ✅ Configurações técnicas (pytest.ini, requirements.txt)

**Justificativa:**
- Convenção universal de programação
- Compatibilidade com ferramentas (linters, IDEs)
- Legibilidade para revisores internacionais (se necessário)

---

## Exemplos

### ✅ Correto

```python
def create_methodologist_graph():
    """
    Cria o grafo do agente Metodologista.

    Este grafo implementa o fluxo de análise de hipóteses científicas,
    incluindo nós para análise, clarificação e decisão final.

    Returns:
        StateGraph: Grafo compilado pronto para execução
    """
    # Definir nós do grafo
    initial_state = create_initial_state(hypothesis)

    # Mensagem ao usuário em PT-BR
    print("🔬 Analisando hipótese...")

    return graph
```

### ❌ Evitar

```python
def criar_grafo_metodologista():  # ❌ Nome de função em PT
    """
    Creates the methodologist agent graph.  # ❌ Docstring em inglês
    """
    estado_inicial = criar_estado_inicial(hipotese)  # ❌ Variáveis em PT

    print("🔬 Analyzing hypothesis...")  # ❌ Mensagem ao usuário em EN

    return grafo
```

---

## Arquivos

### Mensagens ao Usuário

**CLI (core/tools/cli/chat.py):**
```python
print("=" * 70)
print("CLI MINIMALISTA - AGENTE METODOLOGISTA")  # ✅ PT-BR
print("=" * 70)
print("Digite sua hipótese para avaliação metodológica.")  # ✅ PT-BR
```

**Erros e Logs:**
```python
logging.error("❌ Falha ao conectar com API")  # ✅ PT-BR
raise ValueError("Hipótese não pode ser vazia")  # ✅ PT-BR
```

### Código e Testes

**Variáveis, funções e testes:**
```python
# ✅ Correto (inclui nomes de testes)
hypothesis = "..."
thread_id = f"session-{uuid.uuid4()}"
def analyze_hypothesis(state):
    ...

def test_orchestrator_classifies_vague_idea():
    ...

# ❌ Evitar (variáveis e nomes de testes em PT)
hipotese = "..."
id_thread = f"sessao-{uuid.uuid4()}"
def analisar_hipotese(estado):
    ...

def test_classificacao_vaga():
    ...
```

---

## Commits e PRs

### Commits
Use **PT-BR** com convenção Conventional Commits:

```bash
# ✅ Correto
feat: adicionar nó de clarificação ao grafo
fix: corrigir validação de entrada vazia no CLI
docs: atualizar diretrizes de testes

# ❌ Evitar (mistura)
feat: add clarification node to graph
fix: corrige empty input validation
docs: update testing guidelines
```

### Pull Requests
**Título:** PT-BR
**Descrição:** PT-BR com seções estruturadas

```markdown
# ✅ Exemplo
## Resumo
Implementa nó de clarificação para solicitar informações adicionais do usuário.

## Mudanças
- Adiciona função `ask_clarification()` em `agents/methodologist/nodes.py`
- Atualiza grafo para incluir edge condicional
- Adiciona testes unitários para o novo nó

## Testes
- [x] Testes unitários passam
- [x] Validação manual com `scripts/core/<categoria>/validate_*.py`
```

---

## Casos Especiais

### Bibliotecas Externas
Mantenha nomes originais em inglês:
```python
from langgraph.graph import StateGraph  # ✅ Não traduzir
from anthropic import Anthropic  # ✅ Manter original
```

### Termos Técnicos
Use inglês se não houver tradução natural:
```python
# ✅ Preferir inglês para termos técnicos
state = {"thread_id": "...", "checkpoint": "..."}

# ⚠️ Evitar traduções forçadas
estado = {"id_encadeamento": "...", "ponto_verificação": "..."}
```

### Prompt Engineering
Se prompts são em inglês para melhor performance do modelo, **documente isso**:
```python
def analyze(state):
    """
    Analisa hipótese usando Claude.

    Nota: O prompt do sistema está em inglês para otimizar
    performance do modelo Sonnet 4.
    """
    system_prompt = """
    You are a methodologist expert...  # ✅ OK se documentado
    """
```

---

## Checklist

Antes de fazer commit, verifique:

- [ ] Mensagens ao usuário estão em PT-BR
- [ ] Código (variáveis, funções) está em inglês
- [ ] Docstrings e comentários estão em PT-BR
- [ ] Commits seguem convenção PT-BR
- [ ] Arquivos de configuração mantêm nomes em inglês

---

**Versão:** 1.0
**Data:** 11/11/2025
**Status:** Ativo - aplicar em todos os novos códigos
