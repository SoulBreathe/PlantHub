import flet as ft


class CardPremium(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        title: str = None,
        width: int = 400,
        padding: int = 20,
    ):
        """
        Componente de Card Padronizado para Formulários.

        Args:
            content (ft.Control): O conteúdo principal (geralmente uma Column com os campos).
            title (str, optional): Título no topo do card.
            width (int): Largura do card (padrão 400).
            padding (int): Espaçamento interno.
        """

        elementos = []

        # Cabeçalho do Card (Título + Divisória invisível)
        if title:
            elementos.append(
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#333333")
            )
            elementos.append(ft.Divider(height=10, color="transparent"))

        # Adiciona o conteúdo do formulário
        elementos.append(content)

        super().__init__(
            content=ft.Column(
                controls=elementos,
                spacing=5,
                # tight=True faz a coluna ocupar apenas o espaço necessário
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=width,
            padding=padding,
            bgcolor=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(12),
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )
