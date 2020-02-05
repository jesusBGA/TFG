'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

import src.modelo.globales as g
import src.modelo.phStationObject as objecto
import sys

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
    
    #Metodo que consulta a la BBDD por los datos completos de cada ph y station (dates y eprom type/subtype)
    def getPhStationDates(self, cursor):
        #listPhStation=[]
        indices =[]
        datosCompletos=[]
        contador=0
        try:
            cursor.execute(g.sql2)
            data = cursor.fetchall()
            for row in data:
                fechas = []
                aux = str(row[0])+"  "+ str(row[1])
                #listPhStation.append(row)
                if aux not in indices:
                    indices.append(aux)
                    o = objecto.phStationObject(aux, row[4], row[5])
                    fechas.append(row[2])
                    fechas.append(row[3])
                    o.setDateOfUse(fechas)
                    datosCompletos.append(o)
                    #print (o.__dict__)
                    contador+=1
                else:
                    o=datosCompletos[contador-1]
                    datosCompletos.remove(o)
                    fechas.append(row[2])
                    fechas.append(row[3])
                    o.setDateOfUse(fechas)
                    datosCompletos.append(o)
                    
        except ValueError:
            print(g.err1)
               
        return datosCompletos
    
    #Metodo para obtener la fecha más antigua de la vida de los fotometros
    def minFecha(self, cursor):
        try:    
            cursor.execute(g.sql3)
            return cursor.fetchone()
        except ValueError:
            print(g.err1)
        
    #Metodo para obtener la fecha futura más amplia de la vida de los fotometros
    def maxFecha(self, cursor):
        try:
            cursor.execute(g.sql4)
            return cursor.fetchone()
        except ValueError:
            print(g.err1)
    
    #Metodo para obtener los datos AOD para un fotometro y unas fechas dadas
    def getAODChannels(self, cursor, ph):
        try:
            cursor.execute("SELECT C.channel, C.date, avg(C.aod) FROM caelis.cml_aod_channel C JOIN caelis.cml_aod A ON (A.ph=C.ph && A.date=C.date) WHERE (C.ph=10 && C.aod is not null) GROUP BY C.channel, C.date;")
            return cursor.fetchall()
        except:
           print(sys.exc_info())       