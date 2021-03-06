'''
Created on 29 ene. 2020

@author: Jesus Brezmes Gil-Albarellos
'''
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from pandas.plotting import register_matplotlib_converters
from matplotlib.dates import DateFormatter

from matplotlib.dates import num2date
import math
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['toolbar'] = 'toolmanager'
import matplotlib.dates as mdates
from matplotlib.collections import PolyCollection

#Modificaciones: quitar src
from src.vista.NavigationToolbar import NavigationToolbar

#Ventana principal de la aplicación
class mainWindow(QWidget):

    def __init__(self, main_controller):
        
        QWidget.__init__(self)
        
        self.main_controller = main_controller
        
        #Título y tamaño de la ventana principal
        self.setWindowTitle("CÆLIS Viewer")
        self.setFixedSize(1400,800)
        
        #Tabla para mostrar los datos
        self.tablaL = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setFixedWidth(140)
        self.tableWidget.setFixedHeight(450)
        self.tableWidget.setColumnWidth(0, 140)
        self.tableWidget.doubleClicked.connect(self.phClicked)
        self.tableWidget.setFont(QFont('Times New Roman', 10, QFont.Bold))
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalScrollBar().setDisabled(True)
        self.tableWidget.verticalScrollBar().setDisabled(True)
        self.tablaL.addItem(QtWidgets.QSpacerItem(0, 24))
        self.tablaL.addWidget(self.tableWidget)
        self.tablaL.addItem(QtWidgets.QSpacerItem(0, 25))
        
        #Layout y botón de salir
        self.quitButton = QPushButton("Salir")
        self.quitButton.clicked.connect(self.quit)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.setContentsMargins(0,0,10,10)
        self.hbox.addWidget(self.quitButton)
        
        #Layout grafica y navigation toolbar
        self.horizontalLayout = QVBoxLayout()
        
        #Scrollbar para navegar interactivamente por la grafica
        self.contador=2
        self.scrollLayout = QVBoxLayout()
        s_widget = QWidget()
        s_widget.setLayout(self.scrollLayout)
        s_widget.setFixedWidth(50)
        s_widget.setFixedHeight(480)
        self.scrollBar = QtWidgets.QScrollBar()
        self.scrollBar.setFixedWidth(30)
        self.scrollBar.sliderMoved.connect(self.sliderValue)
        self.scrollBar.sliderPressed.connect(self.sliderValue)
        self.scrollBar.valueChanged.connect(self.sliderValue)
        self.scrollLayout.addWidget(self.scrollBar)
        
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
        self.labelsLayout.addItem(QtWidgets.QSpacerItem(170, 0))
        self.labelFmin = QLabel()
        self.labelsLayout.addWidget(self.labelFmin)
        self.labelFmin.setAlignment(QtCore.Qt.AlignLeft)
        #self.labelsLayout.addItem(QtWidgets.QSpacerItem(0, 0, QSizePolicy.Expanding))
        self.labelFmax = QLabel()
        self.labelsLayout.addWidget(self.labelFmax)
        self.labelFmax.setAlignment(QtCore.Qt.AlignRight)
        self.labelsLayout.addItem(QtWidgets.QSpacerItem(80, 0))
        self.lLayout.addWidget(l_widget)
        
        #Layout filtro de datos
        self.filtroLayout = QHBoxLayout()
        self.filtroLayout.setObjectName("filtroLayout")
        f_widget = QWidget()
        f_widget.setLayout(self.filtroLayout)
        f_widget.setFixedHeight(158)
        #Variables auxiliares para el manejo de los radioButtons
        self.auxEprom = ""
        self.aux2Eprom = ""
        self.auxNubes = "1.0"
        self.aux2Nubes = ""
        
        #Campos de texto filtrado por ph y estacion
        self.campo = QGroupBox("Búsqueda")
        self.campoData = QVBoxLayout()
        self.labelDevice = QLabel()
        self.labelDevice.setText("Device:")
        self.device = QLineEdit(self)
        self.device.returnPressed.connect(self.enterDevSite)
        self.labelSite = QLabel()
        self.labelSite.setText("Site:")
        self.site = QLineEdit(self)
        self.site.returnPressed.connect(self.enterDevSite)
        self.campoData.addWidget(self.labelDevice)
        self.campoData.addWidget(self.device)
        self.campoData.addWidget(self.labelSite)
        self.campoData.addWidget(self.site)
        self.campo.setLayout(self.campoData)
        self.filtroLayout.addWidget(self.campo)
        
        #Botones filtrado por eprom y subeprom type
        self.eprom = QGroupBox("Eprom_type/subtype")
        self.epromData = QVBoxLayout()
        self.standard = QRadioButton('Standard')
        self.digital = QRadioButton('Digital Extended')
        self.triple = QRadioButton('Triple')
        self.dualpolar = QRadioButton('Dualpolar')
        #option_1.setChecked(True)  
        self.group = QButtonGroup(self)
        self.group.addButton(self.standard)
        self.group.addButton(self.digital)
        self.group.addButton(self.triple)
        self.group.addButton(self.dualpolar)
        self.epromData.addWidget(self.standard)
        self.epromData.addWidget(self.digital)
        self.epromData.addWidget(self.triple)
        self.epromData.addWidget(self.dualpolar)
        self.eprom.setLayout(self.epromData)
        self.filtroLayout.addWidget(self.eprom)
        self.group.buttonClicked['QAbstractButton *'].connect(self.epromClicked)
        
        #Botones filtrado aod(1.0) y aod(1.5)
        self.nubes = QGroupBox("Cloud Level")
        self.nubesData = QVBoxLayout()
        self.n1 = QRadioButton('AOD(1.0)')
        self.n15 = QRadioButton('AOD(1.5)')
        self.n1.setChecked(True)
        self.group2 = QButtonGroup(self)
        self.group2.addButton(self.n1)
        self.group2.addButton(self.n15)
        self.nubesData.addWidget(self.n1)
        self.nubesData.addWidget(self.n15)
        self.nubes.setLayout(self.nubesData)
        self.filtroLayout.addWidget(self.nubes)
        self.filtroLayout.addItem(QtWidgets.QSpacerItem(400, 0))
        self.group2.buttonClicked['QAbstractButton *'].connect(self.nubesClicked)
        
        #Estructuracion de los layouts
        self.graficaLayout.addLayout(self.tablaL)
        #self.graficaLayout.addWidget(self.canvas)
        self.graficaLayout.addWidget(c_widget)
        self.graficaLayout.addWidget(s_widget)
        self.toolbarLayout.addWidget(self.toolBar)
        self.horizontalLayout.addLayout(self.graficaLayout)
        self.horizontalLayout.addLayout(self.lLayout)
        self.horizontalLayout.addLayout(self.toolbarLayout)
        self.horizontalLayout.addWidget(f_widget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        
        #Evento que detecta la modificación de la gráfica
        self.canvas.mpl_connect("draw_event", self.fechaEvent)
        
        #Layout de la grafica 
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
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
    def plotUsoPh(self, datosPhSt, datosCompletos, fechaMin, fechaMax, cloudLevel):
        #print (str(datosCompletos[0].__getattribute__('phStation')))
        longitud=len(datosPhSt)
        self.scrollBar.setMaximum(longitud)
        self.scroll = longitud
        self.scrolled = longitud
        self.fMin=fechaMin
        self.fMax=fechaMax
        self.alturaTabla=self.tableWidget.height()
        self.datosPH=datosPhSt
        self.datosC=datosCompletos
        verts = []
        colors = []
        labels = []
        yPosition = []
        cats={}
        colormapping={}
        
        if (cloudLevel == "1.5"):
            self.aux2Nubes="1.5"
            df = pd.DataFrame([t.__dict__ for t in self.datosC])
            datosPhSt = df['phStation']
            self.datosPH = datosPhSt
            longitud=len(datosPhSt)
            self.scrollBar.setMaximum(longitud)
            self.scroll = longitud
            self.scrolled = longitud
            #Posición en el eje y de cada fotometro
            for data in datosPhSt:
                clave = data
                cats[clave]=longitud
                labels.insert(0, clave)
                yPosition.insert(0, longitud)
                longitud-=1
        else:
            self.aux2Nubes = ""
            #Posición en el eje y de cada fotometro
            for data in datosPhSt:
                clave=str(data[0])+" "+str(data[1])
                cats[clave]=longitud
                labels.insert(0, clave)
                yPosition.insert(0, longitud)
                longitud-=1
        
        
        
        #Color según el eprom_type/subtype
        for e in self.datosC:
            clave = e.__getattribute__('phStation')
            if (e.__getattribute__('eprom_type')== 'standard'):
                colormapping[clave]="gray"
            elif (e.__getattribute__('eprom_subtype')== 'triple'):
                colormapping[clave]="tab:orange"
            elif ((e.__getattribute__('eprom_subtype')== 'digital') & (e.__getattribute__('eprom_type')== 'extended')):
                colormapping[clave]="tab:brown"
            elif ((e.__getattribute__('eprom_subtype')!= 'triple') & (e.__getattribute__('eprom_type')== 'dualpolar')):
                colormapping[clave]="tab:blue"
            else:    
                colormapping[clave]="gray"
        
        #Representación de los fotometros por poligonos    
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
        
        #Configuracion de los ejes
        self.ax.add_collection(bars)
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.ax.set_xlim([fechaMin,fechaMax])
        self.ax.set_xticklabels([])
        self.ax.set_yticks(yPosition)
        if (len(datosPhSt)>14):
            self.ax.set_ylim([len(datosPhSt)-14.5, len(datosPhSt)+.5])
        else:
            self.ax.set_ylim([len(datosPhSt)-len(datosPhSt)+.5, len(datosPhSt)+.5])
        self.ax.set_yticklabels([])
        self.toolBar.clearCursor()
        self.fig.tight_layout()                      
    
    #Accion del slider para navegar por la gráfica
    def sliderValue(self):
        if(self.scroll>15):
            value = self.scroll - self.scrollBar.value()
            fmin= self.getXMin()
            fmax= self.getXMax()
            if ((self.scroll-value)<5):
                self.ax.set_ylim([self.scroll-14.5, self.scroll+.5])
                self.canvas.draw_idle()
                self.scrolled=self.scroll
            elif ((self.scroll - self.scrollBar.value())<15):
                self.ax.set_ylim([0.5, 15.5])
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
        if (minY<0):
            minY = 0
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
            rows=d         
        elif(dS<15 & dS!=0):
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
            if (nRows>=1):
                altura = self.alturaTabla / nRows
            
        if (nRows>=1):
            self.tableWidget.clear()
            self.tableWidget.reset()
            self.tableWidget.setRowCount(nRows)
            while (contador<nRows):
                if (self.aux2Nubes=="1.5"):
                    item = self.datosPH[value]
                else:
                    i = self.datosPH[value]
                    item = str(i[0])+"  "+i[1] 
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
                self.tableWidget.setItem(contador,0, cellinfo)
                #labels.append(str(dato[0])+" "+str(dato[1]))
                self.tableWidget.setRowHeight(contador, altura)
                contador+=1
                value+=1
        else:
            self.limpiaTabla()
            self.mensajeNoDatos() 
    
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
    
    #Acción de seleccionar un botónn de eprom/subeprom type        
    def epromClicked(self, button):
        clicked = button.text()
        self.aux2Eprom = clicked
        #Implica quitar el filtro, equivale a pulsar sobre el eprom que está marcado
        if (self.auxEprom == self.aux2Eprom):
            self.group.setExclusive(False)
            self.group.checkedButton().setChecked(False)
            self.group.setExclusive(True)
            self.auxEprom = ""
            message = ""
            message, ph = self.compruebaDevice(message)
            message, station = self.compruebaSite(message)   
            if (message != ""):
                self.mensajeErrorFormulario(message)
            else: 
                self.main_controller.filtroEpromPhSite("", station, ph, "")
                self.canvas.draw_idle()
        #Implica que el filtro eprom cambia
        else:
            if (self.group2.checkedButton()):
                if (self.group2.checkedButton()):
                    cloudLevel = self.group2.checkedButton().text()
                    if (cloudLevel == "1.0"):
                        cloudLevel = ""
                message = ""
                message, ph = self.compruebaDevice(message)
                message, station = self.compruebaSite(message)   
                if (message != ""):
                    self.mensajeErrorFormulario(message)
                else: 
                    self.main_controller.filtroEpromPhSite(clicked, station, ph, cloudLevel)
                    self.canvas.draw_idle()
                self.auxEprom = clicked
        
    #Acción de seleccionar un botónn de eprom/subeprom type        
    def nubesClicked(self, button):
        self.clicked = button.text()
        if (self.clicked == "AOD(1.0)"):
            self.clicked = "1.0"
        else:
            self.clicked = "1.5"
        if (self.auxNubes != self.clicked):
            if (self.group2.checkedButton()):
                cloudLevel = self.clicked
                if (cloudLevel == "1.0"):
                        cloudLevel = ""
            message = ""
            message, ph = self.compruebaDevice(message)
            message, station = self.compruebaSite(message)   
            if (message != ""):
                self.mensajeErrorFormulario(message)
            else: 
                if (self.group.checkedButton()):
                    filtroEprom = self.group.checkedButton().text()
                else:
                    filtroEprom = ""    
                self.main_controller.filtroEpromPhSite(filtroEprom, station, ph, cloudLevel)
        self.auxNubes = self.clicked
    
    #Acción de pulsar enter en los campos de entrada device y site
    def enterDevSite(self):
        message = ""
        message, ph = self.compruebaDevice(message)
        message, station = self.compruebaSite(message)   
        if (message != ""):
            self.mensajeErrorFormulario(message)
        else: 
            if (self.group.checkedButton()):
                filtroEprom = self.group.checkedButton().text()
            else:
                filtroEprom = ""
            if (self.group2.checkedButton()):
                cloudLevel = self.group2.checkedButton().text()
                if (cloudLevel == "1.0"):
                    cloudLevel = ""
            self.main_controller.filtroEpromPhSite(filtroEprom, station, ph, cloudLevel)
    
    #Comprueba el formulario del campo de entrada de datos site
    def compruebaSite(self, message):
        try:
            if (self.site.text()):
                if (int(self.site.text())):
                    station = ""
                    message = message + "\nEl campo Site no puede ser un número."
                    self.site.clear()
            else:
                station = "" 
        except:
            station = self.site.text()
        return message, station
        
    #Comprueba el formulario del campo de entrada de datos site    
    def compruebaDevice(self, message):
        try:
            if (self.device.text()): 
                ph = int(self.device.text())
                ph = str(self.device.text())
            else:
                ph = ""
        except:
            ph = ""
            message = message + "\nEl campo Device debe ser un número."
            self.device.clear()
        return message, ph
    
    #Mensaje error formulario
    def mensajeErrorFormulario(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Comprobación del formulario: \n"+message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    
    #Acción de pulsar sobre un item de la tabla de fotometros    
    def phClicked(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            phStation = currentQTableWidgetItem.text()
        fecha = self.ax.get_xlim()
        f1 = str(num2date(fecha[0]))
        f2 = str(num2date(fecha[1]))
        fMin = f1[0:19]
        fMax = f2[0:19]
        self.main_controller.graphWindow(phStation, fMin, fMax)
            
    #Reiniciar y dar formato a los ejes de la gráfica    
    def limpiaPlot(self):
        self.ax.clear()
        self.ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%Y %H:%M:%S'))
        self.ax.set_xlim([self.fMin, self.fMax])
        self.scrollBar.setValue(0)
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.fig.tight_layout() 
        self.canvas.draw_idle()
    
    #Reiniciar la tabla con los valores si en el filtrado no hay resultados    
    def limpiaTabla(self):
        self.tableWidget.clear()
        self.tableWidget.reset()
    
    #Vuelve a poner a AOD(1.0) como opción, consecuencia de no haber encontrado datos AOD(1.5)    
    def reiniciaCloudLevel(self):
        self.n1.setChecked(True)
        self.clicked = "1.0"
        
    #Mensaje no hay datos para el filtro
    def mensajeNoDatos(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No hay datos disponibles que concuerden con esta operación.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec()
    
    #Comunica al controller la finalizacion de la ejecucion
    def quit(self):
        self.main_controller.salir()
    
    