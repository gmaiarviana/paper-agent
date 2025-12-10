"""
Loader de configurações YAML de agentes (Épico 6).

Este módulo carrega e valida configurações de agentes a partir de arquivos YAML
no diretório config/agents/.

"""

import yaml
from pathlib import Path
from typing import Dict, Any, List

from .config_validator import validate_agent_config_schema, ConfigValidationError

# Cache em memória para configurações carregadas
# Evita múltiplas leituras do disco (load_agent_config é chamado 3+ vezes por turno)
_config_cache: Dict[str, Dict[str, Any]] = {}

# Diretório base de configurações
# Suporta tanto a estrutura antiga (agents/memory/) quanto a nova (core/agents/memory/)
# Quando em core/agents/memory/: Path(__file__).parent.parent.parent = core/
# Quando em agents/memory/: Path(__file__).parent.parent.parent = raiz/
def _get_config_dir() -> Path:
    """Retorna o diretório de configurações, suportando ambas as estruturas."""
    current_file = Path(__file__).resolve()
    base_path = current_file.parent.parent.parent
    
    # Se estamos em core/agents/memory/, base_path = core/
    # Então config está em: core/config/agents/
    new_path = base_path / "config" / "agents"
    if new_path.exists():
        return new_path
    
    # Se estamos em agents/memory/, base_path = raiz/
    # Então config está em: raiz/core/config/agents/
    old_path = base_path / "core" / "config" / "agents"
    if old_path.exists():
        return old_path
    
    # Se nenhum existe, retornar o caminho novo (assumindo migração futura)
    return new_path

CONFIG_DIR = _get_config_dir()

class ConfigLoadError(Exception):
    """Exceção levantada quando não é possível carregar configuração."""
    pass

def load_agent_config(agent_name: str) -> Dict[str, Any]:
    """
    Carrega configuração de um agente específico do arquivo YAML.
    
    Utiliza cache em memória para evitar múltiplas leituras do disco
    (esta função é chamada 3+ vezes por turno em diferentes agentes).

    Args:
        agent_name (str): Nome do agente (ex: "orchestrator", "structurer", "methodologist")

    Returns:
        Dict[str, Any]: Configuração validada do agente

    Raises:
        ConfigLoadError: Se arquivo não existe ou está inválido
        ConfigValidationError: Se configuração não passa na validação de schema

    Example:
        >>> config = load_agent_config("orchestrator")
        >>> print(config["model"])
        'claude-3-5-haiku-20241022'
        >>> print(config["context_limits"]["max_input_tokens"])
        4000
    """
    # Verificar cache primeiro
    if agent_name in _config_cache:
        return _config_cache[agent_name]
    
    # Construir caminho do arquivo
    config_file = CONFIG_DIR / f"{agent_name}.yaml"

    # Verificar se arquivo existe
    if not config_file.exists():
        raise ConfigLoadError(
            f"Arquivo de configuração não encontrado: {config_file}\n"
            f"Agente: '{agent_name}'\n"
            f"Diretório esperado: {CONFIG_DIR}"
        )

    # Tentar carregar YAML
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigLoadError(
            f"Erro ao fazer parse do arquivo YAML para agente '{agent_name}': {e}"
        )
    except Exception as e:
        raise ConfigLoadError(
            f"Erro ao ler arquivo de configuração para agente '{agent_name}': {e}"
        )

    # Validar que YAML não está vazio
    if config is None:
        raise ConfigLoadError(
            f"Arquivo de configuração vazio para agente '{agent_name}': {config_file}"
        )

    # Validar schema
    validate_agent_config_schema(config, agent_name)

    # Armazenar no cache
    _config_cache[agent_name] = config

    return config

def load_all_agent_configs() -> Dict[str, Dict[str, Any]]:
    """
    Carrega configurações de todos os agentes disponíveis.

    Busca todos os arquivos .yaml no diretório config/agents/ e carrega cada um,
    validando o schema.

    Returns:
        Dict[str, Dict[str, Any]]: Dicionário mapeando nome do agente para sua configuração

    Raises:
        ConfigLoadError: Se algum arquivo não pode ser carregado
        ConfigValidationError: Se alguma configuração não passa na validação

    Example:
        >>> configs = load_all_agent_configs()
        >>> print(configs.keys())
        dict_keys(['orchestrator', 'structurer', 'methodologist'])
        >>> print(configs['orchestrator']['model'])
        'claude-3-5-haiku-20241022'
    """
    # Verificar se diretório existe
    if not CONFIG_DIR.exists():
        raise ConfigLoadError(
            f"Diretório de configurações não encontrado: {CONFIG_DIR}\n"
            f"Certifique-se de que o diretório 'config/agents/' existe."
        )

    # Buscar todos os arquivos .yaml
    config_files = list(CONFIG_DIR.glob("*.yaml"))

    if not config_files:
        raise ConfigLoadError(
            f"Nenhum arquivo de configuração encontrado em: {CONFIG_DIR}\n"
            f"Esperado pelo menos um arquivo .yaml"
        )

    # Carregar cada configuração
    configs = {}
    errors = []

    for config_file in config_files:
        agent_name = config_file.stem  # Nome do arquivo sem extensão

        try:
            config = load_agent_config(agent_name)
            configs[agent_name] = config
        except (ConfigLoadError, ConfigValidationError) as e:
            errors.append(f"- {agent_name}: {e}")

    # Se houver erros, reportar todos
    if errors:
        raise ConfigLoadError(
            f"Erros ao carregar configurações de agentes:\n" + "\n".join(errors)
        )

    return configs

def get_agent_prompt(agent_name: str) -> str:
    """
    Obtém o system prompt de um agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        str: System prompt do agente

    Raises:
        ConfigLoadError: Se configuração não pode ser carregada

    Example:
        >>> prompt = get_agent_prompt("orchestrator")
        >>> "Orquestrador" in prompt
        True
    """
    config = load_agent_config(agent_name)
    return config["prompt"]

def get_agent_context_limits(agent_name: str) -> Dict[str, int]:
    """
    Obtém os limites de contexto de um agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        Dict[str, int]: Limites de contexto (max_input_tokens, max_output_tokens, max_total_tokens)

    Raises:
        ConfigLoadError: Se configuração não pode ser carregada

    Example:
        >>> limits = get_agent_context_limits("orchestrator")
        >>> print(limits["max_input_tokens"])
        4000
    """
    config = load_agent_config(agent_name)
    return config["context_limits"]

def get_agent_model(agent_name: str) -> str:
    """
    Obtém o modelo LLM de um agente.

    Args:
        agent_name (str): Nome do agente

    Returns:
        str: Nome do modelo LLM

    Raises:
        ConfigLoadError: Se configuração não pode ser carregada

    Example:
        >>> model = get_agent_model("methodologist")
        >>> "claude" in model.lower()
        True
    """
    config = load_agent_config(agent_name)
    return config["model"]

def list_available_agents() -> List[str]:
    """
    Lista nomes de todos os agentes com configurações disponíveis.

    Returns:
        List[str]: Lista de nomes de agentes

    Example:
        >>> agents = list_available_agents()
        >>> "orchestrator" in agents
        True
        >>> "methodologist" in agents
        True
    """
    if not CONFIG_DIR.exists():
        return []

    config_files = CONFIG_DIR.glob("*.yaml")
    return [f.stem for f in config_files]
