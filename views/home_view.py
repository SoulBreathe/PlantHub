# views/home_view.py
import flet as ft


def HomeView(page: ft.Page) -> ft.Column:
    def ir_para_rota(rota: str):
        return lambda _: page.go(rota)

    def criar_card(icono, label, cor_fundo, rota):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Icon(icono, size=40, color=ft.Colors.WHITE),
                        alignment=ft.alignment.center,
                    ),
                    ft.Text(
                        label,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.WHITE,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            width=150,
            height=150,
            bgcolor=cor_fundo,
            border_radius=ft.border_radius.all(15),
            padding=ft.padding.all(10),
            on_click=ir_para_rota(rota),
            ink=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                offset=ft.Offset(0, 3),
            ),
        )

    # Cards
    card_locais = criar_card(
        icono=ft.Icons.LOCATION_ON,
        label="Locais",
        cor_fundo=ft.Colors.GREEN,
        rota="/locais",
    )
    card_plantas = criar_card(
        icono=ft.Icons.LOCAL_FLORIST,
        label="Minhas Plantas",
        cor_fundo=ft.Colors.ORANGE,
        rota="/plantas",
    )
    card_diario = criar_card(
        icono=ft.Icons.BOOK,
        label="Diário",
        cor_fundo=ft.Colors.BLUE,
        rota="/diario",
    )
    card_agenda = criar_card(
        icono=ft.Icons.EVENT,
        label="Agenda",
        cor_fundo=ft.Colors.PURPLE,
        rota="/agenda",
    )
    card_diagnostico = criar_card(
        icono=ft.Icons.HEALTH_AND_SAFETY,
        label="Diagnóstico",
        cor_fundo=ft.Colors.RED,
        rota="/diagnostico",
    )
    card_pragas = criar_card(
        icono=ft.Icons.BUG_REPORT,
        label="Pragas",
        cor_fundo=ft.Colors.DEEP_ORANGE,
        rota="/pragas",
    )

    grid = ft.Row(
        controls=[
            ft.Column(
                controls=[card_locais, card_diario, card_diagnostico],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Column(
                controls=[card_plantas, card_agenda, card_pragas],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40,  # espaçamento entre as colunas
    )

    return ft.Column(
        controls=[
            ft.Text("PlantHub", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            grid,
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
