import flet as ft
from typing import Optional


class AppLayout(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        page: Optional[ft.Page] = None,
        alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START,
    ):
        """
        Layout wrapper para padronizar margens e alinhamento nas páginas.
        """
        super().__init__(
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
            content=ft.Column(
                controls=[content],
                alignment=alignment,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        )
