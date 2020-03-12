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
import src.vista.graphWindow as vg
import src.modelo.consultasBBDD as o

class graphController:
    
    def __init__(self): 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        app = QApplication(sys.argv)
        datos=self.getDatosAOD(10)
        self.screen = vg.graphWindow()
        self.screen.plotGrafica(datos)
        #screen2.plotCSVGrafica()
        self.screen.show()
        sys.exit(app.exec_())
        
    #Devuelve una lista de fotometro, fecha, channel, aod
    def getDatosAOD(self, ph):
        datos=c.consultaBBDD.getAODChannels(self, self.cursor, ph)
        return datos