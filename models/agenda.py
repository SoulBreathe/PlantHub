from dataclasses import dataclass
from typing import Optional


@dataclass
class TarefaAgenda:
    """Modelo de dados para a tabela AgendaDeCuidados."""

    id_agenda: Optional[int] = None
    tipo_tarefa: str = ""
    detalhes: Optional[str] = None
    data_agendada: str = ""
    data_conclusao: Optional[str] = None
    realizada: bool = False
    id_planta: int = 0
