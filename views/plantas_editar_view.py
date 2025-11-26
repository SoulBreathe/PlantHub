import flet as ft
from datetime import datetime
from services.database_service import DatabaseService
from models.planta import Planta
from components.card_padrao import CardPremium


def PlantaEditarView(page: ft.Page):
    db = DatabaseService()

    # 1. Pegar o ID da rota (ex: /plantas/editar/5)
    try:
        id_planta = int(page.route.split("/")[-1])
        planta_atual = db.get_planta_por_id(id_planta)
    except:
        planta_atual = None

    if not planta_atual:
        return ft.Column(
            [
                ft.Text("Planta não encontrada.", size=20),
                ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/plantas")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    # 2. Carregar Listas para Dropdowns
    especies = db.get_all_especies()
    locais = db.get_all_locais()
    opcoes_esp = [
        ft.dropdown.Option(key=str(e.id_especie), text=e.nome_popular) for e in especies
    ]
    opcoes_loc = [ft.dropdown.Option(key=str(l.id_local), text=l.nome) for l in locais]

    # 3. Campos (Preenchidos com valores atuais)
    txt_nome = ft.TextField(
        label="Nome",
        value=planta_atual.nome_personalizado,
        width=280,
        border_color="#097A12",
    )

    dd_especie = ft.Dropdown(
        label="Espécie",
        options=opcoes_esp,
        width=280,
        border_color="#097A12",
        value=str(planta_atual.id_especie),  # Seleciona o valor atual
    )

    dd_local = ft.Dropdown(
        label="Local",
        options=opcoes_loc,
        width=280,
        border_color="#097A12",
        value=str(planta_atual.id_local),  # Seleciona o valor atual
    )

    # DatePicker Logic
    txt_data = ft.TextField(
        label="Data Plantio",
        value=planta_atual.data_plantio,
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
    )

    btn_cal = ft.IconButton(
        ft.Icons.CALENDAR_MONTH,
        icon_color="#097A12",
        icon_size=30,
        on_click=lambda _: page.open(date_picker),
    )

    linha_data = ft.Row(
        [txt_data, btn_cal], alignment=ft.MainAxisAlignment.CENTER, width=280
    )

    # --- AÇÃO: SALVAR EDIÇÃO ---
    def salvar_edicao(e):
        if not txt_nome.value or not dd_especie.value:
            page.open(
                ft.SnackBar(ft.Text("Nome e Espécie são obrigatórios!"), bgcolor="red")
            )
            return

        # Atualiza o objeto
        planta_atual.nome_personalizado = txt_nome.value
        planta_atual.id_especie = int(dd_especie.value)
        planta_atual.id_local = int(dd_local.value)
        planta_atual.data_plantio = txt_data.value

        try:
            db.update_planta(planta_atual)
            page.open(ft.SnackBar(ft.Text("Planta atualizada!"), bgcolor="green"))
            page.go("/plantas")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # --- AÇÃO: EXCLUIR (Com confirmação) ---
    def confirmar_exclusao(e):
        try:
            db.delete_planta(id_planta)
            # Fecha diálogo
            page.open(ft.SnackBar(ft.Text("Planta removida."), bgcolor="green"))
            page.go("/plantas")
        except Exception as ex:
            page.close(dlg_confirmar)
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    dlg_confirmar = ft.AlertDialog(
        modal=True,
        title=ft.Text("Tem certeza?"),
        content=ft.Text("Isso apagará a planta e todo o histórico do diário dela."),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: page.close(dlg_confirmar)),
            ft.TextButton(
                "Sim, Excluir",
                on_click=confirmar_exclusao,
                style=ft.ButtonStyle(color="red"),
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Layout
    conteudo = ft.Column(
        [
            txt_nome,
            dd_especie,
            dd_local,
            linha_data,
            ft.Divider(height=10, color="transparent"),
            # Botões de Ação
            ft.ElevatedButton(
                "Salvar Alterações",
                on_click=salvar_edicao,
                bgcolor="#097A12",
                color="white",
                width=280,
                height=45,
            ),
            ft.TextButton(
                "Excluir Planta",
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
        content=CardPremium(title="Editar Planta", content=conteudo, width=350),
        alignment=ft.alignment.center,
        expand=True,
    )
