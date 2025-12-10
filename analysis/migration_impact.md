# Análise de Impacto da Migração

Estimativas detalhadas do impacto de mover cada módulo principal.

## agents/ → core/agents/

### Arquivos Afetados

- **Arquivos de código**: 45 arquivos
- **Arquivos de testes**: 0 arquivos
- **Arquivos de documentação**: 0 arquivos
- **Total de arquivos no diretório**: 45 arquivos

### Imports a Ajustar

- **Arquivos que precisam ajustar imports**: 84 arquivos
- **Total de imports a ajustar**: ~232 linhas
- **Nota**: ~60 arquivos de teste também precisarão ajustar imports de `from agents.` para `from core.agents.` quando os testes forem migrados

### Referências em Documentação

- **Referências a ajustar**: ~557 referências
### Risco de Quebra

- **Nível**: **Alto**
- **Justificativa**: Muitos arquivos afetados (84) e muitos imports a ajustar (232). Requer atenção cuidadosa e testes extensivos.

### Tempo Estimado de Migração

- **Estimativa**: 4 horas


---


## utils/ → core/utils/

### Arquivos Afetados

- **Arquivos de código**: 22 arquivos
- **Arquivos de testes**: 2 arquivos
- **Arquivos de documentação**: 0 arquivos
- **Total de arquivos no diretório**: 24 arquivos

### Imports a Ajustar

- **Arquivos que precisam ajustar imports**: 55 arquivos
- **Total de imports a ajustar**: ~93 linhas
- **Nota**: ~10 arquivos de teste também precisarão ajustar imports de `from utils.` para `from core.utils.` quando os testes forem migrados

### Referências em Documentação

- **Referências a ajustar**: ~185 referências
### Risco de Quebra

- **Nível**: **Alto**
- **Justificativa**: Muitos arquivos afetados (55) e muitos imports a ajustar (93). Requer atenção cuidadosa e testes extensivos.

### Tempo Estimado de Migração

- **Estimativa**: 2 horas


---


## app/ → products/revelar/app/

### Arquivos Afetados

- **Arquivos de código**: 21 arquivos
- **Arquivos de testes**: 0 arquivos
- **Arquivos de documentação**: 0 arquivos
- **Total de arquivos no diretório**: 21 arquivos

### Imports a Ajustar

- **Arquivos que precisam ajustar imports**: 12 arquivos
- **Total de imports a ajustar**: ~23 linhas
- **Nota**: ~5 arquivos de teste também precisarão ajustar imports de `from app.` para `from products.revelar.app.` quando os testes forem migrados

### Referências em Documentação

- **Referências a ajustar**: ~153 referências
### Risco de Quebra

- **Nível**: **Baixo**
- **Justificativa**: Poucos arquivos afetados (12) e imports (23). Migração relativamente simples.

### Tempo Estimado de Migração

- **Estimativa**: 1.5 horas


---


## cli/ → core/tools/cli/

### Arquivos Afetados

- **Arquivos de código**: 2 arquivos
- **Arquivos de testes**: 0 arquivos
- **Arquivos de documentação**: 0 arquivos
- **Total de arquivos no diretório**: 2 arquivos

### Imports a Ajustar

- **N/A**: Este módulo não é importado por outros (ou não tem imports Python)

### Referências em Documentação

- **Referências a ajustar**: ~59 referências
### Risco de Quebra

- **Nível**: **Baixo**
- **Justificativa**: Poucos arquivos afetados (0) e imports (0). Migração relativamente simples.

### Tempo Estimado de Migração

- **Estimativa**: 52 minutos


---


## tests/ → tests/core/

### Arquivos Afetados

- **Arquivos de código**: 0 arquivos
- **Arquivos de testes**: 73 arquivos
- **Arquivos de documentação**: 4 arquivos
- **Total de arquivos no diretório**: 77 arquivos

### Imports a Ajustar

- **Arquivos de teste que precisam ajustar imports**: ~60 arquivos
- **Total de imports a ajustar**: ~166 linhas (já contabilizados nas migrações de agents/, utils/, app/)
- **Nota**: Os testes importam os módulos que serão movidos, então quando agents/, utils/ e app/ forem migrados, os testes precisarão ajustar seus imports. Isso já está incluído nas estimativas das migrações anteriores.

### Referências em Documentação

- **Referências a ajustar**: ~319 referências
### Risco de Quebra

- **Nível**: **Baixo**
- **Justificativa**: Poucos arquivos afetados (0) e imports (0). Migração relativamente simples.

### Tempo Estimado de Migração

- **Estimativa**: 2 horas


---


## docs/ → docs/core/

### Arquivos Afetados

- **Arquivos de código**: 0 arquivos
- **Arquivos de testes**: 0 arquivos
- **Arquivos de documentação**: 135 arquivos
- **Total de arquivos no diretório**: 139 arquivos

### Imports a Ajustar

- **N/A**: Este módulo não é importado por outros (ou não tem imports Python)

### Referências em Documentação

- **Referências a ajustar**: ~786 referências
### Risco de Quebra

- **Nível**: **Baixo**
- **Justificativa**: Poucos arquivos afetados (0) e imports (0). Migração relativamente simples.

### Tempo Estimado de Migração

- **Estimativa**: 4 horas


---


## Resumo Geral

| Módulo | Arquivos | Imports | Docs | Risco | Tempo |
|--------|----------|---------|------|-------|-------|
| `agents/` | 45 | 232 | 557 | Alto | 4 horas |
| `utils/` | 24 | 93 | 185 | Alto | 2 horas |
| `app/` | 21 | 23 | 153 | Baixo | 1.5 horas |
| `cli/` | 2 | 0 | 59 | Baixo | 52 minutos |
| `tests/` | 73 | 0 | 319 | Baixo | 2 horas |
| `docs/` | 0 | 0 | 786 | Baixo | 4 horas |

**Totais**: 165 arquivos, 348 imports, 2059 referências em docs
