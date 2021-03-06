#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:40:01 2022

@author: couzinier
"""

import mysql.connector as db


def connexion():
    """
    Fonction se connectant à la base de données
    """
    conn= db.connect(
        user="cyril",
        password="cyril",
        host="localhost",
        database="spotifree")
    
    cur = conn.cursor()
    return(conn, cur)


def ajout_musique(nom, artiste, album, lien):
    """
    Fonction ajoutant une musique à la base de donnée
    arguments :
    nom -> str, nom de la musique
    artiste -> str, nom de l'artiste
    album -> str, nom de l'album
    lien -> str, chemin d'acces de la musique sur le serveur
    retourne 'tout va bien' si l'ajout a été fait sans erreur
    """
    conn, cur = connexion()
    
    cur.execute(f"""INSERT INTO musique (nom, artiste, album, lien) VALUES ('{nom}', '{artiste}', '{album}', '{lien}') """)
    
    conn.commit()
    conn.close()
    return('tout va bien')


def ajout_user(nom, mdp):
    # INSERT INTO user (nom_user, mdp) VALUES (nom, mdp)
    conn, cur = connexion()
    
    cur.execute(f"""INSERT INTO user (nom_user, mdp) VALUES ('{nom}', '{mdp}') """)
    
    conn.commit()
    conn.close()
    return('tout va bien')


def recherche_user(nom):
    """
    Fonction recharchant un user avec son nom
    argument:
    nom -> str, nom de l'user à rechercher
    retourne l'utilisateur trouvé
    """
    conn, cur = connexion()
    if nom == "":
        cur.execute(f"""SELECT * FROM user WHERE nom_user LIKE "%{nom}%" """)
    else:
        cur.execute(f"""SELECT * FROM user WHERE nom_user = "{nom}" """)
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return(rows)


def verif_user(nom, mdp):
    """
    verifie l'user pendant la connexion
    nom -> str, nom de l'utilisateur
    mdp -> str, mot de passe de l'utilisateur
    retourne True si les deux valeurs correspondent
    """
    conn, cur = connexion()
    
    cur.execute(f"""SELECT * FROM user WHERE nom_user = '{nom}' AND mdp = '{mdp}' """)
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    if len(rows) == 0:
        return(False)
    else:
        return(True)


def creer_playlist(user, nom_play, prive):
    """
    Fonction créant une playlist
    arguments :
    user -> str, nom de l'utilisateur
    nom_play -> str, nom de la playlist
    prive -> int, 1 pour privé et 0 pour publique
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    
    cur.execute(f"""INSERT INTO playlist (id_user, nom_playlist, prive) VALUES ({id_user}, '{nom_play}', "{prive}") """)
    
    conn.commit()
    conn.close()
    return("tout va bien")


def supr_playlist(user, playlist):
    """
    Fonction supprimant une playlist
    arguments :
    user -> str, nom de l'utilisateur
    playlist -> str, nom de la playlist
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    
    cur.execute(f"""DELETE FROM playlist WHERE id_user = {id_user} AND nom_playlist = '{playlist}' """)
    
    conn.commit()
    conn.close()
    return("tout va bien")


def ajout_musique_play(user, nom_play, nom_musique):
    """
    Fonction ajoutant une musique à la playlist
    arguments :
    user -> str, nom de l'utilisateur
    nom_play -> str, nom de la playlist
    nom_musique -> str, nom de la musique a ajouter
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    id_play = recherche_playlist(nom_play, id_user, True)[0][0]
    id_musique = recherche_musique(nom_musique)[0][0]
                
    
    cur.execute(f"""INSERT INTO musique_playlist VALUES({id_play}, {id_musique})""")
    
    conn.commit()
    conn.close()
    return("tout va bien")


def supr_musique_play(user, nom_play, nom_musique):
    """
    Fonction supprimant une musique à la playlist
    arguments :
    user -> str, nom de l'utilisateur
    nom_play -> str, nom de la playlist
    nom_musique -> str, nom de la musique a ajouter
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    id_play = recherche_playlist(nom_play, id_user)[0][0]
    id_musique = recherche_musique(nom_musique)[0][0]
    
    cur.execute(f"""DELETE FROM musique_playlist WHERE id_musique = {id_musique} AND id_playlist = {id_play}""")
    
    conn.commit()
    conn.close()
    return("tout va bien")


def recherche_playlist(nom_play, usr=False, egal=False):
    """
    Fonction recherchant une playlist
    arguments :
    nom_play -> str, nom de la playlist
    usr -> bool, True pour chercher les playlist liées à l'utilisateur
    egal -> bool, True pour chercher le nom exact de la playlist
    retourne le résultat de la recherche en list
    """
    conn, cur = connexion()
    
    if egal == False:
        if usr == False:
            cur.execute(f"""SELECT * FROM playlist WHERE nom_playlist LIke "%{nom_play}%" """)
        else:
            cur.execute(f"""SELECT * FROM playlist WHERE nom_playlist LIKE "%{nom_play}%" AND (id_user = {usr} OR prive = 0)""")
    else:
        if usr == False:
            cur.execute(f"""SELECT * FROM playlist WHERE nom_playlist = "{nom_play}" """)
        else:
            cur.execute(f"""SELECT * FROM playlist WHERE nom_playlist = "{nom_play}" AND (id_user = {usr} OR prive = 0)""")
        
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return(rows)


def recherche_musique(nom_musique, like = False):
    """
    Fonction recherchant une musique
    arguments :
    nom_musique -> str, nom de la musique
    like -> bool, True pour chercher le nom exact de la musique
    retourne le résultat de la recherche en list
    """
    conn, cur = connexion()
    if like == False:
        cur.execute(f"""SELECT * FROM musique WHERE nom = "{nom_musique}" """)
    else:
        cur.execute(f"""SELECT * FROM musique WHERE nom LIKE "%{nom_musique}%" """)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return(rows)


def ajout_ami(user1, user2):
    """
    Fonction ajoutant un amis
    arguments :
    user1 -> str, nom de l'utilisateur 1
    user2 -> str, nom de l'utilisateur 2
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    # INSERT INTO friends VALUES (user1, user2)
    conn, cur = connexion()
    
    id_user1 = recherche_user(user1)[0][0]
    id_user2 = recherche_user(user2)[0][0]
    
    cur.execute(f"""INSERT INTO friends VALUES({id_user1}, {id_user2})""")
    
    conn.commit()
    conn.close()
    return("tout va bien")


def supr_ami(user1, user2):
    """
    Fonction supprimant un amis
    arguments :
    user1 -> str, nom de l'utilisateur 1
    user2 -> str, nom de l'utilisateur 2
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    conn, cur = connexion()
    
    id_user1 = recherche_user(user1)[0][0]
    id_user2 = recherche_user(user2)[0][0]
    
    cur.execute(f"""DELETE FROM friends WHERE (id_user1 = {id_user1} AND id_user2 = {id_user2}) OR (id_user1 = {id_user2} AND id_user2 = {id_user1})""")
    
    conn.commit()
    conn.close()
    return("tout va bien")


def friend_to_playlist(user, playlist, friend):
    """
    Fonction ajoutant un amis à la playlist
    arguments :
    user -> str, nom de l'utilisateur
    playlist -> str, nom de la playlist
    friend -> str, nom de l'amis
    retourne 'tout va bien' l'action a été faite sans erreur
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    id_playlist = recherche_playlist(playlist, id_user, True)[0][0]
    id_friend = recherche_user(friend)[0][0]
    
    cur.execute(f"""INSERT INTO user_playlist VALUES({id_playlist}, {id_friend})""")
    
    conn.commit()
    conn.close()
    return("tout va bien")


def recherche_ami(user, recherche):
    """
    Fonction recherchant un amis de l'user
    arguments :
    user -> str, nom de l'utilisateur
    recherche -> str, nom de l'ami a rechercher
    retourne le résultat de la recherche en list
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    
    cur.execute(f"""SELECT DISTINCT user.nom_user FROM friends
                INNER JOIN user ON (friends.id_user1 = user.id_user OR friends.id_user2 = user.id_user)
                WHERE (friends.id_user1 = {id_user} OR friends.id_user2 = {id_user})
                AND user.nom_user LIKE '%{recherche}%'""")
    
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return(rows)


def musique_in_play(user, playlist):
    """
    Fonction recherchant les musiques dans une playlist
    arguments :
    user -> str, nom de l'utilisateur
    playlist -> str, nom de la playlist
    retourne le résultat de la recherche en list
    """
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    id_playlist = recherche_playlist(playlist, id_user, True)[0][0]
    
    cur.execute(f"""SELECT DISTINCT musique.nom, musique.artiste, musique.album, musique.lien FROM musique_playlist
                INNER JOIN musique ON musique.id_musique = musique_playlist.id_musique
                WHERE musique_playlist.id_playlist = {id_playlist}""")
    
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return(rows)



if __name__ == "__main__":
    nom = recherche_user("cyril")
    print(nom)