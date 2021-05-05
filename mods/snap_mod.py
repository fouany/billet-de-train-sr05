import os
import sys
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
import msg_mod as msg
import outil_mod as outil
import billet_mod as billet
import time

class SnapshotService:
    def __init__(self,nb_sites=None):
        ## Instantané
        self.couleur = "blanc"
        self.bilan = 0
        self.etat_global=""
        self.prepost=[]
        self.nb_sites_const = nb_sites
        if self.nb_sites_const != None:
            self.isGCH = True
        else:
            self.isGCH = False
        self.nb_sites = 0
        self.NbEtatsAttendus = 0
        self.NbMsgAttendus = 0
    def ALL(self):
        return "all"
    def getCouleur(self):
        return self.couleur
    def flipCouleur(self):
        if self.couleur == "blanc":
            self.couleur = "rouge"
        else:
            self.couleur = "blanc"
    def bilan_incr(self):
        self.bilan += 1
    def propager(self,app,msg_couleur,str_msg):
        self.bilan -= 1
        if msg_couleur == "rouge" and self.couleur == "blanc":
            app.info = "Une snapshot a été effectuée\\n"
            app.print_info()
            self.flipCouleur()
            self.etat_global+=app.str()
            return msg.MessageSnapshot("",app,app.name,"gch",self.couleur,app.nseq,app.lport.getValue(), self.etat_global, self.bilan, typeMessage="FaireSnapshot")
        elif msg_couleur == "blanc" and self.couleur == "rouge":
            return msg.MessageSnapshotPrepost("",app,app.name,self.couleur,app.nseq,app.lport.getValue(), str_msg)
        return None
    def etat_global(self):
        return self.etat_global
    def lancer(self,app):
        if self.isGCH:
            app.info = "Lancer de la snapshot...\\n"
            app.print_info()
            self.flipCouleur()
            self.nb_sites = self.nb_sites_const
            self.prepost=[]
            self.etat_global ="<snapshot>\\n{}".format(app.str())
            self.NbEtatsAttendus = self.nb_sites-1
            self.NbMsgAttendus = self.bilan
        return msg.MessageSnapshot("",app,app.name,self.ALL(),self.couleur,app.nseq,app.lport.getValue(),self.etat_global, self.bilan, typeMessage="FaireSnapshot")
    def receptionMessageSnapshot(self,message,app):
        if not self.isGCH:
            return
        self.etat_global+=message.etat_global()
        self.NbMsgAttendus+=int(message.bilan())
        self.NbEtatsAttendus-=1
        return self.save(app)
    def receptionMessageSnapshotPrepost(self,message,app):
        if not self.isGCH:
            return
        self.prepost+=message.msg_prepost()
        self.NbMsgAttendus-=1
        return self.save(app)
    def save(self,app=None):
        if self.NbMsgAttendus == -(self.nb_sites_const-1) and self.NbEtatsAttendus == 0:
            self.flipCouleur()
            t = time.localtime()
            filename = "snapshot-{}.xml".format(time.strftime("%H_%M_%S",t))
            app.info = "Fin de la snapshot. Celle-ci a été sauvegardé dans {}/{}\\n".format(os.environ["APG_PATH"],filename)
            app.print_info()
            with open("../"+filename,"w") as f:
                f.write(self.etat_global.replace("\\n","\n   "))
                f.write("   <prepost>\n   ")
                for prepost in self.prepost:
                    f.write(prepost)
                f.write("   </prepost>\n</snapshot>")
            # return msg.MessageSnapshot("",app,app.name,self.couleur,self.nseq,self.lport.getValue(), typeMessage="resetSnapshot")
        return None
