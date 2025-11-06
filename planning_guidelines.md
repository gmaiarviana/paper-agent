# Planning Guidelines

## Princípio Fundamental

**Roadmap = FUTURO** (próximos passos + ideias)  
**Documentação Técnica = PRESENTE** (estado atual do sistema)

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