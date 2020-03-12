'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

#import random
from datetime import datetime, timedelta
import pymysql
import sys

import src.modelo.globales as g
from src.modelo.consultasBBDD import consultaBBDD
from src.vista.mainWindow import mainWindow
from src.controlador.mainWController import mainWController
from src.controlador.graphController import graphController
import src.vista.graphWindow as vg

'''class App(QApplication):
    
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = consultaBBDD()
        self.main_controller = mainWController(self.model)
        self.main_view = mainWindow(self.model, self.main_controller)
        self.main_view.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())'''
    
class main:
    
    def __init__(self): 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        #self.cursor.query('SET GLOBAL connection_timeout=600')
        mainWController()
        #graphController()
        
    

#Invoca la ventana graphWindow, la cual muestra datos para un fotometro concreto
def graphWindow(self, ph, fechaMin, fechaMax):
    print(ph[0])
    print(fechaMin)
    print(fechaMax)
    datos= consultaBBDD.getAODChannels(self, self.cursor, ph)
    screen2 = vg.graphWindow(datos)
    screen2.plotGrafica(datos)
    screen2.show()
    
main()

#print (str(datosCompletos[0].__getattribute__('phStation')))

#Crear y abrir ventana con interfaz inicial
#QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
#app = QApplication(sys.argv)

#Ventana principal
'''datosDistinct = m.getDatosPhStation()
datosCompletos = m.getDatosCompletos()
fechaMin = m.getFechaMin()
fechaMax = m.getFechaMax()
screen = v.mainWindow()
screen.setDatosTabla(datosDistinct)
screen.plotUsoPh(datosDistinct, datosCompletos, fechaMin, fechaMax)
screen.show()'''

#Ventana grafica
'''datos=m.getDatosAOD(10)
screen2 = vg.graphWindow()
screen2.plotGrafica(datos)
#screen2.plotCSVGrafica()
screen2.show()'''

#Cerrar ventana 
#sys.exit(app.exec_())    
        

