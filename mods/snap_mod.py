import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))import libapg as apg
import msg_mod as msg
import outil_mod as outil
import billet_mod as billet

class SnapshotService():
    def __init__(self,nb_sites=None):
        ## Instantané
        self.couleur = "blanc"
        self.bilan = 0
        self.etat_global=None
        self.nb_sites = nb_sites
        self.NbEtatsAttendusi = 0
        self.NbMsgAttendusi = 0
    def couleur(self):
        return self.couleur
    def flipCouleur(self):
        if self.couleur = "blanc":
            self.couleur = "rouge"
        else:
            self.couleur = "blanc"
    def bilan(self):
        return self.bilan
    def etat_global(self):
        return self.etat_global
    def lancer(self,str_site):
        if self.nb_sites:
            self.flipCouleur()
            self.EG = str_site
            self.NbEtatsAttendusi = N-1
            self.NbMsgAttendusi = self.bilan
            """pour test"""
            with open("test.txt","w") as f:
                f.write(self.EG)
