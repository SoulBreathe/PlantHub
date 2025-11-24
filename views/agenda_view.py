import flet as ft


def AgendaView(page: ft.Page):
    return ft.Column(
        [
            ft.Icon(ft.Icons.EVENT_BUSY, size=60, color=ft.Colors.GREY_400),
            ft.Text("Agenda em construção...", size=20, color=ft.Colors.GREY_500),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
