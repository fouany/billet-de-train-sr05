```
# instance site client C, thread associé à la réception du site S
definition recevoirMessage() : message
    faire
        soit M : message
        M = recevoir(S)
        si M.type = 'reponse' et M.clientDemandeur = C alors
            arreterThreadDelaiMaxAttenteReponse(M.identifiant)
        sinon si M instancie messageDemandeSnapshot et C.snapshotActive alors
            C.snapshotActive = faux
            lancerThreadDemandeSnapshot(M,S)
        sinon si M instancie messageResetSnapshot et C.snapshotActive = faux alors
            C.snapshotActive = vrai
            lancerThreadResetSnapshot(M,S)
        sinon si M.clientDemandeur != C alors
            transfererMessageSaufSite(M,S)
        fin si
    tant que M.type != reponse ou M.clientDemandeur != C
    retourner M
fin definition
```