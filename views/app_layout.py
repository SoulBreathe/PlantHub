import flet as ft


class AppLayout(ft.Container):
    def __init__(
        self, page: ft.Page, content: ft.Control, alignment=ft.MainAxisAlignment.START
    ):
        """
        Layout base para todas as telas.

        :param alignment: Define se o conteúdo fica no TOPO (START) ou no MEIO (CENTER) verticalmente.
        """
        super().__init__(
            content=ft.Column(
                controls=[content],
                # Aqui usamos o parâmetro que recebemos.
                # Se não passarmos nada, ele usa o START (topo).
                alignment=alignment,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        )
