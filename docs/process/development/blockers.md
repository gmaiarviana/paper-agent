# Bloqueios e Travamentos

## 3. DETECÇÃO DE TRAVAMENTO (OBRIGATÓRIO)

**Critério de travamento:**
- Tentou a mesma solução **3 vezes** sem sucesso
- Teste continua falho após 3 abordagens diferentes
- Erro persistente após 3 tentativas de debug
- Qualquer situação circular/repetitiva

**Quando detectar travamento:**

1. **PARE imediatamente** (não tente 4ª, 5ª, 6ª vez)

2. **Reporte ao dev:**
```
🚨 TRAVAMENTO DETECTADO - Tarefa X.Y.Z

**Tentativas:**
1. [Abordagem 1] → [Resultado/Erro]
2. [Abordagem 2] → [Resultado/Erro]
3. [Abordagem 3] → [Resultado/Erro]

**Problema:**
[Descrição clara do que está travando]

**Opções:**
A) Ajustar abordagem: [sugestão específica]
B) Quebrar tarefa em partes menores
C) Pular tarefa e sinalizar no PR como pendente
D) Mudar estratégia técnica: [alternativa]

Aguardando decisão.
```

3. **Aguardar instrução do dev** (não seguir sozinho)

---

## Tratamento de Erros/Bloqueios

### Se teste não passar:
1. Analisar falha
2. Tentar abordagem diferente
3. Se falhar 3x → **PARAR e reportar travamento**

### Se funcionalidade complexa demais:
1. Quebrar em sub-tarefas menores
2. Implementar incrementalmente
3. Validar parcialmente
4. Se travamento persistir → **PARAR e reportar**

### Se dependência externa falhar:
1. Mockar dependência
2. Implementar lógica principal
3. Documentar necessidade de validação real no PR
4. Se bloqueio total → **PARAR e reportar**

### Se qualquer situação circular (3+ tentativas iguais):
1. **PARAR imediatamente**
2. Reportar travamento com detalhes
3. Sugerir opções (ajuste, quebra, pular, alternativa)
4. Aguardar decisão do dev

---

**Ver também:**
- Para voltar à implementação → [implementation.md](implementation.md)
- Para finalização após resolver bloqueio → [delivery.md](delivery.md)
