# Planning Guidelines

## Princípio Fundamental

**Roadmap = FUTURO** (próximos passos + ideias)
**Documentação Técnica = PRESENTE** (estado atual do sistema)

---

## Categorias de Épicos

### Épicos Refinados (Prontos para Implementação)
✅ ÉPICO 1: Setup Inicial
✅ ÉPICO 2: Agente Metodologista Standalone
✅ ÉPICO 3: Orquestrador com Reasoning
✅ ÉPICO 4: Interface CLI e Streamlit

**Claude Code só implementa funcionalidades de épicos refinados.**

### Épicos Não-Refinados (Requerem Discussão)
⚠️ ÉPICO 5: Integração com LangGraph State (requer aprofundamento em LangGraph antes da implementação)

---

## Estrutura do Roadmap

### 💡 IDEIAS FUTURAS
Ideias abstratas que ainda não viraram épicos. Aguardando maturação.

### 📍 PRÓXIMOS PASSOS

**Épicos podem estar em dois estados:**

- **Não Refinados:** Apenas objetivo definido. Aguardando sessão de refinamento.
- **Refinados:** Com funcionalidades e critérios de aceite. Prontos para implementação.

**Fluxo:** Ideia → Épico (não refinado) → Sessão de refinamento → Épico (refinado) → Implementação

### ✅ CONCLUÍDO RECENTEMENTE
Resumo enxuto (1-2 linhas) dos últimos épicos. Remove manualmente quando acumular.

---

## Template: Épico em Dois Estágios

### Ao promover ideia para épico (Não Refinado):

```markdown
## ÉPICO X: Nome Descritivo
**Objetivo:** [O que queremos alcançar com este épico. Foco no valor de negócio.]
```

### Após sessão de refinamento (Refinado):

```markdown
## ÉPICO X: Nome Descritivo
**Objetivo:** [O que queremos alcançar com este épico. Foco no valor de negócio.]

### Funcionalidades:
#### X.1 Nome da Funcionalidade
#### X.2 Nome da Funcionalidade
[...]
```

**Quando refinar?**
- Em sessão dedicada de refinamento
- Apenas quando épico se tornar prioritário
- Considera estado técnico atual do sistema

---

## Exemplo de Épico:

```markdown
## ÉPICO 3: Autenticação Google

**Objetivo:** Simplificar acesso ao sistema substituindo email/senha por autenticação Google, melhorando segurança e experiência do usuário.

### Funcionalidades:
#### 3.1 Implementação de Google OAuth
#### 3.2 Controle de Acesso via Gestores Cadastrados
#### 3.3 Preparação da Estrutura de Dados
```

---

## Critérios de Qualidade para Épicos:

✅ Objetivo claro: Foca no valor de negócio, não em implementação técnica
✅ Coeso: Funcionalidades relacionadas que fazem sentido juntas
✅ Tamanho adequado: 2-5 funcionalidades (nem muito pequeno, nem gigante)
✅ Incremental: Entrega valor mesmo se parar no meio

---

## Template: Como Escrever uma Funcionalidade

```markdown
#### X.Y Nome Específico da Funcionalidade

- **Descrição:** [O que é esta funcionalidade em 1-2 frases]
- **Critérios de Aceite:**
  - Deve [comportamento esperado específico e testável]
  - Deve [comportamento esperado específico e testável]
  - Não deve [comportamento indesejado se relevante]
```

---

## Exemplo de Funcionalidade:

```markdown
#### 3.1 Implementação de Google OAuth

- **Descrição:** Configurar autenticação via Google OAuth no backend e frontend
- **Critérios de Aceite:**
  - Página de login deve ter apenas botão "Entrar com Google"
  - Após autenticação Google, verificar se email está na lista autorizada
  - Se email autorizado: criar/atualizar usuário e gerar JWT
  - Se email não autorizado: exibir mensagem de acesso negado
```

---

## Critérios de Qualidade para Funcionalidades:

✅ Testável: Critérios de aceite são observáveis e validáveis
✅ Incremental: Entrega valor sozinha, não depende de outras funcionalidades
✅ Específica: Escopo claro, não é genérica ou vaga
✅ Valor claro: Usuário/negócio percebe benefício concreto
✅ Única: Não se sobrepõe com outras funcionalidades

---

## Manutenção do Roadmap

Quando épico/funcionalidade é concluído:

1. Marca ✅ no título do épico
2. Resume em 1-2 linhas o que foi entregue
3. Remove detalhes (objetivo, critérios de aceite, sub-funcionalidades)
4. Move para seção "✅ Concluído Recentemente"

### Exemplo de épico concluído:

```markdown
## ✅ ÉPICO 2: Padronização da Interface de Resumos
Sistema com layout consistente entre páginas de resumo, exibindo dados completos do projeto via API.
```

---

## O que é uma Tarefa?

Uma tarefa é um **conjunto incremental de atividades relacionadas** que:
- ✅ É **curta** e focada
- ✅ **Agrega valor** imediatamente
- ✅ É **testável**
- ✅ Pode ser **comitada** independentemente
- ✅ Permite **rollback** fácil se necessário

### Mentalidade Incremental
Sempre evoluir em fases: **POC → Protótipo → MVP → Melhorias**

Aplica-se em todos os níveis (épico, funcionalidade, tarefa):
1. Fazer
2. Validar
3. Commit
4. Partir para melhorias (ou rollback se necessário)

**Não existe fórmula determinística** - o importante é o progresso incremental e validação constante.

---

## Workflow do Claude Code

### Antes de Começar Qualquer Tarefa
1. ❓ **SEMPRE perguntar** se há dúvidas ou decisões em aberto
2. 🔍 **Validar** que a funcionalidade está em épico refinado
3. 📋 **Alinhar** o que será feito (não assumir nada)
4. ✋ **Parar e perguntar** se não houver informações suficientes

### Durante a Implementação
- Trabalhar em **funcionalidades**, não em épicos inteiros
- Fazer commits incrementais
- Push pode ser a cada commit
- PR/merge só ao **final da funcionalidade**

### Comunicação
**Melhor perguntar do que assumir!**
- "Não tenho informações suficientes para seguir" ✅
- Assumir decisões de arquitetura sem alinhar ❌

---

## Quando Parar e Perguntar

Claude Code deve parar quando:
- ❓ Não tem informações suficientes
- ⚠️ Decisão de arquitetura não está clara
- 🤔 Múltiplas abordagens são possíveis
- 📋 Épico não está refinado

**Aprender com o processo**: Exemplos concretos serão adicionados conforme avançamos.

---

## Git Workflow

### Branches
- Sem convenção rígida no início
- Aprender e definir conforme necessário

### Commits
- Frequentes e incrementais
- Mensagens descritivas (convenção a definir se necessário)
- Push pode ser feito a cada commit

### Pull Requests
- **Uma funcionalidade = Um PR** com múltiplos commits relacionados
- PR/merge só ao final da funcionalidade completa

### Resolução de Conflitos
- Usuário tem voto de minerva
- Debugar caso a caso
- Sem regras rígidas por enquanto (aprender com processo)

---

## Estratégia de Testes

**TDD Pragmático** (aprovado para início):
- Testes para lógica crítica
- Validação incremental
- Balance entre cobertura e velocidade

**Status atual**: Abordagem está boa para começar
**Revisão futura**: Ajustar conforme aprendemos

---

## Retrospectiva de Sessão

### Ao Final de Cada Funcionalidade

Claude Code deve sempre apresentar análise de:

#### 🚧 Onde Travamos
- Quais pontos bloquearam o progresso?
- Informações que faltaram?
- Decisões que precisaram de alinhamento?

#### ⚡ Onde Perdemos Eficiência
- Retrabalho desnecessário?
- Comunicação que poderia ter sido mais clara?
- Etapas que poderiam ter sido puladas ou otimizadas?

#### 💡 Melhorias para o Projeto
- O que pode ser documentado para evitar repetição?
- Exemplos que devem ser adicionados?
- Guidelines que precisam ser atualizadas?
- Ferramentas/processos que facilitariam próximas sessões?

### Importante
- **Sempre apresentar sugestões** antes de aplicar
- **Alinhar com usuário** antes de atualizar documentação
- Focar em **melhorias acionáveis e específicas**