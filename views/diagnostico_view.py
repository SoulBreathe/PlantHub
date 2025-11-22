import flet as ft


def DiagnosticoView(page: ft.Page):
    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.HEALTH_AND_SAFETY, size=80, color="#097A12"),
                        ft.Text(
                            "Assistente de Diagnóstico",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                        ft.Text(
                            "Identifique pragas e doenças com base em sintomas.",
                            size=16,
                            color=ft.Colors.GREY_700,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                expand=True,
                alignment=ft.alignment.center,
            ),
        ],
        expand=True,
    )
