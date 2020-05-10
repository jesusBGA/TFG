'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

import src.modelo.globales as g
import sys
from datetime import datetime, timedelta

#Clase para realizar las diferentes consultas a la BBDD
class consultaBBDD():  
    
    #Metodo para consultar los distinct ph y station
    def getPhStation(self, cursor):
        listPhStation=[]
        try:
            cursor.execute(g.sql1)
            data = cursor.fetchall()
            for row in data:
                listPhStation.append(row)
        except ValueError:
            print(g.err1)
        
        return data
    
    #Metodo para obtener la fecha más antigua de la vida de los fotometros
    def minFecha(self, cursor):
        try:    
            cursor.execute(g.sql3)
            fechaMin = cursor.fetchone()
            #Restamos un día a la fecha mínima para dar un poco de margen
            dia = timedelta(days=1)
            fechaMin = fechaMin[0] - dia
            return fechaMin
        except ValueError:
            print(g.err1)
        
    #Metodo para obtener la fecha futura más amplia de la vida de los fotometros
    def maxFecha(self, cursor):
        try:
            cursor.execute(g.sql4)
            fechaMax = cursor.fetchone()
            #Añadimos un día a la fecha maxima para dar un poco de margen
            dia = timedelta(days=1)
            fechaMax = datetime.strptime(fechaMax[0], '%Y-%m-%d %H:%M:%S')
            fechaMax = fechaMax + dia
            return fechaMax
        except ValueError:
            print(g.err1)
    
    #Metodo que consulta a la BBDD por los datos completos de cada ph y station (dates y eprom type/subtype)
    def getPhStationDates(self, cursor):
        try:
            cursor.execute(g.sql2)
            data = cursor.fetchall()
            return data        
        except ValueError:
            print(g.err1)
                
    
    #Metodo para obtener los datos AOD para un fotometro y unas fechas dadas NO UTILIZADO
    def getAODChannels(self, cursor, ph):
        try:
            cursor.execute("select C.channel, C.date, avg(C.aod) as aod FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.date=C.date) WHERE (C.ph=10 && C.aod is not null && C.date between '2019-04-25 00:00:01' and '2019-05-01 00:00:01') GROUP BY C.channel, C.date;")
            return cursor.fetchall()
        except:
            print(sys.exc_info())
    
           
    #Metodo para obtener los datos AOD para un fotometro y unas fechas dadas, con cloud Level 1.0
    def getAODChannelsL1(self, cursor, ph, station, fechaMin, fechaMax):
        try:
            cursor.execute(g.sql51, (station, ph, fechaMin, fechaMax))
            return cursor.fetchall()
        except:
            print(sys.exc_info())
            
    #Metodo para obtener los datos AOD para un fotometro y unas fechas, dadas con cloud Level 1.5
    def getAODChannelsL15(self, cursor, ph, station, fechaMin, fechaMax):
        try:
            cursor.execute(g.sql6, (station, ph, fechaMin, fechaMax))
            return cursor.fetchall()
        except:
            print(sys.exc_info())
            
    #Metodo para obtener las medidas de temperatura para un fotometro y un rango de fechas
    def getTemperatura(self, cursor, ph, station, fechaMin, fechaMax):
        try:
            cursor.execute(g.sql7, (station, ph, fechaMin, fechaMax))
            return cursor.fetchall()
        except:
            print(sys.exc_info())
    
    #Metodo para obtener las medidas de vapor de agua para un fotometro y un rango de fechas
    def getWVapor(self, cursor, ph, station, fechaMin, fechaMax):
        try:
            cursor.execute(g.sql8, (ph, station, fechaMin, fechaMax))
            return cursor.fetchall()
        except:
            print(sys.exc_info())
            
    #Metodo para obtener las medidas de WExp para un fotometro y un rango de fechas
    def getWExp(self, cursor, ph, station, fechaMin, fechaMax):
        try:
            cursor.execute(g.sql9, (ph, station, fechaMin, fechaMax))
            return cursor.fetchall()
        except:
            print(sys.exc_info())
            
    
