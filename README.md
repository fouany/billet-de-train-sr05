
Nom du projet : Réservation de billets de Train

Langage : Python

-> AIRPLUG

Un site qui détient les informations les billets reservables. (GUICHET)

Les autres sites qui demandent les billets dispos à une date donnée et une destination (CLIENTS)
-> On envoie les billets de train au site qui a réservé.
-> Attente de confirmation du billet, Si prise de trop de temps, on remet le billet en circulation.
-> Après la confirmation, ce n'est plus le site principal qui détient le billet mais le site qui l'a réservé.

Un billet :
-> identifiant
-> date et heure
-> départ
-> destination
-> détenteur
-> (coût)

Un guichet :
-> nom (unique)
-> estampille
-> Liste de billets disponibles
-> Liste de billets en attente de confirmation de réception, puis supprimé
-> séquence d'identifiant
=> CRUD Billet
=> Réception de message d'information
=> Effectuer / Charger une snapshot

Un client :
-> nom (unique)
-> estampille
-> Liste de billets possédés
-> liste des voisins les plus proches
=> Envoi de message demandant inf sur billet (départ, destination, horaire)
=> Envoi de confirmation de réservation
=> Envoi de confirmation de réception
=> Réception de billet
=> Réception de demande de confirmation
=> Effectuer / Charger une snapshot

Un message de demande réservation/consultation  (client_initial -> ... -> client -> guichet):
-> client transmettant
-> client demandeur
-> infos liées au billet
-> boolean réservation/consultation

Un message avec billet (guichet -> client -> ... -> client_final):
-> client/guichet transmettant
-> client demandeur
-> billet

Un message accusé-réception réservation billet (client_initial -> ... -> client -> guichet):
-> client transmettant
-> client demandeur
-> identifiant billet

Un message snapshot (client_initial -> ... -> client -> guichet):
-> client transmettant
-> info client propriétaire de la snapshot

Un message reset snapshot (guichet -> client -> ... -> client_final):
-> client/guichet transmettant

Tout les messages sont de la forme (contenu + estampille)

TO-DO:
-> Estampille
-> Snapshot
-> README utilisation sous linux et structure architecture
-> Diapo (PDF) pour la soutenance (checker réponse prof)
