import flet as ft


def DiagnosticoView(page: ft.Page):
    """Tela inicial do fluxo de diagnóstico (Wizard)."""

    return ft.Container(
        padding=30,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                ft.Container(
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, "#097A12"),
                    border_radius=50,
                    content=ft.Icon(
                        ft.Icons.HEALTH_AND_SAFETY, size=80, color="#097A12"
                    ),
                ),
                ft.Container(height=10),
                ft.Text(
                    "Dr. PlantHub",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color="#333333",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Responda a algumas perguntas rápidas sobre\nos sintomas visuais da sua planta para\nidentificarmos o problema.",
                    size=16,
                    color="grey",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=40),
                ft.ElevatedButton(
                    content=ft.Row(
                        [
                            ft.Text("Iniciar Diagnóstico", size=18),
                            ft.Icon(ft.Icons.ARROW_FORWARD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    bgcolor="#097A12",
                    color="white",
                    height=60,
                    width=300,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
                    on_click=lambda _: page.go("/diagnostico/pergunta/1"),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
        ),
        expand=True,
    )
