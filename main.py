import screen
import html_server as server
from threading import Thread

port = 5000

def main_screen(page: screen.ft.Page):
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

def main_server():
    server.app.run(port=port)

if __name__ == "__main__":
    server_thread = Thread(target=main_server)
    server_thread.daemon = True
    server_thread.start()

    screen.ft.app(target=main_screen)

    server_thread.join()