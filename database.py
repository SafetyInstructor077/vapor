import sqlite3
from requests import get
import re

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
     """Requête qui revoie l'id de la platforme à partir des noms des platformes
    exemple :
        plat = 'WIN,MAC,LNX'
        la fonction retourne 1"""
     requete = """select idPlat from platformes where nomPlat = ?""" 
     return _select(requete, params=(plat,))

def insert_from_id(id):
    res = get(f"https://store.steampowered.com/api/appdetails?appids={id}") # demande les données d'un jeu au API
    if res.status_code == 200:
        data = res.json()
        jeu = data[str(id)]
        if not jeu["success"]: return None
        jeu = jeu["data"]
        if jeu['name'] != None and jeu["detailed_description"] != None and jeu["release_date"]["date"] != None and jeu["header_image"] != None:
            if jeu["release_date"]["coming_soon"]:
                uScore = 0
            else :
                try: uScore = jeu["metacritic"]["score"]
                except: uScore = 0
            try:
                if jeu["achievements"]["total"] == None:
                    achievements = 0
                else:
                    achievements = jeu["achievements"]["total"]
            except: achievements = 0
            try:
                if jeu["price_overview"]["initial"] == None:
                    prix = 0
                else:
                    prix = jeu["price_overview"]["initial"]
            except: prix = 0
            plat = ""
            p = jeu["platforms"]
            if p["windows"]: plat += "WIN" # transformer la platforme en un string convenable à notre base de données
            if p["mac"]: plat += "MAC" if plat == "" else ",MAC"
            if p["linux"]: plat += "LNX" if plat == "" else ",LNX"
            plat = get_plat_id(plat)
            insert_jeu(jeu['name'],jeu["detailed_description"],prix,uScore,jeu["release_date"]["date"],jeu["header_image"],achievements,jeu["developers"][0],jeu["publishers"][0],plat[0][0])

def get_featured():
    res = get("http://store.steampowered.com/api/featured/") # demande au API les jeux qui sont sur le devant du magasin
    if res.status_code == 200:
        res = res.json()
        infoJeux = [jeu for jeu in res["featured_win"]]
        if infoJeux == []:
            return [[0,"Aucun jeu n'est en vedette en ce moment.", "Réessayez plus tard.", 0, 0, "00-00-0000", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/800px-Question_mark_%28black%29.svg.png", 0, 1, 1, 1]]
        conditions = f"'{infoJeux[0]['name']}'" # chercher les jeux dans la BDD
        for name in infoJeux[1:]:
            conditions += f" or nomJeu = '{name['name']}'"
        jeux = _select(f"select idJeu, nomJeu, description, prix, uScore, image, developpeur.nomDev from jeu inner join developpeur on jeu.idDev = developpeur.idDev where nomJeu = {conditions}")
        if jeux == []:
            for jeu in infoJeux:
                insert_from_id(jeu["id"]) # s'il n'y a pas de jeux dans la BDD qui sont sur le devant du magasin alors on les insère
            jeux = _select(f"select idJeu,nomJeu,description,prix,uScore,image,developpeur.nomDev from jeu inner join developpeur on jeu.idDev = developpeur.idDev where nomJeu = {conditions}")
        return format_all(jeux)
    else: return [[0,"Aucun jeu n'est en vedette en ce moment.", "Réessayez plus tard.", 0, 0, "00-00-0000", "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Question_mark_%28black%29.svg/800px-Question_mark_%28black%29.svg.png", 0, 1, 1, 1]]

def get_jeux_by_dev(idDev):
    """Retourne les jeux faits par un certain développeur à partir de son id"""
    requete = """select * from jeu
                        where jeu.idDev=?
                        order by jeu.uScore desc""" # on trie par le score du jeu
    return _select(requete, params=(idDev,))

def get_jeux_by_pub(idEditeur):
    """Retourne les jeux publiés par un certain éditeur à partir de son id"""
    requete = """select * from jeu
                        where jeu.idEditeur=?
                        order by jeu.uScore desc""" # on trie par le score du jeu
    return _select(requete, params=(idEditeur,))

def get_jeux_by_annee(annee):
    """Renvoie une liste des jeux sortis pendant l'année précisée"""
    requete = """select * from jeu
                        where year(jeu.date)=?
                        order by jeu.date asc""" # on trie par la date de sortie du jeu
    return _select(requete, params=(annee,))

def get_all_jeux():
    """Renvoie (avec une limite de 100) les jeux sans les trier et les filtrer"""
    requete = """select nomJeu,idJeu,prix,uScore,date,achievements,developpeur.nomDev,editeur.nomEditeur,platformes.nomPlat from jeu
                 inner join developpeur on developpeur.idDev = jeu.idDev
                 inner join editeur on editeur.idEditeur = jeu.idEditeur
                 inner join platformes on platformes.idPlat = jeu.idPlat
                 limit 100""" # on y ajoute aussi le nom du développeur et celui de l'éditeur, avec les platformes sur lesquelles le jeu est disponible
    return _select(requete)

def get_jeu_by_id(idJeu):
    """Renvoie le jeu dont le id a été précisé"""
    requete = """select nomJeu,description,idJeu,prix,image,uScore,date,achievements,developpeur.nomDev,editeur.nomEditeur,platformes.nomPlat from jeu
                 inner join developpeur on developpeur.idDev = jeu.idDev
                 inner join editeur on editeur.idEditeur = jeu.idEditeur
                 inner join platformes on platformes.idPlat = jeu.idPlat
                 where idJeu = ?
                 limit 1"""
    return _select(requete, params=(idJeu,))

def get_admin(table):
    """Renvoie 200 entrés max de la table précisée
    Les tables possibles sont : (jeu,developpeur,editeur,plarformes)"""
    requete = f"""select * from {table}
                limit 200"""
    return _select(requete)

def get_admin_param(table,parametre,valeur):
    """Admin complexes, même tables que admin
    Les paramètres sont :
        - prix : renvoie les jeux dont le prix et égal ou inférieur à celui précisé
        - keyword : renvoie les jeux où le mot précisé est dans le titre ou la description, sinon dans le nom de l'éditeur, du développeur ou de la platforme
        - dev : relie la table developpeur à la table jeu, l'argument sert à renvoyer les jeux d'un certain développeur
        - editeur : pareil mais avec l'éditeur
    """
    plus = "" # variable pour rajouter certains paramètres spécifiques à certains filtres
    if parametre == "prix": param = f"where prix <= {int(valeur)}"
    elif parametre == "keyword": 
        param = f"where nom like '%{valeur.upper()}%'" # on met tout en majuscules pour que le filtre marche mieux
        nom = 'nomJeu' if table == 'jeu' else 'nomDev' if table == 'developpeur' else 'nomEditeur' if table == 'editeur' else "nomPlat" # définir la colonne où chercher dépendant de la table
        plus = f",upper({nom}) as nom" # la colonne en majuscules
        plus += ',upper(description) as desc' if table == 'jeu' else "" # quand on cherche dansl es jeux alors on cherche aussi dans la description
        param +=  "or desc like '%{valeur.upper()}%'" if table == 'jeu' else ''
    elif parametre == "dev":
        param = "inner join developpeur on jeu.idDev == developpeur.idDev"
        if valeur != "r" : param += f" where developpeur.nomDev == '{valeur}'" # on met r pour voir tous les jeux à la place de filtrer
    elif parametre == "editeur":
        param = "inner join editeur on jeu.idEditeur == editeur.idEditeur"
        if valeur != "r" : param += f" where editeur.nomEditeur == '{valeur}'"
    requete = f"""select *{plus} from {table}
                {param}
                limit 200"""
    return _select(requete)

def get_columns(table):
    requete = f"""PRAGMA table_info({table})""" # retourne les noms des colonnes d'une table
    return _select(requete)

def insert_jeu(nomJeu,description,prix,uScore,date,image,achievements,nomDev,nomEditeur,idPlat): # (nomJeu, description, prix, uScore, date, image, achievements, idDev, idEditeur, idPlatforme)
    print(nomJeu)
    if not dev_existe(nomDev):
        insert_dev(nomDev)
    idDev = _select(f"select idDev from developpeur where nomDev == '{nomDev}'")[0]
    if nomEditeur != None:
        if not editeur_existe(nomEditeur):
            insert_editeur(nomEditeur)
        idEditeur = _select(f"select idEditeur from editeur where nomEditeur == '{nomEditeur}'")[0]
    requete = f"""insert into jeu (nomJeu,description,prix,uScore,date,image,achievements,idDev,idEditeur,idPlat) values ('{nomJeu.replace("'","’")}','{description.replace("'","’")}',{prix},{uScore},'{date}','{image}',{achievements},{idDev[0]},{idEditeur[0]},{idPlat})"""
    return _select(requete)

def insert_dev(nomDev):
    """Insérer un développeur dans la table (pas besoin de présiser le id puisqu'il y a un autoincrement)"""
    requete = f"""insert into developpeur (nomDev) values ('{nomDev}')"""
    return _select(requete)

def insert_editeur(nomEditeur):
    requete = f"""insert into editeur (nomEditeur) values ('{nomEditeur}')"""
    return _select(requete)

def dev_existe(nomDev):
    """Retourne True si le développeur est dans la base de données sinon False"""
    return _select(f"select idDev from developpeur where nomDev == '{nomDev}'") != []

def editeur_existe(nomEditeur):
    return _select(f"select idEditeur from editeur where nomEditeur == '{nomEditeur}'") != []

def format(description):
    while '<img src' in description:
        description = description.replace('<img src', '<img class="htmlImg" src')
    return description

def format_all(jeux):
    for i in range(len(jeux)):
        jeux[i] = list(jeux[i])
        print(jeux[i])
        jeux[i][2] = format(jeux[i][2])
        jeux[i].append(reduire_desc(jeux[i][2]))
    return jeux

def reduire_desc(description):
    # l = re.sub(r'<a(.*</a>)','',re.sub(r'<img(.*/>)','', description))
    # return re.sub(r'<br>','', l) # on soustrait les liens et les images
    return re.sub(r'<a(.*</a>)','',re.sub(r'<img(.*/>)','', description))
