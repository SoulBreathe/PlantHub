import flet as ft
from services.database_service import DatabaseService


def EnciclopediaView(page: ft.Page):
    db = DatabaseService()

    especies = db.get_all_especies()
    pragas = db.get_all_pragas()

    # =========================================================================
    #  POPUP: FICHA TÉCNICA DETALHADA
    # =========================================================================
    def abrir_detalhes(item, tipo):
        is_praga = tipo == "praga"

        cor_tema = "red" if is_praga else "#097A12"
        icone_titulo = ft.Icons.BUG_REPORT if is_praga else ft.Icons.LOCAL_FLORIST
        titulo_principal = item.nome_comum if is_praga else item.nome_popular
        # Garante que subtítulo nunca é None
        subtitulo = (
            item.nome_cientifico if hasattr(item, "nome_cientifico") else ""
        ) or ""

        # Função auxiliar para criar linhas de informação seguras
        def criar_linha_info(icone, label, valor):
            texto_valor = (
                valor if valor and str(valor).strip() != "" else "Não informado"
            )

            return ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icone, color="white", size=18),
                        bgcolor=cor_tema,
                        padding=8,
                        border_radius=8,
                        width=40,
                        height=40,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                label, size=11, weight=ft.FontWeight.BOLD, color="grey"
                            ),
                            ft.Text(
                                texto_valor,
                                size=14,
                                color="#333",
                                weight=ft.FontWeight.W_500,
                            ),
                        ],
                        spacing=2,
                        expand=True,
                    ),  # Expand garante que o texto não corte
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

        infos = []
        if is_praga:
            infos.extend(
                [
                    criar_linha_info(ft.Icons.DESCRIPTION, "Descrição", item.descricao),
                    ft.Divider(height=15, color="#f0f0f0"),
                    criar_linha_info(ft.Icons.SICK, "Sintomas", item.sintomas),
                    ft.Divider(height=15, color="#f0f0f0"),
                    criar_linha_info(ft.Icons.HEALING, "Tratamento", item.tratamento),
                ]
            )
        else:
            infos.extend(
                [
                    criar_linha_info(ft.Icons.WATER_DROP, "Rega", item.instrucoes_rega),
                    ft.Divider(height=15, color="#f0f0f0"),
                    criar_linha_info(
                        ft.Icons.WB_SUNNY, "Iluminação", item.necessidade_sol
                    ),
                    ft.Divider(height=15, color="#f0f0f0"),
                    criar_linha_info(
                        ft.Icons.CONTENT_CUT, "Poda", item.necessidade_poda
                    ),
                    ft.Divider(height=15, color="#f0f0f0"),
                    criar_linha_info(ft.Icons.SCIENCE, "Adubação", item.uso_adubos),
                    ft.Divider(height=15, color="#f0f0f0"),
                    criar_linha_info(
                        ft.Icons.CALENDAR_MONTH, "Época", item.epoca_plantio
                    ),
                ]
            )

        # Imagem do Popup
        img_topo = ft.Container()
        if item.foto_exemplo:
            src = item.foto_exemplo.replace("\\", "/")
            img_topo = ft.Image(
                src=src,
                width=400,
                height=220,
                fit=ft.ImageFit.COVER,
                border_radius=12,
                error_content=ft.Container(bgcolor="#eee", height=220),
            )

        conteudo_popup = ft.Column(
            controls=[
                img_topo,
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Icon(icone_titulo, color=cor_tema, size=30),
                        ft.Column(
                            [
                                ft.Text(
                                    titulo_principal,
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="#333",
                                ),
                                ft.Text(subtitulo, size=14, italic=True, color="grey"),
                            ],
                            spacing=0,
                        ),
                    ]
                ),
                ft.Divider(height=20, color="grey"),
                ft.Column(controls=infos, spacing=5),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        dlg = ft.AlertDialog(
            content=ft.Container(content=conteudo_popup, width=400, height=600),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.close(dlg))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        page.open(dlg)

    # =========================================================================
    #  GRID CARD (300x300) - Imagem 200px
    # =========================================================================
    def criar_card_grade(item, tipo="planta"):
        is_praga = tipo == "praga"

        titulo = item.nome_comum if is_praga else item.nome_popular
        cor_destaque = "red" if is_praga else "#097A12"
        icone_padrao = ft.Icons.BUG_REPORT if is_praga else ft.Icons.LOCAL_FLORIST
        caminho_foto = item.foto_exemplo

        # Configuração da Imagem (200px de altura)
        altura_imagem = 200

        if caminho_foto:
            src = caminho_foto.replace("\\", "/")
            conteudo_topo = ft.Image(
                src=src,
                width=float("inf"),
                height=altura_imagem,
                fit=ft.ImageFit.COVER,
                error_content=ft.Container(
                    bgcolor=ft.Colors.GREY_200,
                    alignment=ft.alignment.center,
                    content=ft.Icon(ft.Icons.BROKEN_IMAGE, color="grey", size=40),
                ),
            )
        else:
            conteudo_topo = ft.Container(
                height=altura_imagem,
                width=float("inf"),
                bgcolor=ft.Colors.with_opacity(0.1, cor_destaque),
                alignment=ft.alignment.center,
                content=ft.Icon(icone_padrao, size=80, color=cor_destaque),
            )

        return ft.Container(
            bgcolor="white",
            border_radius=15,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=8, color=ft.Colors.with_opacity(0.15, "black")
            ),
            ink=True,
            on_click=lambda _: abrir_detalhes(item, tipo),
            content=ft.Column(
                spacing=0,
                controls=[
                    # 1. Imagem (200px)
                    conteudo_topo,
                    # 2. Conteúdo (Restante dos 300px)
                    ft.Container(
                        padding=12,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            [
                                ft.Text(
                                    titulo,
                                    weight=ft.FontWeight.BOLD,
                                    size=18,
                                    color="#333",
                                    text_align=ft.TextAlign.CENTER,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Container(
                                    padding=ft.padding.symmetric(
                                        horizontal=10, vertical=4
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.1, cor_destaque),
                                    border_radius=20,
                                    content=ft.Text(
                                        "Ver detalhes +",
                                        size=11,
                                        color=cor_destaque,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ),
                            ],
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                ],
            ),
        )

    # --- CONFIGURAÇÃO DO GRID ---
    # Para ter cards de aprox 300x300, ajustamos o max_extent e o aspect_ratio

    def criar_grid(lista, tipo):
        if not lista:
            return ft.Column(
                [
                    ft.Icon(ft.Icons.SEARCH_OFF, size=50, color="grey"),
                    ft.Text("Vazio.", color="grey"),
                ],
                alignment="center",
            )

        return ft.GridView(
            controls=[criar_card_grade(item, tipo) for item in lista],
            max_extent=300,  # Largura máxima de cada card
            child_aspect_ratio=0.9,  # Relação Largura/Altura (ajuste fino para chegar nos 300x300 visuais)
            spacing=20,
            run_spacing=20,
            padding=20,
        )

    return ft.Tabs(
        selected_index=0,
        indicator_color="#097A12",
        label_color="#097A12",
        unselected_label_color="grey",
        tabs=[
            ft.Tab(
                text="Espécies",
                icon=ft.Icons.LOCAL_FLORIST,
                content=criar_grid(especies, "planta"),
            ),
            ft.Tab(
                text="Pragas",
                icon=ft.Icons.BUG_REPORT,
                content=criar_grid(pragas, "praga"),
            ),
        ],
        expand=True,
    )
