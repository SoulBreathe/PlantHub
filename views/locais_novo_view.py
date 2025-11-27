import flet as ft
from services.database_service import DatabaseService
from models.local import Local
from components.card_padrao import CardPremium


def LocaisNovaView(page: ft.Page):
    db = DatabaseService()

    # --- Elementos da UI ---
    txt_nome = ft.TextField(
        label="Nome do local (ex: Varanda)", width=300, border_color="#097A12"
    )

    dd_tipo = ft.Dropdown(
        label="Tipo",
        width=300,
        options=[
            ft.dropdown.Option("Estufa"),
            ft.dropdown.Option("Horta"),
            ft.dropdown.Option("Jardim"),
            ft.dropdown.Option("Varanda"),
            ft.dropdown.Option("Interno"),
        ],
        border_color="#097A12",
    )

    txt_area = ft.TextField(
        label="Área (m²)",
        hint_text="ex: 2.5",
        width=300,
        border_color="#097A12",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    txt_desc = ft.TextField(
        label="Descrição (opcional)", multiline=True, max_lines=3, width=300
    )

    # --- Lógica de Salvar ---
    def salvar(e):
        if not txt_nome.value:
            page.open(ft.SnackBar(ft.Text("Nome é obrigatório!"), bgcolor="red"))
            return

        try:
            novo_local = Local(
                nome=txt_nome.value,
                tipo=dd_tipo.value or "Outro",
                area_m2=float(txt_area.value) if txt_area.value else 0.0,
                descricao=txt_desc.value,
            )

            db.add_local(novo_local)
            page.open(
                ft.SnackBar(ft.Text("Local cadastrado com sucesso!"), bgcolor="green")
            )
            page.go("/locais")

        except ValueError:
            page.open(
                ft.SnackBar(
                    ft.Text("Área deve ser um número (use ponto para decimais)."),
                    bgcolor="red",
                )
            )
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # Layout
    conteudo = ft.Column(
        controls=[
            txt_nome,
            dd_tipo,
            txt_area,
            txt_desc,
            ft.Divider(height=15, color="transparent"),
            ft.ElevatedButton(
                text="Salvar Local",
                on_click=salvar,
                bgcolor="#097A12",
                color="white",
                width=300,
                height=45,
            ),
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=CardPremium(title="Novo Local", content=conteudo, width=380),
        alignment=ft.alignment.center,
        padding=20,
        expand=True,
    )
