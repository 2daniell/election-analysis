import pandas as pd
import flet as ft

from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader('template/template'))

dataFrame = pd.read_csv(
    'data.csv',
    encoding='latin1',
    delimiter=';')

def filter_nm_candidato(nm_candidato):
    results = dataFrame[dataFrame["NM_CANDIDATO"] == nm_candidato]
    return results[['NR_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', "DS_CARGO", "NM_UE", 'NM_PARTIDO', 'SG_PARTIDO']]

def filter_ds_cargo(ds_cargo):
    results = dataFrame[dataFrame["DS_CARGO"] == ds_cargo]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO"]]

def filter_sg_partido(sg_partido):
    results = dataFrame[dataFrame["SG_PARTIDO"] == sg_partido]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO"]]

def filter_nm_ue(nm_ue):
    results = dataFrame[dataFrame["NM_UE"] == nm_ue]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO"]]

############
### Tela ###
############

def main_screen(page: ft.Page):
    page.clean()

    title = ft.Text("Analise de Dados", theme_style=ft.TextThemeStyle.DISPLAY_LARGE, text_align=ft.TextAlign.CENTER)

    button = ft.ElevatedButton("Ver Dados", width=500, height=70, color=ft.colors.WHITE, on_click=lambda _:filter_screen(page))

    main_colum = ft.Column(controls=[title, button], spacing=50,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 alignment=ft.MainAxisAlignment.CENTER)

    page.add(main_colum)

def filter_screen(page: ft.Page):
    page.clean()

    title = ft.Text("Filtro", theme_style=ft.TextThemeStyle.DISPLAY_LARGE, text_align=ft.TextAlign.CENTER)
    text_field = ft.TextField(label="Consulta", width=400, height=60)

    main_container = ft.Column(
        controls=[
            title, text_field
        ],
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(main_container)

#################
### PRINCIPAL ###
#################

def main(page: ft.Page):
    page.title = "APE - Analise de Dados"
    page.window.center()
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.theme_mode = 'dark'
    page.window.width = 500
    page.window.height = 650
    page.window.maximizable = False
    page.window.resizable = False

    main_screen(page)

    print(filter_nm_ue("BAYEUX").to_string())


if __name__ == "__main__":
    ft.app(target=main)
