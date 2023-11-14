
# vapor

Exécuter vapor.py pour démarer le serveur flask.

Chemins :
 - **/admin.{*table*}** <- affiche la table demandée (limite de 200 enregistrements), les tables possibles sont jeu, platformes, editeur et developpeur
 - **/admin.{*table*}/{*paramètre*}.{*valeur*}** <- affiche une table dépendant des paramètres (même limite), les paramètres possibles sont : prix, keyword et dev sur la table jeu,
 - **/jeu/{*idJeu*}** <- affiche les données du jeu à partir de l'id d'un jeu

DB : *https://drive.google.com/file/d/1AKCRFnsd1OhBrUcm4JchDZ_EENGsahbZ/view?usp=share_link*
