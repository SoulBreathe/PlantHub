from dataclasses import dataclass
from typing import Optional


@dataclass
class Local:
    id_local: Optional[int] = None
    nome: str = ""
    descricao: Optional[str] = None
    tipo: Optional[str] = "outro"
    area_m2: float = 0.0
    foto_capa: Optional[str] = None
