import flet as ft
from services.database_service import DatabaseService


def LocaisView(page: ft.Page):
    db = DatabaseService()
    locais = db.get_all_locais()

    def criar_card_local(local):
        # Mapeia ícone e cor baseado no tipo do local
        mapa_estilo = {
            "jardim": (ft.Icons.PARK, ft.Colors.GREEN),
            "varanda": (ft.Icons.BALCONY, ft.Colors.ORANGE),
            "estufa": (ft.Icons.HOUSE_SIDING, ft.Colors.BLUE),
            "horta": (ft.Icons.AGRICULTURE, ft.Colors.BROWN),
            "interno": (ft.Icons.HOME, "#097A12"),
        }

        icone, cor = mapa_estilo.get(
            local.tipo.lower(), (ft.Icons.LOCATION_ON, ft.Colors.GREY)
        )

        return ft.Container(
            padding=5,
            bgcolor="white",
            border_radius=12,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.Column(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(icone, color=cor, size=32),
                        title=ft.Text(local.nome, weight=ft.FontWeight.BOLD, size=16),
                        subtitle=ft.Text(
                            f"{local.tipo} • {local.area_m2} m²", size=12, color="grey"
                        ),
                        trailing=ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color="grey",
                            tooltip="Editar Local",
                            on_click=lambda _: page.go(
                                f"/locais/editar/{local.id_local}"
                            ),
                        ),
                    ),
                    ft.Container(
                        padding=ft.padding.only(left=16, right=16, bottom=10),
                        content=ft.Text(
                            local.descricao or "Sem descrição.",
                            size=12,
                            color="grey",
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                    ),
                ],
                spacing=0,
            ),
        )

    # --- Estado Vazio ---
    if not locais:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.ADD_LOCATION_ALT, size=64, color="#097A12"),
                ft.Text("Nenhum local cadastrado", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Adicione onde você cultiva suas plantas.", color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    return ft.ListView(
        controls=[criar_card_local(l) for l in locais], padding=15, expand=True
    )
