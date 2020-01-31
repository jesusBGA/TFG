'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5 import QtCore, QtGui, QtWidgets


from mysql.connector import (connection)
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import sys

import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection
from mysql.connector import (connection)
from setuptools.windows_support import hide_file

#Ventana principal de la aplicación
class mainWindow(QWidget):

    def __init__(self):
        
        QWidget.__init__(self)
        
        #Título y tamaño de la ventana principal
        self.setWindowTitle("Aeronet")
        self.setFixedSize(1300,800)
        
        #Tabla para mostrar las fechas
        '''self.tableFWidget = QTableWidget()
        self.tableFWidget.setRowCount(1)
        self.tableFWidget.setColumnCount(10)
        self.tableFWidget.setMaximumHeight(20)'''
        
        #Tabla para mostrar los datos
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget.setFont(QFont('Times New Roman', 10, QFont.Bold))
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        
        #Layout de la grafica 
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 250)
        self.setLayout(self.mainLayout)
        
        '''self.mainLayout.addWidget(self.tableFWidget)'''
        self.mainLayout.addWidget(self.tableWidget)
        self.setLayout(self.mainLayout)
        
         
     
    #Metodo para rellenar la tabla con fotometro y estacion     
    def setDatosTabla(self, datos):
        self.tableWidget.setRowCount(len(datos))
        contador=0  
        #labels=[] 
        for dato in datos:
            item = str(dato[0])+"  "+str(dato[1]) 
            cellinfo = QTableWidgetItem(item)
            cellinfo.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget.setItem(contador,0, cellinfo)
            #labels.append(str(dato[0])+" "+str(dato[1]))
            contador+=1
        #self.tableWidget.setVerticalHeaderLabels(labels)
        
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
