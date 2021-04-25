```
# instance du site client C
definition envoyerMessage(M : message, S : site)
    M.clientDemandeur = C
    M.clientTransmetteur = C
    si M.type = 'requete' et C.voisins contient S alors
        envoyer(M,S)
        lancerThreadDelaiMaxAttenteReponse(M.identifiant)
    sinon alors
        emettre exception
    fin si
fin definition
```