```
#instance site client C, thread associé au site S
definition threadReception
    tant que toujours faire
        soit M : message
        M = recevoirMessage()
        si M instancie messageAvecBillets alors
            faireReceptionListeBillets(M)
        si ...
        sinon alors
            emettre exception
        fin si
    fin tant que
fin threadReception
```