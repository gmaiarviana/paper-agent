"""
Módulo de memória dinâmica e contexto por agente (Épico 6).

Este módulo gerencia:
- Configuração externa de agentes (YAML)
- Registro de memória com metadados (tokens, summary)
- Reset global de sessão

Componentes:
- config_loader: Carrega configurações YAML de agentes
- config_validator: Valida schema dos arquivos YAML
- memory_manager: Gerencia histórico e metadados por agente

Versão: 1.0 (Épico 6)
Data: 12/11/2025
"""

from .config_loader import load_agent_config, load_all_agent_configs
from .config_validator import validate_agent_config_schema
from .memory_manager import MemoryManager

__all__ = [
    'load_agent_config',
    'load_all_agent_configs',
    'validate_agent_config_schema',
    'MemoryManager'
]
