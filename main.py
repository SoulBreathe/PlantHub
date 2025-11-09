# main.py
import flet as ft
from views.home_view import HomeView
from views.app_layout import AppLayout
from views.locais_view import LocaisView
from views.diagnostico_view import DiagnosticoView
from services.database_service import DatabaseService


def main(page: ft.Page):

    # Temas
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.dark_theme = ft.Theme(color_scheme_seed="#097A12")
    page.theme_mode = ft.ThemeMode.LIGHT

    def update_background():
        if page.theme_mode == ft.ThemeMode.DARK:
            page.bgcolor = "#097A12"
        else:
            page.bgcolor = None
        page.update()

    update_background()

    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        update_background()

    def route_change(route):
        print(f"navegando para a rota: {page.route}")
        page.views.clear()

        if page.route == "/":
            content = HomeView(page)
        elif page.route == "/locais":
            content = LocaisView(page)
        elif page.route == "/diagnostico":
            content = DiagnosticoView(page)
        else:
            content = ft.Text(f"Rota não encontrada: {page.route}", size=20)

        layout = AppLayout(page=page, theme_changed=theme_changed, content=content)

        view = ft.View(
            route=page.route,
            controls=[layout],
            appbar=ft.AppBar(
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.BRIGHTNESS_4_OUTLINED,
                        tooltip="Mudar tema",
                        on_click=theme_changed,
                    )
                ],
            ),
        )

        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
