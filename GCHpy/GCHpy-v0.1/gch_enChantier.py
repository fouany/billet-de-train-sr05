#!/usr/bin/python3
import os
import sys
import gch_mod_lport as lport
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
import msg_mod as msg
import outil_mod as outil
import billet_mod as billet
import time


class GCHApp(apg.Application):
    def __init__(self):
        default_options_values={"default-pld":"Hello World","appname":"GCH","whatwho":True, "bas-dest":"GCH","bas-delay":"1","bas-autosend":False}
        super().__init__(default_options_values)
        self.mandatory_parameters += [] # No mandatory parameter for this app
        self.msg = self.params["default-pld"]
        self.destination_app=self.params["bas-dest"]
        self.destination_zone=self.com.hst_air()
        self.period = float(self.params["bas-delay"])
        self.nseq = 0
        self.lport = lport.lport()
        self.sending_in_progress = None
        self.name='gch'
        self.billets=[]
        b=billet.Billet(id =1, date="12/05/2021", depart="Compiegne", destination="Paris", detenteur=self.name)
        self.billets.append(b)
        b=billet.Billet(id =1, date="10/06/2021", depart="Paris", destination="Compiegne", detenteur=self.name)
        self.billets.append(b)
        self.BilletsDisponibles=[]
        self.MessageAttente={}
        for bi in self.billets :
            self.BilletsDisponibles.append(bi)
        if self.check_mandatory_parameters():
            self.config_gui()
            self.end_initialisation()

    def start(self):
        super().start()
        if self.params["bas-autosend"]:
            self.send_button()

    def repondreMessage(M,S):
        # instance du site guichet G
        M.clientDemandeur=self
        M.type='reponse'
        self.snd(str(M), who=self.destination_app, where=self.destination_zone)

    def annulerReservationBillets(identifiantMessage):
        M=self.MessageAttente.pop(M.identifiantMessageRecu)
        self.BilletsDisponibles.append(M.billets)
        #left to do ?!
        # instance site guichet G
        # definition annulerReservationBillets(identifiantMessage : nombre)
        #     arreterDelaiMaxAttenteReservation(identifiantMessage)
        #     soit M : messageAvecBillets
        #     M = obtenirListeMessageAttente(identifiantMessage)
        #     G.ajouterListeBilletsDisponibles(M.billets)
        #     G.supprimerListeMessageAttente(identifiantMessage)
        # fin definition

    def mettreDeCoteBillets(M):
        # instance site guichet G
        for bil in M.listeBillet:
            self.BilletsDisponibles.remove(bil)
        self.MessageAttente[M.clientDemandeur()+" "+M.id()]= M

    def repondreListeBillets(MessageDemande):
        R=MessageAvecBillets()
        for b in self.billets:
            R.billets.append(b)
        R.typeDemande=MessageDemande.typeDemande
        if R.typeDemande == 'reservation':
            self.mettreDeCoteBillets(R)
        R.clientDestinataire=M.clientDemandeur
        self.repondreMessage(R,R.clientDestinataire)



    def validerListeBillets(M):
        if M.reponse == 0:
            # self.annulerReservationBillets()
            print("tmp")
        else:
            self.MessageAttente.pop(M.identifiantMessageRecu)



    def receive(self, pld, src, dst, where):
        if self.started  and self.check_mandatory_parameters():
            self.vrb("{}.rcv(pld={}, src={}, dst={}, where={})".format(self.APP(),pld, src, dst, where), 6)
            super().receive(pld, src=src, dst=dst, where=where)

            #instance site guichet G, thread associé au site S

            received_message=msg.Message(pld,self)
            if received_message.clientDestinataire() != self.name:
                app.wrb_disperror("Guichet can't pass on a message")

            if received_message.instance() == "MessageDemande":
                self.info=received_message.typeDemande()
                self.repondreListeBillets(received_message)

            elif received_message.instance() == "MessageAccuseReception":
                print("tmp")
                # validerListeBillets(received_message)

            elif received_message.instance() == "MessageSnapshot":
                # self.info="id_message_recu = "+received_message.identifiantMessageRecu()
                # completerSnapshotAvecClient(received_message)
                print("tmp")
            else:
                received_message=msg.Msessage(pld,self)
                self.info="Message lambda"
            if int(received_message.lmp()) > self.lport.getValue():
                self.lport.setValue(int(received_message.lmp()))
            self.lport.incr()
            self.gui.tk_instr("""
self.received_source.config(text="{}")
self.received_payload.config(text="{}")
self.received_nseq.config(text="{}")
self.received_lport.config(text = 'H : {}')
""".format(src, received_message.payload(), received_message.nseq(),self.lport.getValue()))

        else:
            self.vrb_dispwarning("Application {} not started".format(self.APP()))
    #A SUPRIMER de l'interface Graphique:
    def send_button(self, graphic_msg=None, graphic_who=None,graphic_where=None,graphic_period=None):
        time.sleep (100)
    #A suprimer de l'interface Graphique
    def stop_button(self):
        time.sleep (100)
    def config_gui(self):
        """ GUI settings """
        self.gui.tk_instr("""
self.app_zone = tk.LabelFrame(self.root, text="{}")
self.emission_zone = tk.LabelFrame(self.app_zone, text="Emission")
self.var_msg_send = tk.StringVar()
self.var_msg_send.set("{}")
self.msg = tk.Entry(self.emission_zone, width=32, textvariable = self.var_msg_send)
self.msg.pack(side="left")
self.var_who_send = tk.StringVar()
self.var_who_send.set("{}")
self.who = tk.Entry(self.emission_zone, width=10, textvariable = self.var_who_send)
self.who.pack(side="left")
self.var_where_send = tk.StringVar()
self.var_where_send.set("{}")
self.where = tk.Entry(self.emission_zone, width=10, textvariable = self.var_where_send)
self.where.pack(side="left")
self.var_sending_period = tk.StringVar()
self.var_sending_period.set("{}")
self.sending_period= tk.Entry(self.emission_zone, width=3, textvariable=self.var_sending_period)
self.sending_period.pack(side="left")
self.sending_button = tk.Button(self.emission_zone, text="Auto-send", command=partial(self.app().send_button,self.var_msg_send, self.var_who_send, self.var_where_send, self.var_sending_period), activebackground="red", foreground="red", width=10)
self.stop_sending_button = tk.Button(self.emission_zone, text="Stop sending", command=partial(self.app().stop_button), activebackground="green", foreground="red", width=10)
self.sending_button.pack(side="left")
self.stop_sending_button.pack(side="left")
self.reception=tk.LabelFrame(self.app_zone, text="Received message")
self.received_source_label=tk.Label(self.reception, text="Message reçu de")
self.received_source=tk.Label(self.reception, text="-", width=4)
self.received_payload_label = tk.Label(self.reception,text=":")
self.received_payload = tk.Label(self.reception,text="-",width=40)
self.received_nseq_label = tk.Label(self.reception,text="nseq : ")
self.received_nseq = tk.Label(self.reception,text="-", width=4)
self.received_source_label.pack(side="left")
self.received_source.pack(side="left")
self.received_payload_label.pack(side="left")
self.received_payload.pack(side="left")
self.received_nseq_label.pack(side="left")
self.received_nseq.pack(side="left")
self.emission_zone.pack(side="top", fill=tk.BOTH, expand=1)
self.reception.pack(side="top", fill=tk.BOTH, expand=1)
self.app_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format(self.APP(),self.msg, self.destination_app, self.destination_zone, self.period)) # Graphic interface (interpreted if no option notk)
#ajout de l'horloge de Lamport
        self.gui.tk_instr("""
self.lport_zone = tk.LabelFrame(self.root, text="Local Lamport's clock")
self.received_lport = tk.Label(self.lport_zone,text="{}")
self.received_lport.pack(side="left", expand="yes", fill="y", pady=2)
self.lport_zone.pack(fill="both", expand="yes", side="top", pady=5)""".format(self.lport.getValue()))

app = GCHApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")
