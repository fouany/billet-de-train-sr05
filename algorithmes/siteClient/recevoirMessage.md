```
# instance site client C, thread associé à la réception du site S
definition recevoirMessage() : message
    faire
        soit M : message
        M = recevoir(S)
        si M.clientDemandeur = C alors
            arreterThreadDelaiMaxAttenteReponse(M.identifiant)
        sinon alors
            transfererMessageSaufSite(M,S)
        fin si
    tant que M.clientDemandeur != C
    retourner M
fin definition
```