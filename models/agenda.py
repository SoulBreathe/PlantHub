from dataclasses import dataclass
from typing import Optional


@dataclass
class TarefaAgenda:
    id_agenda: Optional[int] = None
    tipo_tarefa: str = ""
    detalhes: Optional[str] = None
    data_agendada: str = ""
    data_conclusao: Optional[str] = None
    realizada: bool = False  # O SQLite retorna 0 ou 1, o Python trata bem
    id_planta: int = 0
