import flet as ft
import os
import shutil
import time
from datetime import datetime
from services.database_service import DatabaseService
from models.diario import EntradaDiario
from components.card_padrao import CardPremium


def DiarioNovoView(page: ft.Page):
    db = DatabaseService()

    # Carregar plantas
    plantas = db.get_all_plantas()
    opcoes = [
        ft.dropdown.Option(key=str(p.id_planta), text=p.nome_personalizado)
        for p in plantas
    ]

    # --- UI Elements ---
    dd_planta = ft.Dropdown(
        label="Qual planta?", options=opcoes, width=300, border_color="#097A12"
    )
    txt_titulo = ft.TextField(
        label="Título (Ex: Primeira folha)", width=300, border_color="#097A12"
    )
    txt_obs = ft.TextField(label="Observação", multiline=True, min_lines=3, width=300)

    # Variáveis de estado para a foto
    # 'caminho_origem' guarda onde o arquivo está AGORA (ex: Downloads)
    caminho_origem = ft.Ref[str]()
    feedback_foto = ft.Ref[ft.Text]()

    def foto_selecionada(e: ft.FilePickerResultEvent):
        if e.files:
            # Guardamos o caminho original temporariamente
            caminho_origem.current = e.files[0].path
            feedback_foto.current.value = f"Imagem selecionada: {e.files[0].name}"
            feedback_foto.current.update()

    picker = ft.FilePicker(on_result=foto_selecionada)
    page.overlay.append(picker)

    # --- LÓGICA DE SALVAR E COPIAR ---
    def salvar(e):
        if not dd_planta.value or not txt_titulo.value:
            page.open(
                ft.SnackBar(ft.Text("Planta e Título são obrigatórios!"), bgcolor="red")
            )
            return

        caminho_final_db = None

        # Se o usuário selecionou uma foto, vamos copiá-la!
        if caminho_origem.current:
            try:
                # 1. Definir pasta de destino (dentro do projeto)
                pasta_destino = os.path.join("assets", "uploads")
                os.makedirs(pasta_destino, exist_ok=True)  # Cria a pasta se não existir

                # 2. Gerar nome único (timestamp) para não sobrescrever arquivos
                # Exemplo: foto_17000000.jpg
                extensao = os.path.splitext(caminho_origem.current)[
                    1
                ]  # Pega .jpg ou .png
                novo_nome = f"foto_{int(time.time())}{extensao}"
                destino_completo = os.path.join(pasta_destino, novo_nome)

                # 3. Copiar o arquivo fisicamente
                shutil.copy(caminho_origem.current, destino_completo)

                # 4. Salvar o caminho relativo para o banco
                # (Isso garante que funcione em qualquer PC)
                caminho_final_db = destino_completo

            except Exception as erro_arquivo:
                print(f"Erro ao copiar arquivo: {erro_arquivo}")
                page.open(
                    ft.SnackBar(ft.Text("Erro ao salvar a imagem."), bgcolor="red")
                )
                return

        # Cria o objeto para salvar no banco
        nova = EntradaDiario(
            data_registro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            titulo=txt_titulo.value,
            observacao=txt_obs.value,
            caminho_foto=caminho_final_db,  # Aqui vai o novo caminho em assets/uploads
            id_planta=int(dd_planta.value),
        )

        try:
            db.add_entrada_diario(nova)
            page.open(
                ft.SnackBar(ft.Text("Salvo no Diário com sucesso!"), bgcolor="green")
            )
            page.go("/diario")
        except Exception as ex:
            page.open(ft.SnackBar(ft.Text(f"Erro no banco: {ex}"), bgcolor="red"))

    # --- Layout ---
    conteudo = ft.Column(
        controls=[
            dd_planta,
            txt_titulo,
            txt_obs,
            ft.OutlinedButton(
                text="Anexar Foto",
                icon=ft.Icons.CAMERA_ALT,
                width=300,
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
