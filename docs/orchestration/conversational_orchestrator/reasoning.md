# Raciocínio do Orquestrador

## Capacidades do Orquestrador POC

O Orquestrador POC deve:

1. **Explorar com perguntas abertas**
   - Quantas perguntas forem necessárias
   - Não classifica, apenas explora o espaço do problema
   - Exemplo: "Me conta mais sobre essa observação. Onde você viu isso acontecer?"

2. **Analisar contexto do input + histórico**
   - Considera não apenas o input atual, mas toda a conversa
   - Identifica padrões, contradições, lacunas
   - Não é "garçom" (não apenas repassa), mas analisa ativamente

3. **Opinar sobre direções possíveis**
   - Sugere múltiplas direções com justificativa clara
   - Explica por que cada direção faz sentido
   - Não impõe, apenas oferece opções

4. **Detectar mudança de direção**
   - Compara novo input com histórico conversacional
   - Identifica contradições ou mudanças de foco
   - Adapta sem questionar ou criar fricção

## Exemplo de Análise Contextual

**Input do usuário:**
```
"Observei que LLMs aumentam produtividade"
```

**Análise do Orquestrador:**
```
Interessante observação! Estou percebendo que você tem uma crença sobre LLMs, 
mas não mencionou como mediu produtividade ou em que contexto. Isso me sugere 
duas direções:

1. Se você quer VALIDAR essa crença, precisamos transformar em hipótese testável 
   (chamar Metodologista ajuda aqui)

2. Se você quer primeiro ENTENDER o que já existe, podemos fazer revisão de 
   literatura

Me conta mais: essa observação veio de experiência pessoal ou você já tem dados?
```

**Características da análise:**
- ✅ Identifica lacuna (falta de medição/contexto)
- ✅ Oferece múltiplas direções com justificativa
- ✅ Faz pergunta aberta para continuar exploração
- ✅ Não classifica como "vague" ou "complete"

## Detecção de Mudança de Direção

### Mecanismo de Detecção

**Como funciona:**
- LLM compara novo input com histórico conversacional
- Detecta contradições ou mudanças de foco
- Adapta sem questionar ou criar fricção

**Exemplo:**

**Histórico:**
```
Usuário: "Quero estudar impacto de LLMs em produtividade de desenvolvedores"
Orquestrador: [explora contexto, sugere direções]
Usuário: "Na verdade, quero focar em qualidade de código, não produtividade"
```

**Detecção:**
```
Orquestrador detecta mudança de foco (produtividade → qualidade) e adapta:
"Entendi! Você mudou o foco de produtividade para qualidade de código. 
Isso muda a abordagem metodológica. Estruturei uma hipótese sobre qualidade: 
[resultado]. Isso direciona bem o que você quer testar?"
[Bastidores: 📝 Estruturador estruturou → 🎯 Orquestrador curou]
```

**Características:**
- ✅ Reconhece mudança explicitamente
- ✅ Não questiona ("por que mudou?")
- ✅ Adapta sugestões ao novo foco
- ✅ Mantém contexto do histórico

### Conceito: "Argumento Focal"

**Definição:**
O sistema está construindo um **"argumento focal"** sobre o que o usuário quer fazer. Esse argumento evolui ao longo da conversa e serve como âncora para detectar contexto e mudanças de direção.

**Conexão com Épico 11:**
No Épico 11, o argumento focal se tornará campo explícito na entidade `Idea` (anteriormente "Topic"), permitindo persistência e rastreamento formal. No POC, ele é implícito (reconstruído a cada turno via histórico).

**No POC:**
- Detecção simples via comparação LLM (novo input vs histórico)
- Argumento focal é implícito (vive apenas no histórico)
- LLM reconstrói argumento focal a cada turno analisando histórico
- Detecta mudanças óbvias (contradições, mudança de foco)

---

**Próximas seções:**
- [Fluxo](./flow.md) - Fluxo conversacional completo
- [Exemplos](./examples.md) - Exemplos concretos de detecção

