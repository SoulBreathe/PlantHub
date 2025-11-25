import flet as ft

# --- LAYOUT & HOME ---
from views.app_layout import AppLayout
from views.home_view import HomeView

# --- LOCAIS ---
from views.locais_view import LocaisView
from views.locais_novo_view import LocaisNovaView

# --- PLANTAS ---
from views.plantas_view import MinhasPlantasView
from views.plantas_novo_view import PlantaNovaView

# --- DIÁRIO ---
from views.diario_view import DiarioView
from views.diario_novo_view import DiarioNovoView

# --- AGENDA ---
from views.agenda_view import AgendaView
from views.agenda_novo_view import AgendaNovoView

# --- ENCICLOPÉDIA ---
from views.enciclopedia_view import EnciclopediaView
from views.enciclopedia_novo_view import EnciclopediaNovoView

# --- DIAGNÓSTICO ---
from views.diagnostico_view import DiagnosticoView
from views.diagnostico_pergunta_view import DiagnosticoPerguntaView
from views.diagnostico_resultado_view import DiagnosticoResultadoView


def criar_appbar(
    page: ft.Page,
    titulo: str,
    icone: str = None,
    cor_icone: str = "#097A12",
    voltar_para: str = None,
    acao=None,
    icone_acao: str = ft.Icons.ADD,
):
    # 1. Botão Voltar (Esquerda)
    leading = None
    if voltar_para:
        leading = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="#333333",
            on_click=lambda _: page.go(voltar_para),
        )

    # 2. Título (Centro)
    content_titulo = ft.Row(
        controls=[],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
    )
    if icone:
        content_titulo.controls.append(ft.Icon(icone, color=cor_icone, size=24))

    content_titulo.controls.append(
        ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color="#333333")
    )

    # 3. Ações (Direita)
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
                margin=ft.margin.only(right=10),
            )
        )

    # 4. Balanceamento
    if leading and not actions:
        actions.append(ft.Container(width=48))

    if not leading and actions:
        leading = ft.Container(width=48)

    return ft.AppBar(
        leading=leading,
        leading_width=48,
        title=content_titulo,
        center_title=True,
        actions=actions,
        bgcolor=ft.Colors.WHITE,
        surface_tint_color=ft.Colors.WHITE,
        shadow_color=ft.Colors.TRANSPARENT,
    )


def main(page: ft.Page):
    page.title = "PlantHub"
    page.theme = ft.Theme(color_scheme_seed="#097A12", use_material3=True)
    page.bgcolor = "#F5F5F5"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        print(f"Rota atual: {page.route}")
        page.views.clear()

        appbar = None
        content = ft.Container()
        alignment = (
            ft.MainAxisAlignment.CENTER
            if page.route.endswith("/novo")
            else ft.MainAxisAlignment.START
        )

        # --- HOME ---
        if page.route == "/":
            content = HomeView(page)
            alignment = ft.MainAxisAlignment.START

        # --- LOCAIS ---
        elif page.route == "/locais":
            content = LocaisView(page)
            # CORREÇÃO AQUI: ft.Icons.PLACE (Maiúsculo)
            appbar = criar_appbar(
                page,
                "Meus Locais",
                ft.Icons.PLACE,
                acao=lambda _: page.go("/locais/novo"),
                voltar_para="/",
            )
        elif page.route == "/locais/novo":
            content = LocaisNovaView(page)
            appbar = criar_appbar(
                page, "Novo Local", ft.Icons.ADD_LOCATION_ALT, voltar_para="/locais"
            )

        # --- PLANTAS ---
        elif page.route == "/plantas":
            content = MinhasPlantasView(page)
            appbar = criar_appbar(
                page,
                "Minhas Plantas",
                ft.Icons.LOCAL_FLORIST,
                acao=lambda _: page.go("/plantas/novo"),
                voltar_para="/",
            )
        elif page.route == "/plantas/novo":
            content = PlantaNovaView(page)
            appbar = criar_appbar(
                page, "Nova Planta", ft.Icons.ADD, voltar_para="/plantas"
            )

        # --- DIÁRIO ---
        elif page.route == "/diario":
            content = DiarioView(page)
            appbar = criar_appbar(
                page,
                "Diário",
                ft.Icons.BOOK,
                acao=lambda _: page.go("/diario/novo"),
                voltar_para="/",
            )
        elif page.route == "/diario/novo":
            content = DiarioNovoView(page)
            appbar = criar_appbar(
                page, "Novo Registro", ft.Icons.EDIT_NOTE, voltar_para="/diario"
            )

        # --- AGENDA ---
        elif page.route == "/agenda":
            content = AgendaView(page)
            appbar = criar_appbar(
                page,
                "Agenda",
                ft.Icons.EVENT,
                acao=lambda _: page.go("/agenda/novo"),
                voltar_para="/",
            )
        elif page.route == "/agenda/novo":
            content = AgendaNovoView(page)
            appbar = criar_appbar(
                page, "Agendar Tarefa", ft.Icons.EVENT_AVAILABLE, voltar_para="/agenda"
            )

        # --- ENCICLOPÉDIA ---
        elif page.route == "/enciclopedia":
            content = EnciclopediaView(page)
            appbar = criar_appbar(
                page,
                "Enciclopédia",
                ft.Icons.MENU_BOOK,
                acao=lambda _: page.go("/enciclopedia/novo"),
                voltar_para="/",
            )
        elif page.route == "/enciclopedia/novo":
            content = EnciclopediaNovoView(page)
            appbar = criar_appbar(
                page,
                "Adicionar à Base",
                ft.Icons.LIBRARY_ADD,
                voltar_para="/enciclopedia",
            )

        # --- DIAGNÓSTICO ---
        elif page.route == "/diagnostico":
            content = DiagnosticoView(page)
            appbar = criar_appbar(
                page, "Diagnóstico", ft.Icons.HEALTH_AND_SAFETY, voltar_para="/"
            )

        elif page.route.startswith("/diagnostico/pergunta/"):
            content = DiagnosticoPerguntaView(page)
            appbar = criar_appbar(
                page, "Assistente", ft.Icons.SUPPORT_AGENT, voltar_para="/diagnostico"
            )

        elif page.route.startswith("/diagnostico/resultado/"):
            content = DiagnosticoResultadoView(page)
            appbar = criar_appbar(
                page, "Resultado", ft.Icons.CHECK_CIRCLE, voltar_para="/diagnostico"
            )

        # --- PLACEHOLDERS PARA EDIÇÃO (Evita erro 404 ao clicar no lápis) ---
        elif "/editar/" in page.route:
            content = ft.Text("Funcionalidade de Edição em breve!", size=20)
            appbar = criar_appbar(page, "Em Construção", voltar_para="/")

        # --- ERRO ---
        else:
            content = ft.Text("Página não encontrada")
            appbar = criar_appbar(page, "Erro 404", voltar_para="/")

        layout = AppLayout(content=content, alignment=alignment)
        view = ft.View(
            route=page.route, controls=[layout], appbar=appbar, bgcolor="#F5F5F5"
        )

        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
