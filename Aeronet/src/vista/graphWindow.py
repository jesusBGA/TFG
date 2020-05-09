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

    def __init__(self, fechaMin, fechaMax, graph_controller):
        
        QWidget.__init__(self)
        self.graphController = graph_controller
        
        self.fMin = datetime.strptime(fechaMin, '%Y-%m-%d %H:%M:%S')
        self.fMax = datetime.strptime(fechaMax, '%Y-%m-%d %H:%M:%S')
        
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
        register_matplotlib_converters()
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.ax.set_xlim([self.fMin, self.fMax])
        self.ax.set_ylim([-1, 8])
        self.fig.autofmt_xdate()
        self.graficaLayout = QVBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        self.toolBar = NavigationToolbar(self.canvas, self)
        self.graficaLayout.addWidget(self.canvas)
        self.graficaLayout.addWidget(self.toolBar)
        self.horizontalLayout.addLayout(self.graficaLayout)
        
        #Layout de todos los botones
        self.botonesLayout = QVBoxLayout()
        self.botonesLayout.setObjectName("botonesLayout")
        
        #Data type botones
        self.dataTypeGB = QGroupBox("Data Type")
        self.dataTypeVL = QVBoxLayout()
        self.dataTypeVL.setObjectName("Data Type")
        self.AOD = QPushButton("AOD")
        self.dataTypeVL.addWidget(self.AOD)
        self.Wexp = QPushButton("Wexp")
        self.Wexp.clicked.connect(self.Wexp_clicked)
        self.dataTypeVL.addWidget(self.Wexp)
        self.Water_Vapor = QPushButton("Water Vapor")
        self.Water_Vapor.clicked.connect(self.WaterVapor_clicked)
        self.dataTypeVL.addWidget(self.Water_Vapor)
        self.PWR = QPushButton("PWR")
        self.dataTypeVL.addWidget(self.PWR)
        self.Temp = QPushButton("Temp")
        self.Temp.clicked.connect(self.temperaturaClicked)
        self.dataTypeVL.addWidget(self.Temp)
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
        self.dataLevelVL.addWidget(self.L1)
        self.L15 = QPushButton("L1.5")
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
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.ax.set_xlim([self.fMin, self.fMax])
        self.ax.set_ylim([-1, 8])
        self.fig.autofmt_xdate()
        self.canvas.draw_idle()
        
    #Acción boton Wext    
    def Wexp_clicked(self):
        self.graphController.graficaWExp()
        
    #Acción boton vapor de agua    
    def WaterVapor_clicked(self):
        self.graphController.graficaWVapor()
    
    #Acción boton temperatura    
    def temperaturaClicked(self): 
        self.graphController.graficaTemperatura()
        
    #Plotea datos sin canales (temperatura y vapor de agua)
    def plotSimpleData(self, dataX, dataY, tipo):
        self.limpiaPlot()
        self.toolBar._nav_stack.clear()
        format = "black"
        yMax = dataY.values.max()
        yMin = dataY.values.min()
        if (tipo =="Temperatura"):
            format = "ro-"
        elif (tipo == "Vapor de agua"):
            format = "bo-"
        self.ax.set_ylim([yMin-1, yMax+1])
        self.ax.plot(dataX, dataY, format, label = tipo)
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
        self.ax.plot(dataX, dataY380, "bo-", label = "alpha 380-500")
        self.ax.set_ylim([yMin-1, yMax+1])
        self.ax.legend()
        self.canvas.draw_idle()
    
    
    #Graficar datos con errorbar y por canales EN PRUEBAS
    def plotDatosError(self, x, y, yErrorLower, yErrorUpper, format1, format2, canal):
        self.ax.plot(x, y, format1, label= "Canal "+str(canal))
        self.ax.errorbar(x, y, yerr=[[yErrorLower], [yErrorUpper]], fmt=format2)
        
    #Fechas   
    def WaterVaporclicked(self):
        fecha = self.ax.get_xlim()
        f1= str(num2date(fecha[0]))
        f2= str(num2date(fecha[1]))
        print(f1[0:19])
        print(f2[0:19])   