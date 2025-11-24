import flet as ft
from services.database_service import DatabaseService
from models.planta import Planta

from components.card_padrao import CardPremium


def PlantaNovaView(page: ft.Page):
    db = DatabaseService()

    # Carregar dados para os Dropdowns
    try:
        especies = db.get_all_especies()
        locais = db.get_all_locais()
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        especies = []
        locais = []

    # --- Campos do formulário ---
    nome = ft.TextField(
        label="Nome da planta (ex: Minha Rosa)",
        width=300,
        border_color="#097A12",
    )

    # Dropdowns convertendo objetos para Options
    dd_especie = ft.Dropdown(
        label="Espécie",
        options=[
            ft.dropdown.Option(key=str(e.id_especie), text=e.nome_popular)
            for e in especies
        ],
        width=300,
        border_color="#097A12",
    )

    dd_local = ft.Dropdown(
        label="Local",
        options=[ft.dropdown.Option(key=str(l.id_local), text=l.nome) for l in locais],
        width=300,
        border_color="#097A12",
    )

    data = ft.TextField(
        label="Data de plantio",
        hint_text="DD-MM-YYYY",
        width=300,
        border_color="#097A12",
    )

    # --- Lógica de Salvar ---
    def salvar(e):
        # Validação simples
        erros = []
        if not nome.value:
            erros.append("Nome obrigatório")
        if not dd_especie.value:
            erros.append("Espécie obrigatória")
        if not dd_local.value:
            erros.append("Local obrigatório")

        if erros:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro: {', '.join(erros)}"), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        nova = Planta(
            nome_personalizado=nome.value,
            id_especie=int(dd_especie.value),
            id_local=int(dd_local.value),
            data_plantio=data.value or None,
        )

        try:
            db.add_planta(nova)
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Planta cadastrada!"), bgcolor="green"
            )
            page.snack_bar.open = True
            page.go("/plantas")
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"❌ Erro: {ex}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # Botão Salvar
    botao_salvar = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.SAVE, size=20), ft.Text("Salvar Planta", size=16)],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor="#097A12",
        color="white",
        width=300,
        height=50,
        on_click=salvar,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    # --- MONTAGEM DO CARD ---
    conteudo_form = ft.Column(
        controls=[
            nome,
            dd_especie,
            dd_local,
            data,
            ft.Container(height=20),
            botao_salvar,
        ],
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 3. Usar o CardPremium
    card = CardPremium(title="Detalhes da Planta", content=conteudo_form)

    return ft.Column(
        controls=[
            ft.Container(
                content=card,
                alignment=ft.alignment.center,
                expand=True,
            ),
        ],
        expand=True,
    )
