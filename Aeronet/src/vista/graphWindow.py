'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5 import QtCore

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
        self.dataTypeVL.addWidget(self.Wexp)
        self.Water_Vapor = QPushButton("Water Vapor")
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
        self.addToolBar = NavigationToolbar(self.canvas, self)
        
    #Plotea los datos del fotometro    
    def plotGrafica(self, datos):
        print("-")