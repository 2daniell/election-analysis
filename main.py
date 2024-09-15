import os
import pandas as pd
import flet as ft

dataFrame = pd.read_csv('data.csv',encoding='latin1', delimiter=';')


#############
### Dados ###
#############

def search(term: str, col: str) -> list:
    results = []
    for index, row in dataFrame.iterrows():
        if isinstance(row[col], str) and row[col].strip().lower() == term.strip().lower():
                results.append(row)
    return results

############
### Tela ###
############

def main_screen(page: ft.Page):
    page.clean()

    title = ft.Text("Data Analiser", theme_style=ft.TextThemeStyle.DISPLAY_LARGE, text_align=ft.TextAlign.CENTER)

    button = ft.ElevatedButton("Ver Dados", width=500, height=70, color=ft.colors.WHITE, on_click=lambda _:filter_screen(page))

    main_colum = ft.Column(controls=[title, button], spacing=50,
                                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                 alignment=ft.MainAxisAlignment.CENTER)

    page.add(main_colum)

def filter_screen(page: ft.Page):
    page.clean()

    a = ft.Text("AAA")
    main_container = ft.Column(controls=[a])

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