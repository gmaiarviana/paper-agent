# Progressão: POC → Protótipo → MVP

A estrutura básica se mantém, mas o raciocínio evolui incrementalmente:

## POC (primeira entrega - foco mínimo viável)

**Raciocínio:**
- Básico: explora, analisa contexto simples, sugere opções óbvias
- Detecção simples: compara input novo com histórico (mudanças óbvias)

**Funcionalidades:**
- 7.1: Orquestrador mantém diálogo fluido (não apenas roteia)
- 7.2: Chama agente automaticamente quando contexto suficiente
- 7.3: Faz curadoria da resposta (tom único, coeso)

**Critérios de aceite:**
- Sistema conversa antes de chamar agente
- Chama agente automaticamente quando contexto suficiente (não pede permissão)
- Orquestrador faz curadoria da resposta final (tom unificado, primeira pessoa)
- Confirma entendimento, não pede permissão
- Transparência nos bastidores (usuário pode ver quem trabalhou)

## Protótipo (segunda entrega - inteligência básica)

**Raciocínio:**
- Refinado: análise mais profunda, identifica padrões sutis
- Provocação: faz perguntas que ajudam usuário a refletir

**Funcionalidades:**
- 7.4: Detecção inteligente de quando agente faz sentido
- 7.5: Provocação de reflexão ("Você pensou em X?")
- 7.6: Handling de mudança de direção

**Critérios de aceite:**
- Sistema sugere agente apropriado no momento certo
- Faz perguntas esclarecedoras que ajudam usuário
- Adapta quando usuário muda de ideia

## MVP (terceira entrega - sistema completo)

**Raciocínio:**
- Argumento focal explícito: extrai e atualiza campo focal_argument no state
- Provocação de reflexão: identifica lacunas na conversa e faz perguntas inteligentes
- Detecção emergente: infere estágio sem classificar explicitamente

**Funcionalidades:**
- 7.8: Argumento Focal Explícito (campo no MultiAgentState)
- 7.9: Provocação de Reflexão (versão simples)
- 7.10: Detecção Emergente de Estágio (exploration → hypothesis)

**Critérios de aceite:**
- Orquestrador extrai e atualiza argumento focal explicitamente (campo focal_argument)
- Identifica lacunas na conversa e faz perguntas que ajudam usuário a refletir
- Sistema detecta quando conversa evoluiu (exploration → hypothesis) e sugere mudança de estágio

---

**Próximas seções:**
- [Implementação](./implementation.md) - Mudanças técnicas
- [Protótipo CLI](./prototype_cli.md) - Detalhes do protótipo

