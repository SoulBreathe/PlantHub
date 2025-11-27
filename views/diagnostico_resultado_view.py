import flet as ft
from services.database_service import DatabaseService


def DiagnosticoResultadoView(page: ft.Page):
    db = DatabaseService()
    praga = None

    # Tenta pegar o ID da URL e buscar a praga
    try:
        id_praga = int(page.route.split("/")[-1])
        todas = db.get_all_pragas()
        praga = next((p for p in todas if p.id_praga == id_praga), None)
    except:
        pass

    # Se não encontrar, mostra erro
    if not praga:
        return ft.Column(
            [ft.Text("Erro ao carregar resultado.")],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # --- 1. PREPARAÇÃO DA IMAGEM ---
    if praga.foto_exemplo:
        src = praga.foto_exemplo.replace("\\", "/")
        img_content = ft.Image(
            src=src,
            fit=ft.ImageFit.COVER,
            width=float("inf"),
            height=250,  # Altura da imagem
        )
    else:
        img_content = ft.Container(
            height=250,
            width=float("inf"),
            bgcolor=ft.Colors.with_opacity(0.1, "red"),
            alignment=ft.alignment.center,
            content=ft.Icon(ft.Icons.BUG_REPORT, size=80, color="red"),
        )

    # --- 2. CARD PRINCIPAL (Resultado) ---
    card_principal = ft.Container(
        bgcolor="white",
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
        width=450,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=ft.Column(
            spacing=0,
            controls=[
                # Cabeçalho Verde
                ft.Container(
                    bgcolor="#E8F5E9",
                    padding=15,
                    width=float("inf"),
                    alignment=ft.alignment.center,
                    content=ft.Text(
                        "Diagnóstico Concluído!",
                        color="#097A12",
                        weight=ft.FontWeight.BOLD,
                        size=18,
                    ),
                ),
                # Imagem Grande
                img_content,
                # Texto (Nome e Sintomas)
                ft.Container(
                    padding=ft.padding.all(20),
                    content=ft.Column(
                        [
                            ft.Text(
                                praga.nome_comum,
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color="#333",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                praga.sintomas or "Sintomas não descritos.",
                                text_align=ft.TextAlign.CENTER,
                                color="grey",
                                size=15,
                                italic=True,
                            ),
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
            ],
        ),
    )

    # --- 3. CARD TRATAMENTO (Recomendação) ---
    texto_tratamento = praga.tratamento
    if not texto_tratamento or texto_tratamento.strip() == "":
        texto_tratamento = "Nenhum tratamento específico cadastrado."

    card_tratamento = ft.Container(
        padding=25,
        bgcolor="white",
        border_radius=15,
        border=ft.border.all(1, "#e0e0e0"),
        width=450,
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.HEALING, color="#097A12", size=24),
                        ft.Text(
                            "Tratamento Recomendado",
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            color="#097A12",
                        ),
                    ]
                ),
                ft.Divider(height=20, color="#eeeeee"),
                ft.Text(
                    texto_tratamento,
                    size=16,
                    color="black",
                    weight=ft.FontWeight.NORMAL,
                    text_align=ft.TextAlign.LEFT,
                    selectable=True,
                ),
            ],
            spacing=5,
        ),
    )

    # --- LAYOUT FINAL ---
    return ft.Container(
        padding=ft.padding.symmetric(vertical=20, horizontal=10),
        bgcolor="#F5F5F5",
        alignment=ft.alignment.top_center,
        content=ft.Column(
            controls=[
                card_principal,
                ft.Container(height=15),
                card_tratamento,
                ft.Container(height=30),
                ft.ElevatedButton(
                    "Concluir",
                    icon=ft.Icons.CHECK,
                    bgcolor="#097A12",
                    color="white",
                    width=200,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=25)),
                    on_click=lambda _: page.go("/diagnostico"),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
        ),
        expand=True,
    )
