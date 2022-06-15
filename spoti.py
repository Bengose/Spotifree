#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:27:09 2022

@author: couzinier
"""
import os
from get_token import get_access_token as tk
import urllib
import json
import subprocess


def recherche_musique(nom, tipe='track'):
    """
    Fonction pemrettant de rechercher un nom de titre/d'artiste sur l'API spotify
    arguments :
    nom -> str, nom du titre/artiste
    tipe -> str, défini si un on cherche un titre ou un artiste
    retourne un dictionnaire des résultats de la recherche
    """
    # Défini l'identifiant de connexion
    url = "https://accounts.spotify.com/api/token"
    client = "fe7f93a0d9664263add7dd0f822de8b1"
    cl_secret = "9575b5da25aa4fdeace64e651f975265"
    
    # Créer un token de connexion
    token = tk(url ,client ,cl_secret)
    
    # Défini les variables d'environement
    os.environ["SPOTIPY_CLIENT_ID"] = client
    os.environ["SPOTIPY_CLIENT_SECRET"] = cl_secret
    
    # Code le nom en http
    nom = urllib.parse.quote_plus(nom)
    
    # Fait la recherche
    #cmd = f"""curl -X "GET" "https://api.spotify.com/v1/search?q={nom}&type={tipe}" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {token}\" --output save.json"""
    
    cmd = f"curl --request GET \
  --url 'https://api.spotify.com/v1/search?q={nom}&type=track&include_external=audio' \
  --header 'Authorization: Bearer {token}' \
  --header 'Content-Type: application/json' --output save.json"
    
    
    subprocess.getoutput(cmd)
    # Traite le json
    
    
    with open('save.json', "r") as file:
        data = json.load(file)
    
    result = []
    print()
    if str(data.keys()) != "dict_keys(['error'])":
        #print(data["tracks"]["items"][0]["artists"][0]["name"])
        for e in  data["tracks"]["items"]:
            dct = {"artiste":e["artists"][0]["name"], "lien":e["external_urls"]['spotify'], "musique":e["name"], "album":e["album"]["name"]}
            result.append(dct)
            #print(e["artists"][0]["name"], e["external_urls"], e["name"])
        return(result)
    else:
        return ("Erreur pas de musique trouvé")
    

def recherche_nom(nom):
    """
    Fonction recherchant le nom d'une musique
    argument :
    nom -> str, nom à rechercher
    retourne l'url de la musique
    """
    
    recherche = recherche_musique(nom, "track")
    
    for dct in recherche:
        print(dct["artiste"], dct["musique"], dct["lien"])
        
    



if __name__ == "__main__":
    recherche_nom("Sainted by the storm")



