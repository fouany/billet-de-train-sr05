class Billet:
    
    def __init__(self, id, date, depart, destination, detenteur):
        self.__id = id
        self.__date = date
        self.__depart = depart
        self.__destination = destination
        self.__detenteur = detenteur
        
    
    def get_id(self):
        return self.__id
    
    def set_id(self, id):
        self.__id = id
        
    def get_date(self):
        return self.__date
    
    def set_date(self, date):
        self.__date = date
        
    def get_depart(self):
        return self.__depart
    
    def set_depart(self, depart):
        self.__depart = depart
    
    def get_destination(self):
        return self.__destination
    
    def set_destination(self, destination):
        self.__destination = destination
    
    def get_detenteur(self):
        return self.__detenteur
    
    def set_detenteur(self, detenteur):
        self.__detenteur = detenteur

