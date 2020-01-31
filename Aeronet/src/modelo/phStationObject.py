'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

#Objeto para mapear los datos de cada fotómetro
class phStationObject:
    
    def __init__(self, phStation, eprom_type, eprom_subtype): 
        self.phStation = phStation
        self.dateOfUse = []     #Lista para contener todas las fechas de uso
        self.eprom_type = eprom_type
        self.eprom_subtype = eprom_subtype
        
    def getPhStation(self):
        return self.phStation

    def setPhStation(self, x):
        self.phStation = x
        
    def getEType(self):
        return self.eprom_type

    def setEType(self, x):
        self.eprom_type = x
        
    def getESubType(self):
        return self.eprom_subtype

    def setESubType(self, x):
        self.eprom_subtype = x
        
    def getDateOfUse(self):
        return self.dateOfUse

    def setDateOfUse(self, x):
        self.dateOfUse.append(x)
        
    
        
    
        
    