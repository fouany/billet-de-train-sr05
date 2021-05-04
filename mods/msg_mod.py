#!/usr/bin/python3
import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg

id_message_seq = 0

class Message(apg.msg.Message):
    """Application-specific abstract message"""
    def __init__(self, text, app, nseq=None, lmp=None, clientDemandeur=None, clientDestinataire=None, instance='default',couleur="blanc"):
        super().__init__(text, app)
        self.fields += ["instance","nseq","lmp","id","clientDemandeur","clientDestinataire","couleur"]
        global id_message_seq
        id_message_seq += 1
        self.content["id"] = id_message_seq
        self.content["couleur"] = couleur
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
    def couleur(self):
        return self.content["couleur"]

class MessageDemande(Message):
    """Application-specific message MessageDemande"""
    def __init__(self, text, app,couleurs="blanc", nseq=None, lmp=None, clientDemandeur=None, typeDemande='consultation', infoBillet=""):
        super().__init__(text,app,nseq,lmp,clientDemandeur,clientDestinataire="gch",instance="MessageDemande",couleur=couleurs)
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
    def __init__(self, text, app,couleurs="blanc", nseq=None, lmp=None, clientDemandeur=None, identifiantMessageRecu=None, reponse=1):
        super().__init__(text,app,nseq,lmp,clientDemandeur,clientDestinataire="gch",instance="MessageAccuseReception",couleur=couleurs)
        self.fields += ["identifiantMessageRecu","reponse"]
        self.content["reponse"] = reponse
        if identifiantMessageRecu != None:
            self.content["identifiantMessageRecu"] = identifiantMessageRecu
        if len(text) > 0:
            self.parse_text(text)
    def identifiantMessageRecu(self):
        return self.content["identifiantMessageRecu"]
    def reponse(self):
        return self.content["reponse"] # 1 accepte la reservation | 0 refuse la reservation

class MessageAvecBillets(Message):
    """Application-specific message MessageAvecBillets"""
    def __init__(self, text, app,couleurs="blanc", nseq=None, lmp=None, clientDestinataire=None, typeDemande='consultation', listeBillet=""):
        super().__init__(text,app,nseq,lmp,"gch",clientDestinataire,instance="MessageAvecBillets",couleur=couleurs)
        self.fields += ["typeDemande","listeBillet"]
        self.content["typeDemande"] = typeDemande
        self.content["listeBillet"] = listeBillet
        if len(text) > 0:
            self.parse_text(text)
    def typeDemande(self):
        return self.content["typeDemande"]
    def listeBillet(self):
        return self.content["listeBillet"]

class messageSnapshot(Message):
    """Application-specific message MessageSnapshot"""
    def __init__(self, text, app, clientDemandeur,couleurs="blanc", nseq=None, lmp=None,listeBillet=[],typeMessage="FaireSnapshot"):
        super().__init__(text,app,nseq,lmp,clientDemandeur,instance="MessageSnapshot",couleur=couleurs)
        self.fields += ["listeBillet","typeMessage"]

        self.content["listeBillet"] = listeBillet
        self.content["typeMessage"] = typeMessage

        if len(text) > 0:
            self.parse_text(text)
    def typeMessage(self):
        return self.content["typeMessage"]
    def listeBillet(self):
        return self.content["listeBillet"]
