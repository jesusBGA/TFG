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
        data = []
        try:
            cursor.execute(g.distinctPhStation)
            data = cursor.fetchall()
        except ValueError:
            print(g.err1)
        return data
    
    #Metodo para consultar los distinct ph y station, filtrando por eprom_type/subtype
    def getPhStation101(self, cursor, filtro):
        data = []
        try:
            query = g.distinctPhStationFiltro % filtro
            cursor.execute(query)
            data = cursor.fetchall()
        except ValueError:
            print(g.err1)
        return data
    
    #Metodo para obtener la fecha más antigua de la vida de los fotometros
    def minFecha(self, cursor):
        try:    
            cursor.execute(g.minFecha)
            fechaMin = cursor.fetchone()
            #Restamos un día a la fecha mínima para dar un poco de margen
            dia = timedelta(days=1)
            fechaMin = fechaMin[0] - dia
            return fechaMin
        except ValueError:
            print(g.err1)
            
    #Metodo para obtener la fecha más antigua de la vida de los fotometros con filtro
    def minFechaFiltro(self, cursor, filtro):
        try: 
            query = g.minFechaFiltro % filtro   
            cursor.execute(query)
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
            cursor.execute(g.maxFecha)
            fechaMax = cursor.fetchone()
            #Añadimos un día a la fecha maxima para dar un poco de margen
            dia = timedelta(days=1)
            fechaMax = datetime.strptime(fechaMax[0], '%Y-%m-%d %H:%M:%S')
            fechaMax = fechaMax + dia
            return fechaMax
        except ValueError:
            print(g.err1)
            
    #Metodo para obtener la fecha más antigua de la vida de los fotometros con filtro
    def maxFechaFiltro(self, cursor, filtro):
        try:    
            query = g.maxFechaFiltro % filtro   
            cursor.execute(query)
            fechaMax = cursor.fetchone()
            #Restamos un día a la fecha mínima para dar un poco de margen
            dia = timedelta(days=1)
            fechaMax = datetime.strptime(fechaMax[0], '%Y-%m-%d %H:%M:%S')
            fechaMax = fechaMax + dia
            return fechaMax
        except ValueError:
            print(g.err1)
    
    #Metodo para obtener la fecha minima con datos y filtro cloud level 1.0
    def minFechaFiltroL1(self, cursor, ph, minFecha, maxFecha):
        fecha = ""
        try:      
            cursor.execute(g.minFechaFiltroL1, (ph, minFecha, maxFecha))
            fecha = cursor.fetchone()
            if (fecha is not None):
                if (fecha[0]):
                    fecha = fecha [0]
            else:
                fecha = ""     
        except ValueError:
            print(g.err1)
            fecha = ""  
        return fecha
            
    #Metodo para obtener la fecha minima con datos y filtro cloud level 1.5
    def minFechaFiltroL15(self, cursor, ph, minFecha, maxFecha):
        fecha = ""
        try:      
            cursor.execute(g.minFechaFiltroL15, (ph, minFecha, maxFecha))
            fecha = cursor.fetchone()
            if (fecha is not None):
                if (fecha[0]):
                    fecha = fecha [0]
            else:
                fecha = ""     
        except ValueError:
            print(g.err1)
            fecha = ""  
        return fecha
            
    #Metodo para obtener la fecha maxima con datos y filtro cloud level 1.0
    def maxFechaFiltroL1(self, cursor, ph, minFecha, maxFecha):
        fecha = ""
        try:      
            cursor.execute(g.maxFechaFiltroL1, (ph, maxFecha, minFecha))
            fecha = cursor.fetchone() 
            if (fecha is not None):
                if (fecha[0]):
                    fecha = fecha [0]
            else:
                fecha = ""     
        except ValueError:
            print(g.err1)
            fecha = ""  
        return fecha
            
    #Metodo para obtener la fecha maxima con datos y filtro cloud level 1.5
    def maxFechaFiltroL15(self, cursor, ph, minFecha, maxFecha):
        fecha = ""
        try:      
            cursor.execute(g.maxFechaFiltroL15, (ph, maxFecha, minFecha))
            fecha = cursor.fetchone() 
            if (fecha is not None):
                if (fecha[0]):
                    fecha = fecha [0]
            else:
                fecha = ""     
        except ValueError:
            print(g.err1)
            fecha = "" 
        return fecha
    
    #Metodo que consulta a la BBDD por los datos completos de cada ph y station (dates y eprom type/subtype)
    def getPhStationDates(self, cursor):
        data = []
        try:
            cursor.execute(g.listPhStationDates)
            data = cursor.fetchall()     
        except ValueError:
            print(g.err1)
        return data 
            
    #Metodo que consulta a la BBDD por los datos completos de cada ph y station filtrando por eprom_type/subtype
    def getPhStationDates21(self, cursor, filtro):
        data = []
        try:
            query = g.listPhStationDatesFiltro % filtro   
            cursor.execute(query)
            data = cursor.fetchall()       
        except ValueError:
            print(g.err1)
        return data 
    
           
    #Metodo para obtener los datos AOD para un fotometro,un rango de fechas y cloud Level 1.0
    def getAODChannelsL1(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.aodL1, (station, ph, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener los datos AOD para un fotometro, un rango de fechas, dadas con cloud Level 1.5
    def getAODChannelsL15(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.aodL15, (station, ph, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener las medidas de temperatura para un fotometro, un rango de fechas y cloud Level L1.0
    def getTemperaturaL1(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.tempL1, (station, ph, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener las medidas de temperatura para un fotometro y un rango de fechas y cloud Level L1.5
    def getTemperaturaL15(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.tempL15, (station, ph, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
    
    #Metodo para obtener las medidas de vapor de agua para un fotometro, un rango de fechas y cloud Level L1.0
    def getWVaporL1(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.waterL1, (ph, station, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener las medidas de vapor de agua para un fotometro, un rango de fechas y cloud Level L1.5
    def getWVaporL15(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.waterL15, (ph, station, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener las medidas de WExp para un fotometro, un rango de fechas y cloud Level L1.0
    def getWExpL1(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.wExpL1, (ph, station, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener las medidas de WExp para un fotometro, un rango de fechas y cloud Level L1.5
    def getWExpL15(self, cursor, ph, station, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.wExpL15, (ph, station, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data 
            
    #Metodo para obtener las medidas PWR para un fotometro y un rango de fechas 
    def getPWR(self, cursor, ph, fechaMin, fechaMax):
        data = []
        try:
            cursor.execute(g.pwr, (ph, fechaMin, fechaMax))
            data = cursor.fetchall()
        except:
            print(sys.exc_info())
        return data    
            
    #NO UTILIZADO/ Prueba
    def getAODChannels(self, cursor, ph):
        try:
            cursor.execute("select C.channel, C.date, avg(C.aod) as aod FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.date=C.date) WHERE (C.ph=10 && C.aod is not null && C.date between '2019-04-25 00:00:01' and '2019-05-01 00:00:01') GROUP BY C.channel, C.date;")
            return cursor.fetchall()
        except:
            print(sys.exc_info())
