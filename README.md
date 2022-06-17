Exercice Spotifree

Auteur : Cyril MARTINEZ-MATOSES, Rania AYACHI, Baptiste CARDOSO, Bastien BOUDOU, Cyril COUZINIER

But :
Le but du logiciel est de lancer des musiques / des playlist demandées par l'utilisateur.
Celui-ci doit se connecter au lancement du logiciel.
L'utilisateur peut avoir des amis avec qui échanger ses playlist
Les musiques sont recherché grace à l'API Spotify


installation :

Charger la base de donnée :
	- Créer une base de donnée spotifree
	- Charger le fichier avec la commande : mariadb -u user_name -p spotifree < spotifree.sql

Dans le fichier main_serveur.py changer la variable dossier_serv (ligne 16) par le chemin ou on veut stocker les musiques sur le serveur.
Dans le fichier main.py changer les 3 variables lignes 34 a 36 avec l'ip, l'utilisateur et le mot de passe du serveur
Dans le fichier recherche_bdd.py changer les paramètre de connexion à la base de donnée (ligne 14 a 17)


Installez les modules python avec la commande : 
pip3 install -r requirements.txt

Et installer le module ffmpeg avec la commande : 
sudo apt install ffmpeg
sudo apt install libqt5multimedia5-plugins
sudo apt-get install qtgstreamer-plugins-qt5


Fonctionnement :
Au lancement du programme main.py l'interface graphique apparait et nous permet de choisir entre 3 onglets différents :
	1 : Ecouter une musique -> permet d'écouter des musiques ou des playlists 
	2 : Télecharger une musique -> permet de télécharger une musique ou de gérer les playlist
	3 : Amis -> permet de gérer les amis

Travail à réaliser :
Faire l'échange de playlist avec des amis (fonction bdd déjà faite, manque intégration)
Faire un proxy nginx pour la connexion ftp
Faire Jenkins
