'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
#import random
import pymysql
import sys

import src.modelo.globales as g
import src.modelo.consultasBBDD as c
import src.vista.mainWindow as v

class main:
    
    def __init__(self): 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        
    def printDatos(self):
        data = c.consultaBBDD.getPhStationDates(self, self.cursor)
        return data
        '''for row in data:
            print("Numero: "+str(row[0])+" Estacion: "+str(row[1]))'''
    
    '''class MatplotlibWidget(QMainWindow):
        
        def __init__(self):
            
            QMainWindow.__init__(self)
    
            loadUi("prueba.ui",self)'''
    
    #Devuelve una lista de distict fotometros y estaciones   
    def getDatosPhStation(self):
        datos=c.consultaBBDD.getPhStation(self, self.cursor)
        return datos
    
    #Devuelve una lista de objetos con el n de fotometro, la estación, el conjunto de fechas que estáactivo y con los eprom type y subtype
    def getDatosCompletos(self):
        datos=c.consultaBBDD.getPhStationDates(self, self.cursor)
        return datos
    
    
m=main()
datosDistinct = m.getDatosPhStation()
datosCompletos = m.getDatosCompletos()

#Crear y abrir ventana con interfaz inicial
app = QApplication(sys.argv)
screen = v.mainWindow()
screen.setDatosTabla(datosDistinct)
screen.show()

#Cerrar ventana
sys.exit(app.exec_())    
        

            
    
'''app = QApplication([])
 window = MatplotlibWidget()
 window.show()
app.exec_()'''
