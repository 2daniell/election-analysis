import screen

from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader('template'))
template = environment.get_template('template.html')
#
#################

def main(page: screen.ft.Page):
    page.title = "APE - Analise de Dados"
    page.window.center()
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    page.theme_mode = 'dark'
    page.window.width = 500
    page.window.height = 650
    page.window.maximizable = False
    page.window.resizable = False

    screen.main_screen(page)


if __name__ == "__main__":
    screen.ft.app(target=main)
