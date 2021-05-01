#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg


class Message(apg.msg.Message):
    """Application-specific abstract message"""
    def __init__(self, text, app, payload=None, nseq=None, lmp=None, clientDemandeur=None, clientTransmetteur=None, type='requete'):
        super().__init__(text, app)
        self.fields += ["payload","nseq","lmp","clientDemandeur","clientTransmetteur","type"]
        if payload != None:
            self.content["payload"] = payload
        if nseq != None :
            self.content["nseq"] = nseq
        if lmp != None :
            self.content["lmp"] = lmp
        if clientDemandeur !=None:
            self.content["clientDemandeur"] = clientDemandeur
        if clientDemandeur !=None:
            self.content["clientTransmetteur"] = clientTransmetteur
        self.content["type"] = type
        if len(text) > 0:
            self.parse_text(text)
    def payload(self):
        return self.content["payload"]
    def nseq(self):
        return self.content["nseq"]
    def lmp(self):
        return self.content["lmp"]
    def clientDemandeur(self):
        return self.content["clientDemandeur"]
    def clientTransmetteur(self):
        return self.content["clientTransmetteur"]

class MessageDemande(Message):
    """Application-specific message MessageDemande"""
    def __init__(self, text, app, payload=None, nseq=None, lmp=None, clientDemandeur=None, clientTransmetteur=None, type='requete', typeDemande='consultation', infoBillet=None):
        super().__init__(text,app,payload,nseq,lmp,clientDemandeur,clientTransmetteur,type)
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
