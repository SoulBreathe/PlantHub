from dataclasses import dataclass
from typing import Optional


@dataclass
class RespostaDiagnostico:
    """Modelo de dados para a tabela DiagnosticoRespostas."""

    id_resposta: Optional[int] = None
    texto_resposta: str = ""
    id_pergunta: int = 0
    id_proxima_pergunta: Optional[int] = None
