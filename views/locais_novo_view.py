import flet as ft
from services.database_service import DatabaseService
from models.local import Local

from components.card_padrao import CardPremium


def LocaisNovaView(page: ft.Page):
    db = DatabaseService()

    # --- Campos do formulário ---
    nome = ft.TextField(
        label="Nome do local (ex: Varanda Sul)",
        width=300,
        border_color="#097A12",
    )

    tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("jardim"),
            ft.dropdown.Option("varanda"),
            ft.dropdown.Option("horta"),
            ft.dropdown.Option("estufa"),
        ],
        width=300,
        border_color="#097A12",
    )

    area = ft.TextField(
        label="Área (m²)",
        hint_text="ex: 2.5",
        width=300,
        border_color="#097A12",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    descricao = ft.TextField(
        label="Descrição (opcional)",
        multiline=True,
        max_lines=3,
        width=300,
        border_color="#097A12",
    )

    # --- Lógica de Salvar ---
    def salvar_local(e):
        if not nome.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Nome é obrigatório!"), bgcolor=ft.Colors.RED_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()
            return

        novo_local = Local(
            nome=nome.value,
            tipo=tipo.value or "outro",
            area_m2=float(area.value) if area.value else 0.0,
            descricao=descricao.value or None,
        )

        try:
            db.add_local(novo_local)
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Local cadastrado!"), bgcolor=ft.Colors.GREEN_ACCENT_700
            )
            page.snack_bar.open = True
            page.go("/locais")
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"⚠️ {str(ve)}"), bgcolor=ft.Colors.ORANGE_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"❌ Erro: {str(e)}"), bgcolor=ft.Colors.RED_ACCENT_700
            )
            page.snack_bar.open = True
            page.update()

    # Botão Salvar
    botao_salvar = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.SAVE, size=20), ft.Text("Salvar Local", size=16)],
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor="#097A12",
        color=ft.Colors.WHITE,
        width=300,
        height=50,
        on_click=salvar_local,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
    )

    # --- MONTAGEM DO CARD ---
    # 2. Agrupar campos numa Coluna
    conteudo_form = ft.Column(
        controls=[
            nome,
            tipo,
            area,
            descricao,
            ft.Container(height=20),
            botao_salvar,
        ],
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 3. Usar o CardPremium
    card = CardPremium(title="Dados do Ambiente", content=conteudo_form)

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
