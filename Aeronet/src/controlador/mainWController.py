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
from src.controlador.graphController import graphController
import src.modelo.phStationObject as objecto

class mainWController:
    
    def __init__(self):
        super().__init__()
        
    def start(self):
        self.main_controller = self
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        app = QApplication(sys.argv)
        datosDistinct = self.getDatosPhStation()
        datosCompletos = self.getDatosCompletos()
        fechaMin = self.getFechaMin()
        fechaMax = self.getFechaMax()
        self.screen = v.mainWindow(self.main_controller)
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
        datosCompletos = self.toPhStationObject(datos)
        return datosCompletos
    
    #Devuelve la fecha minima de uso de los fotometros
    def getFechaMin(self):
        return c.consultaBBDD.minFecha(self, self.cursor)
        
    #Devuelve la fecha maxima de uso de los fotometros
    def getFechaMax(self):    
        return c.consultaBBDD.maxFecha(self, self.cursor)
    
    #Invoca la ventana graphWindow, la cual muestra datos para un fotometro concreto
    def graphWindow(self, ph, fechaMin, fechaMax):
        fot = ph.split()
        nFotometro = fot[0]
        station = fot[1]
        '''datos= consultaBBDD.getAODChannels(self, self.cursor, ph)
        screen2 = vg.graphWindow(datos)
        screen2.plotGrafica(datos)
        screen2.show()'''
        self.graphController = graphController()
        self.graphController.start(nFotometro, station, fechaMin, fechaMax)
    
    #Método para tranformar la lista de fotometros consultada para su tratamiento
    def toPhStationObject(self, data):
        indices =[]
        datosCompletos=[]
        contador=0
        for row in data:
            fechas = []
            aux = str(row[0])+" "+ str(row[1])
            if aux not in indices:
                indices.append(aux)
                o = objecto.phStationObject(aux, row[4], row[5])
                fechas.append(row[2])
                fechas.append(row[3])
                o.setDateOfUse(fechas)
                datosCompletos.append(o)
                contador+=1
            else:
                o=datosCompletos[contador-1]
                datosCompletos.remove(o)
                fechas.append(row[2])
                fechas.append(row[3])
                o.setDateOfUse(fechas)
                datosCompletos.append(o)
        return datosCompletos 