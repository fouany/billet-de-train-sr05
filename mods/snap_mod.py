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
        self.action = "FaireSnapshot"
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
    def flipReset(self,action="FaireSnapshot"):
        if (self.couleur == "rouge" and action=="ResetSnapshot") or (self.couleur == "blanc" and action=="FaireSnapshot"):
            self.action = action
    def bilan_incr(self):
        self.bilan += 1
    def bilan_decr(self):
        self.bilan -= 1
    def propager(self,app,msg_couleur,str_msg):
        if self.action=="FaireSnapshot" and msg_couleur == "rouge" and self.couleur == "blanc":
            app.info = "Une snapshot a été effectuée\\n"
            app.print_info()
            self.flipCouleur()
            self.etat_global+=app.str()
            return msg.MessageSnapshot("",app,app.name,"gch",self.couleur,app.nseq,app.lport.getValue(), self.etat_global, self.bilan, typeMessage="FaireSnapshot")
        elif self.action=="FaireSnapshot" and msg_couleur == "blanc" and self.couleur == "rouge":
            return msg.MessageSnapshotPrepost("",app,app.name,self.couleur,app.nseq,app.lport.getValue(), str_msg)
        elif self.action=="ResetSnapshot" and msg_couleur == "blanc" and self.couleur == "rouge":
            self.flipCouleur()
            return msg.MessageSnapshot("",app,app.name,self.ALL(),self.couleur,app.nseq,app.lport.getValue(), typeMessage="ResetSnapshot")
        return None
    def etat_global(self):
        return self.etat_global
    def lancer(self,app):
        if self.isGCH:
            app.config_gui_masquer_boutons()
            app.info = "Lancement de la snapshot...\\n"
            app.print_info()
            self.flipCouleur()
            self.nb_sites = self.nb_sites_const
            self.prepost=[]
            self.etat_global ="<snapshot>\\n{}".format(app.str())
            self.NbEtatsAttendus = self.nb_sites-1
            self.NbMsgAttendus = self.bilan
        elif self.action == "ResetSnapshot":
            app.info = "Reset du système de snapshot...\\n"
            app.print_info()
            self.flipReset()
            self.etat_global = ""
            return None
        return msg.MessageSnapshot("",app,app.name,self.ALL(),self.couleur,app.nseq,app.lport.getValue(),self.etat_global, self.bilan, typeMessage="FaireSnapshot")
    def receptionMessageSnapshot(self,message,app):
        if not self.isGCH or message.typeMessage() != "FaireSnapshot":
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
    def save(self,app):
        app.info = "nb_msg="+str(self.NbMsgAttendus)+" nb_etat="+str(self.NbEtatsAttendus)+"\\n"
        app.print_info()
        if self.NbMsgAttendus == 0 and self.NbEtatsAttendus == 0:
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
            self.flipCouleur()
            self.bilan = 0
            self.etat_global = ""
            app.config_gui_ajout_boutons()
            return msg.MessageSnapshot("",app,app.name,self.ALL(),self.couleur,app.nseq,app.lport.getValue(), typeMessage="ResetSnapshot")
        return None
