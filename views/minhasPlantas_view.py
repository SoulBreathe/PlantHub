# views/minhasPlantas_view.py
import flet as ft
from models.planta_completa import PlantaCompleta
from services.database_service import DatabaseService


def criar_card_planta(planta: PlantaCompleta) -> ft.Container:
    data_fmt = planta.data_plantio if planta.data_plantio else "—"
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(planta.nome_personalizado, weight=ft.FontWeight.BOLD, size=16),
                ft.Text(f"🌿 {planta.nome_popular}", size=14),
                ft.Text(f"📍 {planta.nome_local}", size=12, color=ft.Colors.GREY_600),
                ft.Text(f"📅 {data_fmt}", size=12, color=ft.Colors.GREY_500),
            ],
            spacing=4,
        ),
        padding=12,
        bgcolor=ft.Colors.SURFACE_VARIANT,
        border_radius=10,
        width=150,
        height=150,
        shadow=ft.BoxShadow(blur_radius=4, color=ft.Colors.BLACK12, spread_radius=1),
    )


def MinhasPlantasView(page: ft.Page):
    db = DatabaseService()
    plantas = db.get_plantas_completas()

    coluna_esq = ft.Column(spacing=16, expand=False)
    coluna_dir = ft.Column(spacing=16, expand=False)

    for i, planta in enumerate(plantas):
        card = criar_card_planta(planta)
        if i % 2 == 0:
            coluna_esq.controls.append(card)
        else:
            coluna_dir.controls.append(card)

    conteudo = ft.Row(
        [coluna_esq, coluna_dir], spacing=16, alignment=ft.MainAxisAlignment.CENTER
    )

    if not plantas:
        conteudo = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=64, color=ft.Colors.GREY_400),
                    ft.Text("Nenhuma planta cadastrada", size=20),
                    ft.Text("Adicione suas plantas para começar!", size=14),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
        )

    return ft.Column(
        controls=[
            ft.ListView(
                controls=[conteudo] if plantas else [conteudo], expand=True, padding=10
            ),
        ],
        expand=True,
    )
