import flet as ft
from services.database_service import DatabaseService


def EnciclopediaView(page: ft.Page):
    db = DatabaseService()

    # Carrega dados (o service retorna lista vazia em caso de erro, então é seguro)
    especies = db.get_all_especies()
    pragas = db.get_all_pragas()

    # --- Builders dos Cards ---
    def criar_card_especie(e):
        return ft.Container(
            padding=5,
            bgcolor="white",
            border_radius=8,
            margin=ft.margin.only(bottom=5),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.NATURE, color="#097A12", size=32),
                title=ft.Text(e.nome_popular, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(
                    f"{e.nome_cientifico or ''}\nSol: {e.necessidade_sol} | Rega: {e.instrucoes_rega}",
                    size=12,
                ),
                is_three_line=True,
            ),
        )

    def criar_card_praga(p):
        return ft.Container(
            padding=5,
            bgcolor="white",
            border_radius=8,
            margin=ft.margin.only(bottom=5),
            # Borda lateral vermelha para indicar perigo/praga
            border=ft.border.only(left=ft.BorderSide(5, "red")),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.BUG_REPORT, color="red", size=32),
                title=ft.Text(p.nome_comum, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(
                    p.sintomas or "Sintomas não descritos", size=12, max_lines=2
                ),
            ),
        )

    # --- Conteúdo das Abas ---

    # Aba Espécies
    if not especies:
        tab_especies = ft.Column(
            [
                ft.Icon(ft.Icons.SEARCH_OFF, size=40, color="grey"),
                ft.Text("Nenhuma planta cadastrada.", color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        tab_especies = ft.ListView(
            controls=[criar_card_especie(e) for e in especies], padding=10, expand=True
        )

    # Aba Pragas
    if not pragas:
        tab_pragas = ft.Column(
            [
                ft.Icon(ft.Icons.PEST_CONTROL, size=40, color="grey"),
                ft.Text("Nenhuma praga registrada.", color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        tab_pragas = ft.ListView(
            controls=[criar_card_praga(p) for p in pragas], padding=10, expand=True
        )

    # --- Layout Final com Abas ---
    return ft.Tabs(
        selected_index=0,
        animation_duration=300,
        indicator_color="#097A12",
        label_color="#097A12",
        unselected_label_color="grey",
        tabs=[
            ft.Tab(text="Espécies", icon=ft.Icons.LOCAL_FLORIST, content=tab_especies),
            ft.Tab(text="Pragas", icon=ft.Icons.BUG_REPORT, content=tab_pragas),
        ],
        expand=True,
    )
