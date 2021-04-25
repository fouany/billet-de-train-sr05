```
# instance du site client C
definition envoyerMessage(M : message, S : site)
    si C.voisins contient S alors
        envoyer(M,S)
        lancerThreadDelaiMaxAttenteReponse(M.identifiant)
    sinon alors
        emettre exception
    fin si
fin definition


definition envoyerMessage(M : message, S_tab : site[])
    soit clefEnvoye : booleen
    clefEnvoye = faux
    Pour S parmi S_tab faire
        si C.voisins contient S alors
            envoyer(M,S)
            clefEnvoye = vrai
        fin si
    fin pour
    si clefEnvoye alors
        lancerThreadDelaiMaxAttenteReponse(M.identifiant)
    sinon alors
        emettre exception
    fin si
fin definition    
```