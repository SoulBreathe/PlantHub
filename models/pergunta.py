from dataclasses import dataclass
from typing import Optional


@dataclass
class PerguntaDiagnostico:
    id_pergunta: Optional[int] = None
    texto_pergunta: str = ""
    ordem: int = 0
