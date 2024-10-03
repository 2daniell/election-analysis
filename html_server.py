import data
import webbrowser
from flask import Flask, render_template
from main import port
app = Flask(__name__, template_folder='template')


@app.route('/candidatos/<int:id>')
def index(id):
    candidatos = data.filter_sq_candidato(id).to_dict(orient='records')
    url_img = "https://raw.githubusercontent.com/davicesarmorais/fotos-candidatos-pb/refs/heads/main/fotos-candidatos-pb/FPB" + str(id) + "_div.jpg"
    redes = data.filter_media_sq_candidato(id).to_dict(orient='records')
    bens = data.find_bens_value(id)
    return render_template("template.html", candidatos=candidatos, url_img=url_img, redes=redes, bens=bens)

@app.route('/statistics')
def statistics():
    return render_template("statistics.html", statistics=data.get_statistics(), partidos=data.get_partidos_prefeito())

@app.route('/municipio/<int:id>')
def municipio():
    return "OI"


def open_browser(id):
    url = "http://127.0.0.1:" + str(port) + "/candidatos/" + str(id)
    webbrowser.open(url, new=True)

def open_browser_url(url):
    webbrowser.open(url, new=True)
