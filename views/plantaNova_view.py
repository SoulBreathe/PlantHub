# views/plantaNova_view.py
import flet as ft
from services.database_service import DatabaseService
from models.planta import Planta


def PlantaNovaView(page: ft.Page):
    db = DatabaseService()
    especies = db.get_all_especies()
    locais = db.get_all_locais()

    # Campos do formulário
    nome = ft.TextField(
        label="Nome da planta (ex: Minha Rosa)",
        width=300,
        border_color="#097A12",
    )
    especie = ft.Dropdown(
        label="Espécie",
        options=[ft.dropdown.Option(e.id_especie, e.nome_popular) for e in especies],
        width=300,
        border_color="#097A12",
    )
    local = ft.Dropdown(
        label="Local",
        options=[ft.dropdown.Option(l.id_local, l.nome) for l in locais],
        width=300,
        border_color="#097A12",
    )
    data = ft.TextField(
        label="Data de plantio (opcional)",
        hint_text="YYYY-MM-DD",
        width=300,
        border_color="#097A12",
    )

    def salvar(e):
        if not nome.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Nome é obrigatório!"), bgcolor=ft.Colors.RED_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()
            return
        if not especie.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Selecione uma espécie!"), bgcolor=ft.Colors.RED_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()
            return
        if not local.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Selecione um local!"), bgcolor=ft.Colors.RED_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()
            return

        nova = Planta(
            nome_personalizado=nome.value,
            id_especie=int(especie.value),
            id_local=int(local.value),
            data_plantio=data.value or None,
        )

        try:
            db.add_planta(nova)
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Planta cadastrada com sucesso!"),
                bgcolor=ft.Colors.GREEN_ACCENT_700,
                duration=3000,
            )
            page.snack_bar.open = True
            page.go("/plantas")
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"❌ Erro: {e}"),
                bgcolor=ft.Colors.RED_ACCENT_700,
                duration=5000,
            )
            page.snack_bar.open = True
            page.update()

    # Botão Salvar
    botao_salvar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SAVE, size=20),
                ft.Text("Salvar Planta", size=18, weight=ft.FontWeight.W_500),
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor="#097A12",
        color=ft.Colors.WHITE,
        width=200,
        height=50,
        on_click=salvar,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    # Card completo
    form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "🪴 Nova Planta",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                nome,
                especie,
                local,
                data,
                ft.Container(height=20),  # espaço acima do botão
                botao_salvar,
                ft.Container(height=10),  # espaço abaixo
            ],
            spacing=16,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400,
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(12),
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.BLACK12,
            spread_radius=2,
        ),
        alignment=ft.alignment.center,
    )

    return ft.Column(
        controls=[
            ft.Container(
                content=form_card,
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        expand=True,
    )
