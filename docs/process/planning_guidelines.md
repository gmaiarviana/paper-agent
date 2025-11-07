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

## Exemplo de Épico

```markdown
## ÉPICO 3: Autenticação Google

**Objetivo:** Simplificar acesso ao sistema substituindo email/senha por autenticação Google, melhorando segurança e experiência do usuário.

### Funcionalidades:
#### 3.1 Implementação de Google OAuth
#### 3.2 Controle de Acesso via Gestores Cadastrados
#### 3.3 Preparação da Estrutura de Dados
```

---

## Critérios de Qualidade para Épicos

✅ Objetivo claro: Foca no valor de negócio, não em implementação técnica
✅ Coeso: Funcionalidades relacionadas que fazem sentido juntas
✅ Tamanho adequado: 2-5 funcionalidades (nem muito pequeno, nem gigante)
✅ Incremental: Entrega valor mesmo se parar no meio

---

## Template: Funcionalidade

```markdown
#### X.Y Nome Específico da Funcionalidade

- **Descrição:** [O que é esta funcionalidade em 1-2 frases]
- **Critérios de Aceite:**
  - Deve [comportamento esperado específico e testável]
  - Deve [comportamento esperado específico e testável]
  - Não deve [comportamento indesejado se relevante]
```

---

## Exemplo de Funcionalidade

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

## Critérios de Qualidade para Funcionalidades

✅ Testável: Critérios de aceite observáveis e validáveis
✅ Incremental: Entrega valor sozinha
✅ Específica: Escopo claro
✅ Valor claro: Benefício concreto
✅ Única: Não se sobrepõe a outras funcionalidades

---

## Manutenção do Roadmap

Quando épico/funcionalidade for concluído:
1. Marque ✅ no título do épico
2. Resuma em 1-2 linhas o que foi entregue
3. Remova detalhes (objetivo, critérios, sub-funcionalidades)
4. Mova para "✅ Concluído Recentemente"

Exemplo:

```markdown
## ✅ ÉPICO 2: Padronização da Interface de Resumos
Sistema com layout consistente entre páginas de resumo, exibindo dados completos do projeto via API.
```

---

## Tarefas

Uma tarefa é um conjunto incremental de atividades relacionadas que:
- ✅ É curta e focada
- ✅ Agrega valor imediatamente
- ✅ É testável
- ✅ Pode ser comitada independentemente
- ✅ Permite rollback fácil

### Mentalidade Incremental
Progresso contínuo: **POC → Protótipo → MVP → Melhorias**

Processo: Fazer → Validar → Commit → Iterar

---

## Workflow do Claude Code

### Antes de Começar
1. Verifique dúvidas ou decisões em aberto
2. Confirme que a funcionalidade pertence a épico refinado
3. Alinhe o escopo com o usuário

### Durante Implementação
- Trabalhe em funcionalidades (não épicos inteiros)
- Commits incrementais
- PR/merge só ao final da funcionalidade

### Comunicação
- Pergunte quando algo não estiver claro
- Evite assumir decisões de arquitetura

---

## Quando Parar e Perguntar
- Falta de informação
- Decisões arquiteturais abertas
- Múltiplas abordagens possíveis
- Épico não refinado

---

## Git Workflow
- Branches flexíveis no início
- Commits frequentes e descritivos
- Uma funcionalidade por PR
- Conflitos resolvidos com apoio do usuário

---

## Estratégia de Testes
- TDD pragmático (lógica crítica primeiro)
- Reavalie a estratégia conforme o projeto evolui
- **Detalhes técnicos**: `docs/testing_guidelines.md` (pirâmide de testes, mocks vs API real, estrutura)

---

## Retrospectiva de Sessão
- Documente bloqueios, perdas de eficiência e melhorias sugeridas
- Sempre alinhe antes de atualizar documentação compartilhada

