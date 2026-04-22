# Fluxos de Execução

## Cenário 1: Ideia vaga + refinamento (Implementado - Épicos 3-4)

```
Usuário: "Método incremental é mais rápido"
↓
Orquestrador: classifica "vague"
↓
Estruturador V1: "Como método incremental impacta velocidade?"
↓
Metodologista: "needs_refinement" (falta população, métricas)
  hypothesis_versions: [] → [V1] → [V1, V2]
↓
Orquestrador: apresenta feedback e opções ao usuário → usuário decide refinar
↓
Estruturador V2: "Método incremental reduz tempo em 30%, medido por sprints, em equipes 2-5 devs"
↓
Metodologista: "approved"
↓
END
```

**Resultado:** Usuário recebe V2 aprovada com histórico V1 → V2

---

## Cenário 2: Hipótese → Metodologista direto (Implementado - Épico 3)

```
Usuário: "Método X reduz tempo em 30% em equipes de 2-5 devs"
↓
Orquestrador: classifica "semi_formed" ou "complete"
↓
Metodologista: valida rigor científico
↓
Status: "approved" ou "rejected"
↓
END
```

---

## Cenário 3: Conversação adaptativa (Futuro - Épico 7 POC)

```
Usuário: "Quero entender impacto de LLMs em produtividade"
↓
Orquestrador: "Interessante! Você quer VER o que já existe ou TESTAR uma hipótese?"
↓
Usuário: "Testar"
↓
Orquestrador: "Legal! Me conta: o que é 'produtividade' pra você?"
↓ [conversa continua]
Usuário: "Velocidade de desenvolvimento"
↓
Orquestrador: "Entendi. Posso chamar o Metodologista pra validar se isso é testável?"
↓
Usuário: "Sim"
↓
[Chama Metodologista] → Feedback: "Falta população e métricas"
↓
Orquestrador: "Ele sugeriu especificar:
               1. Quem você quer estudar?
               2. Como medir velocidade?
               Quer refinar agora ou pesquisar literatura primeiro?"
↓
Usuário: "Refinar"
↓
[Chama Estruturador] → V2 refinada
↓
[Loop continua conforme usuário decide]
```

---

## Referências

- **Estado completo:** [state.md](state.md)
- **Construção do grafo:** [graph.md](graph.md)
- **Implementação dos nós:** [nodes.md](nodes.md)

