# import sqlite3

# DBNAME = "films.db"

# def _select(requete, params=None):
#     """ Exécute une requête type select"""
#     with sqlite3.connect(DBNAME) as db:
#         c = db.cursor()
#         if params is None:
#             c.execute(requete)
#         else:
#             c.execute(requete, params)
#         res = c.fetchall()
#     return res


# def get_films_from(id_director):
#     requete = """select film.titre, film.annee
#                         from film
#                         where film.idRealisateur=?
#                         order by film.annee desc"""
#     return _select(requete, params=(id_director,))

# def get_films_by(id_genrefilm):
#     requete = """select film.titre, film.annee
#                         from film
#                         where film.idgenre=?
#                         order by film.annee desc"""
#     return _select(requete, params=(id_genrefilm,))

# def get_films_by_date(id_datefilm):
#     requete = """select film.titre, film.annee
#                         from film
#                         where film.annee=?
#                         order by film.annee desc"""
#     return _select(requete, params=(id_datefilm,))

# def get_actors_by(id_film):
#     requete = """select nom from personne inner join joue on personne.id=joue.idacteur and joue.idfilm = ? order by nom asc"""
#     return _select(requete, params=(id_film,))

# def get_all_films():
#     requete = """select id, film.titre, (SELECT personne.nom FROM personne WHERE film.idRealisateur=personne.id) , film.annee, genre.nom, genre.id, film.idRealisateur
#                 from film inner join genre on film.idGenre=genre.id"""

#     return _select(requete)
