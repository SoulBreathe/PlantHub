import flet as ft
from services.database_service import DatabaseService


def DiarioView(page: ft.Page):
    db = DatabaseService()

    # Busca plantas e cria mapa de nomes
    plantas = db.get_all_plantas()
    mapa_nomes = {p.id_planta: p.nome_personalizado for p in plantas}

    # Agrega entradas de todas as plantas
    todas_entradas = []
    for p in plantas:
        entradas = db.get_diario_por_planta(p.id_planta)
        for ent in entradas:
            ent.nome_planta_visual = mapa_nomes.get(ent.id_planta, "-")
            todas_entradas.append(ent)

    todas_entradas.sort(key=lambda x: x.data_registro, reverse=True)

    def criar_card_diario(entrada):
        dia = entrada.data_registro[8:10]
        mes = entrada.data_registro[5:7]
        tem_foto = entrada.caminho_foto is not None

        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12),
            content=ft.Row(
                [
                    # Coluna Data
                    ft.Column(
                        controls=[
                            ft.Text(
                                dia, size=20, weight=ft.FontWeight.BOLD, color="#097A12"
                            ),
                            ft.Text(f"Mês {mes}", size=12, color="grey"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    ft.VerticalDivider(width=15, color="#eeeeee"),
                    # Coluna Conteúdo
                    ft.Column(
                        controls=[
                            ft.Text(
                                entrada.titulo or "Sem título",
                                weight=ft.FontWeight.BOLD,
                                size=16,
                                color="#333333",
                            ),
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.LOCAL_FLORIST, size=14, color="grey"
                                    ),
                                    ft.Text(
                                        getattr(entrada, "nome_planta_visual", "-"),
                                        size=12,
                                        color="grey",
                                    ),
                                    # Ícone condicional se tiver foto
                                    (
                                        ft.Icon(
                                            ft.Icons.PHOTO_CAMERA,
                                            size=14,
                                            color="#097A12",
                                        )
                                        if tem_foto
                                        else ft.Container()
                                    ),
                                ]
                            ),
                            ft.Text(
                                entrada.observacao,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                size=13,
                                color="#444444",
                            ),
                        ],
                        expand=True,
                    ),
                ]
            ),
        )

    # --- Estado Vazio ---
    if not todas_entradas:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.BOOK_OUTLINED, size=64, color="grey"),
                ft.Text("Seu diário está vazio.", size=16, color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    # --- Lista de Registros ---
    return ft.ListView(
        controls=[criar_card_diario(e) for e in todas_entradas],
        spacing=10,
        padding=15,
        expand=True,
    )
