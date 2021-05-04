class lport:
    def __init__(self):
        self.__value = 0

    def getValue(self):
        return self.__value

    def setValue(self,val):
        self.__value = val

    def incr(self):
        self.__value += 1
