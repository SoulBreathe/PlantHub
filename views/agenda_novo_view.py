import flet as ft
from datetime import datetime
from services.database_service import DatabaseService
from models.agenda import TarefaAgenda
from components.card_padrao import CardPremium


def AgendaNovoView(page: ft.Page):
    db = DatabaseService()

    # Carrega plantas para o dropdown
    plantas = db.get_all_plantas()
    opcoes = [
        ft.dropdown.Option(key=str(p.id_planta), text=p.nome_personalizado)
        for p in plantas
    ]

    # --- Elementos da UI ---
    dd_planta = ft.Dropdown(
        label="Planta", options=opcoes, width=280, border_color="#097A12"
    )

    dd_tipo = ft.Dropdown(
        label="Tipo de Tarefa",
        width=280,
        options=[
            ft.dropdown.Option("Rega"),
            ft.dropdown.Option("Adubação"),
            ft.dropdown.Option("Poda"),
            ft.dropdown.Option("Colheita"),
            ft.dropdown.Option("Outro"),
        ],
        border_color="#097A12",
    )

    # Configuração do Seletor de Data
    txt_data = ft.TextField(
        label="Data Agendada",
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
        first_date=datetime(2023, 1, 1),
        last_date=datetime(2030, 12, 31),
        confirm_text="Confirmar",
        cancel_text="Cancelar",
    )

    btn_calendario = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        icon_color="#097A12",
        icon_size=30,
        tooltip="Selecionar Data",
        on_click=lambda _: page.open(date_picker),
    )

    linha_data = ft.Row(
        [txt_data, btn_calendario], alignment=ft.MainAxisAlignment.CENTER
    )

    txt_detalhes = ft.TextField(
        label="Detalhes (Opcional)", width=280, border_color="#097A12"
    )

    # --- Lógica de Salvamento ---
    def salvar(e):
        if not dd_planta.value or not dd_tipo.value:
            page.open(ft.SnackBar(ft.Text("Preencha Planta e Tipo!"), bgcolor="red"))
            return

        nova = TarefaAgenda(
            tipo_tarefa=dd_tipo.value,
            data_agendada=txt_data.value,
            detalhes=txt_detalhes.value,
            id_planta=int(dd_planta.value),
        )

        try:
            db.add_tarefa_agenda(nova)
            page.open(ft.SnackBar(ft.Text("Tarefa agendada!"), bgcolor="green"))
            page.go("/agenda")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # Layout
    conteudo = ft.Column(
        controls=[
            dd_planta,
            dd_tipo,
            linha_data,
            txt_detalhes,
            ft.Divider(height=10, color="transparent"),
            ft.ElevatedButton(
                text="Agendar",
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
        content=CardPremium(title="Agendar Cuidados", content=conteudo, width=350),
        alignment=ft.alignment.center,
        expand=True,
    )
