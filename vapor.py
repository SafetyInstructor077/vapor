from flask import render_template, request, Flask
import database as db

app = Flask(__name__)

@app.route('/')
def store():
    jeux = db.get_featured()
    return render_template("store.html", jeux=jeux)

@app.route('/jeu/<int:idJeu>')
def jeu(idJeu):
    print(idJeu)
    jeu = db.get_jeu_by_id(idJeu)
    return render_template("all_games.html", jeux=jeu)

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

@app.route('/insertion')
def insert_page():
    return render_template("insert.html")

if __name__ == "__main__":
    app.run(debug=True)

