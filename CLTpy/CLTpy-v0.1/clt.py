#!/usr/bin/python3
import os
import sys
import time
import clt_mod_lport as lport
sys.path.append(os.path.abspath("{}/LIBAPGpy/LIBAPGpy".format(os.environ["APG_PATH"])))
import libapg as apg
import msg_mod as msg
import outil_mod as outil


class CLTApp(apg.Application):
    def __init__(self):
        default_options_values={"default-pld":"Hello World","name":"CLT","whatwho":True, "bas-dest":"CLT","bas-delay":"1","bas-autosend":False}
        super().__init__(default_options_values)
        self.mandatory_parameters += [] # No mandatory parameter for this app
        self.msg = self.params["default-pld"]
        self.destination_app=self.params["bas-dest"]
        self.name=self.params["name"]
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
self.received_source.config(text="{}")
self.received_instance.config(text="{}")
self.received_nseq.config(text="{}")
self.received_lport.config(text = 'H : {}')
self.received_info.config(text = '{}')
""".format(src, received_message.instance(), received_message.nseq(),self.lport.getValue(),self.info))
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

        self.snd(str(message), who=self.destination_app, where=self.destination_zone)
        self.nseq += 1

        self.sending_in_progress = False
        self.gui.tk_instr('self.sending_button.config(text="Send")')
        return True

    def send_button(self):
        if self.sending_in_progress:
            self.vrb("Already sending, reseting parameters",3)
            return
        self.sending_in_progress = True

        if self.msg == "demande":
            message = msg.MessageDemande("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name)
        else:
            message = msg.Message("",self, self.nseq, lmp = self.lport.getValue(), clientDemandeur = self.name, clientDestinataire = "CLT3")

        self.snd(str(message), who=self.destination_app, where=self.destination_zone)
        self.nseq += 1

        #lamp
        self.lport.incr()
        self.gui.tk_instr("""self.received_lport.config(text = 'H : {}')""".format(self.lport.getValue()))

        self.sending_in_progress = False
        self.gui.tk_instr('self.sending_button.config(text="Send")')

    def config_gui(self):
        """ GUI settings """
        self.gui.tk_instr("""
self.app_zone = tk.LabelFrame(self.root, text="{}")
self.emission_zone = tk.LabelFrame(self.app_zone, text="Emission")
self.msg = tk.Entry(self.emission_zone, width=32, textvariable = self.var_msg_send)
self.msg.pack(side="left")
self.sending_button = tk.Button(self.emission_zone, text="Send", command=partial(self.app().send_button), activebackground="red", foreground="red", width=10)
self.sending_button.pack(side="left")
self.reception=tk.LabelFrame(self.app_zone, text="Received message")
self.received_source_label=tk.Label(self.reception, text="Message reçu de")
self.received_source=tk.Label(self.reception, text="-", width=4)
self.received_instance_label = tk.Label(self.reception,text=":")
self.received_instance = tk.Label(self.reception,text="-",width=40)
self.received_nseq_label = tk.Label(self.reception,text="nseq : ")
self.received_nseq = tk.Label(self.reception,text="-", width=4)
self.received_source_label.pack(side="left")
self.received_source.pack(side="left")
self.received_instance_label.pack(side="left")
self.received_instance.pack(side="left")
self.received_nseq_label.pack(side="left")
self.received_nseq.pack(side="left")
self.emission_zone.pack(side="top", fill=tk.BOTH, expand=1)
self.reception.pack(side="top", fill=tk.BOTH, expand=1)
self.app_zone.pack(fill="both", expand="yes", side="top", pady=5)
""".format(self.APP()))
        # ajout de l'horloge de Lamport
        self.gui.tk_instr("""
self.lport_zone = tk.LabelFrame(self.root, text="Local Lamport's clock")
self.received_lport = tk.Label(self.lport_zone,text="{}")
self.received_lport.pack(side="left", expand="yes", fill="y", pady=2)
self.lport_zone.pack(fill="both", expand="yes", side="top", pady=5)""".format(self.lport.getValue()))
        # ajout info
        self.gui.tk_instr("""
self.info_zone = tk.LabelFrame(self.root, text="Info")
self.received_info = tk.Label(self.info_zone,text="{}")
self.received_info.pack(side="left", expand="yes", fill="y", pady=2)
self.info_zone.pack(fill="both", expand="yes", side="top", pady=5)""".format(self.info))

app = CLTApp()
if app.params["auto"]:
    app.start()
else:
    app.dispwarning("app not started")
