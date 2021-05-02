#!/usr/bin/python3
import os
import sys
import time
import clt_mod_lport as lport
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
import msg_mod as msg
import billet_mod as bil

class CLTApp(apg.Application):
    #
    # Initialisation
    #
    def __init__(self):
        default_options_values={"default-pld":"Hello World","whatwho":True, "bas-dest":"CLT","bas-delay":"1","bas-autosend":False}
        super().__init__(default_options_values)
        self.mandatory_parameters += [] # No mandatory parameter for this app
        self.msg = self.params["default-pld"]
        self.destination_app=self.params["bas-dest"]
        self.name=self.params["ident"]
        self.destination_zone=self.com.hst_air()
        self.nseq = 0
        self.lport = lport.lport()
        self.info = "Bonjour !"
        self.msg_trans = []
        self.liste_billets = []
        self.liste_billets_attente = []
        self.sending_in_progress = None
        if self.check_mandatory_parameters():
            self.config_gui()
            self.end_initialisation()
    #
    # Start
    #
    def start(self):
        super().start()
        if self.params["bas-autosend"]:
            self.send_button()

    #
    # Reception de messages
    #
    def receive(self, pld, src, dst, where):
        if self.started  and self.check_mandatory_parameters():
            self.vrb("{}.rcv(pld={}, src={}, dst={}, where={})".format(self.APP(),pld, src, dst, where), 6)
            super().receive(pld, src=src, dst=dst, where=where)

            # abandonne le traitement si reception d'un écho de son propre message
            received_message=msg.Message(pld,self)
            if received_message.clientDemandeur() == self.name:
                return

            # si on n'a pas deja recu ce message on le gere sinon on abandonne
            codeMessage = received_message.clientDemandeur()+" "+received_message.id()
            if not codeMessage in self.msg_trans:
                self.msg_trans.append(codeMessage)
            else:
                return

            # incrémentation de l'horloge
            if int(received_message.lmp()) > self.lport.getValue():
                self.lport.setValue(int(received_message.lmp()))
            self.lport.incr()

            # si n'est pas destinataire alors transfert du message
            if received_message.clientDestinataire() != self.name:
                self.info="(à transmettre)"
                while not self.transfert(received_message,pld):
                    time.sleep(100)
            # si on est destinataire on receptionne le message
            else:
                # simule un guichet en attendant les guichets
                if received_message.instance() == "MessageDemande":
                    received_message=msg.MessageDemande(pld,self)
                    listeBillet = self.setStrBillets([bil.Billet("",self,"30/06/2021","Paris CDG (FR)","New York (USA)"),bil.Billet("",self,"1/07/2021","Paris CDG (FR)","Londres (UK)")])
                    # on répond au demandeur donc nouveau_message.destinataire = ancien_message.demandeur
                    while self.send(msg.MessageAvecBillets("",self, self.nseq, lmp = self.lport.getValue(), typeDemande=received_message.typeDemande(), clientDestinataire = received_message.clientDemandeur(), listeBillet=listeBillet)):
                        time.sleep(100)
                    self.info=received_message.typeDemande()
                elif received_message.instance() == "MessageAvecBillets":
                    self.gerer_billets(msg.MessageAvecBillets(pld,self))
                # les messages qu'un client n'est pas censés recevoir émettent une erreur
                else:
                    self.info = "Le site "+received_message.clientDemandeur()+" vous a envoyé un message du type"+received_message.instance()

            # affichage
            self.gui.tk_instr("""
self.received_lport.config(text = 'H : {}')
self.received_info.config(text = '{}')
""".format(self.lport.getValue(),self.info))
        else:
            self.vrb_dispwarning("Application {} not started".format(self.APP()))
    #
    # Convertisseur d'un array de Billets en string
    # à passer dans guichet
    #
    def setStrBillets(self,array_billets):
        str = ";"
        for billet in array_billets:
            str+="{}{}".format(billet.str(),";")
        return str
    #
    # Convertisseur d'un string en array de Billets
    # à passer dans guichet
    #
    def getArrayBillets(self,str_array_billets):
        array_billets = str_array_billets.split(";")
        if str_array_billets[0] == ";":
            del(array_billets[0])
        if str_array_billets[-1] == ";":
            del(array_billets[len(array_billets)-1])
        return array_billets
    #
    # Transfert de messages
    #
    def transfert(self, message, pld):
        if self.sending_in_progress:
            self.vrb("Already sending, reseting parameters",3)
            return False
        self.sending_in_progress = True

        if message.instance() == "MessageDemande":
            message = msg.MessageDemande(pld,self)
        elif message.instance() == "MessageAccuseReception":
            message = msg.MessageAccuseReception(pld,self)

        message.incLmp()

        self.snd(str(message), who=self.destination_app, where=self.destination_zone)
        self.nseq += 1

        self.sending_in_progress = False
        return True
    #
    # Gérer la réception d'un message avec billets
    #
    def gerer_billets(self,message):
        if message.typeDemande() == "reservation":
            self.config_gui_masquer_boutons()
            self.liste_billets_attente = []
            self.info = "Veuillez valider la réservation de :"
            self.msg_reservation_id = message.id()
            self.gui.tk_instr("""
self.validation_zone = tk.Frame(self.clt_app_zone)

self.accepter_btn = tk.Button(self.validation_zone, text="Valider", command=partial(self.app().accepte_reservation,1), activebackground="red", activeforeground="red", width=20)
self.accepter_btn.pack(side="left")

self.annuler_btn = tk.Button(self.validation_zone, text="Annuler", command=partial(self.app().accepte_reservation,0), activebackground="red", activeforeground="red", width=20)
self.annuler_btn.pack(side="left")

self.validation_zone.pack(fill="both", expand="yes", side="top", pady=5)
""")
        else:
            self.info = "Vous consultez :"
        array_bil = self.getArrayBillets(message.listeBillet())
        for str_bil in array_bil:
            billet = bil.Billet(str_bil,self)
            if message.typeDemande() == "reservation":
                self.liste_billets_attente.append(billet)
            self.info += """{} le {} partant de {} pour {}""".format(billet.id(),billet.date(),billet.depart(),billet.destination())

    #
    # Gére la réponse de l'utilisateur face au choix de réservation
    #
    def accepte_reservation(self,oui_ou_non):
        self.gui.tk_instr("""
self.accepter_btn.pack_forget()
self.annuler_btn.pack_forget()
self.validation_zone.pack_forget()
""")
        if oui_ou_non:
            self.info = "Vous avez accepté la réservation"
            self.liste_billets += self.liste_billets_attente
        else:
            self.info = "Vous avez rejeté la réservation"
        while self.send(msg.MessageAccuseReception("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name, identifiantMessageRecu = self.msg_reservation_id, reponse=oui_ou_non)):
            time.sleep(100)
        self.liste_billets_attente = []
        self.config_gui_ajout_boutons()
        self.gui.tk_instr("""self.received_info.config(text = '{}')""".format(self.info))
    #
    # Emmission de messages
    #
    def send(self,message):
        if self.sending_in_progress:
            self.vrb("Already sending, reseting parameters",3)
            return
        self.sending_in_progress = True

        self.snd(str(message), who=self.destination_app, where=self.destination_zone)
        self.nseq += 1

        #lamp
        self.lport.incr()
        self.gui.tk_instr("""self.received_lport.config(text = 'H : {}')""".format(self.lport.getValue()))

        self.sending_in_progress = False
    #
    # Action du bouton de consultation
    #
    def send_button_consultation(self):
            self.send(msg.MessageDemande("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name))
    #
    # Action du bouton de réservation
    #
    def send_button_reservation(self):
            self.send(msg.MessageDemande("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name, typeDemande = "reservation"))
    #
    # Afficher les billets possédés
    #
    def afficher_posseder(self):
        self.info = "Vous possédez :"
        for billet in self.liste_billets:
            self.info += """{} le {} partant de {} pour {}""".format(billet.id(),billet.date(),billet.depart(),billet.destination())
        self.gui.tk_instr("""self.received_info.config(text = '{}')""".format(self.info))
    #
    # Ajout des boutons d'actions
    #
    def config_gui_ajout_boutons(self):
        self.gui.tk_instr("""
self.bouton_zone = tk.Frame(self.clt_app_zone)

self.sending_posseder_btn = tk.Button(self.bouton_zone, text="Vos billets", command=partial(self.app().afficher_posseder), activebackground="red", activeforeground="red", width=20)
self.sending_posseder_btn.pack(side="left")

self.sending_consulter_btn = tk.Button(self.bouton_zone, text="Consulter guichet", command=partial(self.app().send_button_consultation), activebackground="red", activeforeground="red", width=20)
self.sending_consulter_btn.pack(side="left")

self.sending_reserver_btn = tk.Button(self.bouton_zone, text="Réserver", command=partial(self.app().send_button_reservation), activebackground="red", activeforeground="red", width=20)
self.sending_reserver_btn.pack(side="left")

self.bouton_zone.pack(fill="both", expand="yes", side="top", pady=5)
""")
    #
    # Ajout des boutons d'actions
    #
    def config_gui_masquer_boutons(self):
        self.gui.tk_instr("""
self.sending_posseder_btn.pack_forget()
self.sending_consulter_btn.pack_forget()
self.sending_reserver_btn.pack_forget()
self.bouton_zone.pack_forget()
""")
    #
    # Configuration de l'interface graphique
    #
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

self.received_info = tk.Label(self.info_zone,text="{}")
self.received_info.pack(side="left", expand="yes", fill="y", pady=2)

self.info_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format(self.info))
        # ajout des boutons d'actions
        self.config_gui_ajout_boutons()
        # pack de notre propre interface
        self.gui.tk_instr("""self.clt_app_zone.pack(side="left",fill="both")""")

app = CLTApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")
