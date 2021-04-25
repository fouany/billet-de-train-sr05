```
# instance site C
definition transfererMessageSaufSite(M : message, S : site)
    M.clientTransmetteur = C
    pour Cible parmi C.voisins faire
        si Cible != S alors
            envoyer(M,Cible)
        fin si
    fin pour
fin definition
```