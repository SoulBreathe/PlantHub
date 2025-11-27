from dataclasses import dataclass
from typing import Optional


@dataclass
class PlantaCompleta:
    """Modelo de visualização (JOIN) para exibir plantas com nomes de espécie e local."""

    id_planta: int
    nome_personalizado: str
    nome_popular: str
    nome_local: str
    data_plantio: Optional[str] = None
