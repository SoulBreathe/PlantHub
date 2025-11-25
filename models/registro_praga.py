from dataclasses import dataclass
from typing import Optional


@dataclass
class RegistroPraga:
    id_registro_praga: Optional[int] = None
    data_identificacao: str = ""
    data_resolucao: Optional[str] = None
    status_tratamento: Optional[str] = "em tratamento"
    id_planta: int = 0
    id_praga: int = 0
