import flet as ft

# --- IMPORTS DAS VIEWS ---
from views.home_view import HomeView
from views.app_layout import AppLayout

# Locais
from views.locais_view import LocaisView
from views.locais_novo_view import LocaisNovaView

# Plantas
from views.plantas_view import MinhasPlantasView
from views.plantas_novo_view import PlantaNovaView

# Diário
from views.diario_view import DiarioView
from views.diario_novo_view import DiarioNovoView

# Diagnóstico
from views.diagnostico_view import DiagnosticoView

# Agenda (Placeholders)
from views.agenda_view import AgendaView
from views.agenda_novo_view import AgendaNovoView

# Pragas (Placeholders)
from views.pragas_view import PragasView
from views.pragas_novo_view import PragasNovoView


def criar_appbar(
    page: ft.Page,
    titulo: str,
    icone: str = None,
    cor_icone: str = "#097A12",
    voltar_para: str = None,  # Se for None, não tem botão. Se for string, tem botão.
    acao=None,
    icone_acao: str = ft.Icons.CHECK,
):
    """
    Cria uma AppBar com título matematicamente centralizado e gestão inteligente de botões.
    """

    # 1. Configurar Botão de Voltar (Leading)
    if voltar_para is not None:
        leading = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color="#333333",
            on_click=lambda _: page.go(voltar_para),
        )
    else:
        leading = None

    # 2. Configurar Título (Centro)
    title_content = ft.Row(
        controls=[],
        spacing=8,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    if icone:
        title_content.controls.append(ft.Icon(icone, color=cor_icone, size=24))

    title_content.controls.append(
        ft.Text(titulo, size=20, weight=ft.FontWeight.BOLD, color="#333333")
    )
    title = ft.Container(content=title_content)

    # 3. Configurar Ações (Direita)
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

    # 4. LÓGICA DE BALANCEAMENTO (FANTASMAS)
    # Isso garante que o título fique EXATAMENTE no meio, mesmo se só tiver botão de um lado.

    # Cenário A: Tem botão na esquerda, mas NÃO tem ação na direita.
    # Solução: Adiciona espaço vazio na direita.
    if leading and not acao:
        actions.append(ft.Container(width=48))  # 48px é a largura padrão do IconButton

    # Cenário B: NÃO tem botão na esquerda, mas tem ação na direita.
    # Solução: Adiciona espaço vazio na esquerda (atribuindo ao leading).
    if not leading and acao:
        leading = ft.Container(width=48)

    return ft.AppBar(
        leading=leading,
        leading_width=48,  # Força a largura
        title=title,
        center_title=True,
        actions=actions,
        bgcolor=ft.Colors.WHITE,
        surface_tint_color=ft.Colors.WHITE,
        shadow_color=ft.Colors.TRANSPARENT,
    )


def main(page: ft.Page):
    # Configuração Geral do Tema
    page.title = "PlantHub"
    page.theme = ft.Theme(
        color_scheme_seed="#097A12",
        use_material3=True,
    )
    page.bgcolor = "#F5F5F5"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        print(f"Navegando para: {page.route}")
        page.views.clear()

        # Variáveis padrão
        appbar = None
        content = ft.Container()

        # --- HOME ---
        if page.route == "/":
            content = HomeView(page)

        # --- LOCAIS ---
        elif page.route == "/locais":
            content = LocaisView(page)
            appbar = criar_appbar(
                page,
                titulo="Biblioteca Locais",
                icone=ft.Icons.LIBRARY_BOOKS_OUTLINED,
                acao=lambda _: page.go("/locais/novo"),
                icone_acao=ft.Icons.ADD,
                voltar_para="/",
            )
        elif page.route == "/locais/novo":
            content = LocaisNovaView(page)
            appbar = criar_appbar(
                page,
                titulo="Novo Local",
                icone=ft.Icons.ADD_LOCATION_ALT_OUTLINED,
                voltar_para="/locais",
            )

        # --- PLANTAS ---
        elif page.route == "/plantas":
            content = MinhasPlantasView(page)
            appbar = criar_appbar(
                page,
                titulo="Minhas Plantas",
                icone=ft.Icons.PHOTO_LIBRARY_OUTLINED,
                acao=lambda _: page.go("/plantas/novo"),
                icone_acao=ft.Icons.ADD,
                voltar_para="/",
            )
        elif page.route == "/plantas/novo":
            content = PlantaNovaView(page)
            appbar = criar_appbar(
                page,
                titulo="Nova Planta",
                icone=ft.Icons.LOCAL_FLORIST_OUTLINED,
                voltar_para="/plantas",
            )

        # --- DIÁRIO ---
        elif page.route == "/diario":
            content = DiarioView(page)
            appbar = criar_appbar(
                page,
                titulo="Diário",
                icone=ft.Icons.BOOK,
                acao=lambda _: page.go("/diario/novo"),
                icone_acao=ft.Icons.ADD,
                voltar_para="/",
            )
        elif page.route == "/diario/novo":
            content = DiarioNovoView(page)
            appbar = criar_appbar(
                page,
                titulo="Nova Entrada",
                icone=ft.Icons.EDIT_NOTE,
                voltar_para="/diario",
            )

        # --- DIAGNÓSTICO ---
        elif page.route == "/diagnostico":
            content = DiagnosticoView(page)
            appbar = criar_appbar(
                page,
                titulo="Diagnóstico",
                icone=ft.Icons.HEALTH_AND_SAFETY,
                acao=lambda _: page.go("/diagnostico/pergunta/1"),
                icone_acao=ft.Icons.PLAY_ARROW,
                voltar_para="/",
            )

        # --- AGENDA ---
        elif page.route == "/agenda":
            content = AgendaView(page)
            appbar = criar_appbar(
                page,
                titulo="Agenda",
                icone=ft.Icons.EVENT,
                acao=lambda _: page.go("/agenda/novo"),
                icone_acao=ft.Icons.ADD,
                voltar_para="/",
            )
        elif page.route == "/agenda/novo":
            content = AgendaNovoView(page)
            appbar = criar_appbar(
                page,
                titulo="Nova Tarefa",
                icone=ft.Icons.EVENT_AVAILABLE,
                voltar_para="/agenda",
            )

        # --- PRAGAS ---
        elif page.route == "/pragas":
            content = PragasView(page)
            appbar = criar_appbar(
                page,
                titulo="Pragas",
                icone=ft.Icons.BUG_REPORT,
                acao=lambda _: page.go("/pragas/novo"),
                icone_acao=ft.Icons.ADD,
                voltar_para="/",
            )
        elif page.route == "/pragas/novo":
            content = PragasNovoView(page)
            appbar = criar_appbar(
                page,
                titulo="Nova Praga",
                icone=ft.Icons.BUG_REPORT,
                voltar_para="/pragas",
            )

        # Rota não encontrada
        else:
            content = ft.Text(f"Rota não encontrada: {page.route}", size=20)
            appbar = criar_appbar(page, "Erro", voltar_para="/")

        # --- LÓGICA DE ALINHAMENTO DO LAYOUT ---
        # Se for tela de cadastro (/novo), centraliza o card verticalmente.
        # Se for lista, alinha ao topo.
        if page.route.endswith("/novo"):
            alinhamento_vertical = ft.MainAxisAlignment.CENTER
        else:
            alinhamento_vertical = ft.MainAxisAlignment.START

        layout = AppLayout(page=page, content=content, alignment=alinhamento_vertical)

        view = ft.View(
            route=page.route, controls=[layout], appbar=appbar, bgcolor="#F5F5F5"
        )

        page.views.append(view)
        page.update()

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)
