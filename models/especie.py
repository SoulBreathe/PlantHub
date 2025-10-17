from dataclasses import dataclass
from typing import Optional

@dataclass
class Especie:
    nome_popular: str
    nome_cientifico: Optional[str]
    instrucoes_rega: Optional[str]
    necessidade_sol: Optional[str]
    necessidade_poda: Optional[str]
    uso_adubos: Optional[str]
    epoca_plantio: Optional[str]
    id_especie: Optional[int] = None
    
