import flet as ft
from datetime import datetime
from services.database_service import DatabaseService


def MinhasPlantasView(page: ft.Page):
    db = DatabaseService()
    plantas = db.get_plantas_completas()

    def formatar_data(data_iso):
        """Converte AAAA-MM-DD para DD/MM/AAAA de forma segura."""
        if not data_iso:
            return "--/--/----"

        data_str = str(data_iso)
        try:
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            return data_obj.strftime("%d/%m/%Y")
        except ValueError:
            return data_str

    def criar_card_planta(p):
        return ft.Container(
            padding=5,
            bgcolor="white",
            border_radius=12,
            margin=ft.margin.only(bottom=10),
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
            border=ft.border.all(1, "#f0f0f0"),
            content=ft.ListTile(
                leading=ft.Container(
                    width=45,
                    height=45,
                    bgcolor="#E8F5E9",
                    border_radius=25,
                    alignment=ft.alignment.center,
                    content=ft.Icon(ft.Icons.LOCAL_FLORIST, color="#097A12", size=24),
                ),
                title=ft.Text(
                    p.nome_personalizado, weight=ft.FontWeight.BOLD, color="#333333"
                ),
                subtitle=ft.Column(
                    controls=[
                        ft.Text(f"Espécie: {p.nome_popular}", size=12, color="grey"),
                        ft.Text(
                            f"Local: {p.nome_local} • {formatar_data(p.data_plantio)}",
                            size=12,
                            color="grey",
                        ),
                    ],
                    spacing=0,
                ),
                trailing=ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    icon_color="grey",
                    tooltip="Editar Planta",
                    on_click=lambda _: page.go(f"/plantas/editar/{p.id_planta}"),
                ),
                is_three_line=True,
            ),
        )

    # --- Estado Vazio ---
    if not plantas:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.EMOJI_NATURE, size=64, color="#097A12"),
                ft.Text(
                    "Sua horta está vazia!",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#333333",
                ),
                ft.Text("Adicione sua primeira planta.", size=14, color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    return ft.ListView(
        controls=[criar_card_planta(p) for p in plantas],
        padding=15,
        spacing=0,
        expand=True,
    )
