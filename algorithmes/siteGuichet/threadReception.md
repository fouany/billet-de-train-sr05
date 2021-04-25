```
#instance site guichet G, thread associé au site S
definition threadReception
    tant que toujours faire
        soit M : message
        M = recevoirMessage()
        si M instancie messageDemande alors
            repondreListeBillets(M)
        si M instancie messageAccuseReception alors
            validerListeBillets(M)
        si M instancie messageSnapshot alors
            completerSnapshotAvecClient(M)
        sinon alors
            emettre exception
        fin si
    fin tant que
fin threadReception
```