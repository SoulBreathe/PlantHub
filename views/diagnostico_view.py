# views/diagnostico_view.py
import flet as ft


def DiagnosticoView(page: ft.Page) -> ft.Column:
    return ft.Column(
        controls=[
            ft.Text(
                "🔍 Assistente de Diagnóstico",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.RED,
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(
                            ft.Icons.HEALTH_AND_SAFETY, size=80, color=ft.Colors.RED
                        ),
                        ft.Text(
                            "Identifique pragas e doenças",
                            size=20,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            "Responda algumas perguntas sobre os sintomas da sua planta.",
                            size=16,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.ElevatedButton(
                            "Iniciar diagnóstico",
                            icon=ft.Icons.PLAY_ARROW,
                            bgcolor=ft.Colors.RED,
                            color=ft.Colors.WHITE,
                            on_click=lambda _: page.go("/diagnostico/pergunta/1"),
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
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
