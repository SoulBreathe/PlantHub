import flet as ft
from services.database_service import DatabaseService
from database.static_content import GUIA_CULTIVO


def EnciclopediaView(page: ft.Page):
    db = DatabaseService()

    especies = db.get_all_especies()
    pragas = db.get_all_pragas()

    # --- POPUP 1: FICHA TÉCNICA ---
    def abrir_detalhes(item, tipo):
        is_praga = tipo == "praga"
        cor_tema = "red" if is_praga else "#097A12"
        icone_titulo = ft.Icons.BUG_REPORT if is_praga else ft.Icons.LOCAL_FLORIST
        titulo_principal = item.nome_comum if is_praga else item.nome_popular
        subtitulo = (
            item.nome_cientifico if hasattr(item, "nome_cientifico") else ""
        ) or ""

        def criar_linha_info(icone, label, valor):
            texto_valor = (
                str(valor) if valor and str(valor).strip() != "" else "Não informado"
            )
            return ft.Container(
                padding=ft.padding.symmetric(vertical=5),
                content=ft.Row(
                    [
                        ft.Container(
                            content=ft.Icon(icone, color="white", size=18),
                            bgcolor=cor_tema,
                            width=40,
                            height=40,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(width=10),
                        ft.Column(
                            [
                                ft.Text(
                                    label,
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                    color="grey",
                                ),
                                ft.Text(
                                    texto_valor,
                                    size=15,
                                    color="#333333",
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
            )

        infos = []
        if is_praga:
            infos.extend(
                [
                    criar_linha_info(ft.Icons.DESCRIPTION, "Descrição", item.descricao),
                    criar_linha_info(ft.Icons.SICK, "Sintomas", item.sintomas),
                    criar_linha_info(ft.Icons.HEALING, "Tratamento", item.tratamento),
                ]
            )
        else:
            infos.extend(
                [
                    criar_linha_info(ft.Icons.WATER_DROP, "Rega", item.instrucoes_rega),
                    criar_linha_info(
                        ft.Icons.WB_SUNNY, "Iluminação", item.necessidade_sol
                    ),
                    criar_linha_info(
                        ft.Icons.CONTENT_CUT, "Poda", item.necessidade_poda
                    ),
                    criar_linha_info(ft.Icons.SCIENCE, "Adubação", item.uso_adubos),
                    criar_linha_info(
                        ft.Icons.CALENDAR_MONTH, "Época", item.epoca_plantio
                    ),
                ]
            )

        img_topo = ft.Container()
        if item.foto_exemplo:
            src = item.foto_exemplo.replace("\\", "/")
            img_topo = ft.Image(
                src=src,
                width=400,
                height=220,
                fit=ft.ImageFit.COVER,
                border_radius=12,
                error_content=ft.Container(bgcolor="#eee", height=200),
            )

        conteudo_popup = ft.Column(
            controls=[
                img_topo,
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Icon(icone_titulo, color=cor_tema, size=32),
                        ft.Column(
                            [
                                ft.Text(
                                    titulo_principal,
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color="#1a1a1a",
                                ),
                                ft.Text(subtitulo, size=14, italic=True, color="grey"),
                            ],
                            spacing=0,
                        ),
                    ]
                ),
                ft.Divider(height=20, color="#eeeeee"),
                ft.Column(controls=infos, spacing=5),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        dlg = ft.AlertDialog(
            content=ft.Container(content=conteudo_popup, width=400, height=620),
            actions=[ft.TextButton("Fechar", on_click=lambda e: page.close(dlg))],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=16),
            bgcolor="white",
        )
        page.open(dlg)

    # --- POPUP 2: GUIA DE CULTIVO ---
    def abrir_popup_guia(titulo, dados):
        icone = dados["icone"]
        cor = dados["cor"]
        texto = dados["texto"]

        conteudo_guia = ft.Column(
            controls=[
                ft.Row(
                    [
                        ft.Icon(icone, color=cor, size=40),
                        ft.Text(
                            titulo, size=24, weight=ft.FontWeight.BOLD, color="#333"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(),
                ft.Text(texto, size=16, color="black", selectable=True, height=None),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        dlg = ft.AlertDialog(
            content=ft.Container(content=conteudo_guia, width=400, height=500),
            actions=[ft.TextButton("Entendi", on_click=lambda e: page.close(dlg))],
            bgcolor="white",
            shape=ft.RoundedRectangleBorder(radius=15),
        )
        page.open(dlg)

    # --- BUILDERS (GRELHA) ---
    def criar_card_base(
        titulo, subtitulo, cor_destaque, icone_padrao, caminho_foto=None, on_click=None
    ):
        altura_imagem = 150

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
                    content=ft.Icon(ft.Icons.BROKEN_IMAGE, color="grey"),
                ),
            )
        else:
            conteudo_topo = ft.Container(
                height=altura_imagem,
                width=float("inf"),
                bgcolor=ft.Colors.with_opacity(0.1, cor_destaque),
                alignment=ft.alignment.center,
                content=ft.Icon(icone_padrao, size=70, color=cor_destaque),
            )

        return ft.Container(
            bgcolor="white",
            border_radius=15,
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            shadow=ft.BoxShadow(
                blur_radius=8, color=ft.Colors.with_opacity(0.15, "black")
            ),
            ink=True,
            on_click=on_click,
            content=ft.Column(
                spacing=0,
                controls=[
                    conteudo_topo,
                    ft.Container(
                        padding=10,
                        expand=True,
                        alignment=ft.alignment.center,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                            controls=[
                                ft.Text(
                                    titulo,
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                    color="#333333",
                                    text_align=ft.TextAlign.CENTER,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Container(
                                    padding=ft.padding.symmetric(
                                        horizontal=12, vertical=4
                                    ),
                                    bgcolor=ft.Colors.with_opacity(0.1, cor_destaque),
                                    border_radius=20,
                                    content=ft.Text(
                                        (
                                            "Ler Guia"
                                            if not subtitulo
                                            else "Ver detalhes +"
                                        ),
                                        size=11,
                                        color=cor_destaque,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def criar_card_item_banco(item, tipo):
        is_praga = tipo == "praga"
        titulo = item.nome_comum if is_praga else item.nome_popular
        cor = "red" if is_praga else "#097A12"
        icone = ft.Icons.BUG_REPORT if is_praga else ft.Icons.LOCAL_FLORIST
        sub = "Praga" if is_praga else "Planta"
        return criar_card_base(
            titulo,
            sub,
            cor,
            icone,
            item.foto_exemplo,
            lambda _: abrir_detalhes(item, tipo),
        )

    # --- GRIDS ---
    def criar_grid_dados(lista, tipo):
        if not lista:
            return ft.Column(
                [
                    ft.Icon(ft.Icons.SEARCH_OFF, size=50, color="grey"),
                    ft.Text("Vazio.", color="grey"),
                ],
                alignment="center",
            )
        return ft.GridView(
            controls=[criar_card_item_banco(item, tipo) for item in lista],
            max_extent=300,
            child_aspect_ratio=0.9,
            spacing=15,
            run_spacing=15,
            padding=15,
        )

    lista_cards_guia = []
    for titulo, dados in GUIA_CULTIVO.items():
        card = criar_card_base(
            titulo=titulo,
            subtitulo=None,
            cor_destaque=dados["cor"],
            icone_padrao=dados["icone"],
            caminho_foto=None,
            on_click=lambda e, t=titulo, d=dados: abrir_popup_guia(t, d),
        )
        lista_cards_guia.append(card)

    grid_guia = ft.GridView(
        controls=lista_cards_guia,
        runs_count=2,
        max_extent=300,
        child_aspect_ratio=0.9,
        spacing=15,
        run_spacing=15,
        padding=15,
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
                content=criar_grid_dados(especies, "planta"),
            ),
            ft.Tab(
                text="Pragas",
                icon=ft.Icons.BUG_REPORT,
                content=criar_grid_dados(pragas, "praga"),
            ),
            ft.Tab(text="Guia", icon=ft.Icons.MENU_BOOK, content=grid_guia),
        ],
        expand=True,
    )
