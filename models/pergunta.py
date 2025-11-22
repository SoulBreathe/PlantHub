from dataclasses import dataclass
from typing import Optional


@dataclass
class PerguntaDiagnostico:
    texto_pergunta: str
    ordem: int = 0
    id_pergunta: Optional[int] = None
