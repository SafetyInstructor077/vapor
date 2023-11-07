from flask import render_template, request, Flask
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    jeux = db.get_all_jeux()
    return render_template("all_games.html", jeux=jeux)

@app.route('/jeu/<int:idJeu>')
def jeu(idJeu):
    print(idJeu)
    jeu = db.get_jeu_by_id(idJeu)
    return render_template("all_games.html", jeux=jeu)

@app.route('/films_genre/<int:id_genre>')
def films_genre(id_genre):
    print(id_genre)
    films = db.get_films_by_genre(id_genre)
    print(films)
    return render_template("liste_films.html", films=films)

@app.route('/films_annee/<int:annee>')
def films_annee(annee):
    print(annee)
    films = db.get_films_by_annee(annee)
    print(films)
    return render_template("liste_films.html", films=films)

@app.route('/acteurs_film/<int:idFilm>')
def acteurs_film(idFilm):
    print(idFilm)
    films = db.get_acteurs_by_idFilm(idFilm)
    print(films)
    return render_template("liste_acteurs.html", films=films)
   
if __name__ == "__main__":
    app.run()

