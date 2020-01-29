'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''


import src.modelo.globales as g

class consultaBBDD():
    
    def getPhStation(self, cursor):
        listPhStation=[]
        try:
            cursor.execute(g.sql2)
            data = cursor.fetchall()
            for row in data:
                listPhStation.append(row)
        except ValueError:
            print(g.err1)
        
        print (listPhStation)
        return data