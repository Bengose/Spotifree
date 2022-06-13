#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 16:18:16 2022

@author: couzinier
"""

import requests

# Lien de référence
# https://stackoverflow.com/questions/36719540/how-can-i-get-an-oauth2-access-token-using-python

def get_access_token(url, client_id, client_secret):
    """
    Fonction permettant de récupérer un token
    arguments:
    url -> str, url de l'API
    client_id -> str, id du client
    client_secret -> str, code secret du client
    retourne un token valide
    """
    
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]


if __name__ == "__main__":
    tkn = get_access_token("https://accounts.spotify.com/api/token", "fe7f93a0d9664263add7dd0f822de8b1", "9575b5da25aa4fdeace64e651f975265")
    print(tkn)



