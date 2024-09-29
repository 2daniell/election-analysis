from flask import Flask, render_template
import data
import webbrowser
app = Flask(__name__, template_folder='template')

@app.route('/candidatos/<int:id>')
def get(id):
    candidatos = data.filter_sq_candidato(id).to_dict(orient='records')
    url_img = "/static/photos/FPB" + str(id) + "_div.jpg"
    redes = data.filter_media_sq_candidato(id).to_dict(orient='records')
    bens = data.find_bens_value(id)
    return render_template("template.html", candidatos=candidatos, url_img=url_img, redes=redes, bens=bens)
