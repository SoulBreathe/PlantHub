import flet as ft


def PragasView(page: ft.Page):
    return ft.Column(
        [
            ft.Icon(ft.Icons.BUG_REPORT_OUTLINED, size=60, color=ft.Colors.GREY_400),
            ft.Text(
                "Catálogo de Pragas em construção...", size=20, color=ft.Colors.GREY_500
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
