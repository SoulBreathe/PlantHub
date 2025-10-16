import flet as ft
from views.home_view import HomeView
from services.database_service import DatabaseService

def main(page: ft.Page):
    page.title = "PlantHub"
    page.window_width = 400
    page.window_height = 800

    # --- Definição dos Temas ---

    # Tema Claro: fundo branco, elementos verdes
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    
    # Tema Escuro: fundo escuro, elementos verdes
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)

    # Inicia o tema claro como padrao 
    page.theme_mode = ft.ThemeMode.LIGHT

    # -- Inicialização de Serviços --
    db_service = DatabaseService

    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    def route_change(route):
        print(f"navegando para a rota: {page.route}")
        page.views.clear()

        if page.route == "/":
            page.views.append(HomeView(page, theme_changed))

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)