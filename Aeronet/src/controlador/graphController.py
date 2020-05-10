'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import pandas as pd
import itertools
#import random
import pymysql
from tkinter import messagebox as MessageBox
import sys

import src.modelo.globales as g
import src.modelo.consultasBBDD as c
import src.vista.mainWindow as v
import src.vista.graphWindow as vg
import src.modelo.consultasBBDD as o

class graphController:
    
    def __init__(self):
        super().__init__()
    
    def start(self, ph, station, fechaMin, fechaMax):
        self.controller = self 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        self.datosAOD=self.getDatosAOD(ph, station, fechaMin, fechaMax)
        if (any(map(len, self.datosAOD))):
            self.screen = vg.graphWindow(ph, station, fechaMin, fechaMax, self.controller)
            self.screen.plotGrafica(self.datosAOD)
            self.screen.show()
        else:
            MessageBox.showinfo("Empty!", "No hay datos para el fotómetro: "+str(ph)+ " "+str(station)+" entre las fechas "+str(fechaMin)+" y "+str(fechaMax))
                
        #Obtener los datos relativos a la temperatura
        temperatura = self.getDatosTemp(ph, station, fechaMin, fechaMax)
        if (any(map(len, temperatura))):
            t = pd.DataFrame(temperatura)
            self.tDateX = t.iloc[:, 0]
            self.tTempY = t.iloc[:, 1]
            
        #Obtener los datos relativos al vapor de agua
        wVapor = self.getDatosWVapor(ph, station, fechaMin, fechaMax)
        if (any(map(len, wVapor))):
            wV = pd.DataFrame(wVapor)
            self.wVDateX = wV.iloc[:, 0]
            self.wVaporY = wV.iloc[:, 1]
            
        #Obtener los dato relativos a WExp
        wExp = self.getDatosWExp(ph, station, fechaMin, fechaMax)
        if (any(map(len, wVapor))):
            wE = pd.DataFrame(wExp)
            self.wEDateX = wE.iloc[:, 0]
            self.wExpAlpha440Y = wE.iloc[:, 1]    
            self.wExpAlpha380Y = wE.iloc[:, 2]
        
    #Devuelve una lista de fotometro, fecha, channel, aod
    def getDatosAOD(self, ph, station, fechaMin, fechaMax):
        datos = c.consultaBBDD.getAODChannelsL1(self, self.cursor, ph, station, fechaMin, fechaMax)
        return datos
    
    #Devuelve una lista con las medidas de temperaturas para un fotómetro een un rango de fechas
    def getDatosTemp(self, ph, station, fechaMin, fechaMax):
        datos = c.consultaBBDD.getTemperatura(self, self.cursor, ph, station, fechaMin, fechaMax)
        return datos
        
    #Devuelve una lista con las medidad WExp para un fotómetro een un rango de fechas
    def getDatosWExp(self, ph, station, fechaMin, fechaMax):
        datos = c.consultaBBDD.getWExp(self, self.cursor, ph, station, fechaMin, fechaMax)
        return datos
        
    #Devuelve una lista con las medidad de vapor de agua temperaturas para un fotómetro een un rango de fechas
    def getDatosWVapor(self, ph, station, fechaMin, fechaMax):
        datos = c.consultaBBDD.getWVapor(self, self.cursor, ph, station, fechaMin, fechaMax)
        return datos
    
    #Descompone las tuplas de datos con canales para su representación en graphWindow
    def tratamientoDatosCanales(self, datos):
        print("")
        
    #Recupera los datos de llas medidas AOD y los manda a la vista para su representación    
    def graficaAOD(self):
        key_func = lambda x: x[0]
        colors = g.fCanalColors
        markers = g.fCanalMarkers
        self.screen.limpiaPlot()
        auxiliar = 0
        
        for key, group in itertools.groupby(self.datosAOD, key_func):
            AOD = list(group)
            aod = pd.DataFrame(AOD)
            aodDateX = aod.iloc[:, 1]
            aodTempY = aod.iloc[:, 2]
            #Comprobaciones para ver el mayor y menor de los valores y estimar el maximo y el minimo en el eje Y de la grafica
            yMax = aodTempY.values.max()
            yMin = aodTempY.values.min()
            if (auxiliar == 0):
                yMaximo = yMax
                yMinimo = yMin
                auxiliar+=1
            else:
                if (yMax>=yMaximo):
                    yMaximo = yMax
                if (yMin<=yMinimo):
                    yMinimo = yMin        
            lowerError = aod.iloc[:, 2] - aod.iloc[:, 3]
            upperError = aod.iloc[:, 4] - aod.iloc[:, 2]
            color = colors[key]
            marker = markers [key]
            desvS = []
            self.screen.plotChannelData(aodDateX, aodTempY, yMinimo, yMaximo, lowerError, upperError, desvS, key, color, marker)
    
    #Recupera los datos de la temperatura y los manda a la vista para su representación    
    def graficaTemperatura(self):
        self.screen.plotSimpleData(self.tDateX, self.tTempY, "Temperatura")
        
    #Recupera los datos del vapor de aua y los manda a la vista para su representación    
    def graficaWVapor(self):
        self.screen.plotSimpleData(self.wVDateX, self.wVaporY, "Vapor de agua")
        
    #Recupera los datos de WExp y los manda a la vista para su representación    
    def graficaWExp(self):
        self.screen.plotWExp(self.wEDateX, self.wExpAlpha440Y, self.wExpAlpha380Y)
        