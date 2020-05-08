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


    
class main:   
    def __init__(self): 
        '''self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        #self.cursor.query('SET GLOBAL connection_timeout=600')
        mainWController()
        #graphController()'''
        self.main_controller = mainWController()
        self.main_controller.start()
    

    #Invoca la ventana graphWindow, la cual muestra datos para un fotometro concreto
    '''def graphWindow(self, ph, fechaMin, fechaMax):
        print(ph[0])
        print(fechaMin)
        print(fechaMax)
        datos= consultaBBDD.getAODChannels(self, self.cursor, ph)
        screen2 = vg.graphWindow(datos)
        screen2.plotGrafica(datos)
        screen2.show()
        graphController()'''

if __name__ == '__main__':    
    main()
    sys.exit(main.exec_())
   
'''class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_controller = mainWController()
        self.main_controller.start()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_()) '''       

