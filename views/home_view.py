import flet as ft 

def HomeView(page: ft.Page, theme_changed) -> ft.View:
   
   return ft.View(
      route="/",
      appbar=ft.AppBar(
          title=ft.Text("PlantHub"), 
          actions=[
             ft.IconButton(
                icon=ft.Icons.BRIGHTNESS_4_OUTLINED,
                tooltip="Mudar Tema",
                on_click=theme_changed
             )
          ]
      ),
      controls=[
         ft.Text("Bem-vindo ao seu assistente de jardinagem!", size=20)
      ],
      vertical_alignment=ft.MainAxisAlignment.CENTER,
      horizontal_alignment=ft.CrossAxisAlignment.CENTER
   )