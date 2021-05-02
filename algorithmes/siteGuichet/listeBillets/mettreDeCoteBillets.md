```
# instance site guichet G
definition mettreDeCoteBillets(M : messageAvecBillets)
    G.enleverListeBilletsDisponibles(M.billets)
    G.ajouterListeMessageAttente(M.identifiant, M)
    
fin definition
```