import flet as ft

"""
Conteúdo estático de texto para a aba 'Guia de Cultivo' da Enciclopédia.
"""

GUIA_CULTIVO = {
    "Iluminação": {
        "icone": ft.Icons.WB_SUNNY,
        "cor": "orange",
        "texto": """
• Sol Pleno:
A planta precisa receber luz direta do sol em suas folhas por pelo menos 6 horas diárias. Ideal para hortaliças (tomate, pimentão) e cactos.

• Sombra Parcial (Meia-sombra):
Gosta de sol fraco (manhã até as 10h ou fim de tarde após 16h). O sol forte do meio-dia queima as folhas. Ideal para Hortelã e Manjericão.

• Sombra:
Apenas luz indireta ou claridade difusa. Nunca sol direto. Ideal para plantas de interior como Jibóia e Lírio da Paz.
""",
    },
    "Rega": {
        "icone": ft.Icons.WATER_DROP,
        "cor": "blue",
        "texto": """
• Teste do Dedo (Regra de Ouro):
Antes de regar, coloque o dedo na terra. Se sair sujo (úmido), não regue! Se sair limpo (seco), regue.

• Diária:
Plantas que amam umidade. A terra nunca deve secar totalmente. (Ex: Hortelã).

• Moderada:
Espere a superfície da terra secar antes de regar novamente. É o padrão para a maioria das plantas.

• Pouca:
Deixe a terra secar completamente (até ao fundo do vaso) antes de regar. (Ex: Suculentas e Cactos).
""",
    },
    "Adubação": {
        "icone": ft.Icons.SCIENCE,
        "cor": "green",
        "texto": """
• NPK 10-10-10 (Manutenção):
Equilibrado. Bom para folhagens verdes e crescimento geral. Use se não souber qual escolher.

• NPK 4-14-8 (Floração/Frutos):
O número do meio (Fósforo) é alto. Ideal para fazer a planta dar flores e frutos (Tomate, Pimentas, Flores).

• Orgânico (Húmus/Esterco):
Libera nutrientes lentamente e melhora a qualidade da terra. É mais seguro e difícil de "queimar" a planta por excesso.
""",
    },
    "Poda": {
        "icone": ft.Icons.CONTENT_CUT,
        "cor": "brown",
        "texto": """
• Poda de Limpeza:
Retire sempre folhas amarelas, secas ou doentes. A planta gasta energia tentando "salvar" essas folhas.

• Poda de Contenção:
Corte as pontas dos galhos mais altos para a planta não ficar muito comprida e desengonçada. Isso estimula ela a ficar mais "cheia".

• Poda de Beliscão:
Em ervas como Manjericão, corte as flores assim que nascerem. Se deixar florir, a planta para de produzir folhas saborosas.
""",
    },
}
