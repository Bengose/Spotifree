#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:27:09 2022

@author: couzinier
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
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
    cmd = f"""curl -X "GET" "https://api.spotify.com/v1/search?q={nom}&type={tipe}" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {token}\" """
    
    recherche = subprocess.getoutput(cmd)
    # Traite le json
    
    i = 0
    for e in recherche:
        if e !="{":
            i += 1
        else :
            recherche = recherche[i:]
            break
        
    print(recherche[0:999])
    data = json.loads(recherche)
    print(data)
    return(data)
    

def recherche_nom(nom):
    """
    Fonction recherchant le nom d'une musique
    argument :
    nom -> str, nom à rechercher
    retourne l'url de la musique
    """
    
    recherche = recherche_musique(nom, "track")
    
    
    lz_uri = 'spotify:artist:5HFkc3t0HYETL4JeEbDB1v'

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    
    results = spotify.artist_top_tracks(lz_uri)
    
    for track in results['tracks']:
        if track['name'] == "Sainted by the Storm":    
            print(track["external_urls"])



if __name__ == "__main__":
    recherche_nom("Forgive me friend")



