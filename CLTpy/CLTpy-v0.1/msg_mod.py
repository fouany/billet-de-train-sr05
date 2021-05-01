#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg

id_message_seq = 0

class Message(apg.msg.Message):
    """Application-specific abstract message"""
    def __init__(self, text, app, payload=None, nseq=None, lmp=None, clientDemandeur=None, clientTransmetteur=None, type='requete'):
        super().__init__(text, app)
        self.fields += ["payload","nseq","lmp","id","clientDemandeur","clientTransmetteur","type"]
        global id_message_seq
        id_message_seq += 1
        self.content["id"] = id_message_seq
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
    def __init__(self, text, app, payload="MessageDemande", nseq=None, lmp=None, clientDemandeur=None, clientTransmetteur=None, typeDemande='consultation', infoBillet=None):
        super().__init__(text,app,payload,nseq,lmp,clientDemandeur,clientTransmetteur,"requete")
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
    def __init__(self, text, app, payload="MessageAccuseReception", nseq=None, lmp=None, clientDemandeur=None, clientTransmetteur=None, identifiantMessageRecu=None):
        super().__init__(text,app,payload,nseq,lmp,clientDemandeur,clientTransmetteur,"requete")
        self.fields += ["identifiantMessageRecu"]
        self.content["identifiantMessageRecu"] = identifiantMessageRecu
        if len(text) > 0:
            self.parse_text(text)
    def identifiantMessageRecu(self):
        return self.content["identifiantMessageRecu"]
