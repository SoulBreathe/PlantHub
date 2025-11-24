import flet as ft


def AgendaNovoView(page: ft.Page):
    return ft.Column(
        [ft.Text("Formulário de nova tarefa (Em breve)")],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
