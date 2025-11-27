import flet as ft
from services.database_service import DatabaseService


def HomeView(page: ft.Page):
    db = DatabaseService()
    stats = db.get_resumo_dashboard()

    def criar_card_menu(icone, titulo, info_extra, cor, rota):
        return ft.Container(
            width=155,
            height=160,
            bgcolor=cor,
            border_radius=20,
            padding=15,
            ink=True,
            on_click=lambda _: page.go(rota),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.2, "black"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                controls=[
                    ft.Container(
                        padding=8,
                        bgcolor=ft.Colors.with_opacity(0.2, "white"),
                        border_radius=50,
                        content=ft.Icon(icone, size=28, color="white"),
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                titulo,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color="white",
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                info_extra,
                                size=12,
                                color=ft.Colors.WHITE70,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
        )

    # --- Configuração do Menu ---
    itens_col1 = [
        {
            "icon": ft.Icons.LOCATION_ON,
            "label": "Locais",
            "info": f"{stats['locais']} ambientes",
            "color": "#558B2F",
            "route": "/locais",
        },
        {
            "icon": ft.Icons.BOOK,
            "label": "Diário",
            "info": f"{stats['diario']} registros",
            "color": "#8D6E63",
            "route": "/diario",
        },
        {
            "icon": ft.Icons.HEALTH_AND_SAFETY,
            "label": "Diagnóstico",
            "info": "Identificar",
            "color": "#BF360C",
            "route": "/diagnostico",
        },
    ]

    itens_col2 = [
        {
            "icon": ft.Icons.LOCAL_FLORIST,
            "label": "Minhas Plantas",
            "info": f"{stats['plantas']} ativas",
            "color": "#2E7D32",
            "route": "/plantas",
        },
        {
            "icon": ft.Icons.EVENT,
            "label": "Agenda",
            "info": f"{stats['agenda']} pendentes",
            "color": "#00897B",
            "route": "/agenda",
        },
        {
            "icon": ft.Icons.MENU_BOOK,
            "label": "Enciclopédia",
            "info": "Consultar",
            "color": "#455A64",
            "route": "/enciclopedia",
        },
    ]

    coluna_esquerda = ft.Column(
        controls=[
            criar_card_menu(i["icon"], i["label"], i["info"], i["color"], i["route"])
            for i in itens_col1
        ],
        spacing=20,
    )

    coluna_direita = ft.Column(
        controls=[
            criar_card_menu(i["icon"], i["label"], i["info"], i["color"], i["route"])
            for i in itens_col2
        ],
        spacing=20,
    )

    # --- Layout Principal ---
    mensagem_boas_vindas = (
        f"Você tem {stats['agenda']} tarefas hoje."
        if stats["agenda"] > 0
        else "Tudo tranquilo por aqui!"
    )
    cor_mensagem = "#097A12" if stats["agenda"] > 0 else "grey"
    peso_mensagem = ft.FontWeight.BOLD if stats["agenda"] > 0 else ft.FontWeight.NORMAL

    return ft.Column(
        controls=[
            ft.Container(height=20),
            ft.Icon(ft.Icons.YARD, size=60, color="#097A12"),
            ft.Text("PlantHub", size=32, weight=ft.FontWeight.BOLD, color="#097A12"),
            ft.Text(
                mensagem_boas_vindas, size=14, color=cor_mensagem, weight=peso_mensagem
            ),
            ft.Container(height=20),
            ft.Row(
                controls=[coluna_esquerda, coluna_direita],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=20,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
