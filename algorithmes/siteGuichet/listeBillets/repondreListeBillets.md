```
# instance site guichet G
definition repondreListeBillets(M : messageDemande)
    soit R : messageAvecBillets
    R.billets = obtenirBilletsDepuisInfo(M.infoBillet)
    R.typeDemande = M.typeDemande
    si R.typeDemande = 'reservation' alors
        mettreDeCoteBillets(R)
    fin si
    R.clientRecepteur = M.clientDemandeur
    repondreMessage(R,R.clientRecepteur)
fin definition
```