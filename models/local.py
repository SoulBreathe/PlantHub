from dataclasses import dataclass
from typing import Optional

@dataclass
class Local:
    nome: str
    id_local: Optional[int] = None