# Projet SR05 - Billet de train
## Structure du projet
Le projet est basé sur la structure de Airplug et ajoute :
* Un dossier CLTPY qui contient le code pour les clients qui souhaitent réserver des billets de train.<br>
* Un dossier GCHpy qui contient le code pour le guichet qui est unique et qui possède les billets.<br>
* De modules supplémentaires inclus dans le dossier LIBAPG

Ces derniers contiennent un module pour les billets, les messages et les outils.
## Utilisation
Pour lancer l'application, il faut aller dans le bin et exécuter successivement :
```
source config.sh
chmod +x updateGCH.sh
chmod +x updateCLT.sh
./updateCLT.sh && ./updateGCh.sh
```
Ensuite il faut choisir une des trois topologies :
```
chmod +x 10-ringUNI.sh
./10-ringUNI.sh
```
```
chmod +x 10-ringUNI.sh
 ./Y-6sommets.sh
```
```
chmod +x topoquelconque.sh
./topoquelconque.sh
```
Une fois l'application lancée, il suffit de prendre l'interface d'un des clients et de tester les commandes. 
<br> On peut consulter les billets disponibles répondant à certains critères, on peut également réserver ces derniers. Une fois réservés, on peut consulter les billets que l'on possède.<br><br>
Via l'interface du guichet, on peut consulter les billets que ces derniers possèdent. On peut également lancer une snapshot.
