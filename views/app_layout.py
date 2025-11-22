import flet as ft


class AppLayout(ft.Container):
    def __init__(self, page: ft.Page, content: ft.Control):
        super().__init__(
            content=ft.Column(
                controls=[content],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            alignment=ft.alignment.center,
            padding=ft.padding.symmetric(horizontal=10, vertical=5),
        )
