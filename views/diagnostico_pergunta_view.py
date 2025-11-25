import flet as ft
from services.database_service import DatabaseService


def DiagnosticoPerguntaView(page: ft.Page):
    db = DatabaseService()

    # Extrai a ordem da URL (ex: /diagnostico/pergunta/1)
    try:
        ordem_atual = int(page.route.split("/")[-1])
    except (ValueError, IndexError):
        ordem_atual = 1

    pergunta = db.get_pergunta_por_ordem(ordem_atual)

    # Caso de erro ou fim inesperado
    if not pergunta:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.SEARCH_OFF, size=64, color="grey"),
                ft.Text("Pergunta não encontrada.", size=18, color="#333333"),
                ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/diagnostico")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    # Busca respostas vinculadas a esta pergunta
    # Nota: Certifique-se que o método no DatabaseService é 'get_respostas_por_pergunta'
    respostas = db.get_respostas_por_pergunta(pergunta.id_pergunta)

    def processar_resposta(e, id_resposta):
        # 1. Verifica se essa resposta leva a um diagnóstico (Praga)
        praga = db.verificar_diagnostico(id_resposta)

        if praga:
            page.go(f"/diagnostico/resultado/{praga.id_praga}")
            return

        # 2. Se não for diagnóstico, tenta ir para a próxima pergunta
        # Nota: Aqui segue a lógica linear (ordem + 1).
        # Futuramente pode-se usar o campo 'id_proxima_pergunta' da tabela de Respostas.
        proxima_ordem = ordem_atual + 1

        if db.get_pergunta_por_ordem(proxima_ordem):
            page.go(f"/diagnostico/pergunta/{proxima_ordem}")
        else:
            page.open(
                ft.SnackBar(
                    ft.Text("Fim do questionário. Nenhum diagnóstico conclusivo.")
                )
            )

    # --- Elementos Visuais ---

    titulo_ordem = ft.Text(
        f"PERGUNTA {ordem_atual}", color="#097A12", weight=ft.FontWeight.BOLD, size=14
    )

    texto_pergunta = ft.Text(
        pergunta.texto_pergunta,
        size=22,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.W_600,
        color="#333333",
    )

    lista_botoes = []
    for resp in respostas:
        btn = ft.Container(
            content=ft.Text(resp.texto_resposta, size=16, color="#333333"),
            padding=20,
            width=320,
            bgcolor="white",
            border=ft.border.all(1, "#097A12"),
            border_radius=12,
            alignment=ft.alignment.center,
            ink=True,  # Efeito visual de clique
            on_click=lambda e, id=resp.id_resposta: processar_resposta(e, id),
        )
        lista_botoes.append(btn)

    return ft.Column(
        controls=[
            ft.Container(height=20),
            titulo_ordem,
            ft.Container(height=10),
            texto_pergunta,
            ft.Container(height=40),
            ft.Column(controls=lista_botoes, spacing=15),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
