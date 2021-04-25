```
# instance site C
definition transfererMessageSaufSite(M : message, S : site)
    pour Cible parmi C.voisins faire
        si Cible != S alors
            envoyer(M,Cible)
        fin si
    fin pour
fin definition
```