# Padrões de Conversa - Revelar

> **Nota:** Para mecânica universal do sistema, consulte `core/docs/vision/conversation_mechanics.md`.

Este documento contém exemplos específicos de conversas no produto Revelar.

---

## 6. Exemplos de Conversas Boas vs Ruins

> **Nota sobre Análise Contextual (Épico 7 POC):**  
> Todos os exemplos seguem o padrão de "análise contextual" onde o Orquestrador analisa o histórico da conversa e o contexto atual antes de tomar decisões. O sistema não classifica automaticamente no primeiro turno, mas explora a intenção do usuário através de diálogo, considerando todo o contexto acumulado para oferecer opções relevantes.

### 6.1 Conversa BOA: Exploração Colaborativa

```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Interessante! Me conta mais: você quer VER o que já existe 
         sobre isso, ou quer TESTAR uma hipótese sua?"
Usuário: "Testar uma hipótese"
Sistema: "Legal! Me conta mais sobre essa observação: em que contexto 
         você observou isso?"
Usuário: "Em equipes de desenvolvimento usando Claude Code"
Sistema: "Perfeito! Organizei sua ideia em uma questão de pesquisa: 
         'Como Claude Code impacta produtividade em equipes de desenvolvimento?' 
         Isso captura o que você quer explorar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
Usuário: "Sim, mas preciso definir como medir produtividade"
Sistema: "Validei e refinei: 'Como Claude Code reduz tempo de desenvolvimento 
         (medido por sprints) em equipes de 2-5 devs?' Isso faz sentido?"
[Bastidores: 🔬 Metodologista validou → 📝 Estruturador refinou → 🎯 Orquestrador curou]
Usuário: "Perfeito!"
Sistema: "Ótimo! Podemos seguir com: 1) definir desenho experimental, 
         2) pesquisar literatura sobre métricas, ou 3) algo diferente?"
```

**Por que é boa:**
- ✅ Sistema explora sem impor (análise contextual antes de classificar)
- ✅ Cada passo é negociado (considera contexto acumulado)
- ✅ Usuário tem controle (sistema oferece opções baseadas no contexto)
- ✅ Opções claras e contextuais (derivadas da análise do histórico)

### 6.2 Conversa RUIM: Pipeline Rígido

```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Detectei que seu input é vago. Classificando como 'vague'. 
         Chamando Estruturador automaticamente."
[Estruturador cria V1]
Sistema: "Chamando Metodologista automaticamente."
[Metodologista: needs_refinement]
Sistema: "Detectado needs_refinement. Refinando automaticamente 
         (iteração 1/2)."
[Estruturador cria V2]
Sistema: "Chamando Metodologista automaticamente."
[Metodologista: approved]
Sistema: "Hipótese aprovada. Finalizando."
```

**Por que é ruim:**
- ❌ Sistema decide sozinho (classifica sem análise contextual)
- ❌ Usuário não participa (não explora intenção através de diálogo)
- ❌ Sem negociação (ignora contexto da conversa)
- ❌ Fluxo determinístico (roteia automaticamente sem considerar histórico)

### 6.2.1 Conversa RUIM: Negociação Explícita (Anti-padrão)

```
Usuário: "Observei que LLMs aumentam produtividade"
Sistema: "Posso chamar o Estruturador para organizar essa ideia?"
Usuário: "Sim"
Sistema: "O Estruturador organizou: [resultado]"
Usuário: "Ok"
Sistema: "Posso chamar o Metodologista para validar?"
Usuário: "Sim"
Sistema: "O Metodologista validou: [resultado]"
```

**Por que é ruim:**
- ❌ Sistema pede permissão para cada transição (cria fricção desnecessária)
- ❌ Quebra fluidez da conversa (usuário precisa aprovar cada passo)
- ❌ Não confia no contexto suficiente (deveria chamar automaticamente)
- ❌ Anti-padrão de transição fluida (deveria apresentar resultado curado diretamente)

### 6.3 Conversa BOA: Mudança de Direção

```
Usuário: "Método X é mais rápido"
Sistema: "Interessante! Você quer testar uma hipótese ou verificar 
         literatura?"
Usuário: "Testar hipótese"
[Fluxo de estruturação e validação]
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Sem problema! Vamos adaptar. Organizei uma questão de pesquisa 
         estruturada (PICO/SPIDER) para revisão: [resultado]. Isso direciona 
         bem o que você quer buscar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
Usuário: "Sim"
Sistema: "Para buscar papers, preciso fazer chamadas de API que podem ter 
         custo. Quer que eu chame o Pesquisador agora?"
```

**Por que é boa:**
- ✅ Sistema aceita mudança sem questionar (analisa novo contexto)
- ✅ Adapta imediatamente (atualiza análise contextual)
- ✅ Preserva contexto útil (mantém informações relevantes do histórico)
- ✅ Oferece próximo passo relevante (baseado no novo contexto)

### 6.4 Conversa RUIM: Resistência a Mudança

```
Usuário: "Método X é mais rápido"
[Fluxo de estruturação]
Usuário: "Na verdade, quero fazer revisão de literatura"
Sistema: "Você já escolheu hipótese empírica. Não posso mudar agora. 
         Quer continuar com a hipótese ou começar nova sessão?"
```

**Por que é ruim:**
- ❌ Sistema resiste a mudança (ignora novo contexto)
- ❌ Força continuidade (não atualiza análise contextual)
- ❌ Não adapta (mantém decisão anterior sem reanalisar)
- ❌ Cria fricção desnecessária (não considera evolução do argumento focal)

---

## Referências

- `core/docs/vision/conversation_mechanics.md` - Mecânica universal de conversação
- `core/docs/vision/epistemology.md` - Base filosófica

