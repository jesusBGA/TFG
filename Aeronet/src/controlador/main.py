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

import src.modelo.globales as g
import src.modelo.consultasBBDD as c

class main:
    
    def __init__(self): 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        
    def printDatos(self):
        data = c.consultaBBDD.getPhStation(self, self.cursor)
        '''for row in data:
            print("Numero: "+str(row[0])+" Estacion: "+str(row[1]))'''
    
    '''class MatplotlibWidget(QMainWindow):
        
        def __init__(self):
            
            QMainWindow.__init__(self)
    
            loadUi("prueba.ui",self)'''
    
    
m=main()
m.printDatos()

    
        

            
    
'''app = QApplication([])
 window = MatplotlibWidget()
 window.show()
app.exec_()'''
