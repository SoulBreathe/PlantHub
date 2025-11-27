import flet as ft
from datetime import datetime
from services.database_service import DatabaseService


def AgendaView(page: ft.Page):
    db = DatabaseService()

    def formatar_data(data_iso):
        if not data_iso:
            return ""
        try:
            data_obj = datetime.strptime(data_iso, "%Y-%m-%d")
            return data_obj.strftime("%d/%m/%Y")
        except:
            return data_iso

    # --- Componente Card Tarefa (Com Animação de Colapso) ---
    def criar_card_tarefa(t, atrasada=False):
        cor_borda = "red" if atrasada else "#097A12"
        icone = ft.Icons.WARNING if atrasada else ft.Icons.EVENT
        cor_icone = "red" if atrasada else "#097A12"
        texto_detalhes = f" | {t.detalhes}" if t.detalhes else ""
        titulo_exibicao = t.tipo_tarefa if t.tipo_tarefa else "Tarefa sem tipo"

        card_container = ft.Container(
            padding=10,
            bgcolor="white",
            border_radius=8,
            margin=ft.margin.only(bottom=8),
            border=ft.border.only(left=ft.BorderSide(4, cor_borda)),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            animate_opacity=300,
        )

        def on_concluir(e):
            # Colapso Visual (UI Otimista)
            card_container.height = 0
            card_container.opacity = 0
            card_container.margin = 0
            card_container.padding = 0
            card_container.update()

            try:
                db.marcar_tarefa_realizada(t.id_agenda)
                page.open(
                    ft.SnackBar(ft.Text("Concluída!"), bgcolor="green", duration=1000)
                )
            except Exception as ex:
                # Rollback em caso de erro
                card_container.height = None
                card_container.opacity = 1
                card_container.margin = ft.margin.only(bottom=8)
                card_container.padding = 10
                card_container.update()
                page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

        card_container.content = ft.ListTile(
            leading=ft.Icon(icone, color=cor_icone, size=28),
            title=ft.Text(
                titulo_exibicao, weight=ft.FontWeight.BOLD, color="#333333", size=16
            ),
            subtitle=ft.Text(
                f"{formatar_data(t.data_agendada)}{texto_detalhes}",
                size=12,
                color="grey",
            ),
            trailing=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.EDIT,
                        icon_color="blue",
                        tooltip="Editar",
                        on_click=lambda _: page.go(f"/agenda/editar/{t.id_agenda}"),
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CHECK_BOX_OUTLINE_BLANK,
                        icon_color="grey",
                        tooltip="Concluir",
                        on_click=on_concluir,
                    ),
                ],
                alignment=ft.MainAxisAlignment.END,
                spacing=0,
                width=100,
            ),
        )
        return card_container

    # --- ABA 1: PRÓXIMAS ---
    lista_futura = db.get_agenda_futura()
    if not lista_futura:
        conteudo_futuro = ft.Column(
            [
                ft.Icon(ft.Icons.EVENT_AVAILABLE, size=60, color="#097A12"),
                ft.Text("Tudo em dia!", size=16, color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        conteudo_futuro = ft.ListView(
            controls=[criar_card_tarefa(t, atrasada=False) for t in lista_futura],
            padding=10,
            expand=True,
        )

    # --- ABA 2: ATRASADAS ---
    lista_atrasada = db.get_agenda_atrasada()
    if not lista_atrasada:
        conteudo_atrasado = ft.Column(
            [
                ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=60, color="green"),
                ft.Text("Sem atrasos!", size=16, color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    else:
        conteudo_atrasado = ft.ListView(
            controls=[criar_card_tarefa(t, atrasada=True) for t in lista_atrasada],
            padding=10,
            expand=True,
        )

    # --- ABA 3: DASHBOARD ---
    stats = db.get_estatisticas_agenda()
    total = stats["pendentes"] + stats["atrasadas"] + stats["concluidas"]

    if total == 0:
        conteudo_dashboard = ft.Column(
            [ft.Text("Sem dados.")], alignment=ft.MainAxisAlignment.CENTER
        )
    else:
        secoes = []
        if stats["concluidas"] > 0:
            secoes.append(
                ft.PieChartSection(
                    stats["concluidas"],
                    title=f"{stats['concluidas']}",
                    color="green",
                    radius=50,
                )
            )
        if stats["pendentes"] > 0:
            secoes.append(
                ft.PieChartSection(
                    stats["pendentes"],
                    title=f"{stats['pendentes']}",
                    color="blue",
                    radius=50,
                )
            )
        if stats["atrasadas"] > 0:
            secoes.append(
                ft.PieChartSection(
                    stats["atrasadas"],
                    title=f"{stats['atrasadas']}",
                    color="red",
                    radius=50,
                )
            )

        grafico = ft.PieChart(
            sections=secoes, sections_space=2, center_space_radius=40, expand=True
        )

        legenda = ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(width=15, height=15, bgcolor="green"),
                        ft.Text("Concluídas"),
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(width=15, height=15, bgcolor="blue"),
                        ft.Text("Em dia"),
                    ]
                ),
                ft.Row(
                    [
                        ft.Container(width=15, height=15, bgcolor="red"),
                        ft.Text("Atrasadas"),
                    ]
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        conteudo_dashboard = ft.Container(
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Desempenho", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(content=grafico, height=250),
                    legenda,
                    ft.Divider(),
                    ft.Text(f"Total: {total}", size=16, weight=ft.FontWeight.BOLD),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

    # --- Montagem Final ---
    return ft.Container(
        expand=True,
        content=ft.Tabs(
            selected_index=0,
            indicator_color="#097A12",
            label_color="#097A12",
            unselected_label_color="grey",
            tabs=[
                ft.Tab(text="Próximas", icon=ft.Icons.EVENT, content=conteudo_futuro),
                ft.Tab(
                    text="Atrasadas", icon=ft.Icons.WARNING, content=conteudo_atrasado
                ),
                ft.Tab(
                    text="Relatório",
                    icon=ft.Icons.PIE_CHART,
                    content=conteudo_dashboard,
                ),
            ],
            expand=True,
        ),
    )
