'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5 import QtCore, QtGui, QtWidgets
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from mysql.connector import (connection)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter

from matplotlib.dates import num2date
import math
import matplotlib.pyplot as plt
from matplotlib import backend_bases
plt.rcParams['toolbar'] = 'toolmanager'
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

from src.vista.NavigationToolbar import NavigationToolbar

#Ventana principal de la aplicación
class mainWindow(QWidget):

    def __init__(self, main_controller):
        
        QWidget.__init__(self)
        
        self.main_controller = main_controller
        
        #Título y tamaño de la ventana principal
        self.setWindowTitle("Aeronet")
        self.setFixedSize(1400,800)
        
        #Tabla para mostrar las fechas
        '''self.tableFWidget = QTableWidget()
        self.tableFWidget.setRowCount(1)
        self.tableFWidget.setColumnCount(10)
        self.tableFWidget.setMaximumHeight(20)'''
        
        #Tabla para mostrar los datos
        self.tablaL = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setFixedWidth(140)
        self.tableWidget.setFixedHeight(450)
        self.tableWidget.setColumnWidth(0, 140)
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget.setFont(QFont('Times New Roman', 10, QFont.Bold))
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalScrollBar().setDisabled(True)
        self.tableWidget.verticalScrollBar().setDisabled(True)
        self.tablaL.addItem(QtWidgets.QSpacerItem(0, 24))
        self.tablaL.addWidget(self.tableWidget)
        self.tablaL.addItem(QtWidgets.QSpacerItem(0, 25))
        
        
        self.quitButton = QPushButton("Salir")
        self.quitButton.clicked.connect(self.quit)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.setContentsMargins(0,0,10,10)
        self.hbox.addWidget(self.quitButton)
        
        #Layout grafica y navigation toolbar
        self.horizontalLayout = QVBoxLayout()
        
        #Scrollbar para navegar interactivamente por la grafica
        '''self.pagesLayout = QVBoxLayout()
        v_widget = QWidget()
        v_widget.setLayout(self.pagesLayout)
        v_widget.setFixedWidth(50)'''
        self.contador=2
        self.scrollLayout = QVBoxLayout()
        s_widget = QWidget()
        s_widget.setLayout(self.scrollLayout)
        s_widget.setFixedWidth(50)
        self.scrollBar = QtWidgets.QScrollBar()
        self.scrollBar.setFixedWidth(30)
        self.scrollBar.sliderMoved.connect(self.sliderValue)
        self.scrollBar.sliderPressed.connect(self.sliderValue)
        self.scrollBar.valueChanged.connect(self.sliderValue)
        self.scrollLayout.addWidget(self.scrollBar)
        '''self.previousButton = QPushButton("Previous 10")
        self.previousButton.clicked.connect(self.previousPage)
        self.nextButton = QPushButton("Next 10")
        self.nextButton.clicked.connect(self.nextPage)
        self.resetZoomButton = QPushButton("Reset zoom")
        self.resetZoomButton.clicked.connect(self.resetZoom)'''
        #self.pagesLayout.addWidget(s_widget)
        '''self.pagesLayout.addWidget(self.previousButton)
        self.pagesLayout.addWidget(self.nextButton)
        self.pagesLayout.addWidget(self.resetZoomButton)'''
        
        #Grafica y navigation toolbar
        self.toolbarLayout = QHBoxLayout()
        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        register_matplotlib_converters()
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.graficaLayout = QHBoxLayout()
        self.canvasL = QVBoxLayout()
        c_widget = QWidget()
        c_widget.setLayout(self.canvasL)
        c_widget.setFixedHeight(499)
        self.canvas = FigureCanvas(self.fig)
        self.toolBar = NavigationToolbar(self.canvas, self)
        self.canvasL.addWidget(self.canvas)

        #Labels eje x de la grafica para indicar fecha minima y maxima
        self.lLayout = QHBoxLayout()
        self.labelsLayout = QHBoxLayout()
        l_widget = QWidget()
        l_widget.setLayout(self.labelsLayout)
        l_widget.setFixedHeight(37)
        self.labelsLayout.addItem(QtWidgets.QSpacerItem(175, 0))
        self.labelFmin = QLabel()
        self.labelsLayout.addWidget(self.labelFmin)
        self.labelFmin.setAlignment(QtCore.Qt.AlignLeft)
        #self.labelsLayout.addItem(QtWidgets.QSpacerItem(0, 0, QSizePolicy.Expanding))
        self.labelFmax = QLabel()
        self.labelsLayout.addWidget(self.labelFmax)
        self.labelFmax.setAlignment(QtCore.Qt.AlignRight)
        self.labelsLayout.addItem(QtWidgets.QSpacerItem(85, 0))
        self.lLayout.addWidget(l_widget)
        
        #Estructuracion de los layouts
        self.graficaLayout.addLayout(self.tablaL)
        #self.graficaLayout.addWidget(self.canvas)
        self.graficaLayout.addWidget(c_widget)
        self.graficaLayout.addWidget(s_widget)
        self.toolbarLayout.addWidget(self.toolBar)
        self.horizontalLayout.addLayout(self.graficaLayout)
        self.horizontalLayout.addLayout(self.lLayout)
        self.horizontalLayout.addLayout(self.toolbarLayout)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        
        '''self.widget = QWidget()
        self.scroll = QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)
        self.canvas.mpl_connect("scroll_event", self.scrolling)'''
        
        #Evento que detecta la modificación de la gráfica
        self.canvas.mpl_connect("draw_event", self.fechaEvent)
        
        #Layout de la grafica 
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 178)
        self.setLayout(self.mainLayout)
        
        #Layout de la barra temporal
        self.timeLayout = QHBoxLayout()
        self.tLayout = QHBoxLayout()
        t_widget = QWidget()
        t_widget.setLayout(self.tLayout)
        self.timeLayout.addItem(QtWidgets.QSpacerItem(60, 0))
        self.timeLayout.addWidget(t_widget)
        self.timeLayout.addItem(QtWidgets.QSpacerItem(60, 0))
        
        #MainLayout de la ventana
        '''self.mainLayout.addWidget(self.tableFWidget)'''
        #self.mainLayout.addLayout(self.timeLayout)
        self.mainLayout.addLayout(self.horizontalLayout)
        self.mainLayout.addLayout(self.hbox)
        self.setLayout(self.mainLayout) 
     
    #Metodo para rellenar la tabla con fotometro y estacion     
    def setDatosTabla(self, datos):
        self.lista = datos
        self.tableWidget.setRowCount(len(datos))
        contador=0  
        #labels=[] 
        for dato in datos:
            item = str(dato[0])+"  "+str(dato[1]) 
            cellinfo = QTableWidgetItem(item)
            cellinfo.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.tableWidget.setItem(contador,0, cellinfo)
            #labels.append(str(dato[0])+" "+str(dato[1]))
            contador+=1
        #self.tableWidget.setVerticalHeaderLabels(labels)
        
    #Metodo para plotear la grafica de uso
    def plotUsoPh(self, datosPhSt, datosCompletos, fechaMin, fechaMax):
        #print (str(datosCompletos[0].__getattribute__('phStation')))
        longitud=len(datosPhSt)
        self.scrollBar.setMaximum(longitud)
        self.scroll = longitud
        self.scrolled = longitud
        self.fMin=fechaMin
        self.fMax=fechaMax
        self.datosPH=datosPhSt
        self.datosC=datosCompletos
        self.alturaTabla=self.tableWidget.height()
        verts = []
        colors = []
        labels = []
        yPosition = []
        cats={}
        colormapping={}
        
        for data in datosPhSt:
            clave=str(data[0])+" "+str(data[1])
            cats[clave]=longitud
            labels.insert(0, clave)
            yPosition.insert(0, longitud)
            longitud-=1
        
        for e in self.datosC:
            clave = e.__getattribute__('phStation')
            if (e.__getattribute__('eprom_subtype')== 'triple'):
                colormapping[clave]="tab:orange"
            elif ((e.__getattribute__('eprom_subtype')== 'digital') & (e.__getattribute__('eprom_type')== 'extended')):
                colormapping[clave]="tab:brown"
            elif ((e.__getattribute__('eprom_subtype')!= 'triple') & (e.__getattribute__('eprom_type')== 'dualpolar')):
                colormapping[clave]="tab:blue"
            else:    
                colormapping[clave]="gray"
            
        for elemento in datosCompletos:
            fechas = elemento.__getattribute__('dateOfUse')
            phStation = elemento.__getattribute__('phStation')
            for f in fechas:
                v =  [(mdates.date2num(f[0]), cats[phStation]-.4),
                      (mdates.date2num(f[0]), cats[phStation]+.4),
                      (mdates.date2num(f[1]), cats[phStation]+.4),
                      (mdates.date2num(f[1]), cats[phStation]-.4),
                      (mdates.date2num(f[0]), cats[phStation]-.4)]
                verts.append(v)
                colors.append(colormapping[phStation])
                
        bars = PolyCollection(verts, facecolors=colors)
        register_matplotlib_converters()
        
        #plt.grid(color='Black', linestyle='solid')
        self.ax.add_collection(bars)
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.ax.set_xlim([fechaMin,fechaMax])
        self.ax.set_xticklabels([])
        #self.fig.autofmt_xdate()
        
        #self.ax.set_yticks(0-len(datosPhSt))
        self.ax.set_yticks(yPosition)
        #self.ax.set_yticklabels(labels)
        self.ax.set_ylim([len(datosPhSt)-14.5, len(datosPhSt)+.5])
        self.ax.set_yticklabels([])
        self.fig.tight_layout()                      
    
    #Accion del slider para navegar por la gráfica
    def sliderValue(self):
        value = self.scroll - self.scrollBar.value()
        fmin= self.getXMin()
        fmax= self.getXMax()
        if ((self.scroll-value)<5):
            self.ax.set_ylim([self.scroll-14.5, self.scroll+.5])
            self.canvas.draw_idle()
            self.scrolled=self.scroll
        elif ((self.scroll - self.scrollBar.value())<15):
            self.ax.set_ylim([0, 15])
            self.canvas.draw_idle()
            self.scrolled = 15
        elif (value>=0 & value<=self.scroll):
            self.ax.set_ylim([value-14.5, value+.5])
            self.canvas.draw_idle()
            self.scrolled=value
        
        #print(self.tableWidget.rowAt(0))
        #self.tableWidget.scrollToItem(self.tableWidget.itemAt(0, 19), QAbstractItemView.EnsureVisible | QAbstractItemView.PositionAtTop )
        #Control para no borrar registro de acciones si se mueve el scroll con el zoom activado
        self.toolBar.push_current()
        #self.changeTableW()
        if ((fmin==str(self.fMin)) & (fmax==str(self.fMax))):
            self.toolBar.clearCursor()
    
    #Obtener valores minimo actual del eje x
    def getXMin(self):
        fecha = self.ax.get_xlim()
        fmin = str(num2date(fecha[0]))
        return fmin[0:19]
    
    #Obtener valor maximo actual del eje x
    def getXMax(self):
        fecha = self.ax.get_xlim()
        fmax = str(num2date(fecha[1]))
        return fmax[0:19]
    
    #Obtener valores minimo actual del eje y
    def getYMin(self):
        minY = self.ax.get_ylim()
        return minY[0]
    
    #Obtener valor maximo actual del eje y
    def getYMax(self):
        maxY = self.ax.get_ylim()
        return maxY[1]
    
    #Modifica la tabla tras la utilización del slider
    def changeTableW(self):
        fmin= self.getXMin()
        fmax= self.getXMax()
        minY = self.getYMin()
        maxY = self.getYMax()
        if ((fmin==str(self.fMin)) & (fmax==str(self.fMax))):
            if (minY!=0):
                minY-=.5
            if (maxY!=15):
                maxY-=.5
        else:
            if (minY!=0):
                minY = math.floor(minY)
            if (maxY!=15):
                maxY = math.ceil(maxY)
                maxY-=1
        rows=0
        d = maxY-minY
        dS = self.scroll-self.scrollBar.value()
        if (d<15):
            if(dS<15):
                rows=15
            else:
                rows = d 
        elif (dS<15 & dS!=0):
            rows = dS
        else:
            rows=15
        self.changeRows(rows, maxY)
        #self.tableWidget.resizeRowsToContents()  Ajustar alto de las celdas
        #self.tableWidget.setRowHeight(0, 40)
    
    #Puebla la tabla de fotometros con el numero de filas segun el zoom aplicado      
    def changeRows(self, nRows, maxY):
        contador=0
        altura = 0
        maxY=int(maxY)
        value =self.scroll-maxY
        if (nRows==1):
            altura=self.alturaTabla
        elif (nRows==15):
            altura = self.alturaTabla / 15
        else:
            altura = self.alturaTabla / nRows
            
        if (nRows>=1):
            self.tableWidget.clear()
            self.tableWidget.reset()
            self.tableWidget.setRowCount(nRows)
            while (contador<nRows):
                i = self.datosPH[value]
                item = str(i[0])+"  "+i[1] 
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                self.tableWidget.setItem(contador,0, cellinfo)
                #labels.append(str(dato[0])+" "+str(dato[1]))
                self.tableWidget.setRowHeight(contador, altura)
                contador+=1
                value+=1
    
    #Tras detectar un evento de dibujo sobre la grafica, realiza la llamada para actualizar la tabla de fotometros
    def fechaEvent(self, event):
        self.changeTableW()
        self.setTimeLabels()
    
    #Modifica las labels del ejex, las cuales hacen referencia a la fecha minima y maxima de la grafica      
    def setTimeLabels(self):
        fechaMin = self.getXMin()
        fechaMax = self.getXMax()
        self.labelFmin.setText("<--- " + fechaMin)
        self.labelFmax.setText(fechaMax + " --->")
            
                             
    def scrolling(self, event):
        if (self.contador%2)==0:
            self.contador+=1
            if event.button=="down":
                if self.scrolled>2:
                    self.scrolled-=2
            else:
                if self.scrolled<(self.scroll-2):
                    self.scrolled+=2
                else:
                    self.scrolled= self.scroll
            self.ax.set_ylim([self.scrolled-14.5, self.scrolled+.5])
            self.canvas.draw_idle()
        else:
            self.contador+=1
            
            
    def quit(self):
        print("Salir")
        
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            phStation = currentQTableWidgetItem.text()
        fecha = self.ax.get_xlim()
        f1 = str(num2date(fecha[0]))
        f2 = str(num2date(fecha[1]))
        fMin = f1[0:19]
        fMax = f2[0:19]
        self.main_controller.graphWindow(phStation, fMin, fMax)
        #main.graphWindow(self, phStation, fMin ,fMax)
           
    def on_press(self, event):
        print(event.name)
        lims=self.ax.get_ylim()
        min = math.floor(lims[0])
        max = math.ceil(lims[1]) 
        self.scrolled=max
        
    
    #Accion de avanzar fotometros en la grafica
    def nextPage(self):
        lims=self.ax.get_ylim()
        min = lims[0]
        max = lims[1]
        if self.previousButton.isEnabled()==False:
            self.previousButton.setEnabled(True)
        if self.scrolled>10:
            self.scrolled-=10
            self.ax.set_ylim([self.scrolled-9.5, self.scrolled+.5])
            self.canvas.draw_idle()
            if self.scrolled<=10:
                self.nextButton.setEnabled(False)
                
    #Accion de retroceder fotometros en la grafica
    def previousPage(self):
        lims=self.ax.get_ylim()
        min = lims[0]
        max = lims[1]  
        if self.nextButton.isEnabled()==False:
            self.nextButton.setEnabled(True)
        if self.scrolled<(self.scroll-9):
            self.scrolled+=10
            if self.scroll<self.scrolled+10:
                self.previousButton.setEnabled(False)
        else:
            self.scrolled= self.scroll
                
        self.ax.set_ylim([self.scrolled-9.5, self.scrolled+.5])
        self.canvas.draw_idle()
        
    #Accion de reiniciar el zoom de la gráfica
    def resetZoom(self):
        self.ax.set_xlim([self.fMin,self.fMax])
        if (self.scrolled<=15):
            self.ax.set_ylim([0, 15])
        else:
            self.ax.set_ylim([self.scrolled-14.5, self.scrolled+.5])
        self.canvas.draw_idle()
    
    