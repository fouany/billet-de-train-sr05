```
# instance du site guichet G
definition repondreMessage(M : message, S : site)
    M.clientTransmetteur = G
    M.type = 'reponse'
    si G.voisins contient S alors
        envoyer(M,S)
    sinon alors
        emettre exception
    fin si
fin definition
```