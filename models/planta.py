from dataclasses import dataclass
from typing import Optional


@dataclass
class Planta:
    id_planta: Optional[int] = None
    nome_personalizado: str = ""
    data_plantio: Optional[str] = None
    id_especie: int = 0
    id_local: int = 0
    status: str = "ativa"
    foto_principal: Optional[str] = None
