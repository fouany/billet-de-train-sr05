#!/usr/bin/python3
import os
import sys
import gch_mod_lport as lport
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
import msg_mod as msg
import outil_mod as outil
import billet_mod as billet
import snap_mod as snap
import time


class GCHApp(apg.Application):
    def __init__(self):
        default_options_values={"default-pld":"Hello World","appname":"GCH","whatwho":True, "bas-dest":"GCH","bas-delay":"1","bas-autosend":False,"nb-sites":"1"}
        super().__init__(default_options_values)
        self.mandatory_parameters += [] # No mandatory parameter for this app
        self.destination_app=self.params["bas-dest"]
        self.name=self.params["ident"]
        self.destination_zone=self.com.hst_air()
        self.period = float(self.params["bas-delay"])
        self.info = "Bonjour !\\n"
        self.nseq = 0
        self.sending_in_progress = None
        self.msg_trans = []

        ## Création du module pour les estampilles
        self.lport = lport.lport()

        ## Création d'un service de snapshot
        self.snapshot = snap.SnapshotService(int(self.params["nb-sites"]))

        ## Création d'une liste de billets
        self.BilletsDisponibles=[]
        b=billet.Billet("",self, date="2021/05/12", depart="Compiegne (FR)", destination="Paris Gare du Nord (FR)", detenteur=self.name)
        self.BilletsDisponibles.append(b)
        b=billet.Billet("",self, date="2021/06/10", depart="Paris Gare du Nord (FR)", destination="Compiegne (FR)", detenteur=self.name)
        self.BilletsDisponibles.append(b)
        b=billet.Billet("",self, date="2021/05/13", depart="Lyon Part Dieu (FR)", destination="ST Etienne (FR)", detenteur=self.name)
        self.BilletsDisponibles.append(b)
        b=billet.Billet("",self, date="2021/05/13", depart="Lyon Part Dieu (FR)", destination="Paris Gare du Nord (FR)", detenteur=self.name)
        self.BilletsDisponibles.append(b)
        b=billet.Billet("",self, date="2021/05/25", depart="Lyon Part Dieu (FR)", destination="Paris Gare du Nord (FR)", detenteur=self.name)
        self.BilletsDisponibles.append(b)
        b=billet.Billet("",self, date="2021/05/25", depart="Compiegne (FR)", destination="Paris Gare du Nord (FR)", detenteur=self.name)
        self.BilletsDisponibles.append(b)
        self.MessageAttente={}

        if self.check_mandatory_parameters():
            self.config_gui()
            self.end_initialisation()
    def str(self):
        rep="<guichet>\\n"
        #name
        rep+="   <name>"+self.name+"</name>\\n"
        #nseq
        rep+="   <nseq>"+str(self.nseq)+"</nseq>\\n"
        #lport
        rep+="   <lport>"+str(self.lport.getValue())+"</lport>\\n"
        #BilletsDisponibles
        rep+=outil.FormaliserBillet(self.BilletsDisponibles,"   ")
        #MessageAttente
        rep+=outil.FormaliserMessageAttente(self.MessageAttente,"   ")
        rep+="</guichet>"+"\\n"
        return rep
    def start(self):
        super().start()
        if self.params["bas-autosend"]:
            self.send_button()

    def annulerReservationBillets(self,identifiantMessage):
        message=self.MessageAttente.pop(str(identifiantMessage))
        for str_billet in outil.getArrayBillets(message.listeBillet()):
            self.BilletsDisponibles.append(billet.Billet(str_billet,self))

    def mettreDeCoteBillets(self,message,listeBillet):
        for bil in listeBillet:
            for x in self.BilletsDisponibles:
                if x.id() == bil.id():
                    self.BilletsDisponibles.remove(x)
        self.MessageAttente[str(message.id())]= message

    def filtrer(self,tab_filtres,filtre,operator,deja_filtre,arrayMatchedBillets):
        if len(tab_filtres) != 0 and tab_filtres.__contains__(filtre):
            if deja_filtre:
                arrayMatchedBilletsStep1 = list(arrayMatchedBillets)
            else:
                arrayMatchedBilletsStep1 = list(self.BilletsDisponibles)
            arrayMatchedBillets = []
            deja_filtre = True
            for x in arrayMatchedBilletsStep1:
                if operator == "==" and x.get(filtre).find(tab_filtres[filtre]) > -1:
                    arrayMatchedBillets += [x]
                elif operator == ">=" and x.get(filtre) >= tab_filtres[filtre]:
                    arrayMatchedBillets += [x]
                elif operator == "<=" and x.get(filtre) <= tab_filtres[filtre]:
                    arrayMatchedBillets += [x]
            tab_filtres.pop(filtre)
        return deja_filtre,arrayMatchedBillets

    def repondreListeBillets(self,messageDemande):
        self.snapshot.bilan_decr()
        arrayMatchedBillets = []
        deja_filtre = False
        filtres = outil.parse_info_billet(messageDemande.infoBillet())
        if len(filtres) == 0:
            arrayMatchedBillets = list(self.BilletsDisponibles)
        else:
            deja_filtre,arrayMatchedBillets = self.filtrer(filtres,"destination","==",deja_filtre,arrayMatchedBillets)
            deja_filtre,arrayMatchedBillets = self.filtrer(filtres,"depart","==",deja_filtre,arrayMatchedBillets)
            deja_filtre,arrayMatchedBillets = self.filtrer(filtres,"datemin",">=",deja_filtre,arrayMatchedBillets)
            deja_filtre,arrayMatchedBillets = self.filtrer(filtres,"datemax","<=",deja_filtre,arrayMatchedBillets)
        listeBillet = outil.setStrBillets(arrayMatchedBillets)
        typeDemande=messageDemande.typeDemande()
        clientDestinataire=messageDemande.clientDemandeur()
        reponse=msg.MessageAvecBillets("", self, self.snapshot.getCouleur(),self.nseq, self.lport.getValue(), clientDestinataire, typeDemande, listeBillet)
        self.nseq += 1
        if typeDemande == 'reservation':
            self.mettreDeCoteBillets(reponse,arrayMatchedBillets)
        self.send(reponse)

    def validerListeBillets(self,message):
        self.snapshot.bilan_decr()
        if message.reponse() == "False":
            self.annulerReservationBillets(message.identifiantMessageRecu())
        else:
            self.MessageAttente.pop(str(message.identifiantMessageRecu()))

    def send(self,message):
        self.snd(str(message), who=self.destination_app, where=self.destination_zone)
        if(message.instance() != "MessageSnapshot" and message.instance() != "MessageSnapshotPrepost"):
            self.snapshot.bilan_incr()

    def receive(self, pld, src, dst, where):
        if self.started  and self.check_mandatory_parameters():
            self.vrb("{}.rcv(pld={}, src={}, dst={}, where={})".format(self.APP(),pld, src, dst, where), 6)
            super().receive(pld, src=src, dst=dst, where=where)

            received_message=msg.Message(pld,self)
            if received_message.clientDestinataire() != self.name:
                return

            codeMessage = received_message.clientDemandeur()+" "+str(received_message.id())
            if not codeMessage in self.msg_trans:
                self.msg_trans.append(codeMessage)
            else:
                return

            if int(received_message.lmp()) > self.lport.getValue():
                self.lport.setValue(int(received_message.lmp()))
            self.lport.incr()

            if received_message.instance() == "MessageDemande":
                received_message = msg.MessageDemande(pld,self)
                self.repondreListeBillets(received_message)
            elif received_message.instance() == "MessageAccuseReception":
                received_message = msg.MessageAccuseReception(pld,self)
                self.validerListeBillets(received_message)
            elif received_message.instance() == "MessageSnapshot":
                received_message = msg.MessageSnapshot(pld,self)
                reset_snapshot = self.snapshot.receptionMessageSnapshot(received_message,self)
                if reset_snapshot != None:
                    self.send(reset_snapshot)
            elif received_message.instance() == "MessageSnapshotPrepost":
                received_message = msg.MessageSnapshotPrepost(pld,self)
                reset_snapshot = self.snapshot.receptionMessageSnapshotPrepost(received_message,self)
                if reset_snapshot != None:
                    self.send(reset_snapshot)
            self.print_info()
        else:
            self.vrb_dispwarning("Application {} not started".format(self.APP()))

    #
    # Afficher les billets possédés
    #
    def afficher_posseder(self):
        self.lport.incr()
        self.info = "Vous possédez :\\n"
        for billet in self.BilletsDisponibles:
            self.info += """{} le {} partant de {} pour {}\\n""".format(billet.id(),billet.date(),billet.depart(),billet.destination())
        self.print_info()
    #
    # Lancée la snapchot
    #
    def Lancee_Snapshot(self):
        self.lport.incr()
        self.send(self.snapshot.lancer(self))
        #Propager la snapshot
    #
    # Imprimer self.info sur l'interface graphique
    #
    def print_info(self):
        self.gui.tk_instr("""
self.received_lport.config(text = 'H : {}')
self.received_info.config(state='normal')
self.received_info.insert(tk.INSERT,'{}')
self.received_info.config(state='disabled')
""".format(self.lport.getValue(),self.info))
        self.info = ""
    #
    # Ajout des boutons d'actions
    #
    def config_gui_ajout_boutons(self):
        self.gui.tk_instr("""
self.bouton_zone = tk.Frame(self.clt_app_zone)

self.form_zone = tk.LabelFrame(self.bouton_zone,text='Formulaire de recherche de billets')

self.form_zone.pack(fill="both", expand="yes", side="top", pady=5)

self.sending_posseder_btn = tk.Button(self.bouton_zone, text="Vos billets", command=partial(self.app().afficher_posseder), activebackground="red", activeforeground="red", width=20)
self.sending_posseder_btn.pack(side="left")
self.sending_snapshot_btn = tk.Button(self.bouton_zone, text="Realiser une snapshot", command=partial(self.app().Lancee_Snapshot), activebackground="red", activeforeground="red", width=20)
self.sending_snapshot_btn.pack(side="left")
self.bouton_zone.pack(fill="both", expand="yes", side="top", pady=5)
""")
    #
    # Masquer les boutons d'actions
    #
    def config_gui_masquer_boutons(self):
        self.gui.tk_instr("""
self.sending_posseder_btn.pack_forget()
self.sending_snapshot_btn.pack_forget()
self.bouton_zone.pack_forget()
""")
    def config_gui(self):
        # suppression des interfaces inutiles
        self.gui.tk_instr("""
self.airplug_zone.pack_forget()
self.send_zone.pack_forget()
self.subscribe_zone.pack_forget()
self.receive_zone.pack_forget()
""")
        # ajout de notre propre interface : app_zone
        self.gui.tk_instr("""self.clt_app_zone = tk.LabelFrame(self.root, text="Bienvenue !", width=40)""")
        # ajout de la zone de l'horloge de Lamport
        self.gui.tk_instr("""
self.lport_zone = tk.LabelFrame(self.clt_app_zone, text="Local Lamport's clock")

self.received_lport = tk.Label(self.lport_zone,text="{}")
self.received_lport.pack(side="left", expand="yes", fill="y", pady=2)

self.lport_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format(self.lport.getValue()))
        # ajout de la zone d'information
        self.gui.tk_instr("""
self.info_zone = tk.Frame(self.clt_app_zone)

self.received_info = tk.Text(self.info_zone,wrap="word")
self.received_info.pack(side="left", expand="yes", fill="y", pady=2)

self.info_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format())
        self.print_info()
        # ajout des boutons d'actions
        self.config_gui_ajout_boutons()
        # pack de notre propre interface
        self.gui.tk_instr("""self.clt_app_zone.pack(side="left",fill="both")""")

app = GCHApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")
