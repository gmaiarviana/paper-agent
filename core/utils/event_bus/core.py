"""
Core da classe EventBus - Gerenciamento de arquivos e persistência.

Este módulo contém a classe base EventBus com métodos privados para
carregar e salvar eventos em arquivos JSON.
"""

import json
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class EventBusCore:
    """
    Classe base do EventBus com funcionalidades de persistência.

    Gerencia carregamento e salvamento de eventos em arquivos JSON.
    Cada sessão tem seu próprio arquivo.
    """

    def __init__(self, events_dir: Optional[Path] = None):
        """
        Inicializa EventBusCore.

        Args:
            events_dir (Path, optional): Diretório para armazenar eventos.
                Default: {temp_dir}/paper-agent-events (multiplataforma)
        """
        if events_dir is None:
            # Usar diretório temp do sistema operacional (funciona em Windows, Linux, Mac)
            system_temp = Path(tempfile.gettempdir())
            self.events_dir = system_temp / "paper-agent-events"
        else:
            self.events_dir = events_dir

        self.events_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"EventBus inicializado: {self.events_dir}")

    def _get_event_file(self, session_id: str) -> Path:
        """
        Retorna caminho do arquivo de eventos para uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Path: Caminho do arquivo JSON
        """
        return self.events_dir / f"events-{session_id}.json"

    def _load_events(self, session_id: str) -> Dict[str, Any]:
        """
        Carrega eventos existentes de uma sessão.

        Args:
            session_id (str): ID da sessão

        Returns:
            Dict: Estrutura {"session_id": str, "events": list}
        """
        file_path = self._get_event_file(session_id)

        if not file_path.exists():
            return {
                "session_id": session_id,
                "events": []
            }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Erro ao carregar eventos de {session_id}: {e}")
            return {
                "session_id": session_id,
                "events": []
            }

    def _save_events(self, session_id: str, data: Dict[str, Any]) -> None:
        """
        Salva eventos no arquivo da sessão.

        Args:
            session_id (str): ID da sessão
            data (Dict): Estrutura {"session_id": str, "events": list}
        """
        file_path = self._get_event_file(session_id)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logger.error(f"Erro ao salvar eventos de {session_id}: {e}")

