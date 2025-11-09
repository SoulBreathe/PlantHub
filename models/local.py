from dataclasses import dataclass
from typing import Optional


@dataclass
class Local:
    nome: str
    descricao: Optional[str] = None
    tipo: Optional[str] = None
    area_m2: float = 0.0
    id_local: Optional[int] = None
