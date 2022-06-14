#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:07:45 2022

@author: couzinier
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QComboBox, QListWidget, QMessageBox, QSpacerItem, QScrollBar)

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sys
from PyQt5.QtGui import QIcon
import spoti
import sip
import os


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
        self.show()
        
    def initUi(self):
        """
        Fonction créant les widgets de la fenetre
        """
        self.resize(500, 500)
        self.setWindowTitle("Spotifree")
        # Création du widget central
        self.centralW = QWidget(parent=self)
        self.setCentralWidget(self.centralW)
        
        # Création des boutons
        button = QPushButton(QIcon('icones/recherche.png'), "")
        button.clicked.connect(self.recherche)
        
        # Création du menu déroulant
        self.combo_recherche = QComboBox()
        self.combo_recherche.addItem('Musique')
        self.combo_recherche.addItem('Playlist')
        self.combo_recherche.addItem('Ami')
        
        # Création des line edit
        self.line_edit = QLineEdit()
        
        # Création des Layout
        h_recherche = QHBoxLayout()
        h_recherche.addWidget(self.line_edit)
        h_recherche.addWidget(self.combo_recherche)
        h_recherche.addWidget(button)
        
        self.v_main = QVBoxLayout()
        self.v_main.addLayout(h_recherche)
        self.v_main.addStretch()
        
        self.centralW.setLayout(self.v_main)
        
        
    def recherche(self):
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
                
                
    def musique_choisi(self, recherche):
        """
        Fonction récupérant la musique choisi et la télécharge
        arugument:
        recherche -> str contenant la musique choisi aison que son lien 
        """
        item = self.poppup.list.currentItem()
        self.poppup.close()
        artiste = item.text().split(' : ')[0]
        nom = item.text().split(' : ')[1]
        lien = item.text().split(' : ')[2]
        print(artiste, nom, lien)
        commande = f"spotify_dl -l {lien} -o musique"
        os.system(commande)
        
        chemin = "musique/" + nom + "/" + artiste + ' - ' + nom + ".mp3"
        os.system(f"chmod +x '{chemin}'")
        
        self.lancer_musique(chemin)
        
        
    def lancer_musique(self, chemin):
        """
        Fonction permettant le lancer une musique 
        chemin -> str, chemin vers la musique
        """
        # Création des boutons
        self.bt_play = QPushButton(QIcon("icones/play.jpg"), '')
        self.bt_play.clicked.connect(self.play)
        
        
        self.bt_pause = QPushButton(QIcon("icones/pause.jpg"), "")
        self.bt_pause.clicked.connect(self.pause)
        self.bt_pause.setEnabled(False)
        
        self.bt_stop = QPushButton(QIcon("icones/stop.png"), '')
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
        
        self.v_musique = QVBoxLayout()
        self.v_musique.addLayout(h_btp)
        self.v_musique.addLayout(h_son)
        
        self.v_main.addLayout(self.v_musique)
        
        
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
            item = dct["artiste"] + " : " + dct["musique"] + " : " + dct["lien"]
            self.list.addItem(item)
            
        # Création des layout
        h_bt = QHBoxLayout()
        h_bt.addWidget(self.bt_valider)
        h_bt.addWidget(self.bt_annuler)
        
        
        v_main = QVBoxLayout()
        v_main.addWidget(self.list)
        v_main.addLayout(h_bt)
        
        self.centralW.setLayout(v_main)

    

        


# Afficher la fenetre
if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_app = mainUi()
    app.exec()      
