import flet as ft


def HomeView(page: ft.Page):

    def criar_card_menu(icone, titulo, cor, rota):
        return ft.Container(
            width=155,
            height=150,
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
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(0.2, "white"),
                        border_radius=50,
                        content=ft.Icon(icone, size=32, color="white"),
                    ),
                    ft.Text(
                        titulo,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="white",
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
            ),
        )

    # Coluna da Esquerda
    itens_col1 = [
        {
            "icon": ft.Icons.LOCATION_ON,
            "label": "Locais",
            "color": "#558B2F",
            "route": "/locais",
        },  # Verde Musgo
        {
            "icon": ft.Icons.BOOK,
            "label": "Diário",
            "color": "#8D6E63",
            "route": "/diario",
        },  # Marrom Terra
        {
            "icon": ft.Icons.HEALTH_AND_SAFETY,
            "label": "Diagnóstico",
            "color": "#BF360C",
            "route": "/diagnostico",
        },  # Terracota
    ]

    # Coluna da Direita
    itens_col2 = [
        {
            "icon": ft.Icons.LOCAL_FLORIST,
            "label": "Minhas Plantas",
            "color": "#2E7D32",
            "route": "/plantas",
        },  # Verde Floresta
        {
            "icon": ft.Icons.EVENT,
            "label": "Agenda",
            "color": "#00897B",
            "route": "/agenda",
        },  # Verde Água
        {
            "icon": ft.Icons.MENU_BOOK,
            "label": "Enciclopédia",
            "color": "#455A64",
            "route": "/enciclopedia",
        },  # Azul Pedra
    ]

    # Gerar os Cards
    coluna_esquerda = ft.Column(
        controls=[
            criar_card_menu(i["icon"], i["label"], i["color"], i["route"])
            for i in itens_col1
        ],
        spacing=20,
    )

    coluna_direita = ft.Column(
        controls=[
            criar_card_menu(i["icon"], i["label"], i["color"], i["route"])
            for i in itens_col2
        ],
        spacing=20,
    )

    # --- Layout Principal ---
    return ft.Column(
        controls=[
            ft.Container(height=20),  # Espaço topo
            ft.Icon(ft.Icons.YARD, size=60, color="#097A12"),
            ft.Text("PlantHub", size=32, weight=ft.FontWeight.BOLD, color="#097A12"),
            ft.Text("Gerencie sua horta com carinho", size=14, color="grey"),
            ft.Container(height=20),
            # Grid do Menu
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
