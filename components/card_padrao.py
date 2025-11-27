import flet as ft
from typing import Optional


class CardPremium(ft.Container):
    def __init__(
        self,
        content: ft.Control,
        title: Optional[str] = None,
        width: int = 350,
        height: Optional[int] = None,
        padding: int = 30,
    ):
        """
        Componente visual padronizado para formulários.
        Possui sombra suave, bordas arredondadas e ajuste automático de altura (tight).
        """

        # Estrutura interna
        elementos = []

        if title:
            elementos.extend(
                [
                    ft.Text(
                        title,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#333333",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=20, color="transparent"),
                ]
            )

        elementos.append(content)

        super().__init__(
            width=width,
            height=height,
            padding=padding,
            bgcolor="white",
            border_radius=20,
            alignment=None,  # None permite que o 'tight' da Column funcione
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=15,
                spread_radius=2,
                color=ft.Colors.with_opacity(0.1, "black"),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Column(
                controls=elementos,
                spacing=0,
                tight=True if height is None else False,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
