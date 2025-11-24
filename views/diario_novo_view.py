import flet as ft
from services.database_service import DatabaseService
from models.diario import EntradaDiario
from datetime import datetime

# Importamos o componente visual padronizado
from components.card_padrao import CardPremium


def DiarioNovoView(page: ft.Page):
    db = DatabaseService()

    # Variáveis de estado
    caminho_foto = ft.Ref[str]()
    texto_feedback_foto = ft.Ref[ft.Text]()

    # Buscar plantas para o Dropdown
    plantas = db.get_all_plantas()
    if not plantas:
        opcoes_plantas = []
    else:
        # Cria as opções: valor=ID, texto=Nome
        opcoes_plantas = [
            ft.dropdown.Option(key=str(p.id_planta), text=p.nome_personalizado)
            for p in plantas
        ]

    # --- Componentes do Formulário ---

    dd_planta = ft.Dropdown(
        label="Qual planta?",
        options=opcoes_plantas,
        width=300,
        border_color="#097A12",
    )

    txt_observacao = ft.TextField(
        label="O que observou hoje?",
        multiline=True,
        min_lines=3,
        max_lines=5,
        width=300,
        border_color="#097A12",
    )

    # Lógica da Foto (FilePicker)
    def ao_selecionar_arquivo(e: ft.FilePickerResultEvent):
        if e.files:
            path = e.files[0].path
            caminho_foto.current = path
            # Mostra apenas o final do nome do arquivo para não ocupar muito espaço
            nome_arquivo = path.split("\\")[-1] if "\\" in path else path.split("/")[-1]
            texto_feedback_foto.current.value = f"Foto: {nome_arquivo}"
            texto_feedback_foto.current.color = "#097A12"
            texto_feedback_foto.current.update()

    file_picker = ft.FilePicker(on_result=ao_selecionar_arquivo)
    page.overlay.append(file_picker)  # Importante adicionar ao overlay da página

    btn_foto = ft.OutlinedButton(
        text="Adicionar Foto",
        icon=ft.Icons.CAMERA_ALT,
        icon_color="#097A12",
        style=ft.ButtonStyle(color="#097A12"),
        width=300,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE
        ),
    )

    # Lógica de Salvar
    def salvar_diario(e):
        if not dd_planta.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Selecione uma planta!"), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        if not txt_observacao.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Escreva uma observação!"), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        nova_entrada = EntradaDiario(
            data_registro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            observacao=txt_observacao.value,
            caminho_foto=caminho_foto.current,  # Pode ser None se não escolheu foto
            id_planta=int(dd_planta.value),
        )

        try:
            db.add_entrada_diario(nova_entrada)
            page.snack_bar = ft.SnackBar(
                ft.Text("Diário salvo com sucesso!"), bgcolor="green"
            )
            page.snack_bar.open = True
            page.go("/diario")  # Redireciona para a lista
        except Exception as ex:
            print(ex)
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro ao salvar: {ex}"), bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    btn_salvar = ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.SAVE, size=20), ft.Text("Salvar Entrada", size=16)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor="#097A12",
        color="white",
        width=300,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        on_click=salvar_diario,
    )

    # --- Montagem usando o CardPremium ---

    conteudo_form = ft.Column(
        controls=[
            dd_planta,
            txt_observacao,
            ft.Divider(height=10, color="transparent"),
            btn_foto,
            ft.Text(ref=texto_feedback_foto, value="", size=12, italic=True),
            ft.Divider(height=20, color="transparent"),
            btn_salvar,
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    card = CardPremium(title="Novo Registro", content=conteudo_form)

    return ft.Column(
        controls=[
            ft.Container(content=card, alignment=ft.alignment.center, expand=True)
        ],
        expand=True,
    )
