from dataclasses import dataclass
from typing import Optional


@dataclass
class Especie:
    id_especie: Optional[int] = None
    nome_popular: str = ""
    nome_cientifico: Optional[str] = None
    instrucoes_rega: Optional[str] = None
    necessidade_sol: Optional[str] = None
    necessidade_poda: Optional[str] = None
    uso_adubos: Optional[str] = None
    epoca_plantio: Optional[str] = None
    foto_exemplo: Optional[str] = None
