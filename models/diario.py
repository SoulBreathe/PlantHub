from dataclasses import dataclass
from typing import Optional


@dataclass
class EntradaDiario:
    id_diario: Optional[int] = None
    data_registro: str = ""
    titulo: Optional[str] = None
    observacao: str = ""
    caminho_foto: Optional[str] = None
    id_planta: int = 0
