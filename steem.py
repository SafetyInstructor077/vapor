from flask import render_template, request, Flask
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


#essayez d'appeler cette route avec par exemple l'URL : http://127.0.0.1:5000/films_de/13848
#13848 est l'id de Charles Chaplin
# @app.route('/films_de/<int:id_real>')
# def films_de(id_real):
#     print(id_real)
#     films = db.get_films_from(id_real)
#     print(films)
#     return render_template("liste_films.html", films=films)

# @app.route('/genre/<int:id_genre>')
# def genre(id_genre):
#     print(id_genre)
#     films = db.get_films_by(id_genre)
#     print(films)
#     return render_template("liste_films.html", films=films)

# @app.route('/date/<int:id_date>')
# def date(id_date):
#     print(id_date)
#     films = db.get_films_by_date(id_date)
#     print(films)
#     return render_template("liste_films.html", films=films)

# @app.route('/actors/<int:id_film>')
# def actor(id_film):
#     print(id_film)
#     actors = db.get_actors_by(id_film)
#     print(actors)
    return render_template("liste_actors.html", actors=actors)




   
if __name__ == "__main__":
    app.run(debug=True)

