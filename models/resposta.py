from dataclasses import dataclass
from typing import Optional


@dataclass
class RespostaDiagnostico:
    texto_resposta: str
    id_pergunta: int = 0
    id_resposta: Optional[int] = None
