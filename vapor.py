from flask import render_template, request, Flask
import database as db

app = Flask(__name__)

@app.route('/')
def store():
    jeux = db.get_featured()
    print(jeux)
    return render_template("store.html", jeux=jeux)

@app.route('/library')
def library():
    jeux = db.get_all_jeux()
    print(jeux)
    return render_template("list_games.html", jeux=jeux)

@app.route('/jeu/<int:idJeu>')
def jeu(idJeu):
    print(idJeu)
    jeu = db.get_jeu_by_id(idJeu)
    return render_template("game.html", jeu=jeu)

@app.route('/platforme/<int:idPlat>')
def platforme(idPlat):
    jeux = db.get_jeux_by_plat(idPlat)
    return render_template("list_games.html", jeux=jeux)

@app.route('/admin.<table>')
def admin(table):
    print("admin : ", table)
    jeux = db.get_admin(table)
    colonnes = db.get_columns(table)
    return render_template("admin.html", jeux=jeux, colonnes=colonnes)

@app.route('/admin.<table>/<parametre>.<valeur>')
def admin_param(table,parametre,valeur):
    print(f"admin : {table}, {parametre} : {valeur}")
    jeux = db.get_admin_param(table,parametre,valeur)
    colonnes = db.get_columns(table)
    return render_template("admin.html", jeux=jeux, colonnes=colonnes)

@app.route('/insert')
def insert_page():
    platformes = db.get_admin("platformes")
    return render_template("insert.html", platformes=platformes)

@app.route('/insertion', methods=["POST"])
def insert_form():
    if request.method == 'POST':
        jeu = request.form
        print(jeu)

if __name__ == "__main__":
    app.run(debug=True)
