import flet as ft


class AppLayout(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        page: ft.Page = None,  # Mantido para compatibilidade, mas não é usado internamente
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START,
    ):
        """Layout base para padronizar margens e alinhamento vertical."""

        super().__init__(
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            content=ft.Column(
                controls=[content],
                alignment=alignment,  # START (Topo) ou CENTER (Meio)
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )
