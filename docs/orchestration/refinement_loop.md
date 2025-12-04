# Refinement Loop - Especificação Técnica

## Visão Geral

Mecânica de refinamento colaborativo que permite ao sistema multi-agente melhorar ideias vagas até ficarem testáveis, ao invés de apenas validar ou rejeitar.

**⚠️ MUDANÇA IMPORTANTE (13/11/2025):** O loop **não é mais automático**. O refinamento acontece **sob demanda**, quando o usuário decide refinar após receber feedback do Metodologista. O Orquestrador apresenta opções e o usuário escolhe o próximo passo.

**Decisão arquitetural:** Mecânica implementada no super-grafo (não criar grafo interno no Estruturador).

---

## Componentes

### 1. MultiAgentState

Ver schema completo em `docs/orchestration/multi_agent_architecture.md`.

### 2. Metodologista - Modo Colaborativo

**Output:** Ver estrutura completa em `docs/orchestration/multi_agent_architecture.md` (seção "Estrutura de `methodologist_output`").

**Lógica de decisão:**

1. **approved:**
   - Hipótese testável, falseável, específica, operacionalizada
   - Pode ter pequenas lacunas, mas estrutura sólida
   - Pronta para desenho experimental
2. **needs_refinement:**
   - Tem potencial científico
   - Faltam elementos específicos (população, métricas, variáveis)
   - Pode ser melhorada com refinamento
   - Campo `improvements` preenchido com gaps
3. **rejected:**
   - Sem potencial científico (crença popular, impossível testar)
   - Antropomorfização sem base
   - Vagueza extrema que refinamento não resolve

**Prompt do Metodologista (atualizado):**

Adicionar ao prompt existente:

```
MODO COLABORATIVO (Épico 4):

Você é um PARCEIRO que ajuda a CONSTRUIR hipóteses, não apenas validar
Use "needs_refinement" quando a ideia tem potencial mas falta especificidade
Use "rejected" APENAS quando não há base científica
Campo "improvements": seja ESPECÍFICO sobre o que falta e como preencher

EXEMPLOS DE "needs_refinement":
Input: "Método X melhora Y"
Output: {
"status": "needs_refinement",
"justification": "Ideia central clara, mas falta operacionalização",
"improvements": [
{
"aspect": "população",
"gap": "Não especificada",
"suggestion": "Definir população-alvo (ex: desenvolvedores 2-5 anos experiência)"
},
{
"aspect": "métricas",
"gap": "Y não mensurável",
"suggestion": "Operacionalizar Y (ex: bugs/sprint, tempo de debug)"
}
]
}
```

### 3. Estruturador - Processamento de Feedback

**Input no refinamento (V2+):** Estruturador recebe `methodologist_output` do estado compartilhado (`MultiAgentState`). Ver `docs/orchestration/multi_agent_architecture.md` para estrutura completa.

**Lógica de refinamento:**

1. Ler gaps do Metodologista
2. Para cada gap, adicionar elemento faltante na questão
3. Manter essência da ideia original
4. Gerar V2 que endereça todos os gaps

**Prompt do Estruturador (atualizado):**

Adicionar ao prompt existente:

```
REFINAMENTO (Épico 4):
Quando receber feedback do Metodologista:

Identifique gaps específicos
Adicione elementos faltantes SEM mudar a essência
Endereçe TODOS os gaps listados

EXEMPLO:
Input original: "Método X é mais rápido"
Feedback: falta população, métricas
V2: "Método X reduz tempo em 30%, medido por sprints, em equipes de 2-5 devs"
Gaps endereçados:

População: "equipes de 2-5 devs"
Métricas: "tempo em 30%", "sprints"
```

### 4. Orquestrador - Negociação de Refinamento

**⚠️ MUDANÇA:** Router automático foi removido. Agora o Orquestrador apresenta opções ao usuário.

**Após Metodologista dar feedback:**

O Orquestrador recebe o output do Metodologista e:

1. **Se status = "approved":** Informa aprovação e oferece próximos passos
2. **Se status = "rejected":** Informa rejeição e oferece alternativas
3. **Se status = "needs_refinement":** Apresenta feedback e **pergunta ao usuário** o que fazer

**Exemplo de negociação (needs_refinement):**

```
Orquestrador: "O Metodologista sugeriu refinamentos: falta população 
              e métricas. O que você quer fazer?
              1) Refinar agora (chamar Estruturador)
              2) Pesquisar mais sobre métricas primeiro
              3) Seguir em outra direção"
              
Usuário: "Refinar agora"
         ↓
Orquestrador: "Perfeito! Chamando Estruturador para refinar..."
         ↓
Estruturador V2: [refina com base no feedback]
         ↓
Orquestrador: "Versão refinada criada: [resultado]. Validei novamente: [resultado da validação]. Isso faz sentido?"
[Bastidores: 📝 Estruturador refinou → 🔬 Metodologista validou → 🎯 Orquestrador curou]
```

**Código a manter (mecânica técnica):**
- `structurer_node` com lógica de refinamento (funciona bem)
- `decide_collaborative` com feedback estruturado (útil)
- Estado com versionamento (histórico de versões)

**Código a remover/refatorar:**
- ❌ Router automático `route_after_methodologist` (não consulta usuário)
- ❌ Loop forçado (sistema decide sozinho)
- ❌ `force_decision_collaborative` (não precisa mais - usuário decide)

---

## Fluxo Completo (Refinamento Sob Demanda)

### Cenário 1: Ideia vaga + refinamento sob demanda → aprovada

1. User: "Método incremental é mais rápido"
2. Orquestrador: "Interessante! Você quer testar uma hipótese ou verificar literatura?"
3. User: "Testar hipótese"
4. Orquestrador: "Organizei sua ideia em uma questão de pesquisa: 'Como método incremental impacta velocidade?' Isso captura o que você quer explorar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
5. User: "Sim, mas preciso ser mais específico"
6. Orquestrador: "Validei e refinei: 'Método incremental reduz tempo em 30%, medido por sprints, em equipes 2-5 devs'. Isso faz sentido?"
[Bastidores: 🔬 Metodologista validou → 📝 Estruturador refinou → 🎯 Orquestrador curou]
7. User: "Perfeito!"
8. Orquestrador: "Ótimo! Podemos seguir com: 1) definir desenho experimental, 2) pesquisar literatura, ou 3) algo diferente?"

### Cenário 2: Usuário escolhe pesquisar antes de refinar

1. User: "Observei X"
2. [Estruturador V1 criado]
3. Metodologista: "needs_refinement" (falta contexto, métricas)
4. **Orquestrador: "Ele sugeriu refinamentos. O que você quer fazer? 1) Refinar agora, 2) Pesquisar mais sobre métricas, 3) Outra direção"**
5. **User: "Pesquisar mais sobre métricas"**
6. Orquestrador: "Perfeito! Chamando Pesquisador..."
7. Pesquisador: [busca e sintetiza papers sobre métricas]
8. Orquestrador: "Pesquisa concluída. Agora quer refinar a questão com essas informações?"
9. User: "Sim"
10. Estruturador V2: [refina usando informações da pesquisa]
11. [Continua fluxo...]

### Cenário 3: Usuário muda de direção

1. [Fluxo de refinamento em andamento]
2. Metodologista: "needs_refinement" (falta métricas)
3. **Orquestrador: "Ele sugeriu refinamentos. O que você quer fazer? 1) Refinar agora, 2) Pesquisar mais, 3) Outra direção"**
4. **User: "Outra direção - na verdade quero fazer revisão de literatura"**
5. Orquestrador: "Sem problema! Vamos adaptar. Posso chamar o Estruturador para ajudar a definir uma questão de pesquisa estruturada (tipo PICO/SPIDER)?"
6. [Fluxo adapta para revisão...]

**Diferenças principais:**
- ✅ Usuário decide se quer refinar
- ✅ Usuário pode escolher pesquisar antes
- ✅ Usuário pode mudar de direção
- ✅ Não há limite fixo de iterações (usuário controla)
- ✅ Não há decisão forçada (sistema não decide sozinho)

---

## Implementação

**⚠️ NOTA:** Esta seção descreve a mecânica técnica que deve ser mantida. O controle do fluxo agora é conversacional (Orquestrador pergunta ao usuário).

**Arquivos com mecânica técnica (manter):**

1. `agents/orchestrator/state.py`
   - Campos úteis: `hypothesis_versions` (histórico de versões)
   - ❌ Remover: `refinement_iteration`, `max_refinements` (não precisam mais - usuário controla)

2. `agents/methodologist/nodes.py`
   - ✅ Manter: `decide_collaborative` com 3 status (approved/needs_refinement/rejected)
   - ✅ Manter: Campo `improvements` com gaps específicos
   - ❌ Remover: `force_decision_collaborative` (não precisa mais)

3. `agents/structurer/nodes.py`
   - ✅ Manter: Lógica de refinamento (processar feedback do Metodologista)
   - ✅ Manter: Versionamento (V1 → V2 → V3)

4. `agents/multi_agent_graph.py`
   - ❌ Remover: Router automático `route_after_methodologist`
   - ✅ Adicionar: Nó do Orquestrador após Metodologista (negocia com usuário)
   - ✅ Manter: Edge Metodologista → Orquestrador (não mais → Estruturador automático)

5. `utils/prompts/` (modularizado por agente)
   - ✅ Manter: Prompt do Metodologista V2 (modo colaborativo) em `methodologist.py`
   - ✅ Manter: Prompt do Estruturador V1 (handling de feedback) em `structurer.py`

**Fluxo conversacional (novo):**

Após Metodologista processar:
1. Metodologista → Orquestrador (sempre)
2. Orquestrador apresenta feedback e opções ao usuário
3. Usuário escolhe: refinar, pesquisar, ou outra direção
4. Orquestrador roteia conforme decisão do usuário

---

## Testes

**Testes unitários (mocks):**

- `test_methodologist_collaborative_mode.py`
- `test_structurer_refinement.py`
- `test_refinement_router.py`

**Testes de integração (API real):**

- `test_refinement_loop_smoke.py`

**Scripts de validação manual:**

- `scripts/flows/validate_refinement_loop.py`

---

## Metadados

- **Versão:** 2.0 (Refinamento Sob Demanda)
- **Data:** 13/11/2025
- **Status:** Especificação atualizada - loop não é mais automático, refinamento sob demanda
- **Mudança principal:** Router automático removido, Orquestrador negocia com usuário


