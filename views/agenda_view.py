import flet as ft
from datetime import datetime
from services.database_service import DatabaseService


def AgendaView(page: ft.Page):
    db = DatabaseService()
    tarefas = db.get_agenda_pendente()

    def formatar_data(data_iso):
        if not data_iso:
            return ""
        try:
            # Converte para dia/mês
            data_obj = datetime.strptime(data_iso, "%Y-%m-%d")
            return data_obj.strftime("%d/%m")
        except:
            return data_iso

    def concluir_tarefa(e, id_agenda):
        try:
            db.marcar_tarefa_realizada(id_agenda)
            page.open(ft.SnackBar(ft.Text("Tarefa concluída!"), bgcolor="green"))
            page.go("/agenda")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    def criar_card_tarefa(t):
        texto_detalhes = f" | {t.detalhes}" if t.detalhes else ""
        data_br = formatar_data(t.data_agendada)

        return ft.Container(
            padding=10,
            bgcolor="white",
            border_radius=8,
            margin=ft.margin.only(bottom=8),
            border=ft.border.only(left=ft.BorderSide(4, "#097A12")),
            shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.BLACK12),
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.EVENT_NOTE, color="#097A12", size=28),
                title=ft.Text(
                    t.tipo_tarefa, weight=ft.FontWeight.BOLD, color="#333333"
                ),
                # Data formatada no subtítulo 👇
                subtitle=ft.Text(f"{data_br}{texto_detalhes}", size=12, color="grey"),
                trailing=ft.IconButton(
                    icon=ft.Icons.CHECK_BOX_OUTLINE_BLANK,
                    icon_color="grey",
                    tooltip="Marcar como concluída",
                    on_click=lambda e: concluir_tarefa(e, t.id_agenda),
                ),
            ),
        )

    if not tarefas:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.EVENT_AVAILABLE, size=64, color="#097A12"),
                ft.Text(
                    "Tudo em dia!", size=18, weight=ft.FontWeight.BOLD, color="#333333"
                ),
                ft.Text("Nenhuma tarefa pendente.", size=14, color="grey"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    return ft.ListView(
        controls=[criar_card_tarefa(t) for t in tarefas],
        padding=15,
        expand=True,
    )
