'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import pandas as pd
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
        super().__init__()
    
    def start(self, ph, station, fechaMin, fechaMax):
        self.controller = self 
        self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        datosAOD=self.getDatosAOD(ph, station, fechaMin, fechaMax)
        if (any(map(len, datosAOD))):
            self.screen = vg.graphWindow(fechaMin, fechaMax, self.controller)
            self.screen.plotGrafica(datosAOD)
            self.screen.show()
            
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
    
    #Recupera los datos de la temperatura y los manda a la vista para su representación    
    def graficaTemperatura(self):
        self.screen.plotSimpleData(self.tDateX, self.tTempY, "Temperatura")
        
    #Recupera los datos del vapor de aua y los manda a la vista para su representación    
    def graficaWVapor(self):
        self.screen.plotSimpleData(self.wVDateX, self.wVaporY, "Vapor de agua")
        
    ##Recupera los datos de WExp y los manda a la vista para su representación    
    def graficaWExp(self):
        self.screen.plotWExp(self.wEDateX, self.wExpAlpha440Y, self.wExpAlpha380Y)