
def GetInstance(msg):
    return GetNode(msg,'instance')

def GetNode(msg,type):
    n=msg.find(type)
    msg=msg[n+len(type)+1:]
    m=msg.find('^')
    msg=msg[:m]
    return msg
# ligne="^appnet~CTL^clientDemendeur~NET^clientTransmetteur~Net^Imp~5^nseq~5^instance~Hello Word^type~requete^typeDemande~consultation^"
# print (GetNode(ligne,'clientTransmetteur'))
