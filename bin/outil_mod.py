
def GetPayload(msg):
    n=ligne.find('payload')
    msg=msg[n+8:]
    m=msg.find('^')
    msg=msg[:m]
    return msg

# ligne="^appnet~CTL^clientDemendeur~NET^clientTransmetteur~Net^Imp~5^nseq~5^payload~Hello Word^type~requete^typeDemande~consultation^"
# print (GetPayload(ligne))
