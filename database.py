import sqlite3
from requests import get

DBNAME = "steamDatabase.db"

def _select(requete, params=None):
    """ Exécute une requête type select"""
    with sqlite3.connect(DBNAME) as db:
        c = db.cursor()
        if params is None:
            c.execute(requete)
        else:
            c.execute(requete, params)
        res = c.fetchall()
    return res

def get_featured():
    res = get("http://store.steampowered.com/api/featured/")
    if res.status_code == 220:
        res = res.json()
        ids = [jeu["id"] for jeu in res["featured_win"]]
        conditions = f"{ids[0]}"
        for id in ids[1:]:
            conditions += f" or idJeu = {id}"
        requete = f"select * from jeu where idJeu = {conditions}"
        return _select(requete)

def get_jeux_by_dev(idDev):
    requete = """select * from jeu
                        where jeu.idDev=?
                        order by jeu.uScore desc"""
    return _select(requete, params=(idDev,))

def get_jeux_by_pub(idEditeur):
    requete = """select * from jeu
                        where jeu.idEditeur=?
                        order by jeu.uScore desc"""
    return _select(requete, params=(idEditeur,))

def get_jeux_by_annee(annee):
    requete = """select * from jeu
                        where year(jeu.date)=?
                        order by jeu.date asc"""
    return _select(requete, params=(annee,))

def get_all_jeux():
    requete = """select nomJeu,idJeu,prix,uScore,date,achievements,developpeur.nomDev,editeur.nomEditeur,platformes.nomPlat from jeu
                 inner join developpeur on developpeur.idDev = jeu.idDev
                 inner join editeur on editeur.idEditeur = jeu.idEditeur
                 inner join platformes on platformes.idPlat = jeu.idPlat
                 limit 100"""
    return _select(requete)

def get_jeu_by_id(idJeu):
    requete = """select nomJeu,idJeu,prix,uScore,date,achievements,developpeur.nomDev,editeur.nomEditeur,platformes.nomPlat from jeu
                 inner join developpeur on developpeur.idDev = jeu.idDev
                 inner join editeur on editeur.idEditeur = jeu.idEditeur
                 inner join platformes on platformes.idPlat = jeu.idPlat
                 where idJeu = ?
                 limit 1"""
    return _select(requete, params=(idJeu,))

def get_admin(table):
    requete = f"""select * from {table}
                limit 200"""
    return _select(requete, params=())

def get_admin_param(table,parametre,valeur):
    plus = ""
    if parametre == "prix": param = f"where prix <= {int(valeur)}"
    elif parametre == "keyword": 
        param = f"where nom like '%{valeur.upper()}%' or desc like '%{valeur.upper()}%'"
        plus = ",upper(nomJeu) as nom,upper(description) as desc"
    elif parametre == "dev":
        param = "inner join developpeur on jeu.idDev == developpeur.idDev"
        if valeur != "r" : param += f" where developpeur.nomDev == '{valeur}'"
    requete = f"""select *{plus} from {table}
                {param}
                limit 100"""
    return _select(requete, params=())

def get_columns(table):
    requete = f"""PRAGMA table_info({table})"""
    return _select(requete, params=())
