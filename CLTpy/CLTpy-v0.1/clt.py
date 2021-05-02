#!/usr/bin/python3
import os
import sys
import time
import clt_mod_lport as lport
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
import msg_mod as msg

class CLTApp(apg.Application):
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
        self.info = self.destination_app
        self.msg_trans = []
        self.sending_in_progress = None
        if self.check_mandatory_parameters():
            self.config_gui()
            self.end_initialisation()
    def start(self):
        super().start()
        if self.params["bas-autosend"]:
            self.send_button()
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
                if received_message.instance() == "MessageDemande":
                    received_message=msg.MessageDemande(pld,self)
                    self.info=received_message.typeDemande()
                    infoBillet=received_message.infoBillet()
                    if len(infoBillet) > 0:
                        self.info+=" pour un billet : "+infoBillet
                elif received_message.instance() == "MessageAccuseReception":
                    received_message=msg.MessageAccuseReception(pld,self)
                    self.info="id_message_recu = "+received_message.identifiantMessageRecu()
                else:
                    self.info = "Message lambda"

            # affichage
            self.gui.tk_instr("""
self.received_lport.config(text = 'H : {}')
self.received_info.config(text = '{}')
""".format(self.lport.getValue(),self.info))
        else:
            self.vrb_dispwarning("Application {} not started".format(self.APP()))

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


    def send_button_consultation(self):
            self.send(msg.MessageDemande("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name))

    def send_button_accuseReception(self): # pour tester
            self.send(msg.MessageAccuseReception("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name, identifiantMessageRecu = -1))

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

        # ajout des boutons d'actions
        self.gui.tk_instr("""
self.bouton_zone = tk.Frame(self.clt_app_zone)

self.sending_consulter_btn = tk.Button(self.bouton_zone, text="Consulter", command=partial(self.app().send_button_consultation), activebackground="red", activeforeground="red", width=20)
self.sending_consulter_btn.pack(side="left")

self.sending_accuseReception_btn = tk.Button(self.bouton_zone, text="AccuseReception", command=partial(self.app().send_button_accuseReception), activebackground="red", activeforeground="red", width=20)
self.sending_accuseReception_btn.pack(side="left")

self.bouton_zone.pack(fill="both", expand="yes", side="top", pady=5)
""")
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

        # pack de notre propre interface
        self.gui.tk_instr("""self.clt_app_zone.pack(side="left",fill="both")""")

app = CLTApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")
