# views/locais_novo_view.py
import flet as ft
from services.database_service import DatabaseService
from models.local import Local


def LocaisNovaView(page: ft.Page):
    db = DatabaseService()

    # Campos do formulário
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
    )

    def salvar_local(e):
        if not nome.value:
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Nome é obrigatório!"),
                bgcolor=ft.Colors.RED_ACCENT_700,
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
                content=ft.Text("✅ Local cadastrado com sucesso!"),
                bgcolor=ft.Colors.GREEN_ACCENT_700,
                duration=3000,
            )
            page.snack_bar.open = True
            page.go("/locais")
        except ValueError as ve:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"⚠️ {str(ve)}"),
                bgcolor=ft.Colors.ORANGE_ACCENT_700,
                duration=4000,
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"❌ Erro: {str(e)}"),
                bgcolor=ft.Colors.RED_ACCENT_700,
                duration=5000,
            )
            page.snack_bar.open = True
            page.update()

    # Botão Salvar — retangular, maior, com ícone
    botao_salvar = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SAVE, size=20),
                ft.Text("Salvar Local", size=16, weight=ft.FontWeight.W_500),
            ],
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

    # Card completo — título dentro, layout premium
    form_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "📍 Novo Local",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                nome,
                tipo,
                area,
                descricao,
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
