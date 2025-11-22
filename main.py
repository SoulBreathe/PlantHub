# main.py
import flet as ft
from views.home_view import HomeView
from views.app_layout import AppLayout
from views.locais_view import LocaisView
from views.locaisNovo_view import LocaisNovaView
from views.minhasPlantas_view import MinhasPlantasView
from views.plantaNova_view import PlantaNovaView
from views.diagnostico_view import DiagnosticoView


def criar_appbar(
    page: ft.Page,
    titulo: str,
    icone: str = None,
    cor_icone: str = "#097A12",
    voltar_para: str = "/",
    acao=None,
    icone_acao: str = ft.Icons.CHECK,
):
    leading = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=lambda _: page.go(voltar_para),
    )

    title_content = ft.Row(
        controls=[],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
    )
    if icone:
        title_content.controls.append(ft.Icon(icone, color=cor_icone, size=22))
    title_content.controls.append(ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD))

    title = ft.Container(
        content=title_content,
        alignment=ft.alignment.center,
        expand=True,
    )

    actions = []
    if acao:
        actions.append(
            ft.Container(
                content=ft.IconButton(
                    icon=icone_acao,
                    icon_color=ft.Colors.WHITE,
                    bgcolor="#097A12",
                    on_click=acao,
                ),
                margin=ft.margin.only(right=16),
            )
        )

    return ft.AppBar(
        leading=leading,
        title=title,
        actions=actions,
        bgcolor=ft.Colors.WHITE,
        shadow_color=ft.Colors.TRANSPARENT,
    )


def main(page: ft.Page):
    # Tema único: claro + verde
    page.theme = ft.Theme(
        color_scheme_seed="#097A12",
        use_material3=True,
    )
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        print(f"navegando para a rota: {page.route}")
        page.views.clear()

        if page.route == "/":
            content = HomeView(page)
            appbar = None
        elif page.route == "/locais":
            content = LocaisView(page)
            appbar = criar_appbar(
                page,
                titulo="",
                icone=ft.Icons.LOCATION_ON,
                acao=lambda _: page.go("/locais/novo"),
                icone_acao=ft.Icons.ADD,
            )
        elif page.route == "/locais/novo":
            content = LocaisNovaView(page)
            appbar = criar_appbar(
                page,
                titulo="",
                icone=ft.Icons.ADD_LOCATION,
                voltar_para="/locais",
            )
        elif page.route == "/plantas":
            content = MinhasPlantasView(page)
            appbar = criar_appbar(
                page,
                titulo="Minhas Plantas",
                icone=ft.Icons.LOCAL_FLORIST,
                acao=lambda _: page.go("/plantas/novo"),
                icone_acao=ft.Icons.ADD,
            )
        elif page.route == "/plantas/novo":
            content = PlantaNovaView(page)
            appbar = criar_appbar(page, titulo="", voltar_para="/plantas")

        elif page.route == "/diagnostico":
            content = DiagnosticoView(page)
            appbar = criar_appbar(
                page,
                titulo="Diagnóstico",
                icone=ft.Icons.HEALTH_AND_SAFETY,
                acao=lambda _: page.go("/diagnostico/pergunta/1"),
                icone_acao=ft.Icons.PLAY_ARROW,
            )
        elif page.route == "/agenda":
            content = ft.Text("Em breve...", size=20)
            appbar = criar_appbar(
                page,
                titulo="Agenda",
                icone=ft.Icons.EVENT,
                acao=lambda _: page.go("/agenda/novo"),
                icone_acao=ft.Icons.ADD,
            )
        elif page.route == "/diario":
            content = ft.Text("Em breve...", size=20)
            appbar = criar_appbar(
                page,
                titulo="Diário",
                icone=ft.Icons.BOOK,
                acao=lambda _: page.go("/diario/novo"),
                icone_acao=ft.Icons.ADD,
            )
        elif page.route == "/pragas":
            content = ft.Text("Em breve...", size=20)
            appbar = criar_appbar(
                page,
                titulo="Pragas",
                icone=ft.Icons.BUG_REPORT,
                acao=lambda _: page.go("/pragas/novo"),
                icone_acao=ft.Icons.ADD,
            )
        else:
            content = ft.Text(f"Rota não encontrada: {page.route}", size=20)
            appbar = criar_appbar(page, titulo="Erro", voltar_para="/")

        layout = AppLayout(page=page, content=content)

        view = ft.View(
            route=page.route,
            controls=[layout],
            appbar=appbar,
        )

        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
