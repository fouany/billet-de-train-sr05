```
# instance site guichet G, thread associé à la réception du site S
definition recevoirMessage() : message
    faire
        soit M : message
        M = recevoir(S)
    tant que M.type != requete
    retourner M
fin definition
```