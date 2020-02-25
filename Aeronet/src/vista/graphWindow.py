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
import datetime
from matplotlib.dates import date2num, num2date
from matplotlib.dates import DateFormatter
import pandas as pd
from pandas.plotting import register_matplotlib_converters

#Ventana para graficar los datos de cada fotometro individualmente
class graphWindow(QWidget):

    def __init__(self):
        
        QWidget.__init__(self)
        
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
        self.ax.set_xlim([datetime.datetime(2019, 4, 24, 0, 0, 0),datetime.datetime(2019, 5, 1, 0, 0, 0)])
        self.ax.set_ylim([-1, 4])
        self.fig.autofmt_xdate()
        self.graficaLayout = QVBoxLayout()
        self.canvas = FigureCanvas(self.fig)
        self.addToolBar = NavigationToolbar(self.canvas, self)
        self.graficaLayout.addWidget(self.canvas)
        self.graficaLayout.addWidget(self.addToolBar)
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
        self.Wexp.clicked.connect(self.Wext_clicked)
        self.dataTypeVL.addWidget(self.Wexp)
        self.Water_Vapor = QPushButton("Water Vapor")
        self.Water_Vapor.clicked.connect(self.WaterVapor_clicked)
        self.dataTypeVL.addWidget(self.Water_Vapor)
        self.SDA = QPushButton("SDA")
        self.dataTypeVL.addWidget(self.SDA)
        self.Temp = QPushButton("Temp")
        self.dataTypeVL.addWidget(self.Temp)
        self.Int_V = QPushButton("Int V")
        self.dataTypeVL.addWidget(self.Int_V)
        self.BLK = QPushButton("BLK")
        self.dataTypeVL.addWidget(self.BLK)
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
            if row[0]==1:
                self.ax.plot(row[1], row[2],"ro")
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
        
    #Plotea los datos del fotometro desde el csv
    def plotCSVGrafica(self):
        data= pd.read_csv('../modelo/aod.csv', index_col=0)
        data.plot()
        '''c1=data.loc["1"]
        c2=data.loc["2"]
        years=data.columns
        self.ax.plot(years, c1, "ro", label="Channel1")
        self.ax.plot(years, c2, "bx", label="Channel2")'''
    
    
    #Reiniciar y dar formato a los ejes de la gráfica    
    def limpiaPlot(self):
        self.ax.clear()
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.ax.set_xlim([datetime.datetime(2019, 4, 24, 0, 0, 0),datetime.datetime(2019, 5, 1, 0, 0, 0)])
        self.ax.set_ylim([-1, 4])
        self.fig.autofmt_xdate()
        self.canvas.draw()
        self.canvas.flush_events()
        
    #Acción boton Wext    
    def Wext_clicked(self):
        self.limpiaPlot()
        self.ax.plot(datetime.datetime(2019, 4, 30, 0, 0), 2.8, "ro")
        self.canvas.draw()
        
    #Acción boton Wext    
    def WaterVapor_clicked(self):
        fecha = self.ax.get_xlim()
        f1= str(num2date(fecha[0]))
        f2= str(num2date(fecha[1]))
        print(f1[0:19])
        print(f2[0:19])
        
        