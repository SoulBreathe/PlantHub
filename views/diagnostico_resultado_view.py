import flet as ft
from services.database_service import DatabaseService


def DiagnosticoResultadoView(page: ft.Page):
    db = DatabaseService()
    praga = None

    # Tenta extrair o ID da rota e buscar a praga correspondente
    try:
        id_praga = int(page.route.split("/")[-1])
        # Filtra na lista (solução temporária enquanto não temos get_by_id no service)
        todas = db.get_all_pragas()
        praga = next((p for p in todas if p.id_praga == id_praga), None)
    except (ValueError, IndexError):
        pass

    # --- Tela de Erro (Caso ID inválido ou não encontrado) ---
    if not praga:
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color="red"),
                ft.Text("Resultado não encontrado.", size=18, color="grey"),
                ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/diagnostico")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    # --- Tela de Sucesso (Resultado) ---
    return ft.Column(
        controls=[
            ft.Icon(ft.Icons.MEDICAL_SERVICES_OUTLINED, color="#097A12", size=60),
            ft.Text("Diagnóstico Identificado", size=14, color="grey"),
            ft.Text(
                praga.nome_comum, size=26, weight=ft.FontWeight.BOLD, color="#333333"
            ),
            ft.Container(height=20),
            # Card com Detalhes
            ft.Container(
                padding=20,
                bgcolor="white",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
                width=350,  # Largura fixa para ficar elegante
                content=ft.Column(
                    controls=[
                        ft.Text("Sintomas:", weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(
                            praga.sintomas or "Não informados.",
                            size=14,
                            color="#555555",
                        ),
                        ft.Divider(height=20, color="#eeeeee"),
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.HEALING, size=18, color="#097A12"),
                                ft.Text(
                                    "Tratamento:",
                                    weight=ft.FontWeight.BOLD,
                                    size=14,
                                    color="#097A12",
                                ),
                            ]
                        ),
                        ft.Text(
                            praga.tratamento or "Consulte um especialista.",
                            size=15,
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                    spacing=5,
                ),
            ),
            ft.Container(height=30),
            ft.ElevatedButton(
                text="Concluir Diagnóstico",
                bgcolor="#097A12",
                color="white",
                height=45,
                width=200,
                on_click=lambda _: page.go("/diagnostico"),
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=20,
        scroll=ft.ScrollMode.AUTO,  # Importante caso o texto do tratamento seja longo
        expand=True,
    )
