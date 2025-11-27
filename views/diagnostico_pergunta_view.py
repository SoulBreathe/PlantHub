import flet as ft
from services.database_service import DatabaseService


def DiagnosticoPerguntaView(page: ft.Page):
    db = DatabaseService()

    try:
        ordem_atual = int(page.route.split("/")[-1])
    except (ValueError, IndexError):
        ordem_atual = 1

    pergunta = db.get_pergunta_por_ordem(ordem_atual)

    # --- Estado de Erro (Sem Pergunta) ---
    if not pergunta:
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.SEARCH_OFF, size=64, color="grey"),
                    ft.Text(
                        "Não foi possível determinar o problema.",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#333",
                    ),
                    ft.ElevatedButton(
                        "Voltar ao Início", on_click=lambda _: page.go("/diagnostico")
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    respostas = db.get_respostas_por_pergunta(pergunta.id_pergunta)

    # --- Lógica de Navegação ---
    def processar_resposta(id_resposta, id_proxima):
        praga_detectada = db.verificar_diagnostico(id_resposta)

        if praga_detectada:
            page.go(f"/diagnostico/resultado/{praga_detectada.id_praga}")
        else:
            proxima = id_proxima if id_proxima else (ordem_atual + 1)
            page.go(f"/diagnostico/pergunta/{proxima}")

    # --- Elementos da UI ---
    barra_progresso = ft.ProgressBar(
        value=ordem_atual * 0.25, color="#097A12", bgcolor=ft.Colors.GREY_200, height=8
    )

    titulo = ft.Text(
        f"PERGUNTA {ordem_atual}", color="#097A12", weight=ft.FontWeight.BOLD, size=14
    )

    texto_perg = ft.Text(
        pergunta.texto_pergunta,
        size=24,
        text_align=ft.TextAlign.CENTER,
        weight=ft.FontWeight.BOLD,
        color="#333333",
    )

    lista_botoes = []
    for resp in respostas:
        btn = ft.Container(
            content=ft.Row(
                [
                    ft.Text(
                        resp.texto_resposta,
                        size=16,
                        color="#333333",
                        weight=ft.FontWeight.W_500,
                        expand=True,
                    ),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#097A12"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
            width=350,
            bgcolor="white",
            border=ft.border.all(1, "#E0E0E0"),
            border_radius=12,
            shadow=ft.BoxShadow(
                blur_radius=5, color=ft.Colors.with_opacity(0.05, "black")
            ),
            on_click=lambda e, r_id=resp.id_resposta, p_id=resp.id_proxima_pergunta: processar_resposta(
                r_id, p_id
            ),
            ink=True,
            animate=ft.Animation(200, "easeOut"),
        )
        lista_botoes.append(btn)

    # --- Layout Final ---
    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                barra_progresso,
                ft.Container(height=20),
                titulo,
                ft.Container(height=10),
                texto_perg,
                ft.Container(height=40),
                ft.Column(lista_botoes, spacing=15),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )
