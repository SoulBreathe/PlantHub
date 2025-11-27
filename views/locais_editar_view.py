import flet as ft
from services.database_service import DatabaseService
from models.local import Local
from components.card_padrao import CardPremium


def LocaisEditarView(page: ft.Page):
    db = DatabaseService()

    # 1. Pegar ID da rota
    try:
        id_local = int(page.route.split("/")[-1])
        local_atual = db.get_local_por_id(id_local)
    except:
        local_atual = None

    if not local_atual:
        return ft.Column(
            [
                ft.Text("Local não encontrado."),
                ft.ElevatedButton("Voltar", on_click=lambda _: page.go("/locais")),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    # 2. Campos da UI
    txt_nome = ft.TextField(
        label="Nome", value=local_atual.nome, width=300, border_color="#097A12"
    )

    dd_tipo = ft.Dropdown(
        label="Tipo",
        width=300,
        border_color="#097A12",
        value=local_atual.tipo,
        options=[
            ft.dropdown.Option("Estufa"),
            ft.dropdown.Option("Horta"),
            ft.dropdown.Option("Jardim"),
            ft.dropdown.Option("Varanda"),
            ft.dropdown.Option("Interno"),
        ],
    )

    txt_area = ft.TextField(
        label="Área (m²)",
        value=str(local_atual.area_m2),
        width=300,
        border_color="#097A12",
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    txt_desc = ft.TextField(
        label="Descrição",
        value=local_atual.descricao,
        multiline=True,
        max_lines=3,
        width=300,
    )

    # --- AÇÃO: SALVAR ---
    def salvar(e):
        if not txt_nome.value:
            page.open(ft.SnackBar(ft.Text("Nome é obrigatório!"), bgcolor="red"))
            return

        local_atual.nome = txt_nome.value
        local_atual.tipo = dd_tipo.value or "Outro"
        local_atual.descricao = txt_desc.value
        try:
            local_atual.area_m2 = float(txt_area.value) if txt_area.value else 0.0
            db.update_local(local_atual)
            page.open(ft.SnackBar(ft.Text("Local atualizado!"), bgcolor="green"))
            page.go("/locais")
        except ValueError:
            page.open(ft.SnackBar(ft.Text("Área inválida."), bgcolor="red"))
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # --- AÇÃO: EXCLUIR (COM MIGRAÇÃO) ---
    def executar_exclusao(e):
        try:
            db.migrar_e_excluir_local(id_local)
            page.open(
                ft.SnackBar(ft.Text("Local excluído com sucesso."), bgcolor="green")
            )
            page.go("/locais")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # Diálogos de Confirmação
    dlg_simples = ft.AlertDialog(
        title=ft.Text("Excluir Local?"),
        content=ft.Text("Não há plantas aqui. O local será apagado."),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda _: page.close(dlg_simples)),
            ft.TextButton(
                "Excluir", style=ft.ButtonStyle(color="red"), on_click=executar_exclusao
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def abrir_confirmacao(e):
        qtd_plantas = db.count_plantas_no_local(id_local)

        if qtd_plantas > 0:
            dlg_migracao = ft.AlertDialog(
                title=ft.Text("Atenção!"),
                content=ft.Column(
                    [
                        ft.Text(f"Existem {qtd_plantas} plantas neste local."),
                        ft.Text(
                            "Se excluir, elas serão movidas para 'Sem Local'.",
                            weight=ft.FontWeight.BOLD,
                            color="orange",
                        ),
                        ft.Text("Deseja continuar?"),
                    ],
                    tight=True,
                ),
                actions=[
                    ft.TextButton(
                        "Cancelar", on_click=lambda _: page.close(dlg_migracao)
                    ),
                    ft.TextButton(
                        "Mover e Excluir",
                        style=ft.ButtonStyle(color="red"),
                        on_click=executar_exclusao,
                    ),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.open(dlg_migracao)
        else:
            page.open(dlg_simples)

    # Layout
    conteudo = ft.Column(
        [
            txt_nome,
            dd_tipo,
            txt_area,
            txt_desc,
            ft.Divider(height=10, color="transparent"),
            ft.ElevatedButton(
                "Salvar Alterações",
                on_click=salvar,
                bgcolor="#097A12",
                color="white",
                width=300,
                height=45,
            ),
            ft.TextButton(
                "Excluir Local",
                icon=ft.Icons.DELETE,
                icon_color="red",
                style=ft.ButtonStyle(color="red"),
                on_click=abrir_confirmacao,
            ),
        ],
        spacing=15,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=CardPremium(title="Editar Local", content=conteudo, width=350),
        alignment=ft.alignment.center,
        expand=True,
    )
