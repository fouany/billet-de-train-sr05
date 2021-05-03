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
