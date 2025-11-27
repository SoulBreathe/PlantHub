import flet as ft
from services.database_service import DatabaseService


def DiarioView(page: ft.Page):
    db = DatabaseService()

    # --- EVENTOS AUXILIARES ---
    def abrir_foto(caminho_bruto):
        if not caminho_bruto:
            return
        caminho_corrigido = caminho_bruto.replace("\\", "/")

        img = ft.Image(
            src=caminho_corrigido,
            width=600,
            height=400,
            fit=ft.ImageFit.CONTAIN,
            error_content=ft.Column(
                [
                    ft.Icon(ft.Icons.BROKEN_IMAGE, color="grey"),
                    ft.Text("Erro ao carregar imagem", color="grey"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

        dlg = ft.AlertDialog(
            title=ft.Text("Registro Fotográfico"),
            content=ft.Container(content=img, alignment=ft.alignment.center),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.close(dlg))],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg)

    # --- BUILDER DO CARD ---
    def criar_card_diario(entrada):
        dia = entrada.data_registro[8:10]
        mes = entrada.data_registro[5:7]
        tem_foto = bool(entrada.caminho_foto)

        botao_foto = ft.Icon(ft.Icons.NO_PHOTOGRAPHY, color=ft.Colors.GREY_300, size=20)
        if tem_foto:
            botao_foto = ft.IconButton(
                icon=ft.Icons.PHOTO_CAMERA,
                icon_color="white",
                bgcolor="#097A12",
                icon_size=20,
                tooltip="Ver foto",
                on_click=lambda _: abrir_foto(entrada.caminho_foto),
            )

        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=12,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            border=ft.border.all(1, "#f0f0f0"),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                dia, size=20, weight=ft.FontWeight.BOLD, color="#097A12"
                            ),
                            ft.Text(f"Mês {mes}", size=12, color="grey"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    ft.VerticalDivider(width=15, color="#eeeeee"),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        entrada.titulo or "Sem título",
                                        weight=ft.FontWeight.BOLD,
                                        size=15,
                                        color="#333333",
                                    ),
                                    botao_foto,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text(
                                entrada.observacao,
                                max_lines=3,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                size=13,
                                color="#555555",
                            ),
                        ],
                        expand=True,
                    ),
                ]
            ),
        )

    # --- LÓGICA DE AGRUPAMENTO ---
    plantas = db.get_all_plantas()
    grupos_de_diario = []

    for planta in plantas:
        entradas = db.get_diario_por_planta(planta.id_planta)

        if entradas:
            grupo = ft.Container(
                bgcolor="white",
                border_radius=10,
                margin=ft.margin.only(bottom=10),
                shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
                content=ft.ExpansionTile(
                    leading=ft.Icon(ft.Icons.LOCAL_FLORIST, color="#097A12"),
                    title=ft.Text(
                        planta.nome_personalizado, weight=ft.FontWeight.BOLD, size=16
                    ),
                    subtitle=ft.Text(
                        f"{len(entradas)} registros", size=12, color="grey"
                    ),
                    initially_expanded=False,
                    controls_padding=ft.padding.only(
                        left=20, right=10, top=10, bottom=10
                    ),
                    controls=[
                        ft.Column(
                            controls=[criar_card_diario(e) for e in entradas], spacing=0
                        )
                    ],
                ),
            )
            grupos_de_diario.append(grupo)

    # --- ESTADO VAZIO ---
    if not grupos_de_diario:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.BOOK_OUTLINED, size=64, color="grey"),
                ft.Text(
                    "Seu diário está vazio.",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#333333",
                ),
                ft.Text(
                    "Comece a registrar a história das suas plantas!",
                    size=14,
                    color="grey",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    return ft.ListView(controls=grupos_de_diario, padding=15, expand=True)
