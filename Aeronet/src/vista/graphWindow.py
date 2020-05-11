'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
plt.style.use('classic')
from PyQt5 import QtCore
from datetime import datetime, timedelta
from matplotlib.dates import date2num, num2date
from matplotlib.dates import DateFormatter
import pandas as pd
from pandas.plotting import register_matplotlib_converters

#Ventana para graficar los datos de cada fotometro individualmente
class graphWindow(QWidget):

    def __init__(self, ph, station, fechaMin, fechaMax, graph_controller):
        
        QWidget.__init__(self)
        self.graphController = graph_controller
        
        self.fMin = datetime.strptime(fechaMin, '%Y-%m-%d %H:%M:%S')
        self.fMax = datetime.strptime(fechaMax, '%Y-%m-%d %H:%M:%S')
        #Variable botón check
        self.check="AOD"
        self.checkNubes="1.0"
        
        #Título de la ventana
        self.setWindowTitle(str(ph)+" "+str(station))
        
        #Tamaño de la ventana
        self.setFixedSize(1300,780)
        self.setMaximumSize(1300, 780)
        
        #Layout principal
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        
        #Layout grafica y navigation toolbar
        self.horizontalLayout = QHBoxLayout()
        
        #Grafica y navigation toolbar
        self.fig, self.ax = plt.subplots()
        #self.fig.tight_layout()
        self.fig.suptitle('AOD 1.0', fontsize=20)
        register_matplotlib_converters()
        #Formato completo '%d-%b-%Y %H:%M:%S'
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%b-%Y'))
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.ax.set_xlim([self.fMin, self.fMax])   
        self.ax.set_ylim([-1, 8])
        #self.fig.autofmt_xdate()
        self.graficaLayout = QVBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        self.toolBar = NavigationToolbar(self.canvas, self)
        self.graficaLayout.addWidget(self.canvas)
        self.graficaLayout.addWidget(self.toolBar)
        self.horizontalLayout.addLayout(self.graficaLayout)
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%b-%Y'))
        self.formatoFecha()
        
        #Layout de todos los botones
        self.botonesLayout = QVBoxLayout()
        self.botonesLayout.setObjectName("botonesLayout")
        
        #Data type botones
        self.dataTypeGB = QGroupBox("Data Type")
        self.dataTypeVL = QVBoxLayout()
        self.groupButtons = QButtonGroup()
        self.dataTypeVL.setObjectName("Data Type")
        self.AOD = QPushButton("AOD")
        self.AOD.setChecked(True)
        self.AOD.clicked.connect(self.AOD_clicked)
        self.dataTypeVL.addWidget(self.AOD)
        self.groupButtons.addButton(self.AOD)
        self.Wexp = QPushButton("Wexp")
        self.Wexp.clicked.connect(self.Wexp_clicked)
        self.dataTypeVL.addWidget(self.Wexp)
        self.groupButtons.addButton(self.Wexp)
        self.Water_Vapor = QPushButton("Water Vapor")
        self.Water_Vapor.clicked.connect(self.WaterVapor_clicked)
        self.dataTypeVL.addWidget(self.Water_Vapor)
        self.groupButtons.addButton(self.Water_Vapor)
        self.Temp = QPushButton("Temp")
        self.Temp.clicked.connect(self.temperaturaClicked)
        self.dataTypeVL.addWidget(self.Temp)
        self.groupButtons.addButton(self.Temp)
        self.PWR = QPushButton("PWR")
        #self.PWR.clicked.connect(self.probando)
        self.dataTypeVL.addWidget(self.PWR)
        self.groupButtons.addButton(self.PWR)
        '''self.Int_V = QPushButton("Int V")
        self.dataTypeVL.addWidget(self.Int_V)
        self.BLK = QPushButton("BLK")
        self.dataTypeVL.addWidget(self.BLK)'''
        self.dataTypeGB.setLayout(self.dataTypeVL)
        self.botonesLayout.addWidget(self.dataTypeGB)
        
        #Data level botones
        self.dataLevelGB = QGroupBox("Data Level")
        self.dataLevelVL = QVBoxLayout()
        self.L1 = QPushButton("L1.0")
        self.L1.clicked.connect(self.filtroNubesL1)
        self.dataLevelVL.addWidget(self.L1)
        self.L15 = QPushButton("L1.5")
        self.L15.clicked.connect(self.filtroNubesL15)
        self.dataLevelVL.addWidget(self.L15)
        self.dataLevelGB.setLayout(self.dataLevelVL)
        self.botonesLayout.addWidget(self.dataLevelGB)
        
        #Data switches botones
        self.dataSwitchesGB = QGroupBox("Data Switches")
        self.dataSwitchesVL = QVBoxLayout()
        self.dataSwitchesVL.setObjectName("dataSwitchesVL")
        self.HEB = QPushButton("Hide Error Bars")
        self.dataSwitchesVL.addWidget(self.HEB)
        self.DA = QPushButton("Daily Averages")
        self.dataSwitchesVL.addWidget(self.DA)
        self.SA = QPushButton("Show Alpha")
        self.dataSwitchesVL.addWidget(self.SA)
        self.STC = QPushButton("Show TC")
        self.dataSwitchesVL.addWidget(self.STC)
        self.SLC = QPushButton("Show Last Call")
        self.dataSwitchesVL.addWidget(self.SLC)
        self.dataSwitchesGB.setLayout(self.dataSwitchesVL)
        self.botonesLayout.addWidget(self.dataSwitchesGB)
        
        #Commands botones
        self.commandsGB = QGroupBox("Commands")
        self.commandsVL = QVBoxLayout()
        self.commandsVL.setObjectName("commandsVL")
        self.AC = QPushButton("Apply cal")
        self.commandsVL.addWidget(self.AC)
        self.Langley = QPushButton("Langley")
        self.commandsVL.addWidget(self.Langley)
        self.SendScreen = QPushButton("Send Screen")
        self.commandsVL.addWidget(self.SendScreen)
        self.SRA = QPushButton("Send Raw and AOD")
        self.commandsVL.addWidget(self.SRA)
        self.commandsGB.setLayout(self.commandsVL)
        self.botonesLayout.addWidget(self.commandsGB)
        
        #Evento que detecta la modificación de la gráfica
        self.ax.callbacks.connect('xlim_changed', self.fechaEvent)
        
        #MainLayout de la ventana
        self.horizontalLayout.addLayout(self.botonesLayout)
        self.mainLayout.addLayout(self.horizontalLayout)
        self.setLayout(self.mainLayout)
        
    #Plotea los datos del fotometro    
    def plotGrafica(self, datos):
        switcher = {
            1: "ro",
            2: "bx",
            3: "c^",
            4: "ms",
            5: "yp",
            6: "o<",
            7: "lime>",
            8: "siennaD",
            9: "*",
            10: ",",
            11: "November",
            12: "December"
        }
        
        for row in datos:
            lowerError = row[2]-row[3]
            upperError = row[4]-row[2]
            '''lowerError = row[3]
            upperError = row[4]'''
            if row[0]==1:
                self.ax.bar(row[1], 0.025, bottom = row[2]-0.0125, width=0.05, color='white', edgecolor = 'red', align='center')
                self.ax.errorbar(row[1], row[2], yerr = [[lowerError],[upperError]], marker= "o", color= "r")
            elif row[0]==2:
                self.ax.plot(row[1], row[2],"bx")
            elif row[0]==3:
                self.ax.plot(row[1], row[2],"c^")
            elif row[0]==4:
                self.ax.plot(row[1], row[2],"ms")
            elif row[0]==5:
                self.ax.plot(row[1], row[2],"yp")
            elif row[0]==6:
                self.ax.plot(row[1], row[2],"gD")
            elif row[0]==7:
                self.ax.plot(row[1], row[2],"C7*")
            elif row[0]==8:
                self.ax.plot(row[1], row[2],"r<")    
            #self.ax.plot(row[1], row[2], switcher.get(row[0], "k"))
        self.ax.legend()
        #self.canvas.draw()
      
    #Reiniciar y dar formato a los ejes de la gráfica    
    def limpiaPlot(self):
        self.ax.clear()
        self.ax.callbacks.connect('xlim_changed', self.fechaEvent)
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%b-%Y'))
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(6))
        self.ax.set_xlim([self.fMin, self.fMax])
        self.formatoFecha()
        self.canvas.draw_idle()
    
    #Fechas   
    def AOD_clicked(self):
        if (self.check!="AOD"):
            self.fig.suptitle('AOD '+self.checkNubes, fontsize=20)
            if (self.checkNubes=="1.0"): 
                self.graphController.graficaAOD(self.checkNubes)
            elif (self.checkNubes=="1.5"):
                self.graphController.graficaAOD(self.checkNubes)
            self.check="AOD"
        
    #Acción boton Wext    
    def Wexp_clicked(self):
        if (self.check!="WExp"):
            self.fig.suptitle('WExp '+self.checkNubes, fontsize=20)
            if (self.checkNubes=="1.0"): 
                self.graphController.graficaWExpL1()
            elif (self.checkNubes=="1.5"):
                self.graphController.graficaWExpL15()
            self.check="WExp"
        
    #Acción boton vapor de agua    
    def WaterVapor_clicked(self):
        if (self.check!="WaterVapor"):
            self.fig.suptitle('Water Vapor '+self.checkNubes, fontsize=20)
            if (self.checkNubes=="1.0"): 
                self.graphController.graficaWVaporL1()
            elif (self.checkNubes=="1.5"):
                self.graphController.graficaWVaporL15()
            self.check="WaterVapor"
    
    #Acción boton temperatura    
    def temperaturaClicked(self):
        if (self.check!="Temperatura"):
            self.fig.suptitle('Temperatura '+self.checkNubes, fontsize=20)
            if (self.checkNubes=="1.0"): 
                self.graphController.graficaTemperaturaL1()
            elif (self.checkNubes=="1.5"):
                self.graphController.graficaTemperaturaL15()
            self.check="Temperatura"
            
    #Acción boton temperatura    
    def PWRClicked(self):
        if (self.check!="PWR"):
            self.fig.suptitle('PWR '+self.checkNubes, fontsize=20)
            if (self.checkNubes=="1.0"): 
                self.graphController.graficaPWRL1()
            elif (self.checkNubes=="1.5"):
                self.graphController.graficaPWRL15() 
            self.check="PWR"
    
    #Acción de botón Level 1.0
    def filtroNubesL1(self):
        if (self.checkNubes!="1.0"):
            self.checkNubes="1.0"
            self.cambiarFiltro()
            
    #Acción de botón Level 1.5
    def filtroNubesL15(self):
        if (self.checkNubes!="1.5"):
            self.checkNubes="1.5"
            self.cambiarFiltro()
            
    #Llamada a obtener datos si hay que cambiar el filtro de nubes
    def cambiarFiltro(self):
        if (self.check=="AOD"):
            self.check="aod"
            self.AOD_clicked()
        elif (self.check=="Temperatura"):
            self.check="Temp"
            self.temperaturaClicked()
        elif (self.check=="PWR"):
            self.PWRClicked()
            self.check="pwr"
        elif (self.check=="WaterVapor"):
            self.check="WV"
            self.WaterVapor_clicked()
        elif (self.check=="WExp"):
            self.check="WE"
            self.Wexp_clicked()
            
    #Plotea datos sin canales (temperatura y vapor de agua)
    def plotSimpleData(self, dataX, dataY, tipo):
        self.limpiaPlot()
        self.toolBar._nav_stack.clear()
        yMax = dataY.values.max()
        yMin = dataY.values.min()
        fmt = "black"
        if (tipo =="Temperatura"):
            fmt = "ro-"
        elif (tipo == "Vapor de agua"):
            fmt = "bo-"
        self.ax.set_ylim([yMin-1, yMax+1])
        self.ax.plot(dataX, dataY, fmt, label = tipo)
        self.ax.legend()
        self.canvas.draw_idle()
    
    #Plotea los datos referentes a WExp, formado por alpha 440-870 y alpha 380-500
    def plotWExp(self, dataX, dataY440, dataY380):
        self.limpiaPlot()
        self.toolBar._nav_stack.clear()
        #Seleccionar maximo y minimo entre los 2 canales
        yMax440 = dataY440.values.max()
        yMin440 = dataY440.values.min()
        yMax380 = dataY380.values.max()
        yMin380 = dataY380.values.min()
        if (yMax440>=yMax380):
            yMax=yMax440
        else:
            yMax=yMax380
        if (yMin440<=yMin380):
            yMin=yMin440
        else:
            yMin=yMin380
        self.ax.plot(dataX, dataY440, "ro-", label = "alpha 440-870")
        self.ax.plot(dataX, dataY380, "bD-", label = "alpha 380-500")
        self.ax.set_ylim([yMin-1, yMax+1])
        self.ax.legend()
        self.canvas.draw_idle()
    
    #Plotea los datos con canales (AOD y PWR)
    def plotChannelData(self, dataX, dataY, yMin, yMax, lowerE, upperE, desvS, nChannel, color, marker):
        self.ax.errorbar(dataX, dataY, yerr=[lowerE, upperE], color = color, marker = marker, label = "Banda: "+str(nChannel))
        self.ax.set_ylim([yMin-1, yMax+1])
        self.ax.legend(loc = 0, fontsize = 12)
    
    #Tras detectar un evento de dibujo sobre la grafica, actualiza el formato de la fecha del eje x
    def fechaEvent(self, event):
        self.formatoFecha()
        
    #Obtener valores minimo actual del eje x
    def getXMin(self):
        fecha = self.ax.get_xlim()
        fmin = str(num2date(fecha[0]))
        return fmin[0:19]
    
    #Obtener valor maximo actual del eje x
    def getXMax(self):
        fecha = self.ax.get_xlim()
        fmax = str(num2date(fecha[1]))
        return fmax[0:19]
    
    #Definir el formato de la fecha segun el zoom aplicado
    def formatoFecha(self):
        fechaMin = self.getXMin()
        anoMin = fechaMin[0:4] 
        mesMin = fechaMin[5:7]
        diaMin = fechaMin[8:10]
        fechaMax = self.getXMax()
        anoMax = fechaMax[0:4]
        mesMax = fechaMax[5:7]
        diaMax = fechaMax[8:10]
        if ((diaMax==diaMin) & (mesMax==mesMin) & (anoMax==anoMin)):
            self.ax.xaxis.set_major_formatter(DateFormatter('%d-%H:%M'))
        elif((diaMax!=diaMin) & (mesMax==mesMin) & (anoMax==anoMin)):
            self.ax.xaxis.set_major_formatter(DateFormatter('%d-%b %H:00'))
        else:
            self.ax.xaxis.set_major_formatter(DateFormatter('%d-%b-%Y'))
        self.canvas.draw_idle()    
    
            
    #Graficar datos con errorbar y por canales EN PRUEBAS
    def plotDatosError(self, x, y, yErrorLower, yErrorUpper, format1, format2, canal):
        self.ax.plot(x, y, format1, label= "Canal "+str(canal))
        self.ax.errorbar(x, y, yerr=[[yErrorLower], [yErrorUpper]], fmt=format2)
        
    #Fechas   
    def probando(self, event):
        fecha = self.ax.get_xlim()
        f1= str(num2date(fecha[0]))
        f2= str(num2date(fecha[1]))
        '''print(f1[0:19])
        print(f2[0:19]) '''
        self.formatoFecha()
        self.canvas.draw()
        