from dataclasses import dataclass
from typing import Optional


@dataclass
class PerguntaDiagnostico:
    """Modelo de dados para a tabela DiagnosticoPerguntas."""

    id_pergunta: Optional[int] = None
    texto_pergunta: str = ""
    ordem: int = 0
