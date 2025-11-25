from dataclasses import dataclass
from typing import Optional


@dataclass
class Praga:
    id_praga: Optional[int] = None
    nome_comum: str = ""
    descricao: Optional[str] = None
    sintomas: Optional[str] = None
    tratamento: Optional[str] = None
    foto_exemplo: Optional[str] = None
