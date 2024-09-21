from re import search

import pandas as pd
import flet as ft

from jinja2 import Environment, FileSystemLoader

initial_results_amount = 100;

environment = Environment(loader=FileSystemLoader('template'))
template = environment.get_template('template.html')

dataFrame = pd.read_csv(
    'data.csv',
    encoding='latin1',
    delimiter=';')

def filter_nm_candidato(nm_candidato):
    results = dataFrame[dataFrame["NM_CANDIDATO"] == nm_candidato]
    return results[['NR_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', "DS_CARGO", "NM_UE", 'NM_PARTIDO', 'SG_PARTIDO', 'SQ_CANDIDATO']]

def filter_ds_cargo(ds_cargo):
    results = dataFrame[dataFrame["DS_CARGO"] == ds_cargo]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_sg_partido(sg_partido):
    results = dataFrame[dataFrame["SG_PARTIDO"] == sg_partido]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nm_ue(nm_ue):
    results = dataFrame[dataFrame["NM_UE"] == nm_ue]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def results_initial(number):
    return dataFrame.head(number)[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

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
    drop_down = ft.Dropdown(width=400,
                            options=[
                                ft.dropdown.Option("Numero do Candidato"),
                                ft.dropdown.Option("Nome do Candidato"),
                                ft.dropdown.Option("Nome do Candidato na Urna"),
                                ft.dropdown.Option("Nome do Partido"),
                                ft.dropdown.Option("Sigla do Partido"),
                                ft.dropdown.Option("Municipio"),
                                ft.dropdown.Option("Cargo")
                            ],
                            hint_text="Parâmetro de Busca")



    sub_container = ft.Column(
        controls=[text_field, drop_down],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    def filter(e):
        results_list = []

    def format_results(iterrows):
        results = []
        for _, row in iterrows:
            card = ft.Card(
                content=ft.Container(
                    on_click=lambda e, code=int(row['SQ_CANDIDATO']):print(code),
                    content=ft.Column([

                        ft.ListTile(
                            title=ft.Text(str(row['NM_CANDIDATO']).strip().title(), text_align=ft.TextAlign.CENTER,
                                          weight=ft.FontWeight.BOLD)
                        ),

                        ft.Divider(),

                        ft.Row(
                            controls=[
                                ft.Text("Nome na Urna: ", weight=ft.FontWeight.BOLD),
                                ft.Text(str(row['NM_URNA_CANDIDATO']).title())
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),

                        ft.Row(
                            controls=[
                                ft.Text("Número do Candidato: ", weight=ft.FontWeight.BOLD),
                                ft.Text(str(row['NR_CANDIDATO']))
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),

                        ft.Row(
                            controls=[
                                ft.Text("Cargo: ", weight=ft.FontWeight.BOLD),
                                ft.Text(str(row['DS_CARGO']).capitalize())
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),

                        ft.Row(
                            controls=[
                                ft.Text("Municipio: ", weight=ft.FontWeight.BOLD),
                                ft.Text(str(row['NM_UE']).title())
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),

                        ft.Row(
                            controls=[
                                ft.Text("Partido do Candidato: ", weight=ft.FontWeight.BOLD),
                                ft.Text("".join(f'{str(row['NM_PARTIDO']).title()} ({str(row['SG_PARTIDO']).upper()})'))
                            ],
                            alignment=ft.MainAxisAlignment.START
                        ),
                    ]),
                    padding=ft.Padding(left=10, top=10, right=10, bottom=10),
                )
            )

            results.append(card)
        return results

    search_button = ft.ElevatedButton("Buscar", width=300, height=60)

    results_listview = ft.ListView(
        controls=format_results(results_initial(initial_results_amount).iterrows()),
        visible=True,
        expand=True,
        height=300,
        auto_scroll=False
    )

    main_container = ft.Column(
        controls=[
            title, sub_container, search_button, results_listview
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


if __name__ == "__main__":
    ft.app(target=main)
