#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:07:45 2022

@author: couzinier
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QComboBox, QListWidget, QMessageBox, QSpacerItem, QLabel, QApplication,
                             QAction, QTextEdit, QTabWidget, QSlider)

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl, Qt
import sys
from PyQt5.QtGui import QIcon, QPixmap
import spoti
import sip
import os
import subprocess
import ftplib
import glob


class mainUi(QMainWindow):
    """
    Fenetre principale de spotifree
    """
    def __init__(self):
        """
        Fonction d'initialisation du programme spotifree
        """
        QMainWindow.__init__(self)
        # Créer les variables d'environement pour télécharger les musique
        client = "fe7f93a0d9664263add7dd0f822de8b1"
        cl_secret = "9575b5da25aa4fdeace64e651f975265"
        os.environ["SPOTIPY_CLIENT_ID"] = client
        os.environ["SPOTIPY_CLIENT_SECRET"] = cl_secret
        # Défini l'affichage
        self.initUi()
        self.identifiant()
        self.show()
        
    def initUi(self):
        """
        Fonction créant les widgets de la fenetre
        """
        
        self.resize(500, 500)
        self.setWindowTitle("Spotifree")
        # Création du widget central
        self.centralW = QWidget(parent=self)
        self.centralT = QWidget(parent=self)
        self.centralA = QWidget(parent=self)
        
        # Création d'une icone
        label_icon = QLabel()
        label_icon.setPixmap(QPixmap('icones/spotifree.svg').scaled(400,400, Qt.AspectRatioMode.KeepAspectRatio))
        
        # Création des tab widgets
        self.tabs = QTabWidget(parent=self)
        self.tabs.addTab(self.centralT, 'Ecouter une musique')
        self.tabs.addTab(self.centralW, 'Télecharger une musique')
        self.tabs.addTab(self.centralA, 'Ami')
        
        ##
        ##### Contenue de la tab Télecharger une musique
        ##
        
        self.setCentralWidget(self.tabs)
        
        # Création des boutons
        self.button = QPushButton(QIcon('icones/recherche.png'), "")
        self.button.clicked.connect(self.recherche_serv)
        
        # Création du menu déroulant
        self.combo_recherche = QComboBox()
        self.combo_recherche.addItem('Musique')
        self.combo_recherche.addItem('Ajout musique dans playlist')
        self.combo_recherche.addItem('Retirer musique dans playlist')
        self.combo_recherche.addItem('Nouvelle playlist')
        self.combo_recherche.addItem('Supprimer playlist')
        
        # Création de la menu bar
        self.menu = self.menuBar()
        
        menu_fichier = self.menu.addMenu('Fichier')
        mf_quit = QAction("Quitter", parent=self)
        mf_quit.setShortcut("Ctrl+Q")
        mf_quit.setStatusTip("Quitte l'application")
        mf_quit.triggered.connect(self.close)
        menu_fichier.addAction(mf_quit)
        
        # Création des line edit
        self.line_edit = QLineEdit()
        
        # bloque les widgets
        self.combo_recherche.setEnabled(False)
        self.button.setEnabled(False)
        self.line_edit.setEnabled(False)
        
        # Création des Layout
        h_recherche = QHBoxLayout()
        h_recherche.addWidget(self.line_edit)
        h_recherche.addWidget(self.combo_recherche)
        h_recherche.addWidget(self.button)
        
        self.v_main = QVBoxLayout()
        self.v_main.addWidget(label_icon)
        self.v_main.addLayout(h_recherche)
        self.v_main.addStretch()
        
        self.centralW.setLayout(self.v_main)
        
        ##
        ##### Contenue de la tab Ecouter une musique
        ##
        
        label_icon = QLabel()
        label_icon.setPixmap(QPixmap('icones/spotifree.svg').scaled(400,400, Qt.AspectRatioMode.KeepAspectRatio))
        
        self.label_musique = QLabel()
        
        # Création des boutons
        self.button_e = QPushButton(QIcon('icones/recherche.png'), "")
        self.button_e.clicked.connect(self.recherche_client)
        
        # Création du menu déroulant
        self.combo_recherche_e = QComboBox()
        self.combo_recherche_e.addItem('Musique')
        self.combo_recherche_e.addItem('Playlist')
        
        # Création des line edit
        self.line_edit_e = QLineEdit()
        
        # bloque les widgets
        self.combo_recherche_e.setEnabled(False)
        self.button_e.setEnabled(False)
        self.line_edit_e.setEnabled(False)
        
        # Layout de la gestion des sons
        self.v_musique = QVBoxLayout()
        
        # Création des Layout
        h_recherche_e = QHBoxLayout()
        h_recherche_e.addWidget(self.line_edit_e)
        h_recherche_e.addWidget(self.combo_recherche_e)
        h_recherche_e.addWidget(self.button_e)
        
        self.v_main_e = QVBoxLayout()
        self.v_main_e.addWidget(label_icon)
        self.v_main_e.addLayout(h_recherche_e)
        self.v_main_e.addStretch()
        self.v_main_e.addWidget(self.label_musique)
        self.v_main_e.addLayout(self.v_musique)
        
        self.centralT.setLayout(self.v_main_e)
        
        
        ##
        ##### Contenue de la tab des amis
        ##
        
        label_icon = QLabel()
        label_icon.setPixmap(QPixmap('icones/spotifree.svg').scaled(400,400, Qt.AspectRatioMode.KeepAspectRatio))
        
        self.label_musique = QLabel()
        
        # Création des boutons
        self.button_a = QPushButton(QIcon('icones/recherche.png'), "")
        self.button_a.clicked.connect(self.recherche_ami)
        
        # Création du menu déroulant
        self.combo_recherche_a = QComboBox()
        self.combo_recherche_a.addItem('Ami')
        self.combo_recherche_a.addItem('Ajouter')
        self.combo_recherche_a.addItem('Supprimer')
        
        # Création des line edit
        self.line_edit_a = QLineEdit()
        
        # bloque les widgets
        self.combo_recherche_a.setEnabled(False)
        self.button_a.setEnabled(False)
        self.line_edit_a.setEnabled(False)
        
        # Layout de la gestion des sons
        self.v_musique = QVBoxLayout()
        
        # Création des Layout
        h_recherche_a = QHBoxLayout()
        h_recherche_a.addWidget(self.line_edit_a)
        h_recherche_a.addWidget(self.combo_recherche_a)
        h_recherche_a.addWidget(self.button_a)
        
        self.v_main_a = QVBoxLayout()
        self.v_main_a.addWidget(label_icon)
        self.v_main_a.addLayout(h_recherche_a)
        self.v_main_a.addStretch()
        self.v_main_a.addWidget(self.label_musique)
        self.v_main_a.addLayout(self.v_musique)
        
        self.centralA.setLayout(self.v_main_a)
        
        
        
    def recherche_serv(self):
        """
        Fonction permettant de rechercher l'élément rentré dans le line edit en fonction du type de recherche niveau serveur
        """
        
        recherche = self.line_edit.text()
        tpe = self.combo_recherche.currentText()
        
        # Si on cherche une musique
        if tpe == "Musique":
            self.liste_musique = spoti.recherche_musique(recherche, "track")
            self.poppup = poppupChoix(self.liste_musique)
            self.poppup.bt_valider.clicked.connect(self.serv_download)
        
        # Si on supprime une musique dans une playlist
        elif tpe == "Retirer musique dans playlist":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py playlist '{recherche}' '{self.utilisateur}' "]).decode().replace("\n", '')
            lst = eval(ssh_stdout)
            self.poppup = playlist(lst, self.utilisateur)
            self.poppup.bt_valider.clicked.connect(self.music_out_playlist)
        
        # Si on ajoute une musique dans une playlist
        elif tpe == "Ajout musique dans playlist":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py playlist '{recherche}' '{self.utilisateur}' "]).decode().replace("\n", '')
            lst = eval(ssh_stdout)
            self.poppup = playlist(lst, self.utilisateur)
            self.poppup.bt_valider.clicked.connect(self.music_in_playlist)
          
        # Si on créer une playlist
        elif tpe == "Nouvelle playlist":
            self.message = QMessageBox.question(self, 'Nouvelle Playlist', f'Voulez vous que la playlist : {recherche} soit privé')
            if self.message == QMessageBox.Yes:
                ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py new_playlist '{self.utilisateur}' '{recherche}' '1' "]).decode().replace("\n", '')
            if self.message == QMessageBox.No:
                ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py new_playlist '{self.utilisateur}' '{recherche}' '0' "]).decode().replace("\n", '')

        # Si on supprime une playlist
        elif tpe == "Supprimer playlist":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py playlist '{recherche}' '{self.utilisateur}' "]).decode().replace("\n", '')
            lst = eval(ssh_stdout)
            self.poppup = playlist(lst, self.utilisateur)
            self.poppup.bt_valider.clicked.connect(self.del_playlist)
            
            
    def recherche_client(self):
        """
        Fonction permettant de rechercher l'élément rentré dans le line edit en fonction du type de recherche niveau client
        """
        recherche = self.line_edit_e.text()
        tpe = self.combo_recherche_e.currentText()
        
        # Si on cherche une musique
        if tpe == "Musique":
            commande = f"shopt -s nocaseglob && ls -d clone/Spotifree/musique/*{recherche}*"
            result = subprocess.check_output(['ssh', '127.0.0.1', commande]).decode()
            self.poppup = poppupChoix(result.split("\n"))
            self.poppup.bt_valider.clicked.connect(lambda: self.lancer_musique([self.chemin_musique(self.poppup.list.currentItem().text())]))
       
        # Si on cherche une playlist
        elif tpe == "Playlist":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py playlist '{recherche}' '{self.utilisateur}' "]).decode().replace("\n", '')
            lst = eval(ssh_stdout)
            self.poppup = playlist(lst, self.utilisateur)
            self.poppup.bt_valider.clicked.connect(self.download_playlist)
           

    def recherche_ami(self):
        """
        Fonction permettant de rechercher l'élément rentré dans le line edit en fonction du type de recherche niveau des amis
        """
        recherche = self.line_edit_a.text()
        tpe = self.combo_recherche_a.currentText()
        
        # Si on cherche une musique
        if tpe == "Ami":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py search_friends '{self.utilisateur}' '{recherche}' "]).decode().replace("\n", '')
            ssh_stdout = eval(ssh_stdout)
            ami = []
            if recherche == "":
                for a in ssh_stdout[1:]:
                    ami.append(a[0])
            else:
                for a in ssh_stdout:
                    ami.append(a[0])
                
            print(ami)
            self.poppup = poppupChoix(ami)
            self.poppup.bt_valider.setEnabled(False)
            #self.poppup.bt_valider.clicked.connect(lambda: self.lancer_musique([self.chemin_musique(self.poppup.list.currentItem().text())]))
       
        elif tpe == "Ajouter":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', "python3 /home/couzinier/clone/Spotifree/main_server.py search_user '' "]).decode().replace("\n", '')
            ssh_stdout = eval(ssh_stdout)
            print(ssh_stdout)
            user = []
            for a in ssh_stdout:
                if a[1] != self.utilisateur:
                    user.append(a[1])
                    
            print(user)
            self.poppup = poppupChoix(user)
            self.poppup.bt_valider.clicked.connect(self.ajout_ami)
            
        elif tpe == "Supprimer":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py search_friends '{self.utilisateur}' '{recherche}' "]).decode().replace("\n", '')
            ssh_stdout = eval(ssh_stdout)
            ami = []
            if recherche == "":
                for a in ssh_stdout[1:]:
                    ami.append(a[0])
            else:
                for a in ssh_stdout:
                    ami.append(a[0])
            print(ami)
            self.poppup = poppupChoix(ami)
            self.poppup.bt_valider.clicked.connect(self.supr_ami)
            
            
            
            
       
    def chemin_musique(self, nom):
        """
        Permet d'obtenir le chemin d'une musique
        argument :
        nom -> str, nom de la musique
        retourne le chemin d ela musique
        """
        chemin = glob.glob(f"/home/couzinier/clone/Spotifree/musique/{nom}/*.mp3")[0]
        return (chemin)
        
        
    def lancer_musique(self, chemin):
        """
        Fonction permettant le lancer une musique 
        chemin -> list, chemin vers les musiques
        """
        
        self.poppup.close()
        # Clear le layout
        self.clearAll(self.v_musique)
        # Création des boutons
        self.bt_play = QPushButton(QIcon("icones/play.svg"), '')
        self.bt_play.clicked.connect(self.play)
        
        self.bt_pause = QPushButton(QIcon("icones/pause.svg"), "")
        self.bt_pause.clicked.connect(self.pause)
        self.bt_pause.setEnabled(False)
        
        self.bt_stop = QPushButton(QIcon("icones/stop.svg"), '')
        self.bt_stop.clicked.connect(self.stop)
        self.bt_stop.setEnabled(False)
        
        self.bt_plus = QPushButton('<<')
        self.bt_plus.clicked.connect(lambda: self.player.playlist().previous())
        
        self.bt_moins = QPushButton('>>')
        self.bt_moins.clicked.connect(lambda: self.player.playlist().next())
        
        # Création du slider de son
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setRange(0, 100)
        self.sld.setValue(50)
        self.sld.valueChanged.connect(self.updatesong)
        
        # Création du média player
        self.player = QMediaPlayer()
        self.playlist_cours = QMediaPlaylist()
        self.player.setPlaylist(self.playlist_cours)
        self.player.setVolume(50)
        self.playlist_cours.currentIndexChanged.connect(self.changer_nom)
        
        # Mise en place de la playlist
        for e in chemin:
            path = os.path.join(os.getcwd(), e)
            url = QUrl.fromLocalFile(path)
            self.playlist_cours.addMedia(QMediaContent(url))
            
        # Création des layout
        h_btp = QHBoxLayout()
        h_btp.addWidget(self.bt_play)
        h_btp.addWidget(self.bt_pause)
        h_btp.addWidget(self.bt_stop)
        
        h_son = QHBoxLayout()
        h_son.addWidget(self.bt_plus)
        h_son.addWidget(self.bt_moins)
        
        self.v_musique.addLayout(h_btp)
        self.v_musique.addLayout(h_son)
        self.v_musique.addWidget(self.sld)
        
    def changer_nom(self):
        """
        Change le nom de la musique en cours
        """
        musique = self.playlist_cours.currentMedia().canonicalUrl()
        musique = musique.toString().split("/")[-1].replace(".mp3", "")
        self.label_musique.setText(musique)
    
    
    def updatesong(self, valeur):
        """
        Met à jour le volume du son en fontion de la barre réglable
        """
        self.player.setVolume(valeur)
    
        
    def play(self):
        """
        Fonction permettant de jouer la musique en cours
        """
        self.bt_play.setEnabled(False)
        self.bt_pause.setEnabled(True)
        self.bt_stop.setEnabled(True)
        self.player.play()
        

    def pause(self):
        """
        Fonction permettant de mettre en pause la musique en cours
        """
        self.bt_play.setEnabled(True)
        self.bt_pause.setEnabled(False)
        self.bt_stop.setEnabled(True)
        self.player.pause()
    
    
    def stop(self):
        """
        Fonction permettant d'arreter la musique en cours
        """
        self.bt_play.setEnabled(True)
        self.bt_pause.setEnabled(False)
        self.bt_stop.setEnabled(False)
        self.player.stop()
 
          
    def identifiant(self):
        """
        Fonction permettant de gérer la connexion des utilisateurs
        """
        self.ident = identfiant()
        self.ident.bt_valid.clicked.connect(self.connexion)
        self.ident.bt_inscription.clicked.connect(self.inscription)
        
        
    def connexion(self):
        """
        vérifie l'identifiant et le mot de passe de l'user
        """
        self.utilisateur = self.ident.line_user.text()
        
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py verifie '{self.utilisateur}' '{self.ident.line_mdp.text()}'"])
        
        if ssh_stdout == b'True\n':
            self.ident.close()
        
            # Si tout va bien, on active les boutons
            self.combo_recherche.setEnabled(True)
            self.button.setEnabled(True)
            self.line_edit.setEnabled(True)
            
            self.combo_recherche_e.setEnabled(True)
            self.button_e.setEnabled(True)
            self.line_edit_e.setEnabled(True)
            
            self.combo_recherche_a.setEnabled(True)
            self.button_a.setEnabled(True)
            self.line_edit_a.setEnabled(True)
        

    def inscription(self):
        """
        Créer un compte utilisateur
        """
        self.utilisateur = self.ident.line_user.text()
        
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py new_user '{self.utilisateur}' '{self.ident.line_mdp.text()}'"])
        
        if ssh_stdout == b'tout va bien\n':
            self.ident.close()
        
        self.combo_recherche.setEnabled(True)
        self.button.setEnabled(True)
        self.line_edit.setEnabled(True)


    def music_out_playlist(self):
        """
        Choisi la musique à retirer de la playlist
        """
        nom_play = self.poppup.list.currentItem().text()
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py musique_in_playlist '{self.utilisateur}' '{nom_play}'"])
        ssh_stdout = eval(ssh_stdout)
        musique = []
        print(ssh_stdout)
        for m in ssh_stdout:
            musique.append(m[0])
        self.poppup_ch = poppupChoix(musique)
        self.poppup_ch.bt_valider.clicked.connect(self.supr_mus_play)


    def supr_ami(self):
        nom_ami = self.poppup.list.currentItem().text()
        self.message = QMessageBox.question(self, 'Supprimer ami', f'Voulez vous supprimer cet ami : {nom_ami} ')
        if self.message == QMessageBox.Yes:
            subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py supr_ami '{self.utilisateur}' '{nom_ami}'"])
        self.poppup.close()
        
        
    def ajout_ami(self):
        nom_ami = self.poppup.list.currentItem().text()
        subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py ajout_ami '{self.utilisateur}' '{nom_ami}'"])
        self.poppup.close()
        

    def supr_mus_play(self):
        """
        Retire une musique de la playlist
        """
        nom_play = self.poppup.list.currentItem().text()
        nom_musique = self.poppup_ch.list.currentItem().text()
        subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py supr_musique_play '{self.utilisateur}' '{nom_play}' '{nom_musique}' "])
        self.poppup.close()
        self.poppup_ch.close()
        
        
    def del_playlist(self):
        """
        Supprime la playlist 
        """
        nom_play = self.poppup.list.currentItem().text()
        self.message = QMessageBox.question(self, 'Supprimer Playlist', f'Voulez vous supprimer la playlist : {nom_play} ')
        if self.message == QMessageBox.Yes:
            subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py del_playlist '{self.utilisateur}' '{nom_play}' "])
        self.poppup.close()
    
    def music_in_playlist(self):
        """
        Choisi la musique à ajouter dans la playlist
        """
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', "python3 /home/couzinier/clone/Spotifree/main_server.py search_musique ''"])
        ssh_stdout = eval(ssh_stdout)
        musique = []
        print(ssh_stdout)
        for m in ssh_stdout:
            musique.append(m[1])
        self.poppup_ch = poppupChoix(musique)
        self.poppup_ch.bt_valider.clicked.connect(self.add_mus_play)
        
    
    def add_mus_play(self):
        """
        Ajoute une musique dans la playlist
        """
        nom_play = self.poppup.list.currentItem().text()
        nom_musique = self.poppup_ch.list.currentItem().text()
        
        subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py add_musique_play '{self.utilisateur}' '{nom_play}' '{nom_musique}' "])

        self.poppup.close()
        self.poppup_ch.close()
        

    def download_music(self, nom):
        """
        Télecharge une musique sur le client 
        """
        
        if not os.path.exists(f"/home/couzinier/clone/Spotifree/musique/{nom}"):
            HOSTNAME = "127.0.0.1"
            USERNAME = "couzinier"
            PASSWORD = "motdepasse"
            ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
            os.system(f"mkdir /home/couzinier/clone/Spotifree/musique/'{nom}'")
            QApplication.setOverrideCursor(Qt.WaitCursor)
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py download '{nom}'"]).decode().replace('\n', '')
            nom_file = ssh_stdout.replace("serveur", 'musique')
            

            QApplication.restoreOverrideCursor()
            self.poppup.close()
            QMessageBox.about(self, 'Fini', f"Le téléchargement de : {nom} est fini")
            
            with open(nom_file, "wb") as file:
            # Command for Downloading the file "RETR filename"
                ftp_server.retrbinary(f"RETR {ssh_stdout}", file.write)


    def serv_download(self):
        """
        Télécharge une musique sur le serveur avec spotify_dl
        """
        QApplication.setOverrideCursor(Qt.WaitCursor)
        nom = self.poppup.list.currentItem().text().split(" : ")[1]
        
        for dct in self.liste_musique:
            if dct['musique'] == nom:
                nom_musique = dct["musique"]
                artiste = dct["artiste"]
                album = dct["album"]
                lien = dct["lien"]
        
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py serv_dwld '{nom_musique}' '{artiste}' '{album}' '{lien}'"]).decode().replace('\n', '')
        
        QApplication.restoreOverrideCursor()
        self.download_music(ssh_stdout)
        self.poppup.close()
        
        
    def download_playlist(self):
        """
        Télécharge une playlist présente sur le serveur
        """
        nom_play = self.poppup.list.currentItem().text()
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py musique_in_playlist '{self.utilisateur}' '{nom_play}'"])
        ssh_stdout = eval(ssh_stdout)
        musique = []
        print(ssh_stdout)
        for m in ssh_stdout:
            musique.append(self.chemin_musique(m[0].replace(r'/', "")))
            print(m[0])
            self.download_music(m[0].replace(r'/', ""))
        self.poppup.close()
        self.lancer_musique(musique)


    def clearAll(self, objet):
        """
        Fonction permettant de supprimer ce qui se trouve dans un objet  Qt
        argument :
        objet -> QT objet, c'est l'objet à supprimer
        """
        if isinstance(objet, QWidget):
            self.clearObject(objet)
        else:
            self.clearLayout(objet)
        
    def clearObject(self, objet):
        """
        Fonction permettant de supprimer ce qui se trouve dans un objet enfant d'un parent Qt
        argument :
        objet -> QT objet, c'est l'objet à vider
        """
        widgets = objet.children()
        for widget in widgets:
            self.clearObject(widget)
            sip.delete(widget)  
            
    def clearLayout(self, layout):
        """
        Fonction permettant de supprimer ce qui se trouve dans un layout  Qt
        argument :
        objet -> QT layout, c'est le layout à supprimer
        """
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget is not None:
                layout.removeWidget(widget)
                widget.setParent(None)
            else:
                if type(item) == QSpacerItem:
                    layout.removeItem(item)
                    sip.delete(item)
                else:
                    self.clearLayout(item.layout())
                    sip.delete(item)  
                    
            
class poppupChoix(QMainWindow):
    """
    Classe de la poppup de choix des chansons
    """
    def __init__(self, musiques):
        """
        Fonction d'initialisation de la poppup
        argument :
        musique -> dict, contient la liste eds musiques à choisir
        """
        QMainWindow.__init__(self)
        self.initUi(musiques)
        self.show()
        
        
    def initUi(self, musiques):
        """
        Fonction permettant de génerer l'interface
        argument :
        musique -> dict, contient la liste eds musiques à choisir
        """
        self.resize(500, 500)
        self.setWindowTitle("Choix musique")
        # Création du widget central
        self.centralW = QWidget(parent=self)
        self.setCentralWidget(self.centralW)
        
        # Création des boutons
        self.bt_valider = QPushButton("Valider")
        self.bt_annuler = QPushButton("Annuler")
        self.bt_annuler.clicked.connect(lambda: self.close())
        
        # Création d'une liste
        
        self.list = QListWidget()
        for dct in musiques:
            if type(dct) == str:
                if len(dct.split(r'/')) == 4:
                    self.list.addItem(dct.split(r'/')[3])
                elif len(dct.split(r'/')) == 1:
                    self.list.addItem(dct)
                    
            elif type(dct) == dict:
                self.list.addItem(dct["artiste"] + " : " + dct["musique"])
        
        # Création des layout
        h_bt = QHBoxLayout()
        h_bt.addWidget(self.bt_valider)
        h_bt.addWidget(self.bt_annuler)
        
        
        v_main = QVBoxLayout()
        v_main.addWidget(self.list)
        v_main.addLayout(h_bt)
        
        self.centralW.setLayout(v_main)



class identfiant(QMainWindow):
    """
    Class premettant de créer une poppupde connexion pour l'utilisateur
    """
    def __init__(self):
        """
        Fonction d'initialisation de la poppup
        """
        QMainWindow.__init__(self)
        self.initUi()
        self.show()
        
        
    def initUi(self):
        """
        Fonction permettant de génerer l'interface
        """
        self.resize(250, 250)
        self.setWindowTitle("Connexion")
        # Création du widget central
        self.centralW = QWidget(parent=self)
        self.setCentralWidget(self.centralW)
        
        # Création des label
        label_user = QLabel("Nom d'utilisateur")
        label_mdp = QLabel("Mot de passe")
        
        # Création des boutons
        self.bt_valid = QPushButton('Connexion')
        self.bt_inscription = QPushButton('Inscription')
        
        # Création des line edit
        self.line_user = QLineEdit()
        self.line_user.setText('CyrilC')
        self.line_mdp = QLineEdit()
        self.line_mdp.setText('cyril')
        self.line_mdp.setEchoMode(QLineEdit.Password)
        
        # définir les layouts
        v_user = QVBoxLayout()
        v_user.addWidget(label_user)
        v_user.addWidget(self.line_user)
        v_user.addStretch()
        
        v_mdp = QVBoxLayout()
        v_mdp.addWidget(label_mdp)
        v_mdp.addWidget(self.line_mdp)
        v_mdp.addStretch()
        
        h_btp = QHBoxLayout()
        h_btp.addWidget(self.bt_valid)
        h_btp.addWidget(self.bt_inscription)
        
        v_main = QVBoxLayout()
        v_main.addLayout(v_user)
        v_main.addLayout(v_mdp)
        v_main.addLayout(h_btp)
        
        self.centralW.setLayout(v_main)


class playlist(QMainWindow):
    """
    Classe de la poppup des playlist
    """
    def __init__(self, playlist, utilisateur):
        """
        Fonction d'initialisation de la poppup
        argument :
        musique -> list, contient la liste des playlist
        """
        QMainWindow.__init__(self)
        self.initUi(playlist, utilisateur)
        self.show()
        
        
    def initUi(self, playlist, utilisateur):
        """
        Fonction permettant de génerer l'interface
        argument :
        musique -> list, contient la liste des playlist
        """
        self.user = utilisateur
        self.resize(500, 500)
        self.setWindowTitle("Choix musique")
        # Création du widget central
        self.centralW = QWidget(parent=self)
        self.setCentralWidget(self.centralW)
        
        # Création des boutons
        self.bt_valider = QPushButton("Valider")
        self.bt_annuler = QPushButton("Annuler")
        self.bt_annuler.clicked.connect(lambda: self.close())
        
        # Création d'une liste
        self.list = QListWidget()
        for dct in playlist:
            item = dct[2]
            self.list.addItem(item)
        self.list.itemClicked.connect(self.show_music)
            
        # Création du text edit
        self.edit = QTextEdit()
        
        # Création des layout
        h_bt = QHBoxLayout()
        h_bt.addWidget(self.bt_valider)
        h_bt.addWidget(self.bt_annuler)
        
        h_affichage = QHBoxLayout()
        h_affichage.addWidget(self.list)
        h_affichage.addWidget(self.edit)
        
        v_main = QVBoxLayout()
        v_main.addLayout(h_affichage)
        v_main.addLayout(h_bt)
        
        self.centralW.setLayout(v_main)        

    def show_music(self):
        """
        Montre les musique dans une playlist
        """
        self.nom_playlist = self.list.currentItem().text()
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py musique_in_playlist '{self.user}' '{self.nom_playlist}'"])
        ssh_stdout = eval(ssh_stdout)
        text = 'Musique :\n'
        for e in ssh_stdout:
            text += "- " + e[0] +"\n"
        
        self.edit.setText(text)







# Afficher la fenetre
if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = mainUi()
    app.exec()      
