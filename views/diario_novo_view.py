import flet as ft
from datetime import datetime
from services.database_service import DatabaseService
from models.diario import EntradaDiario
from components.card_padrao import CardPremium


def DiarioNovoView(page: ft.Page):
    db = DatabaseService()

    # Carregar plantas para o dropdown
    plantas = db.get_all_plantas()
    opcoes = [
        ft.dropdown.Option(key=str(p.id_planta), text=p.nome_personalizado)
        for p in plantas
    ]

    # --- Elementos da UI ---
    dd_planta = ft.Dropdown(
        label="Qual planta?", options=opcoes, width=300, border_color="#097A12"
    )
    txt_titulo = ft.TextField(
        label="Título (Ex: Primeira folha)", width=300, border_color="#097A12"
    )
    txt_obs = ft.TextField(label="Observação", multiline=True, min_lines=3, width=300)

    # Referências para a foto
    caminho_foto = ft.Ref[str]()
    feedback_foto = ft.Ref[ft.Text]()

    def foto_selecionada(e: ft.FilePickerResultEvent):
        if e.files:
            caminho_foto.current = e.files[0].path
            feedback_foto.current.value = f"Imagem: {e.files[0].name}"
            feedback_foto.current.update()

    picker = ft.FilePicker(on_result=foto_selecionada)
    page.overlay.append(picker)

    # --- Lógica de Salvar ---
    def salvar(e):
        if not dd_planta.value or not txt_titulo.value:
            page.open(
                ft.SnackBar(ft.Text("Planta e Título são obrigatórios!"), bgcolor="red")
            )
            return

        nova = EntradaDiario(
            data_registro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            titulo=txt_titulo.value,
            observacao=txt_obs.value,
            caminho_foto=caminho_foto.current,
            id_planta=int(dd_planta.value),
        )

        try:
            db.add_entrada_diario(nova)
            page.open(ft.SnackBar(ft.Text("Salvo no Diário!"), bgcolor="green"))
            page.go("/diario")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro: {ex}"), bgcolor="red"))

    # Layout do Conteúdo
    conteudo = ft.Column(
        controls=[
            dd_planta,
            txt_titulo,
            txt_obs,
            ft.OutlinedButton(
                text="Anexar Foto",
                icon=ft.Icons.CAMERA_ALT,
                width=300,
                # Filtra apenas imagens para evitar arquivos errados
                on_click=lambda _: picker.pick_files(
                    allow_multiple=False, file_type=ft.FilePickerFileType.IMAGE
                ),
            ),
            ft.Text(ref=feedback_foto, size=12, color="green"),
            ft.Divider(height=10, color="transparent"),
            ft.ElevatedButton(
                text="Salvar Registro",
                on_click=salvar,
                bgcolor="#097A12",
                color="white",
                width=300,
                height=45,
            ),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=CardPremium(title="Novo Registro", content=conteudo, width=400),
        alignment=ft.alignment.center,
        expand=True,
    )
