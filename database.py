import sqlite3
from requests import get
import json

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

def get_plat_id(plat):
     requete = """select idPlat from platformes where nomPlat = ?"""
     return _select(requete, params=(plat,))

def insert_from_id(id):
    res = get(f"https://store.steampowered.com/api/appdetails?appids={id}")
    if res.status_code == 200:
        data = json.load(res)
        for jeu in data:
            if jeu['name'] != None and jeu["detailed_description"] != None and jeu["price_overview"]["initial"] != None != None and jeu["release_date"]["date"] != None and jeu["image"] != None:
                if jeu["release_date"]["coming_soon"]:
                    uScore = 0
                else :
                    try: uScore = jeu["metacritic"]["score"]
                    except: uScore = 0
                if jeu["achievements"] == None:
                    achievements = 0
                else:
                    achievements = jeu["achievements"]
                if jeu["developers"] != None:
                    if not dev_existe(jeu["developers"]):
                        insert_dev(jeu["developers"])
                    dev = _select(f"select idDev from developpeur where nomDev = '{jeu['developeurs']}'")
                else: dev=None
                if jeu["publishers"] != None:
                    if not editeur_existe(jeu["publishers"]):
                        insert_editeur(jeu["publishers"])
                    pub = _select(f"select idDev from developpeur where nomDev = '{jeu['publishers']}'")
                else: pub=None
                plat = ""
                p = jeu["platforms"]
                if p["windows"]: plat += "WIN"
                if p["mac"]: plat += "MAC" if plat == "" else ",MAC"
                if p["linux"]: plat += "LNX" if plat == "" else ",LNX"
                plat = get_plat_id(plat)
                insert_jeu(jeu['name'],jeu["detailed_description"],jeu["price_overview"]["initial"],uScore,jeu["release_date"]["date"],jeu["header_image"],achievements,dev,pub,plat[0][0])

def get_featured():
    res = get("http://store.steampowered.com/api/featured/")
    if res.status_code == 200:
        res = res.json()
        ids = [jeu["id"] for jeu in res["featured_win"]]
        print(ids)
        conditions = f"{ids[0]}"
        for id in ids[1:]:
            conditions += f" or idJeu = {id}"
        jeux = _select(f"select * from jeu where idJeu = {conditions}")
        print(jeux)
        if jeux == []:
            for id in ids:
                insert_from_id(id)
            jeux = _select(f"select * from jeu where idJeu = {conditions}")
        return jeux
    else: return ()

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
    return _select(requete)

def get_admin_param(table,parametre,valeur):
    plus = ""
    if parametre == "prix": param = f"where prix <= {int(valeur)}"
    elif parametre == "keyword": 
        param = f"where nom like '%{valeur.upper()}%'"
        nom = 'nomJeu' if table == 'jeu' else 'nomDev' if table == 'developpeur' else 'nomEditeur' if table == 'editeur' else "nomPlat"
        plus = f",upper({nom}) as nom"
        plus += ',upper(description) as desc' if table == 'jeu' else ""
        param +=  "or desc like '%{valeur.upper()}%'" if table == 'jeu' else ''
    elif parametre == "dev":
        param = "inner join developpeur on jeu.idDev == developpeur.idDev"
        if valeur != "r" : param += f" where developpeur.nomDev == '{valeur}'"
    elif parametre == "editeur":
        param = "inner join editeur on jeu.idEditeur == editeur.idEditeur"
        if valeur != "r" : param += f" where editeur.nomEditeur == '{valeur}'"
    requete = f"""select *{plus} from {table}
                {param}
                limit 200"""
    return _select(requete, params=())

def get_columns(table):
    requete = f"""PRAGMA table_info({table})"""
    return _select(requete, params=())

def insert_jeu(nomJeu,description,prix,uScore,date,image,achievements,nomDev,nomEditeur,idPlat): # (nomJeu, description, prix, uScore, date, image, achievements, idDev, idEditeur, idPlatforme)
    if not dev_existe(nomDev):
        insert_dev(nomDev)
        idDev = _select(f"select idDev from developpeur where nomDev = '{nomDev}'")
    if nomEditeur != None:
        if not editeur_existe(nomEditeur):
            insert_editeur(nomEditeur)
            idEditeur = _select(f"select idEditeur from editeur where nomEditeur = '{nomEditeur}'")
    requete = f"""insert into jeu values ({nomJeu},{description},{prix},{uScore},{date},{image},{achievements},{idDev},{idEditeur},{idPlat})"""
    return _select(requete, params=())

def insert_dev(nomDev):
    requete = f"""insert into developpeur values ({nomDev})"""
    return _select(requete, params=())

def insert_editeur(nomEditeur):
    requete = f"""insert into editeur values ({nomEditeur})"""
    return _select(requete, params=())

def dev_existe(nomDev):
    return _select(f"select idDev from developpeur where nomDev = '{nomDev}'") != []

def editeur_existe(nomEditeur):
    return _select(f"select idEditeur from editeur where nomDev = '{nomEditeur}'") != []
