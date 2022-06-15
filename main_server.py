#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 16:37:03 2022

@author: couzinier
"""

import sys
import recherche_bdd as bdd
import subprocess


if len(sys.argv) == 1:
    raise TypeError("Il manque des arguments")
    
# Traitement de l'arg 1

if sys.argv[1] == 'verifie':
    # print("On doit vérifier l'user")
    if len(sys.argv) == 4:
        result = bdd.verif_user(sys.argv[2], sys.argv[3])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
    
    
elif sys.argv[1] == 'new_user':
    #print("On doit créer l'user")
    if len(sys.argv) == 4:
        result = bdd.ajout_user(sys.argv[2], sys.argv[3])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
     
        
elif sys.argv[1] == 'add_musique':
    # print("On doit ajouter une musique")
    if len(sys.argv) == 6:
        result = bdd.ajout_musique(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

    
elif sys.argv[1] == 'new_playlist':
    #print("On doit créer une playlist")
    if len(sys.argv) == 5:
        result = bdd.creer_playlist(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
    
    
elif sys.argv[1] == 'del_playlist':
    #print("On doit supr une playlist")    
    if len(sys.argv) == 4:
        result = bdd.supr_playlist(sys.argv[2], sys.argv[3])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

 
elif sys.argv[1] == 'add_musique_play':
    #print("On doit ajouter une musique a la playlist")
    if len(sys.argv) == 5:
        result = bdd.ajout_musique_play(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")


elif sys.argv[1] == 'supr_musique_play':
    #print("On doit supprimer une musique a la playlist")   
    if len(sys.argv) == 5:
        result = bdd.supr_musique_play(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
    
    
elif sys.argv[1] == 'ajout_ami':
    #print("On doit ajouter un ami")
    if len(sys.argv) == 4:
        result = bdd.ajout_ami(sys.argv[2], sys.argv[3])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

elif sys.argv[1] == 'supr_ami':
    #print("On doit supr un ami")
    if len(sys.argv) == 4:
        result = bdd.supr_ami(sys.argv[2], sys.argv[3])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
    
elif sys.argv[1] == 'playlist':
    #print("On doit demander playlist")
    if len(sys.argv) == 4:
        id_user = bdd.recherche_user(sys.argv[3])[0][0]
        result = bdd.recherche_playlist(sys.argv[2], id_user)
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

elif sys.argv[1] == 'musique_playlist':
    #print("On doit demander playlist")
    if len(sys.argv) == 4:
        id_user = bdd.recherche_user(sys.argv[3])[0][0]
        result = bdd.recherche_playlist(sys.argv[2], id_user)
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

elif sys.argv[1] == 'friend_to_playlist':
    #print("On doit demander playlist")
    if len(sys.argv) == 5:
        result = bdd.friend_to_playlist(sys.argv[2], sys.argv[3], sys.argv[4])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

elif sys.argv[1] == 'search_friends':
    #print("On doit demander playlist")
    if len(sys.argv) == 3:
        result = bdd.recherche_ami(sys.argv[2])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")

elif sys.argv[1] == 'musique_in_playlist':
    #print("On doit demander playlist")
    if len(sys.argv) == 4:
        
        result = bdd.musique_in_play(sys.argv[2], sys.argv[3])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
    
elif sys.argv[1] == 'search_musique':
    #print("On doit demander playlist")
    if len(sys.argv) == 3:
        
        result = bdd.recherche_musique(sys.argv[2])
        print(result)
    else:
        raise TypeError("Les arguments ne sont pas valide")
        
elif sys.argv[1] == 'musique_dispo':
    
    if len(sys.argv) == 3:
        commande = f"ls -d clone/Spotifree/serveur/*{sys.argv[2]}*"
        print(subprocess.check_output(commande, shell=True).decode())
    else:
        raise TypeError("Les arguments ne sont pas valide")
    
    
    
    
    
    
    
    