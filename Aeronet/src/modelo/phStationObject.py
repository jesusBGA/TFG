'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

#Objeto para mapear los datos de cada fotómetro
class phStationObject:
    
    def __init__(self): 
        self.phStation = ""
        self.dateOfUse = []
        self.eprom_type = ""
        self.eprom_subtype = ""
        
    def getPhStatiopn(self):
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
        
    
        
    
        
    