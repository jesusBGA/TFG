'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mysql.connector import (connection)
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import sys
from pandas.plotting import register_matplotlib_converters
import datetime
from matplotlib.dates import DateFormatter

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
        self.setFixedSize(1400,800)
        
        #Tabla para mostrar las fechas
        '''self.tableFWidget = QTableWidget()
        self.tableFWidget.setRowCount(1)
        self.tableFWidget.setColumnCount(10)
        self.tableFWidget.setMaximumHeight(20)'''
        
        #Tabla para mostrar los datos
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setFixedWidth(100)
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget.setFont(QFont('Times New Roman', 10, QFont.Bold))
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        
        self.quitButton = QPushButton("Salir")
        self.quitButton.clicked.connect(self.quit)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.setContentsMargins(0,0,10,10)
        self.hbox.addWidget(self.quitButton)
        
        #Layout grafica y navigation toolbar
        self.horizontalLayout = QVBoxLayout()
        
        #Botones siguiente pagina y anterior
        self.pagesLayout = QVBoxLayout()
        v_widget = QWidget()
        v_widget.setLayout(self.pagesLayout)
        v_widget.setFixedWidth(110)
        #self.pagesLayout.addStretch(1)
        self.previousButton = QPushButton("Previous 10")
        self.previousButton.clicked.connect(self.previousPage)
        self.nextButton = QPushButton("Next 10")
        self.nextButton.clicked.connect(self.nextPage)
        self.pagesLayout.addWidget(self.previousButton)
        self.pagesLayout.addWidget(self.nextButton)
        
        #Grafica y navigation toolbar
        self.fig, self.ax = plt.subplots()
        register_matplotlib_converters()
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.graficaLayout = QHBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        self.addToolBar = NavigationToolbar(self.canvas, self)
        self.graficaLayout.addWidget(self.tableWidget)
        self.graficaLayout.addWidget(self.canvas)
        self.graficaLayout.addWidget(v_widget)
        self.horizontalLayout.addLayout(self.graficaLayout)
        self.horizontalLayout.addWidget(self.addToolBar)
        
        #Layout de la grafica 
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 180)
        self.setLayout(self.mainLayout)
        
        '''self.mainLayout.addWidget(self.tableFWidget)'''
        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addLayout(self.hbox)
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
        
    #Metodo para plotear la grafica de uso
    def plotUsoPh(self, datosPhSt, datosCompletos, fechaMin, fechaMax):
        #print (str(datosCompletos[0].__getattribute__('phStation')))
        longitud=len(datosPhSt)
        self.scroll = longitud
        self.scrolled = longitud
        verts = []
        colors = []
        labels = []
        yPosition = []
        cats={}
        colormapping={}
        
        for data in datosPhSt:
            clave=str(data[0])+" "+str(data[1])
            cats[clave]=longitud
            colormapping[clave]="gray"
            labels.insert(0, clave)
            yPosition.insert(0, longitud)
            longitud-=1
            
        for elemento in datosCompletos:
            fechas = elemento.__getattribute__('dateOfUse')
            phStation = elemento.__getattribute__('phStation')
            for f in fechas:
                v =  [(mdates.date2num(f[0]), cats[phStation]-.4),
                      (mdates.date2num(f[0]), cats[phStation]+.4),
                      (mdates.date2num(f[1]), cats[phStation]+.4),
                      (mdates.date2num(f[1]), cats[phStation]-.4),
                      (mdates.date2num(f[0]), cats[phStation]-.4)]
                verts.append(v)
                colors.append(colormapping[phStation])
                
        bars = PolyCollection(verts, facecolors=colors)
        register_matplotlib_converters()
        
        plt.grid(color='Black', linestyle='solid')
        self.ax.add_collection(bars)
        self.ax.autoscale()
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M'))
        #self.ax.set_xlim([datetime.datetime(2000, 5, 14, 19, 0),datetime.datetime(2028, 3, 14, 13, 59, 59)])
        self.ax.set_xlim([fechaMin,fechaMax])
        self.fig.autofmt_xdate()
        
        #self.ax.set_yticks(0-len(datosPhSt))
        self.ax.set_yticks(yPosition)
        self.ax.set_yticklabels(labels)
        self.ax.set_ylim([len(datosPhSt)-9.5, len(datosPhSt)+.5])
        
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
    
    #Accion de avanzar fotometros en la grafica
    def nextPage(self):
        lims=self.ax.get_ylim()
        min = lims[0]
        max = lims[1]
        if self.previousButton.isEnabled()==False:
            self.previousButton.setEnabled(True)
        if self.scrolled>10:
            self.scrolled-=10
            self.ax.set_ylim([self.scrolled-9.5, self.scrolled+.5])
            self.canvas.draw_idle()
            if self.scrolled<=10:
                self.nextButton.setEnabled(False)
                
    #Accion de retroceder fotometros en la grafica
    def previousPage(self):
        lims=self.ax.get_ylim()
        min = lims[0]
        max = lims[1]  
        if self.nextButton.isEnabled()==False:
            self.nextButton.setEnabled(True)
        if self.scrolled<(self.scroll-9):
            self.scrolled+=10
            self.ax.set_ylim([self.scrolled-9.5, self.scrolled+.5])
            self.canvas.draw_idle()
            if self.scroll<self.scrolled+10:
                self.previousButton.setEnabled(False)
            
    def quit(self):
        print("Salir")
    
