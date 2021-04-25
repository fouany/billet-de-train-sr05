```
# instance site C, C est le terminal demandeur
definition faireAccuseReceptionListeBillets(identifiantMessageRecu : nombre)
    soit M : messageAccuseRecpetion
    M.identifiantMessageRecu = identifiantMessageRecu
    envoyerMessage(M)
fin definition
```