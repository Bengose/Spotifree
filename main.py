#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:07:45 2022

@author: couzinier
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QComboBox, QListWidget, QMessageBox, QSpacerItem, QLabel, QApplication,
                             QAction, QTextEdit, QTabWidget)

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt
import sys
from PyQt5.QtGui import QIcon, QPixmap
import spoti
import sip
import os
import subprocess



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
        
        # Création d'une icone
        label_icon = QLabel()
        label_icon.setPixmap(QPixmap('icones/spotifree.svg').scaled(400,400, Qt.AspectRatioMode.KeepAspectRatio))
        
        # Création des tab widgets
        self.tabs = QTabWidget(parent=self)
        self.tabs.addTab(QWidget(), 'Ecouter une musique')
        self.tabs.addTab(self.centralW, 'Télecharger une musique')
        
        self.setCentralWidget(self.tabs)
        
        # Création des boutons
        self.button = QPushButton(QIcon('icones/recherche.png'), "")
        self.button.clicked.connect(self.recherche)
        
        # Création du menu déroulant
        self.combo_recherche = QComboBox()
        self.combo_recherche.addItem('Musique')
        self.combo_recherche.addItem('Playlist')
        self.combo_recherche.addItem('Ami')
        
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
        
        # Layout de la gestion des sons
        self.v_musique = QVBoxLayout()
        
        # Création des Layout
        h_recherche = QHBoxLayout()
        h_recherche.addWidget(self.line_edit)
        h_recherche.addWidget(self.combo_recherche)
        h_recherche.addWidget(self.button)
        
        self.v_main = QVBoxLayout()
        self.v_main.addWidget(label_icon)
        self.v_main.addLayout(h_recherche)
        self.v_main.addStretch()
        self.v_main.addLayout(self.v_musique)
        
        self.centralW.setLayout(self.v_main)
        
    def recherche(self):
        recherche = self.line_edit.text()
        tpe = self.combo_recherche.currentText()
        if tpe == "Musique":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py musique_dispo '{recherche}' "]).decode("utf-8")
            print(ssh_stdout)
            self.poppup = poppupChoix(ssh_stdout.split("\n"))
        
    def recherche_old(self):
        """
        Fonction permettant de rechercher une musique
        """
        recherche = self.line_edit.text()
        tpe = self.combo_recherche.currentText()
        if tpe == "Musique":
            recherche = spoti.recherche_musique(recherche, "track")
            if  recherche == "Erreur pas de musique trouvé":
                QMessageBox.warning(self, "Erreur de recherche", recherche)
            else:
                self.poppup = poppupChoix(recherche)
                self.poppup.bt_valider.clicked.connect(lambda: self.musique_choisi(recherche))
        
        elif tpe == "Playlist":
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py playlist '{recherche}' '{self.utilisateur}' "]).decode("utf-8")
            ssh_stdout = eval(ssh_stdout)
            
            self.poppup_playlist = playlist(ssh_stdout, self.utilisateur)
                
        elif tpe == "Ami":
            pass
                
    def musique_choisi(self, recherche):
        """
        Fonction récupérant la musique choisi et la télécharge
        arugument:
        recherche -> str contenant la musique choisi ainsi que son lien 
        """
        item = self.poppup.list.currentItem()
        self.poppup.close()
        artiste = item.text().split(' : ')[0].replace("'", " ")
        nom = item.text().split(' : ')[1].replace("'", " ")
        album = item.text().split(' : ')[2].replace("'", " ")
        lien = item.text().split(' : ')[3].replace("'", " ")
        print(artiste)
        print(nom)
        print(album)
        print(lien)
        
        self.download_music(lien, nom)
        
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"""python3 /home/couzinier/clone/Spotifree/main_server.py search_musique "{nom}\" """])
        
        if ssh_stdout == b'[]\n':
            ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"""python3 /home/couzinier/clone/Spotifree/main_server.py add_musique "{nom}" "{artiste}" "{album}" '{lien}'"""])
        
        chemin = "musique/{self.last_musique}/*.mp3"
        #"musique/" + nom + "/" + artiste + ' - ' + nom + ".mp3"
        os.system(f"chmod +x 'musique/{self.last_musique}/*.mp3'")
        
        self.lancer_musique(chemin)
        
        
    def lancer_musique(self, chemin):
        """
        Fonction permettant le lancer une musique 
        chemin -> str, chemin vers la musique
        """
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
        
        self.bt_plus = QPushButton('+')
        self.bt_plus.clicked.connect(self.plus)
        
        self.bt_moins = QPushButton('-')
        self.bt_moins.clicked.connect(self.moins)
        
        # Création du média player
        self.player = QMediaPlayer()
        path = os.path.join(os.getcwd(), chemin)
        url = QUrl.fromLocalFile(path)
        content = QMediaContent(url)
        self.player.setVolume(50)
        
        self.player.setMedia(content)
        
        # Création de la scroll bar
        # self.scrol = QScrollBar()
        # self.scrol.setMaximum(100)
        # self.scrol.resize(100, 5)
        
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
        
        
    def plus(self):
        """
        Fonction permettant de monter le son
        """
        self.player.setVolume(self.player.volume() + 5)
        
        
    def moins(self):
        """
        Fonction permettant de baisser le son
        """
        self.player.setVolume(self.player.volume() - 5)
 
          
    def identifiant(self):
        self.ident = identfiant()
        self.ident.bt_valid.clicked.connect(self.connexion)
        self.ident.bt_inscription.clicked.connect(self.inscription)
        
        
    def connexion(self):
        self.utilisateur = self.ident.line_user.text()
        
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py verifie '{self.utilisateur}' '{self.ident.line_mdp.text()}'"])
        
        if ssh_stdout == b'True\n':
            self.ident.close()
        
        self.combo_recherche.setEnabled(True)
        self.button.setEnabled(True)
        self.line_edit.setEnabled(True)
        
        print(ssh_stdout)


    def inscription(self):
        self.utilisateur = self.ident.line_user.text()
        
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py new_user '{self.utilisateur}' '{self.ident.line_mdp.text()}'"])
        
        if ssh_stdout == b'tout va bien\n':
            self.ident.close()
        
        self.combo_recherche.setEnabled(True)
        self.button.setEnabled(True)
        self.line_edit.setEnabled(True)
        
        print(ssh_stdout)


    def download_music(self, lien, nom_musique):
        
        if not os.path.exists(f"musique/'{nom_musique}'"):
            commande = f"spotify_dl -l {lien} -o musique"
            subprocess.check_output(commande, shell=True).decode()
            #commande = "ls -t musique | head -n1"
            #self.last_musique = subprocess.check_output(commande, shell=True).decode().replace(r"\n", '')
            #os.system(commande)


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
            if len(dct.split(r'/')) == 4:
                self.list.addItem(dct.split(r'/')[3])
            
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
        self.nom_playlist = self.list.currentItem().text()
        ssh_stdout = subprocess.check_output(['ssh', '127.0.0.1', f"python3 /home/couzinier/clone/Spotifree/main_server.py musique_in_playlist '{self.user}' '{self.nom_playlist}'"])
        ssh_stdout = eval(ssh_stdout)
        print(ssh_stdout)
        text = 'Musique :\n'
        for e in ssh_stdout:
            text += "- " + e[0] +"\n"
        
        self.edit.setText(text)







# Afficher la fenetre
if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = mainUi()
    app.exec()      
