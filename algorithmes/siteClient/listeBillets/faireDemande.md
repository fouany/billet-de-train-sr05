```
# instance site C, C est le terminal demandeur
definition faireDemandeListeBillets(typeDemande : 'consultation' ou 'reservation')
    soit M : messageDemande
    M.typeDemande = typeDemande
    M.type = 'requete'
    faireEntrerLesInfosALUtilisateur(M)
    envoyerMessage(M)
fin definition
```