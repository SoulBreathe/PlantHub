from dataclasses import dataclass
from typing import Optional


@dataclass
class EntradaDiario:
    data_registro: str
    observacao: str
    caminho_foto: Optional[str] = None
    id_planta: int = 0
    id_diario: Optional[int] = None
