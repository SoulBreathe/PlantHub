import flet as ft
from typing import Optional


class CardPremium(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        title: Optional[str] = None,
        width: int = 400,
        height: Optional[int] = None,
        padding: int = 20,
    ):
        """Componente visual padronizado para formulários (Card branco com sombra)."""

        # Monta a estrutura interna
        elementos = []

        if title:
            elementos.extend(
                [
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color="#333333"),
                    ft.Divider(height=10, color="transparent"),
                ]
            )

        elementos.append(content)

        super().__init__(
            width=width,
            height=height,
            padding=padding,
            bgcolor="white",
            border_radius=12,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                blur_radius=10,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.1, "black"),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Column(
                controls=elementos,
                spacing=5,
                # Se não tem altura fixa, ajusta-se ao conteúdo (tight)
                tight=True if height is None else False,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
