'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5.QtWidgets import*
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
#import random
import pymysql
import sys

import src.modelo.globales as g
import src.modelo.consultasBBDD as c
import src.vista.mainWindow as v
import src.vista.graphWindow as vg
import src.modelo.consultasBBDD as o

class main:
    
    def __init__(self): 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
    
       
    #Devuelve una lista de distict fotometros y estaciones   
    def getDatosPhStation(self):
        datos=c.consultaBBDD.getPhStation(self, self.cursor)
        return datos
    
    #Devuelve una lista de objetos con el n de fotometro, la estación, el conjunto de fechas que estáactivo y con los eprom type y subtype
    def getDatosCompletos(self):
        datos=c.consultaBBDD.getPhStationDates(self, self.cursor)
        return datos
    
    #Devuelve una lista de fotometro, fecha, channel, aod
    def getDatosAOD(self, ph):
        datos=c.consultaBBDD.getAODChannels(self, self.cursor, ph)
        return datos
    
    #Invoca la ventana graphWindow, la cual muestra datos para un fotometro concreto
    def graphWindow(self, ph):
        print(ph[0])
        '''datos=c.consultaBBDD.getAODChannels(self, self.cursor, ph)
        screen2 = vg.graphWindow(datos)
        screen2.plotGrafica(datos)
        screen2.show()''' 
    
m=main()
datosDistinct = m.getDatosPhStation()
datosCompletos = m.getDatosCompletos()
#print (str(datosCompletos[0].__getattribute__('phStation')))



#Crear y abrir ventana con interfaz inicial
#QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
'''screen = v.mainWindow()
screen.setDatosTabla(datosDistinct)
screen.show()'''

#datos=m.getDatosAOD(10)
screen2 = vg.graphWindow()
#screen2.plotGrafica(datos)
screen2.show()

#Cerrar ventana 
sys.exit(app.exec_())    
        

