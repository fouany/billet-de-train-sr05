```
# instance site guichet G
definition validerListeBillets(M : messageAccuseReception)
    arreterDelaiMaxAttenteReservation(M.identifiantMessageRecu)
    G.supprimerListeMessageAttente(M.identifiantMessageRecu)
fin definition
```