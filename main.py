#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:07:45 2022

@author: couzinier
"""

from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLineEdit, QComboBox, QListWidget, QMessageBox, QSpacerItem)

import sys
from PyQt5.QtGui import QIcon
import spoti
import sip
import os


class mainUi(QMainWindow):
    def __init__(self):
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
        
        v_main = QVBoxLayout()
        v_main.addLayout(h_recherche)
        v_main.addStretch()
        
        self.centralW.setLayout(v_main)
        
        
    def recherche(self):
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
        item = self.poppup.list.currentItem()
        self.poppup.close()
        artiste = item.text().split(' : ')[0]
        nom = item.text().split(' : ')[1]
        lien = item.text().split(' : ')[2]
        print(artiste, nom, lien)
        commande = f"spotify_dl -l {lien} -o musique"
        os.system(commande)
        
        chemin = nom + "/" + artiste + ' - ' + nom + ".mp3"
        self.lancer_musique(chemin)
        
        
    def lancer_musique(self):
        pass
        
                
                
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
    def __init__(self, musiques):
        QMainWindow.__init__(self)
        self.initUi(musiques)
        self.show()
        
        
    def initUi(self, musiques):
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
