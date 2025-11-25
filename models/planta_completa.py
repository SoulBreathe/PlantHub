from dataclasses import dataclass
from typing import Optional


@dataclass
class PlantaCompleta:
    id_planta: int
    nome_personalizado: str
    nome_popular: str
    nome_local: str
    data_plantio: Optional[str] = None
