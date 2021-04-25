```
# instance site C, C est le terminal demandeur
definition faireDemandeListeBillets()
    soit M : messageDemande
    M.typeDemande = 'consultation'
    M.type = 'requete'
    faireEntrerLesInfosALUtilisateur(M)
    envoyerMessage(M)
fin definition
```