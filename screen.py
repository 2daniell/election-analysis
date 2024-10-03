import data
import flet as ft
import html_server as server
from main import port

initial_results_amount = 100

def main_screen(page: ft.Page):
    page.clean()

    title = ft.Text("Analise de Dados", theme_style=ft.TextThemeStyle.DISPLAY_LARGE, text_align=ft.TextAlign.CENTER)

    button = ft.ElevatedButton("Candidados", width=500, height=70, color=ft.colors.WHITE, on_click=lambda _:filter_screen(page))

    mnc_button = ft.ElevatedButton("Municipios", width=500, height=70, color=ft.colors.WHITE, on_click=lambda _:municipio_screen(page))

    stc_button = ft.ElevatedButton("Estatisticas", width=500, height=70, color=ft.colors.WHITE,
                                   on_click=lambda _:alert_confirm())

    main_colum = ft.Column(controls=[title, ft.Column(
        controls=[button, mnc_button, stc_button],
        spacing=15
    )],
                           spacing=50,
                           horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                           alignment=ft.MainAxisAlignment.CENTER)

    def alert_confirm():

        def handle_accept(e):
            server.open_browser_url("http://127.0.0.1:" + str(port) + "/statistics")
            page.close(dlg)

        def handle_close(e):
            page.close(dlg)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Deseja acessar pagina html?"),
            actions = [
                ft.TextButton("Sim", on_click=handle_accept),
                ft.TextButton("Não", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.open(dlg)

    page.add(main_colum)

def municipio_screen(page: ft.Page):
    page.clean()

    title = ft.Text("Filtro", theme_style=ft.TextThemeStyle.DISPLAY_LARGE, text_align=ft.TextAlign.CENTER)
    text_field = ft.TextField(label="Consulta", width=400, height=60)

    sub_container = ft.Column(
        controls=[text_field],
        spacing=0,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER
    )

    def alert_confirm(code):

        def handle_accept(e):
            server.open_browser_url("http://127.0.0.1:" + str(port) + "/municipio/" + code)
            page.close(dlg)

        def handle_close(e):
            page.close(dlg)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Deseja acessar pagina html?"),
            actions = [
                ft.TextButton("Sim", on_click=handle_accept),
                ft.TextButton("Não", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.open(dlg)

    def format_results(iterrows):
        results = []
        for _, row in iterrows:
            card = ft.Card(
                content=ft.Container(
                    on_click= lambda _: alert_confirm(int(row['SQ_UE'])),
                    content=ft.Column([

                        ft.ListTile(
                            title=ft.Text(str(row['NM_UE']).strip().title(), text_align=ft.TextAlign.CENTER,
                                          weight=ft.FontWeight.BOLD)
                        )

                    ]),
                    padding=ft.Padding(left=10, top=10, right=10, bottom=10),
                )
            )

            results.append(card)
        return results

    search_button = ft.ElevatedButton("Buscar", width=300, height=60)

    results_listview = ft.ListView(
        controls=format_results(data.municipio_results().iterrows()),
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
                results_list = data.filter_nr_candidato(typed)
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
                results_list = data.filter_nm_candidato(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Nome do Partido"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                text_align=ft.TextAlign.CENTER,
                                color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = data.filter_nm_partido(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Sigla do Partido"):
            typed = typed.upper()
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = data.filter_sg_partido(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Municipio"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = data.filter_nm_ue(typed.strip().upper())
                show_results(results_list)

        elif (parameter == "Cargo"):
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = data.filter_ds_cargo(typed.strip().upper())
                show_results(results_list)
        else:
            if not (typed):
                results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                     text_align=ft.TextAlign.CENTER,
                                                     color=ft.colors.ERROR)]
                page.update()
            else:
                results_list = data.filter_nm_urna_candidato(typed.strip().upper())
                show_results(results_list)

    def is_valid():
        if (drop_down.value):
            filter()
        else:
            results_listview.controls = [ft.Text("Não foi possivel realizar buscar", weight=ft.FontWeight.BOLD,
                                                 text_align=ft.TextAlign.CENTER,
                                                 color=ft.colors.ERROR)]
            page.update()


    def alert_confirm(code):

        def handle_accept(e):
            server.open_browser(code)
            page.close(dlg)

        def handle_close(e):
            page.close(dlg)

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Deseja acessar pagina html?"),
            actions = [
                ft.TextButton("Sim", on_click=handle_accept),
                ft.TextButton("Não", on_click=handle_close),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )

        page.open(dlg)


    def format_results(iterrows):
        results = []
        for _, row in iterrows:
            card = ft.Card(
                content=ft.Container(
                    on_click=lambda e, code=int(row['SQ_CANDIDATO']):alert_confirm(code),
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
                                ft.Text(f"{str(row['NM_PARTIDO']).title()} ({str(row['SG_PARTIDO']).upper()})")
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
        controls=format_results(data.results_initial(initial_results_amount).iterrows()),
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
