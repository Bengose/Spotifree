#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:40:01 2022

@author: couzinier
"""

import mysql.connector as db


def ajout_musique(nom, artiste, album, lien):
    conn, cur = connexion()
    
    cur.execute(f"""INSERT INTO musique (nom, artiste, album, lien) VALUES ('{nom}', '{artiste}', '{album}', '{lien}') """)
    
    conn.commit()
    conn.close()
    return('Tout va bien')

def connexion():
    conn= db.connect(
        user="cyril",
        password="cyril",
        host="localhost",
        database="spotifree")
    
    cur = conn.cursor()
    return(conn, cur)



def ajout_user(nom, mdp):
    # INSERT INTO user (nom_user, mdp) VALUES (nom, mdp)
    conn, cur = connexion()
    
    cur.execute(f"""INSERT INTO user (nom_user, mdp) VALUES ('{nom}', '{mdp}') """)
    
    conn.commit()
    conn.close()
    return('Tout va bien')


def recherche_user(nom):
    """
    Fonction recharchant un user avec son nom
    argument:
    nom -> str, nom de l'user à rechercher
    retourne l'utilisateur trouvé
    """
    conn, cur = connexion()
    
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
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    
    cur.execute(f"""INSERT INTO playlist (id_user, nom_playlist, prive) VALUES ({id_user}, '{nom_play}', "{prive}") """)
    
    conn.commit()
    conn.close()
    return("tout va bien")


def supr_playlist(user, playlist):
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    
    cur.execute(f"""DELETE FROM playlist WHERE id_user = {id_user} AND nom_playlist = '{playlist}' """)
    
    conn.commit()
    conn.close()
    return("tout va bien")


def ajout_musique_play(user, nom_play, nom_musique):
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    id_play = recherche_playlist(nom_play, id_user)[0][0]
    id_musique = recherche_musique(nom_musique)[0][0]
                
    
    cur.execute(f"""INSERT INTO musique_playlist VALUES({id_play}, {id_musique})""")
    
    conn.commit()
    conn.close()
    return("tout va bien")


def supr_musique_play(user, nom_play, nom_musique):
    conn, cur = connexion()
    
    id_user = recherche_user(user)[0][0]
    print(id_user)
    id_play = recherche_playlist(nom_play, id_user)[0][0]
    id_musique = recherche_musique(nom_musique)[0][0]
    
    cur.execute(f"""DELETE FROM musique_playlist WHERE id_musique = {id_musique} AND id_playlist = {id_play}""")
    
    conn.commit()
    conn.close()
    return("tout va bien")



def recherche_playlist(nom_play, usr=False):
    conn, cur = connexion()
    
    if usr == False:
        cur.execute(f"""SELECT * FROM playlist WHERE nom_playlist = "{nom_play}" """)
    else:
        cur.execute(f"""SELECT * FROM playlist WHERE nom_playlist = "{nom_play}" AND id_user = {usr}""")
        
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()
    return(rows)


def recherche_musique(nom_musique):
    conn, cur = connexion()
    cur.execute(f"""SELECT * FROM musique WHERE nom = "{nom_musique}" """)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return(rows)



def supr_musique():
    pass


def ajout_ami(user1, user2):
    # INSERT INTO friends VALUES (user1, user2)
    pass


def recherche_ami():
    pass


def supr_ami():
    pass

def supr_user():
    pass


if __name__ == "__main__":
    nom = recherche_user("cyril")
    print(nom)