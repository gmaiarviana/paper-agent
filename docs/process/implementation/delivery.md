# Fechamento e Entrega

## 4. FINALIZAÇÃO: BRANCH PRONTA + AVISAR DEV

Quando todas tarefas concluídas:

> **📌 IMPORTANTE - Processo de Pull Request:**
> - ✅ Template de PR é **automático** (`.github/PULL_REQUEST_TEMPLATE.md`)
> - ✅ Agente faz **push da branch** e **avisa que está pronto**
> - ✅ Dev cria o PR **manualmente pela interface do GitHub**
> - ✅ Template é aplicado automaticamente ao criar o PR
> - ❌ Agente **NÃO precisa criar PR via `gh pr create`**

**Formato da mensagem final (OBRIGATÓRIO):**

Quando terminar, fornecer mensagem neste formato:

```
✅ Branch pronta! Você pode criar o PR pela interface do GitHub.

📋 Comandos de validação (copie e cole):

# Baixar branch
git fetch origin
git checkout <nome-real-da-branch>

# [Comandos específicos do projeto - venv, dependências, etc]

# Rodar testes
[comando específico]

# Rodar aplicação
[comando específico]

# Resultados esperados:
# - ✅ [descrição do resultado esperado 1]
# - ✅ [descrição do resultado esperado 2]
```

**Observações:**
- Substituir `<nome-real-da-branch>` pelo nome real
- Incluir comandos específicos para ativar ambiente (venv, etc)
- Comandos prontos para copiar e colar sem edição

### Checklist Obrigatório

**Testes:**
- [ ] Suite completa rodando e passando
- [ ] Coverage adequado em lógica crítica
- [ ] Sem testes quebrados ou skippados

**Código:**
- [ ] Aplicação rodando sem erros
- [ ] Console limpo (sem warnings críticos)
- [ ] Comportamento conforme roadmap

**Documentação (OBRIGATÓRIA):**
- [ ] README.md atualizado (se mudou setup/comandos)
- [ ] docs/ARCHITECTURE.md atualizado (se mudou estrutura)
- [ ] ROADMAP.md marcado como concluído
- [ ] Comentários em código complexo

**Git:**
- [ ] Branch criada: `feature/X.Y-nome-funcionalidade`
- [ ] Commits organizados (se houver vários)
- [ ] Push realizado para branch remota
- [ ] **Dev notificado que branch está pronta** (dev cria PR pela interface)
- [ ] **Comandos de validação local fornecidos COM NOME REAL DA BRANCH** (copiar e colar)
- [ ] **Merge somente após validação manual do dev**

### Template de PR (Referência)

> **📌 NOTA:** O template oficial está em `.github/PULL_REQUEST_TEMPLATE.md` e é aplicado automaticamente quando você cria um PR pela interface do GitHub. O template abaixo é apenas para referência sobre o que incluir.

````markdown
## Funcionalidade X.Y: [Nome]

### Implementado
- [Resumo do que foi feito]
- [Principais mudanças técnicas]

### Testes
- [Onde foram adicionados testes]
- [Coverage: X%]
- [Como rodar: `npm test` ou similar]

### Documentação Atualizada
- [ ] README.md
- [ ] docs/ARCHITECTURE.md
- [ ] ROADMAP.md

### ⚙️ Validação Local (para dev testar antes de mergear)

**1. Baixar e preparar branch:**
```powershell
# Buscar branch remota
git fetch origin

# Criar ou atualizar branch local a partir da remota
git checkout feature/X.Y-nome-funcionalidade
git pull origin feature/X.Y-nome-funcionalidade

# Instalar/atualizar dependências (se houver mudanças)
[comando específico: npm install; poetry install; etc]
```

**2. Rodar aplicação:**
```powershell
[comandos específicos baseados no README.md]
# Exemplo: docker compose up -d
# Exemplo: npm run dev
# Exemplo: uvicorn app.main:app --reload
```

**3. Rodar testes:**
```powershell
[comando específico de testes]
# Exemplo: npm test
# Exemplo: pytest
# Exemplo: python -m pytest tests/unit
```

**4. Validar funcionalidade:**

**Teste Manual 1:**
- Acesse: `http://localhost:XXXX/rota-especifica`
- Ação: [descrição exata do que fazer]
- Resultado esperado: [o que deve acontecer]

**Teste Manual 2:**
- [outro cenário de teste]

**Teste Manual 3:**
- [outro cenário de teste]

**Critérios de Aceite:**
✅ [Comportamento 1 deve funcionar]
✅ [Comportamento 2 deve funcionar]
❌ [Comportamento 3 NÃO deve acontecer]

**5. Encerrar:**
```powershell
# Parar aplicação
[comando específico: docker compose down; Ctrl+C; etc]

# Voltar para branch principal (se quiser)
git checkout main
```

### Notas Técnicas
[Qualquer observação importante para review]
[Decisões técnicas tomadas]
[Possíveis pontos de atenção]

### Travamentos/Bloqueios
- [ ] Nenhum travamento durante implementação
- [ ] OU: [Descrição de travamentos e como foram resolvidos]
````

---

**Ver também:**
- Para regras de qualidade → [quality_rules.md](quality_rules.md)
- Para entender o fluxo completo → [workflow.md](workflow.md)
