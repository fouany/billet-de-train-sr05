from sortedcontainers import SortedDict

def GetInstance(msg):
    return GetNode(msg,'instance')

def GetNode(msg,type):
    n=msg.find(type)
    msg=msg[n+len(type)+1:]
    m=msg.find('^')
    msg=msg[:m]
    return msg
#
# Convertisseur d'un array de Billets en string
# à passer dans guichet
#
def setStrBillets(array_billets):
    str = ";"
    for billet in array_billets:
        str+="{}{}".format(billet.str(),";")
    return str
#
# Convertisseur d'un string en array de Billets
# à passer dans guichet
#
def getArrayBillets(str_array_billets):
    array_billets = str_array_billets.split(";")
    if str_array_billets[0] == ";":
        del(array_billets[0])
    if str_array_billets[-1] == ";":
        del(array_billets[len(array_billets)-1])
    return array_billets

#
# Parse un string de critères de billets
#
def parse_info_billet(txt):
    msg = txt.split("+")
    arr = SortedDict()
    if txt[0] == "+":
        del(msg[0])
    if txt[-1] == "+":
        del(msg[len(msg)-1])
    for elt in msg:
        l=str(elt).split("|", 1)
        if len(elt)>0:
            arr[l[0]] = l[1]
    return arr

def FormaliserMessage(array_Message,decalage=""):
    rep=decalage+"<liste_de_messages>\n"
    if str(type(array_Message)) == "<class 'list'>":
        for Message in array_Message:
            rep+=decalage+"   <Message>\n"
            rep+=decalage+"      "+str(Message)+"\n"
            rep+=decalage+"   </Message>\n"
        rep+=decalage+"</liste_de_messages>\n"
    elif str(type(array_Message)) == "<class 'dict'>":
        for key,Message in array_Message.items():
            rep+=decalage+"   <Message>\n"
            rep+=decalage+"      "+str(Message)+"\n"
            rep+=decalage+"   </Message>\n"
        rep+=decalage+"</liste_de_messages>\n"
    else:
        with open("war.txt","w") as f:
            f.write(type(array_Message))
    return rep

def FormaliserBillet(array_billets,decalage=""):
    rep=decalage+"<liste_de_billets>\n"
    for billet in array_billets:
        rep+=decalage+"   <Billet>\n"
        rep+=decalage+"      "+billet.str()+"\n"
        rep+=decalage+"   </Billet>\n"
    rep+=decalage+"</liste_de_billets>\n"
    return rep
def FormaliserPrepost(prepost):
    rep="<Message_Prepost>\n"
    rep+="<!--Message recu postclic et envoyé précli-->\n"
    rep+="   "+prepost+"\n"
    rep+="</Message_Prepost>\n"
