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
        self.ph = ph
        self.station = station
        self.fechaMin = fechaMin
        self.fechaMax = fechaMax
        self.getDatosAOD(ph, station, fechaMin, fechaMax)
        self.screen = vg.graphWindow(ph, station, fechaMin, fechaMax, self.controller)
        if (any(map(len, self.datosAOD))):
            self.screen.plotGrafica(self.datosAOD)
            self.screen.show()
        else:
            MessageBox.showwarning("Empty!", "No hay datos para el fotómetro: "+str(ph)+ " "+str(station)+" entre las fechas "+str(fechaMin)+" y "+str(fechaMax))
    
    #Devuelve una lista con las medidas AOD para un fotometro, un rango de fechas y cloud level 1.0
    def getDatosAOD(self, ph, station, fechaMin, fechaMax):
        self.datosAOD = c.consultaBBDD.getAODChannelsL1(self, self.cursor, ph, station, fechaMin, fechaMax)
        
    #Devuelve una lista con las medidas AOD para un fotometro, un rango de fechas y cloud level 1.0
    def getDatosAODL1(self, ph, station, fechaMin, fechaMax):
        try:
            datosAOD = c.consultaBBDD.getAODChannelsL1(self, self.cursor, ph, station, fechaMin, fechaMax)
            return datosAOD
        except ValueError:
            datosAOD = []
            print(g.err1)
            return datosAOD
    
    #Devuelve una lista con las medidas AOD para un fotometro, un rango de fechas y cloud level 1.5
    def getDatosAODL15(self, ph, station, fechaMin, fechaMax):
        try:
            datosAOD = c.consultaBBDD.getAODChannelsL15(self, self.cursor, ph, station, fechaMin, fechaMax)
            return datosAOD
        except ValueError:
            datosAOD = []
            print(g.err1)
            return datosAOD
        
    #Devuelve una lista con las medidas de temperaturas para un fotómetro en un rango de fechas y cloud level 1.0
    def getDatosTempL1(self, ph, station, fechaMin, fechaMax):
        try:
            temperatura = c.consultaBBDD.getTemperaturaL1(self, self.cursor, ph, station, fechaMin, fechaMax)
            return temperatura
        except ValueError:
            temperatura = []
            print(g.err1)
            return temperatura
            
    #Devuelve una lista con las medidas de temperaturas para un fotómetro en un rango de fechas y cloud level 1.5
    def getDatosTempL15(self, ph, station, fechaMin, fechaMax):
        try:
            temperatura = c.consultaBBDD.getTemperaturaL15(self, self.cursor, ph, station, fechaMin, fechaMax)
            return temperatura
        except ValueError:
            temperatura = []
            print(g.err1)
            return temperatura
                
    #Devuelve una lista con las medidad WExp para un fotómetro een un rango de fechas y cloud level 1.0
    def getDatosWExpL1(self, ph, station, fechaMin, fechaMax):
        try:
            wExp = c.consultaBBDD.getWExpL1(self, self.cursor, ph, station, fechaMin, fechaMax)
            return wExp
        except ValueError:
            wExp = []
            print(g.err1)
            return wExp        
    
    #Devuelve una lista con las medidad WExp para un fotómetro een un rango de fechas y cloud level 1.5
    def getDatosWExpL15(self, ph, station, fechaMin, fechaMax):
        try:
            wExp = c.consultaBBDD.getWExpL15(self, self.cursor, ph, station, fechaMin, fechaMax)
            return wExp
        except ValueError:
            wExp = []
            print(g.err1)
            return wExp        
        
    #Devuelve una lista con las medidad de vapor de agua para un fotómetro en un rango de fechas y cloud level 1.0
    def getDatosWVaporL1(self, ph, station, fechaMin, fechaMax):
        try:
            wVapor = c.consultaBBDD.getWVaporL1(self, self.cursor, ph, station, fechaMin, fechaMax)
            return wVapor
        except ValueError:
            wVapor = []
            print(g.err1)
            return wVapor 
    
    #Devuelve una lista con las medidad de vapor de agua para un fotómetro en un rango de fechas y cloud level 1.5
    def getDatosWVaporL15(self, ph, station, fechaMin, fechaMax):
        try:
            wVapor = c.consultaBBDD.getWVaporL15(self, self.cursor, ph, station, fechaMin, fechaMax)
            return wVapor
        except ValueError:
            wVapor = []
            print(g.err1)
            return wVapor
        
    #Devuelve una lista con las medidad PWR para un fotómetro en un rango de fechas y cloud level 1.0
    def getDatosPWRL1(self, ph, station, fechaMin, fechaMax):
        try:
            pwr = c.consultaBBDD.getPWRL1(self, self.cursor, ph, station, fechaMin, fechaMax)
            return pwr
        except ValueError:
            pwr = []
            print(g.err1)
            return pwr 
    
    #Devuelve una lista con las medidad PWR para un fotómetro en un rango de fechas y cloud level 1.5
    def getDatosPWRL15(self, ph, station, fechaMin, fechaMax):
        try:
            pwr = c.consultaBBDD.getPWRL15(self, self.cursor, ph, station, fechaMin, fechaMax)
            return pwr
        except ValueError:
            pwr = []
            print(g.err1)
            return pwr  
    
    #Recupera los datos de llas medidas AOD y los manda a la vista para su representación    
    def graficaAOD(self, checkNubes):
        key_func = lambda x: x[0]
        colors = g.fCanalColors
        markers = g.fCanalMarkers
        self.screen.limpiaPlot()
        auxiliar = 0
        if (checkNubes=="1.0"):
            datosAOD = self.getDatosAODL1(self.ph, self.station, self.fechaMin, self.fechaMax)
        elif (checkNubes=="1.5"):
            datosAOD = self.getDatosAODL15(self.ph, self.station, self.fechaMin, self.fechaMax)
        #Si hay datos divide la tupla por canales, y grafica cada canal con su respectiva media, minimo y maximo
        if (any(map(len, datosAOD))):    
            for key, group in itertools.groupby(datosAOD, key_func):
                AOD = list(group)
                aod = pd.DataFrame(AOD)
                aodDateX = aod.iloc[:, 1]
                aodTempY = aod.iloc[:, 2]
                aodBanda = aod.iloc[:, 5]
                #Wlc: ancho de banda para la leyenda
                banda = aodBanda[0]*1000
                banda = round(banda, 2)
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
                self.screen.plotChannelData(aodDateX, aodTempY, yMinimo, yMaximo, lowerError, upperError, desvS, banda, color, marker)
        else:
            self.screen.limpiaPlot()        
    
    #Recupera los datos de la temperatura y los manda a la vista para su representación, cloud level 1.0    
    def graficaTemperaturaL1(self):
        temperatura = self.getDatosTempL1(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, temperatura))):
            t = pd.DataFrame(temperatura)
            tDateX = t.iloc[:, 0]                
            tTempY = t.iloc[:, 1]
            self.screen.plotSimpleData(tDateX, tTempY, "Temperatura")
        else:
            self.screen.limpiaPlot() 
        
    #Recupera los datos de la temperatura y los manda a la vista para su representación, cloud level 1.0    
    def graficaTemperaturaL15(self):
        temperatura = self.getDatosTempL15(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, temperatura))):
            t = pd.DataFrame(temperatura)
            tDateX = t.iloc[:, 0]
            tTempY = t.iloc[:, 1]
            self.screen.plotSimpleData(tDateX, tTempY, "Temperatura")
        else:
            self.screen.limpiaPlot() 
        
    #Recupera los datos del vapor de aua y los manda a la vista para su representación, cloud level 1.0    
    def graficaWVaporL1(self):
        wVapor = self.getDatosWVaporL1(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, wVapor))):
                wV = pd.DataFrame(wVapor)
                self.wVDateX = wV.iloc[:, 0]
                self.wVaporY = wV.iloc[:, 1]
                self.screen.plotSimpleData(self.wVDateX, self.wVaporY, "Vapor de agua")
        else:
            self.screen.limpiaPlot()
        
    #Recupera los datos del vapor de aua y los manda a la vista para su representación, cloud level 1.5    
    def graficaWVaporL15(self):
        wVapor = self.getDatosWVaporL15(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, wVapor))):
                wV = pd.DataFrame(wVapor)
                wVDateX = wV.iloc[:, 0]
                wVaporY = wV.iloc[:, 1]
                self.screen.plotSimpleData(wVDateX, wVaporY, "Vapor de agua")
        else:
            self.screen.limpiaPlot()
        
    #Recupera los datos de WExp y los manda a la vista para su representación, cloud level 1.0     
    def graficaWExpL1(self):
        wExp = self.getDatosWExpL1(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, wExp))):
                wE = pd.DataFrame(wExp)
                wEDateX = wE.iloc[:, 0]
                wExpAlpha440Y = wE.iloc[:, 1]    
                wExpAlpha380Y = wE.iloc[:, 2]
                self.screen.plotWExp(wEDateX, wExpAlpha440Y, wExpAlpha380Y)
        else:
            self.screen.limpiaPlot()
        
    #Recupera los datos de WExp y los manda a la vista para su representación, cloud level 1.5     
    def graficaWExpL15(self):
        wExp = self.getDatosWExpL15(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, wExp))):
                wE = pd.DataFrame(wExp)
                wEDateX = wE.iloc[:, 0]
                wExpAlpha440Y = wE.iloc[:, 1]    
                wExpAlpha380Y = wE.iloc[:, 2]
                self.screen.plotWExp(wEDateX, wExpAlpha440Y, wExpAlpha380Y)
        else:
            self.screen.limpiaPlot()
    
        
    #Recupera los datos de PWR y los manda a la vista para su representación, cloud level 1.0     
    def graficaPWRL1(self):
        pwr = self.getDatosPWRL1(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, pwr))):
                PWR = pd.DataFrame(pwr)
                pwrDateX = PWR.iloc[:, 0]
                pwrY = PWR.iloc[:, 1]
                self.screen.plotSimpleData(pwrDateX, pwrY, "PWR")
        else:
            print ("No hay datos")
            self.screen.limpiaPlot()
        
    #Recupera los datos de PWR y los manda a la vista para su representación, cloud level 1.5     
    def graficaPWRL15(self):
        pwr = self.getDatosPWRL15(self.ph, self.station, self.fechaMin, self.fechaMax)
        if (any(map(len, pwr))):
                PWR = pd.DataFrame(pwr)
                pwrDateX = PWR.iloc[:, 0]
                pwrY = PWR.iloc[:, 1]
                self.screen.plotSimpleData(pwrDateX, pwrY, "PWR")
        else:
            print ("No hay datos")
            self.screen.limpiaPlot()
        