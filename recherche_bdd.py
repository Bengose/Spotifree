#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:40:01 2022

@author: couzinier
"""

import mysql.connector as db


def ajout_ami(user1, user2):
    # INSERT INTO friends VALUES (user1, user2)
    pass


def recherche_ami():
    pass


def supr_ami():
    pass





def ajout_musique():
    pass


def recherche_musique():
    pass


def supr_musique():
    pass






def ajout_user(nom, mdp):
    # INSERT INTO user (nom_user, mdp) VALUES (nom, mdp)
    pass


def recherche_user(nom):
    conn= db.connect(
        user="cyril",
        password="cyril",
        host="localhost",
        database="spotifree")
    
    cur = conn.cursor()
    
    cur.execute(f"""SELECT * FROM user WHERE nom_user LIKE "%{nom}%" """)
    rows = cur.fetchall()
    
    conn.close()
    return(rows)


def supr_user():
    pass




def ajout_playlist():
    pass


def recherche_playlist():
    pass


def supr_playlist():
    pass




if __name__ == "__main__":
    nom = recherche_user("cyril")
    print(nom)