'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
import pymysql
import sys
from PyQt5.QtWidgets import QApplication

import src.modelo.globales as g
import src.vista.mainWindow as v
import src.modelo.consultasBBDD as c

class mainWController:
    
    def __init__(self):
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        app = QApplication(sys.argv)
        datosDistinct = self.getDatosPhStation()
        datosCompletos = self.getDatosCompletos()
        fechaMin = self.getFechaMin()
        fechaMax = self.getFechaMax()
        self.screen = v.mainWindow()
        self.screen.plotUsoPh(datosDistinct, datosCompletos, fechaMin, fechaMax)
        self.screen.setDatosTabla(datosDistinct)
        self.screen.show()
        sys.exit(app.exec_())
        
    
    #Devuelve una lista de distict fotometros y estaciones   
    def getDatosPhStation(self):
        datos=c.consultaBBDD.getPhStation(self, self.cursor)
        return datos
    
    #Devuelve una lista de objetos con el n de fotometro, la estación, el conjunto de fechas que estáactivo y con los eprom type y subtype
    def getDatosCompletos(self):
        datos=c.consultaBBDD.getPhStationDates(self, self.cursor)
        return datos
    
    #Devuelve la fecha minima de uso de los fotometros
    def getFechaMin(self):
        return c.consultaBBDD.minFecha(self, self.cursor)
        
    #Devuelve la fecha maxima de uso de los fotometros
    def getFechaMax(self):    
        return c.consultaBBDD.maxFecha(self, self.cursor)
    