'''
Created on 28 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''

from src.controlador.mainWController import mainWController
import sys
from PyQt5.QtWidgets import QMessageBox
import pymysql
import src.modelo.globales as g
    
class main:
       
    def __init__(self): 
        '''self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
        self.cursor = self.db.cursor()
        #self.cursor.query('SET GLOBAL connection_timeout=600')
        mainWController()
        #graphController()'''
        try:
            self.db = pymysql.connect(g.database_host, g.user, g.password, g.database_name)
            self.cursor = self.db.cursor()
            self.cursor.execute('SELECT version();')
            version = self.cursor.fetchall()
            print("SQL Server: "+str(version[0]))
            self.db.close()
            self.main_controller = mainWController()
            self.main_controller.start()
        except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
            print("No ha sido posible establecer conexión con la base de datos:\n", e)
            sys.exit(1)
        
if __name__ == '__main__':    
    main()
    sys.exit(main.exec_())
   
'''class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_controller = mainWController()
        self.main_controller.start()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_()) '''       

