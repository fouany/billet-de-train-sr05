```
# instance site guichet G
definition validerListeBillets(M : messageAccuseReception)
    si M.reponse == 'refuser'
        G.annulerReservationBillets
    sinon:
        G.supprimerListeMessageAttente(M.identifiantMessageRecu)
fin definition
```