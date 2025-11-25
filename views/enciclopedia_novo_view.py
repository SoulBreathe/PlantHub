import flet as ft
from services.database_service import DatabaseService
from models.especie import Especie
from models.praga import Praga
from components.card_padrao import CardPremium


def EnciclopediaNovoView(page: ft.Page):
    db = DatabaseService()

    # =========================================================================
    # ABA 1: NOVA ESPÉCIE
    # =========================================================================
    txt_nome_pop = ft.TextField(label="Nome Popular", border_color="#097A12")
    txt_nome_cient = ft.TextField(
        label="Nome Científico", text_size=12, border_color="#097A12"
    )

    dd_rega = ft.Dropdown(
        label="Frequência de Rega",
        options=[
            ft.dropdown.Option("Diária"),
            ft.dropdown.Option("Regular (2-3 dias)"),
            ft.dropdown.Option("Moderada (Semanal)"),
            ft.dropdown.Option("Pouca (Cactos/Suculentas)"),
        ],
        border_color="#097A12",
    )

    dd_sol = ft.Dropdown(
        label="Necessidade de Sol",
        options=[
            ft.dropdown.Option("Sol Pleno"),
            ft.dropdown.Option("Sombra Parcial"),
            ft.dropdown.Option("Sombra"),
        ],
        border_color="#097A12",
    )

    def salvar_especie(e):
        if not txt_nome_pop.value:
            page.open(
                ft.SnackBar(ft.Text("O nome popular é obrigatório!"), bgcolor="red")
            )
            return

        nova_especie = Especie(
            nome_popular=txt_nome_pop.value,
            nome_cientifico=txt_nome_cient.value,
            instrucoes_rega=dd_rega.value,
            necessidade_sol=dd_sol.value,
        )

        try:
            db.add_especie(nova_especie)
            page.open(
                ft.SnackBar(
                    ft.Text(f"Espécie '{txt_nome_pop.value}' cadastrada!"),
                    bgcolor="green",
                )
            )
            page.go("/enciclopedia")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    form_especie = ft.Column(
        controls=[
            txt_nome_pop,
            txt_nome_cient,
            dd_rega,
            dd_sol,
            ft.Divider(height=10, color="transparent"),
            ft.ElevatedButton(
                text="Salvar Espécie",
                bgcolor="#097A12",
                color="white",
                width=280,
                height=45,
                on_click=salvar_especie,
            ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # =========================================================================
    # ABA 2: NOVA PRAGA
    # =========================================================================
    txt_praga = ft.TextField(label="Nome da Praga/Doença", border_color="red")
    txt_sintomas = ft.TextField(
        label="Sintomas Visíveis", multiline=True, min_lines=2, border_color="red"
    )
    txt_tratamento = ft.TextField(
        label="Tratamento Recomendado", multiline=True, min_lines=2, border_color="red"
    )

    def salvar_praga(e):
        if not txt_praga.value:
            page.open(
                ft.SnackBar(ft.Text("O nome da praga é obrigatório!"), bgcolor="red")
            )
            return

        nova_praga = Praga(
            nome_comum=txt_praga.value,
            sintomas=txt_sintomas.value,
            tratamento=txt_tratamento.value,
        )

        try:
            db.add_praga(nova_praga)
            page.open(
                ft.SnackBar(
                    ft.Text(f"Praga '{txt_praga.value}' cadastrada!"), bgcolor="orange"
                )
            )
            page.go("/enciclopedia")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    form_praga = ft.Column(
        controls=[
            txt_praga,
            txt_sintomas,
            txt_tratamento,
            ft.Divider(height=10, color="transparent"),
            ft.ElevatedButton(
                text="Salvar Praga",
                bgcolor="red",  # Cor de alerta para pragas
                color="white",
                width=280,
                height=45,
                on_click=salvar_praga,
            ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # =========================================================================
    # MONTAGEM FINAL
    # =========================================================================

    tabs = ft.Tabs(
        selected_index=0,
        indicator_color="#097A12",
        label_color="#097A12",
        tabs=[
            ft.Tab(
                text="Nova Planta",
                icon=ft.Icons.LOCAL_FLORIST,
                content=ft.Container(content=form_especie, padding=10),
            ),
            ft.Tab(
                text="Nova Praga",
                icon=ft.Icons.BUG_REPORT,
                content=ft.Container(content=form_praga, padding=10),
            ),
        ],
        expand=True,
    )

    # Usa o CardPremium como container principal
    return ft.Container(
        content=CardPremium(
            title="Adicionar à Base",
            content=tabs,
            width=350,
            height=600,  # Altura fixa para acomodar os campos
        ),
        alignment=ft.alignment.center,
        expand=True,
    )
