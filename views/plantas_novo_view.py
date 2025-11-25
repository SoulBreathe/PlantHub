import flet as ft
from datetime import datetime
from services.database_service import DatabaseService
from models.planta import Planta
from components.card_padrao import CardPremium


def PlantaNovaView(page: ft.Page):
    db = DatabaseService()

    # Carregar dados para os dropdowns
    especies = db.get_all_especies()
    locais = db.get_all_locais()

    # Opções
    opcoes_especies = [
        ft.dropdown.Option(key=str(e.id_especie), text=e.nome_popular) for e in especies
    ]
    opcoes_locais = [
        ft.dropdown.Option(key=str(l.id_local), text=l.nome) for l in locais
    ]

    # --- Elementos do Formulário ---
    txt_nome = ft.TextField(
        label="Nome carinhoso (Ex: Tomatinho)", width=280, border_color="#097A12"
    )
    dd_especie = ft.Dropdown(
        label="Espécie", options=opcoes_especies, width=280, border_color="#097A12"
    )
    dd_local = ft.Dropdown(
        label="Onde está plantada?",
        options=opcoes_locais,
        width=280,
        border_color="#097A12",
    )

    # --- Configuração de Data ---
    txt_data = ft.TextField(
        label="Data do Plantio",
        value=datetime.today().strftime("%Y-%m-%d"),
        width=220,
        read_only=True,
        border_color="#097A12",
    )

    def data_mudou(e):
        if date_picker.value:
            txt_data.value = date_picker.value.strftime("%Y-%m-%d")
            txt_data.update()

    date_picker = ft.DatePicker(
        on_change=data_mudou,
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        confirm_text="Confirmar",
        cancel_text="Cancelar",
        help_text="Quando você plantou?",
    )

    btn_calendario = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        icon_color="#097A12",
        icon_size=30,
        tooltip="Selecionar Data",
        on_click=lambda _: page.open(date_picker),
    )

    linha_data = ft.Row(
        [txt_data, btn_calendario], alignment=ft.MainAxisAlignment.CENTER, width=280
    )

    # --- Lógica de Salvar ---
    def salvar(e):
        if not txt_nome.value or not dd_especie.value or not dd_local.value:
            page.open(
                ft.SnackBar(ft.Text("Preencha Nome, Espécie e Local!"), bgcolor="red")
            )
            return

        try:
            nova_planta = Planta(
                nome_personalizado=txt_nome.value,
                data_plantio=txt_data.value,
                id_especie=int(dd_especie.value),
                id_local=int(dd_local.value),
                status="ativa",
            )
            db.add_planta(nova_planta)
            page.open(
                ft.SnackBar(ft.Text("Planta adicionada com amor! 🌱"), bgcolor="green")
            )
            page.go("/plantas")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # --- Montagem do Layout ---

    # Validação inicial: Impede cadastro se não houver dados base
    if not especies or not locais:
        conteudo = ft.Column(
            controls=[
                ft.Icon(ft.Icons.WARNING_AMBER, color="orange", size=48),
                ft.Text("Faltam dados!", weight=ft.FontWeight.BOLD, size=16),
                ft.Text(
                    "Cadastre Espécies na Enciclopédia\ne Locais antes de adicionar plantas.",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Container(height=10),
                ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/plantas")),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
    else:
        conteudo = ft.Column(
            controls=[
                txt_nome,
                dd_especie,
                dd_local,
                linha_data,
                ft.Divider(height=10, color="transparent"),
                ft.ElevatedButton(
                    text="Plantar",
                    on_click=salvar,
                    bgcolor="#097A12",
                    color="white",
                    width=280,
                    height=45,
                ),
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    return ft.Container(
        content=CardPremium(title="Nova Planta", content=conteudo, width=350),
        alignment=ft.alignment.center,
        expand=True,
    )
