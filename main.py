import pandas as pd
import flet as ft

from jinja2 import Environment, FileSystemLoader

initial_results_amount = 100

environment = Environment(loader=FileSystemLoader('template'))
template = environment.get_template('template.html')

dataFrame = pd.read_csv(
    'data.csv',
    encoding='latin1',
    delimiter=';')

def filter_nm_candidato(nm_candidato):
    results = dataFrame[dataFrame["NM_CANDIDATO"].str.contains(nm_candidato, case=False, na=False)]
    return results[['NR_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', "DS_CARGO", "NM_UE", 'NM_PARTIDO', 'SG_PARTIDO', 'SQ_CANDIDATO']]

def filter_nm_urna_candidato(nm_urna_candidato):
    results = dataFrame[dataFrame["NM_URNA_CANDIDATO"].str.contains(nm_urna_candidato, case=False, na=False)]
    return results[['NR_CANDIDATO', 'NM_CANDIDATO', 'NM_URNA_CANDIDATO', "DS_CARGO", "NM_UE", 'NM_PARTIDO', 'SG_PARTIDO', 'SQ_CANDIDATO']]

def filter_ds_cargo(ds_cargo):
    results = dataFrame[dataFrame["DS_CARGO"].str.contains(ds_cargo, case=False, na=False)]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_sg_partido(sg_partido):
    results = dataFrame[dataFrame["SG_PARTIDO"] == sg_partido]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nm_partido(nm_partido):
    results = dataFrame[dataFrame["NM_PARTIDO"].str.contains(nm_partido, case=False, na=False)]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nr_candidato(nr_candidato):
    results = dataFrame[dataFrame["NR_CANDIDATO"] == nr_candidato]
    return results[["NR_CANDIDATO", "NM_CANDIDATO", "NM_URNA_CANDIDATO", "DS_CARGO", "NM_UE", "NM_PARTIDO", "SG_PARTIDO", "SQ_CANDIDATO"]]

def filter_nm_ue(nm_ue):
    results = dataFrame[dataFrame["NM_UE"].str.contains(nm_ue, case=False, na=False)]
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

    def show_results(results):
        if not (results.empty):
            results_listview.controls = format_results(results.iterrows())
            page.update()
        else:
            results_listview.controls = [ft.ListTile(title=ft.Text("Nada encontrado na busca.", weight=ft.FontWeight.BOLD,
                                                color=ft.colors.ERROR, text_align=ft.TextAlign.CENTER))]
        page.update()

    def filter():
        page.update()

        parameter = drop_down.value
        typed = text_field.value

        if parameter == "Numero do Candidato":
            try:
                typed = int(typed)
                results_list = filter_nr_candidato(typed)
                show_results(results_list)
            except ValueError:
                results_listview.controls = [
                    ft.Text("O valor inserido deve ser um numero inteiro.",
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.ERROR)
                ]
                page.update()

        elif (parameter == "Nome do Candidato"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = filter_nm_candidato(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Nome do Partido"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = filter_nm_partido(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Sigla do Partido"):
            typed = typed.upper()
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = filter_sg_partido(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Municipio"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = filter_nm_ue(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Cargo"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = filter_ds_cargo(typed.strip().upper())
                show_results(results_list)
        else:
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = filter_nm_urna_candidato(typed.strip().upper())
                show_results(results_list)

    def is_valid():
        if (drop_down.value):
            filter()
        else:
            results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                 text_align=ft.TextAlign.CENTER,
                                                 color=ft.colors.ERROR)]
            page.update()


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

    search_button = ft.ElevatedButton("Buscar", width=300, height=60,
                                      on_click=lambda _:is_valid())

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
