```
# instance site guichet G
definition annulerReservationBillets(identifiantMessage : nombre)
    arreterDelaiMaxAttenteReservation(identifiantMessage)
    soit M : messageAvecBillets
    M = obtenirListeMessageAttente(identifiantMessage)
    G.ajouterListeBilletsDisponibles(M.billets)
    G.supprimerListeMessageAttente(identifiantMessage)
fin definition
```