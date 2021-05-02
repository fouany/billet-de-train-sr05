#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg

id_message_seq = 0

class Message(apg.msg.Message):
    """Application-specific abstract message"""
    def __init__(self, text, app, nseq=None, lmp=None, clientDemandeur=None, clientDestinataire=None, instance='default'):
        super().__init__(text, app)
        self.fields += ["instance","nseq","lmp","id","clientDemandeur","clientDestinataire"]
        global id_message_seq
        id_message_seq += 1
        self.content["id"] = id_message_seq
        if instance != None:
            self.content["instance"] = instance
        if nseq != None :
            self.content["nseq"] = nseq
        if lmp != None :
            self.content["lmp"] = lmp
        if clientDemandeur !=None:
            self.content["clientDemandeur"] = clientDemandeur
        if clientDestinataire !=None:
            self.content["clientDestinataire"] = clientDestinataire
        if len(text) > 0:
            self.parse_text(text)
    def instance(self):
        return self.content["instance"]
    def id(self):
        return self.content["id"]
    def nseq(self):
        return self.content["nseq"]
    def lmp(self):
        return self.content["lmp"]
    def incLmp(self):
        self.content["lmp"] = str(int(self.content["lmp"]) + 1)
    def clientDemandeur(self):
        return self.content["clientDemandeur"]
    def clientDestinataire(self):
        return self.content["clientDestinataire"]

class MessageDemande(Message):
    """Application-specific message MessageDemande"""
    def __init__(self, text, app, nseq=None, lmp=None, clientDemandeur=None, typeDemande='consultation', infoBillet=""):
        super().__init__(text,app,nseq,lmp,clientDemandeur,clientDestinataire="node1",instance="MessageDemande")
        self.fields += ["typeDemande","infoBillet"]
        self.content["typeDemande"] = typeDemande
        if infoBillet != None:
            self.content["infoBillet"] = infoBillet
        if len(text) > 0:
            self.parse_text(text)
    def typeDemande(self):
        return self.content["typeDemande"]
    def infoBillet(self):
        return self.content["infoBillet"]

class MessageAccuseReception(Message):
    """Application-specific message MessageAccuseReception"""
    def __init__(self, text, app, nseq=None, lmp=None, clientDemandeur=None, identifiantMessageRecu=None):
        super().__init__(text,app,nseq,lmp,clientDemandeur,clientDestinataire="node1",instance="MessageAccuseReception")
        self.fields += ["identifiantMessageRecu"]
        self.content["identifiantMessageRecu"] = identifiantMessageRecu
        if len(text) > 0:
            self.parse_text(text)
    def identifiantMessageRecu(self):
        return self.content["identifiantMessageRecu"]

# definition messageAvecBillets herite message
#     typeDemande : 'consultation' ou 'reservation'
#     billets : billet[]
# fin definition


class MessageAvecBillets(Message):
    """Application-specific message MessageDemande"""
    def __init__(self, text, app, nseq=None, lmp=None, clientDemandeur=None, typeDemande='consultation', listeBillet=[]):
        super().__init__(text,app,nseq,lmp,clientDemandeur,clientDestinataire="CLT3",instance="MessageAvecBillets")
        self.fields += ["typeDemande","listeBillet"]
        self.content["typeDemande"] = typeDemande
        self.content["listeBillet"] = listeBillet
        if len(text) > 0:
            self.parse_text(text)
    def typeDemande(self):
        return self.content["typeDemande"]
    def listeBillet(self):
        return self.content["listeBillet"]
