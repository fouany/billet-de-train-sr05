```
# instance site client C, thread associé à la réception du site S
definition faireReceptionListeBillets(M : messageAvecBillets)
    si M.billets est vide alors
        afficher('Pas de billets correspondant')
    sinon alors
        si M.typeDemande = 'consultation' alors
            afficher('Billets disponibles correspondants :')
        sinon alors
            afficher('Vous avez réservé :')
            faireAccuseReceptionListeBillets(M.identifiant)
            C.ajouterBillets(M.billets)
        fin si
        pour b parmi M.billets faire
            afficher(b)
        fin pour
    fin si
fin definition
```