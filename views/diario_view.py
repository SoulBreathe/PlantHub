import flet as ft
from services.database_service import DatabaseService


# ATENÇÃO AQUI: O nome da função deve ser DiarioView (com D maiúsculo)
def DiarioView(page: ft.Page):
    db = DatabaseService()

    # 1. Buscar todas as plantas (para pegar o nome)
    plantas = db.get_all_plantas()

    # Dicionário auxiliar para achar nome da planta pelo ID rapidamente
    # Ex: {1: "Rosa", 2: "Samambaia"}
    mapa_plantas = {p.id_planta: p.nome_personalizado for p in plantas}

    todas_entradas = []

    # Buscar diários de cada planta
    for planta in plantas:
        entradas = db.get_diario_por_planta(planta.id_planta)
        for ent in entradas:
            # Adicionamos o nome da planta ao objeto entrada dinamicamente
            ent.nome_planta_temp = planta.nome_personalizado
            todas_entradas.append(ent)

    # Ordenar por data (mais recente primeiro)
    todas_entradas.sort(key=lambda x: x.data_registro, reverse=True)

    # 2. Função para criar o Card de cada entrada (Timeline)
    def criar_item_diario(entrada):
        # Ícone muda se tiver foto ou não
        icone = ft.Icons.PHOTO_CAMERA if entrada.caminho_foto else ft.Icons.NOTE
        cor_icone = "#097A12" if entrada.caminho_foto else ft.Colors.GREY_500

        return ft.Container(
            padding=15,
            bgcolor="white",
            border_radius=10,
            shadow=ft.BoxShadow(
                blur_radius=5,
                color=ft.Colors.with_opacity(0.1, "black"),
                offset=ft.Offset(0, 2),
            ),
            content=ft.Row(
                controls=[
                    # Data e Hora (Coluna Esquerda)
                    ft.Column(
                        [
                            ft.Text(
                                entrada.data_registro[8:10],
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#097A12",
                            ),  # Dia
                            ft.Text(
                                entrada.data_registro[5:7], size=12, color="grey"
                            ),  # Mês
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    ft.VerticalDivider(width=1, color="grey"),
                    # Conteúdo (Coluna Direita)
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Icon(icone, size=16, color=cor_icone),
                                    ft.Text(
                                        getattr(entrada, "nome_planta_temp", "Planta"),
                                        weight=ft.FontWeight.BOLD,
                                        size=14,
                                    ),
                                ]
                            ),
                            ft.Text(
                                entrada.observacao,
                                size=14,
                                color="#333333",
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        expand=True,
                        spacing=2,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        )

    # 3. Montar a Lista
    if not todas_entradas:
        conteudo = ft.Column(
            [
                ft.Icon(
                    ft.Icons.AUTO_STORIES_OUTLINED, size=64, color=ft.Colors.GREY_300
                ),
                ft.Text("Seu diário está vazio.", color=ft.Colors.GREY_500),
                ft.Text("Clique no + para adicionar.", color=ft.Colors.GREY_500),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        lista_cards = [criar_item_diario(e) for e in todas_entradas]
        conteudo = ft.ListView(
            controls=lista_cards, expand=True, spacing=10, padding=15
        )

    return ft.Column(controls=[conteudo], expand=True)
