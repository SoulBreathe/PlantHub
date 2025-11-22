from dataclasses import dataclass
from typing import Optional


@dataclass
class Praga:
    nome_comum: str
    descricao: Optional[str] = None
    sintomas: Optional[str] = None
    tratamento: Optional[str] = None
    id_praga: Optional[int] = None
