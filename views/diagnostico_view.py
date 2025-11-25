import flet as ft


def DiagnosticoView(page: ft.Page):
    """Tela inicial do fluxo de diagnóstico (Wizard)."""

    return ft.Container(
        padding=30,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.HEALTH_AND_SAFETY, size=100, color="#097A12"),
                ft.Text(
                    "Assistente de Diagnóstico",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#333333",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Responda a perguntas rápidas para identificarmos\no problema da sua planta.",
                    size=16,
                    color="grey",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=30),
                ft.ElevatedButton(
                    text="Iniciar Diagnóstico",
                    icon=ft.Icons.PLAY_ARROW,
                    bgcolor="#097A12",
                    color="white",
                    height=50,
                    width=250,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    on_click=lambda _: page.go("/diagnostico/pergunta/1"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        expand=True,
    )
