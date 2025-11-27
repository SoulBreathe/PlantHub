import flet as ft
from datetime import datetime
from services.database_service import DatabaseService
from components.card_padrao import CardPremium


def AgendaEditarView(page: ft.Page):
    db = DatabaseService()

    # 1. Buscar Tarefa pelo ID da rota
    try:
        id_agenda = int(page.route.split("/")[-1])
        tarefa_atual = db.get_tarefa_por_id(id_agenda)
    except:
        tarefa_atual = None

    if not tarefa_atual:
        return ft.Column(
            controls=[
                ft.Text("Tarefa não encontrada", size=20),
                ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/agenda")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # 2. Elementos da UI (Dropdowns, Inputs)
    plantas = db.get_all_plantas()
    opcoes_plantas = [
        ft.dropdown.Option(key=str(p.id_planta), text=p.nome_personalizado)
        for p in plantas
    ]

    dd_planta = ft.Dropdown(
        label="Planta",
        options=opcoes_plantas,
        width=280,
        border_color="#097A12",
        value=str(tarefa_atual.id_planta),
    )

    dd_tipo = ft.Dropdown(
        label="Tipo de Tarefa",
        width=280,
        border_color="#097A12",
        options=[
            ft.dropdown.Option("Rega"),
            ft.dropdown.Option("Adubação"),
            ft.dropdown.Option("Poda"),
            ft.dropdown.Option("Colheita"),
            ft.dropdown.Option("Outro"),
        ],
        value=tarefa_atual.tipo_tarefa,
    )

    txt_data = ft.TextField(
        label="Data",
        value=tarefa_atual.data_agendada,
        width=220,
        read_only=True,
        border_color="#097A12",
    )
    txt_detalhes = ft.TextField(
        label="Detalhes", value=tarefa_atual.detalhes, width=280, border_color="#097A12"
    )

    # Lógica do DatePicker
    def mudou_data(e):
        if date_picker.value:
            txt_data.value = date_picker.value.strftime("%Y-%m-%d")
            txt_data.update()

    date_picker = ft.DatePicker(
        on_change=mudou_data,
        first_date=datetime(2023, 1, 1),
        confirm_text="Confirmar",
        cancel_text="Cancelar",
    )
    btn_cal = ft.IconButton(
        icon=ft.Icons.CALENDAR_MONTH,
        icon_color="#097A12",
        on_click=lambda _: page.open(date_picker),
    )
    linha_data = ft.Row(
        [txt_data, btn_cal], alignment=ft.MainAxisAlignment.CENTER, width=280
    )

    # --- AÇÃO: SALVAR ---
    def salvar(e):
        if not dd_planta.value or not dd_tipo.value:
            page.open(
                ft.SnackBar(ft.Text("Planta e Tipo obrigatórios!"), bgcolor="red")
            )
            return

        tarefa_atual.id_planta = int(dd_planta.value)
        tarefa_atual.tipo_tarefa = dd_tipo.value
        tarefa_atual.data_agendada = txt_data.value
        tarefa_atual.detalhes = txt_detalhes.value

        try:
            db.update_tarefa_agenda(tarefa_atual)
            page.open(
                ft.SnackBar(ft.Text("Tarefa atualizada com sucesso!"), bgcolor="green")
            )
            page.go("/agenda")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # --- AÇÃO: EXCLUIR ---
    def confirmar_exclusao(e):
        try:
            db.delete_tarefa_agenda(id_agenda)
            page.open(ft.SnackBar(ft.Text("Tarefa removida!"), bgcolor="green"))
            page.go("/agenda")
        except Exception as ex:
            page.close(dlg_confirmar)  # Fecha diálogo apenas se ficar na tela
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    dlg_confirmar = ft.AlertDialog(
        title=ft.Text("Excluir Tarefa?"),
        content=ft.Text("Essa ação não pode ser desfeita."),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: page.close(dlg_confirmar)),
            ft.TextButton(
                "Excluir",
                style=ft.ButtonStyle(color="red"),
                on_click=confirmar_exclusao,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Montagem do Layout
    conteudo = ft.Column(
        controls=[
            dd_planta,
            dd_tipo,
            linha_data,
            txt_detalhes,
            ft.Divider(height=10, color="transparent"),
            ft.ElevatedButton(
                text="Salvar Alterações",
                on_click=salvar,
                bgcolor="#097A12",
                color="white",
                width=280,
                height=45,
            ),
            ft.TextButton(
                text="Excluir Tarefa",
                icon=ft.Icons.DELETE,
                icon_color="red",
                style=ft.ButtonStyle(color="red"),
                on_click=lambda _: page.open(dlg_confirmar),
            ),
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=CardPremium(title="Editar Tarefa", content=conteudo, width=350),
        alignment=ft.alignment.center,
        expand=True,
    )
