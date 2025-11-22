from dataclasses import dataclass
from typing import Optional


@dataclass
class RegistroPraga:
    data_identificacao: str
    id_planta: int = 0
    id_praga: int = 0
    status_tratamento: Optional[str] = None
    id_registro_praga: Optional[int] = None
