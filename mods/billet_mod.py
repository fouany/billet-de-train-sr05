from sortedcontainers import SortedDict

id_billet_seq = 0

class Billet:
    def __init__(self,str, app, date=None, depart=None, destination=None, detenteur=None):
        global id_billet_seq
        id_billet_seq += 1
        self.application = app
        self.content = SortedDict()
        self.fields = ["id","date","depart","destination","detenteur"]
        self.content["id"] = id_billet_seq
        if date != None:
            self.content["date"] = date
        if depart != None:
            self.content["depart"] = depart
        if destination != None:
            self.content["destination"] = destination
        if detenteur != None:
            self.content["detenteur"] = detenteur
        if len(str) > 0:
            self.parse_text(str)
    def id(self):
        return self.content["id"]
    def date(self):
        return self.content["date"]
    def depart(self):
        return self.content["depart"]
    def destination(self):
        return self.content["destination"]
    def detenteur(self):
        return self.content["detenteur"]
    # methodes pour passer l'objet dans les messages
    def parse_text(self,txt):
        self.app().vrb("apg.msg.parse_text(text={})".format(txt),6)
        msg = txt.split("_")
        if txt[0] == "_":
            del(msg[0])
        if txt[-1] == "_":
            del(msg[len(msg)-1])
        for elt in msg:
            l=str(elt).split(":", 1)
            if len(elt)>0:
                self.content[l[0]] = l[1]
    def str(self):
        r="_"
        for key in self.content:
            value = str(self.content[key])
            r+="{}{}{}{}".format(key, ":", value, "_")
        return r
    def app(self):
        return self.application
