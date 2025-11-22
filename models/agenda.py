from dataclasses import dataclass
from typing import Optional


@dataclass
class TarefaAgenda:
    tipo_tarefa: str
    data_agendada: str
    id_planta: int = 0
    detalhes: Optional[str] = None
    realizada: bool = False
    id_agenda: Optional[int] = None
