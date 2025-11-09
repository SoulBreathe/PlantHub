import flet as ft
from services.database_service import DatabaseService


def LocaisView(page: ft.Page) -> ft.Column:
    db = DatabaseService()
    try:
        locais = (
            db.get_all_locais()
        )  # ← deve retornar Local(id_local, nome, descricao, tipo, area_m2)
    except Exception as e:
        print(f"Erro ao carregar locais: {e}")
        locais = []

    def criar_card(local):
        # Define ícone e cor pelo tipo (ex: jardim = verde, varanda = laranja)
        icon_map = {
            "jardim": (ft.Icons.PARK, ft.Colors.GREEN),
            "varanda": (ft.Icons.BALCONY, ft.Colors.ORANGE),
            "estufa": (ft.Icons.HOUSE, ft.Colors.BLUE),
            "horta": (ft.Icons.GARDEN_CART, ft.Colors.BROWN),
        }
        icono, cor = icon_map.get(
            local.tipo.lower(), (ft.Icons.LOCATION_ON, ft.Colors.GREY)
        )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(icono, color=cor, size=36),
                            title=ft.Text(
                                local.nome, weight=ft.FontWeight.BOLD, size=18
                            ),
                            subtitle=ft.Text(
                                f"{local.tipo.title()} • {local.area_m2:.1f} m²",
                                color=ft.Colors.GREY_700,
                            ),
                        ),
                        ft.Container(
                            padding=ft.padding.only(left=16, right=16, bottom=8),
                            content=ft.Text(
                                local.descricao or "Sem descrição",
                                size=13,
                                color=ft.Colors.GREY_600,
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=ft.padding.all(0),
            ),
            elevation=2,
        )

    cards = [criar_card(local) for local in locais] or [
        ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=64, color=ft.Colors.GREY_400),
                    ft.Text("Nenhum local cadastrado", size=20),
                    ft.Text(
                        "Adicione seus espaços de cultivo!",
                        size=14,
                        color=ft.Colors.GREY_600,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )
    ]

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Meus Locais", size=24, weight=ft.FontWeight.BOLD),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        on_click=lambda _: page.go("/locais/novo"),
                        bgcolor=ft.Colors.GREEN,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.ListView(
                controls=cards,
                expand=True,
                padding=ft.padding.all(10),
            ),
        ],
        expand=True,
    )
