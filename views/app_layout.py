# views/app_layout.py
import flet as ft


class AppLayout(ft.ResponsiveRow):
    def __init__(self, page: ft.Page, theme_changed, content: ft.Control):
        super().__init__(
            columns=12,
            spacing=0,
            run_spacing=0,
            expand=True,
        )
        self.controls = [
            ft.Column(
                controls=[content],
                col={"xs": 12},
                expand=True,
            )
        ]

        self.page = page
        self.theme_changed = theme_changed
        self.page_content = content

        # Só exibe o conteúdo centralizado
        self.build_layout()

    def build_layout(self):
        self.controls.clear()

        content_col = ft.Column(
            controls=[self.page_content],
            col={"xs": 12, "md": 12},  # ocupa toda a largura
            expand=True,
        )

        self.controls = [content_col]

    def nav_change(self, e):  # pode manter, mas não será usado
        pass
