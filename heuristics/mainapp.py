import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5 import QtSql
import mysql.connector as MySQLdb
from multiprocessing import Pool

import pandas as pd
import location as loc
import vehicle
from customer import *
from model import *
class DTBDialog(QDialog): #may change layout to table if there are multiple weight and size vehicles
    """create database dialog"""
    def __init__(self):
        super(DTBDialog,self).__init__()
        self.createformbox()
        self.setWindowTitle('Specify Vehicle')
        # set flags
        self.setWindowModality(Qt.ApplicationModal)
        #self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        #create button
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok|QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        #create main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        return
    def createformbox(self):
        """create form"""
        self.formGroupBox = QGroupBox("Vehicle")
        #define data headers
        self.IP=QLineEdit()
        self.Name=QLineEdit()
        self.Password=QLineEdit()
        self.Database=QLineEdit()
        #create form layout
        layout = QFormLayout()
        layout.addRow(QLabel("Server IP:"), self.IP)
        layout.addRow(QLabel("User name:"), self.Name)
        layout.addRow(QLabel("Password:"), self.Password)
        layout.addRow(QLabel("Database:"), self.Database)
        self.formGroupBox.setLayout(layout)
        return

class leftwidget(QWidget):
    def __init__(self):
         super(leftwidget,self).__init__()      
         layout=QVBoxLayout()
         #create tab widget
         self.tabs=QTabWidget()         
         #create first tab
         self.tablewidget=QWidget()
         self.createdatatable()
         #create second tab        
         self.formwidget=QWidget()         
         self.createDCform()
         #add tabs
         self.tabs.addTab(self.tablewidget,"Customer orders")
         self.tabs.addTab(self.formwidget,"form")
         #add layout
         layout.addWidget(self.tabs)
         self.setLayout(layout)
    #create first tab content
    def createdatatable(self):
        """create data table"""
        self.datatable = QTableWidget()
        self.createtbltools()
        #create layout for main window
        layout = QVBoxLayout()       
        layout.addWidget(self.DataToolbar) 
        layout.addWidget(self.datatable) 
        self.tablewidget.setLayout(layout)
    def createtbltools(self):
        """create data table toolbar"""
        self.DataToolbar=QToolBar()
        #add action
        self.hidebtn=QAction(QIcon("image/collaspe.bmp"),"hide columns if pressed.\npress again to show columns")        
        self.DataToolbar.addAction(self.hidebtn)
        self.hidebtn.triggered.connect(self.hide)
        self.hidebtn.setEnabled(False)#set hide button disabled
        return
    def hide(self):
        """collaspe table"""
        if(self.datatable.isColumnHidden(2)==False):
            self.datatable.setColumnHidden(1,True)
            self.datatable.setColumnHidden(2,True)
            self.datatable.setColumnHidden(3,True)
        else:
            self.datatable.setColumnHidden(1,False)
            self.datatable.setColumnHidden(2,False)
            self.datatable.setColumnHidden(3,False)

    #create second tab content
    def createDCform(self):
        """create DC form"""
        #create form box
        self.DCform = QGroupBox("distribution centers")
        self.DCform.setMaximumHeight(150)
        #create form layout
        self.DCLayout=QFormLayout()
        self.createformtools()
        self.DCLayout.addWidget(self.FormToolbar)
        self.DClist=[QLineEdit()]
        self.DCLayout.addRow(QLabel("DC 1"), self.DClist[0])
        self.DCform.setLayout(self.DCLayout)
        #create Vehicle layout
        self.Vform=QGroupBox("Vehicle")
        self.Vform.setMaximumHeight(150)
        self.DeclareVehicle()
        VehicleLayout=QVBoxLayout()
        VehicleLayout.addWidget(self.VTable)
        self.Vform.setLayout(VehicleLayout)
        #create algorithm form layout
        self.algoform = QGroupBox("algorithm")
        algolayout=QVBoxLayout()
        self.algorithm=QComboBox()
        #create algorithm parameters
        self.AlgorithmParamTbl=QTableWidget()
        self.AlgorithmParamTbl.setColumnCount(2)
            #add item to combobox
        self.algorithm.addItem("Genetic Algorithm")
        algolayout.addWidget(self.algorithm)
        algolayout.addWidget(self.AlgorithmParamTbl)
        self.algorithm.currentIndexChanged.connect(self.OnAlgorithmChanged)
        #init
        self.AlgorithmParamTbl.setRowCount(5)
        self.AlgorithmParamTbl.setItem(0,0,QTableWidgetItem("Max Iteration"))
        self.AlgorithmParamTbl.item(0,0).setFlags(Qt.ItemIsEnabled)
        self.AlgorithmParamTbl.setItem(1,0,QTableWidgetItem("Population Size"))
        self.AlgorithmParamTbl.item(1,0).setFlags(Qt.ItemIsEnabled)
        self.AlgorithmParamTbl.setItem(2,0,QTableWidgetItem("Vehicle Weight"))
        self.AlgorithmParamTbl.item(2,0).setFlags(Qt.ItemIsEnabled)
        self.AlgorithmParamTbl.setItem(3,0,QTableWidgetItem("Distance Weight"))
        self.AlgorithmParamTbl.item(3,0).setFlags(Qt.ItemIsEnabled)
        self.AlgorithmParamTbl.setItem(4,0,QTableWidgetItem("Crossover Threshold"))
        self.AlgorithmParamTbl.item(4,0).setFlags(Qt.ItemIsEnabled)
        self.AlgorithmParamTbl.setItem(0,1,QTableWidgetItem("1000"))
        self.AlgorithmParamTbl.setItem(1,1,QTableWidgetItem("50"))
        self.AlgorithmParamTbl.setItem(2,1,QTableWidgetItem("0.8"))
        self.AlgorithmParamTbl.setItem(3,1,QTableWidgetItem("0.2"))
        self.AlgorithmParamTbl.setItem(4,1,QTableWidgetItem("0.8"))
        self.algoform.setLayout(algolayout)        
        #create form tab layout
        self.formwidget.layout=QVBoxLayout()        
        self.formwidget.layout.addWidget(self.DCform)
        self.formwidget.layout.addWidget(self.Vform)
        self.formwidget.layout.addWidget(self.algoform)        
        self.formwidget.setLayout(self.formwidget.layout)
    def OnAlgorithmChanged(self,index):
        if(index==0):
            self.AlgorithmParamTbl.setRowCount(5)
            self.AlgorithmParamTbl.setItem(0,0,QTableWidgetItem("Max Iteration"))
            self.AlgorithmParamTbl.item(0,0).setFlags(Qt.ItemIsEnabled)
            self.AlgorithmParamTbl.setItem(1,0,QTableWidgetItem("Population Size"))
            self.AlgorithmParamTbl.item(1,0).setFlags(Qt.ItemIsEnabled)
            self.AlgorithmParamTbl.setItem(2,0,QTableWidgetItem("Vehicle Weight"))
            self.AlgorithmParamTbl.item(2,0).setFlags(Qt.ItemIsEnabled)
            self.AlgorithmParamTbl.setItem(3,0,QTableWidgetItem("Distance Weight"))
            self.AlgorithmParamTbl.item(3,0).setFlags(Qt.ItemIsEnabled)
            self.AlgorithmParamTbl.setItem(4,0,QTableWidgetItem("Crossover Threshold"))
            self.AlgorithmParamTbl.item(4,0).setFlags(Qt.ItemIsEnabled)
            self.AlgorithmParamTbl.setItem(0,1,QTableWidgetItem("1000"))
            self.AlgorithmParamTbl.setItem(1,1,QTableWidgetItem("50"))
            self.AlgorithmParamTbl.setItem(2,1,QTableWidgetItem("0.8"))
            self.AlgorithmParamTbl.setItem(3,1,QTableWidgetItem("0.2"))
            self.AlgorithmParamTbl.setItem(4,1,QTableWidgetItem("0.8"))
    def createformtools(self):
        """create DC form toolbar"""
        self.FormToolbar=QToolBar()
        #create buttons
        self.addDCbtn=QAction(QIcon("image/add.bmp"),"Add distribution center")
        self.rmEmptyDCbtn=QAction(QIcon("image/minus.bmp"),"Remove empty distribution center")             
        #add action
        self.FormToolbar.addAction(self.addDCbtn)
        self.FormToolbar.addAction(self.rmEmptyDCbtn)
        #set action
        self.addDCbtn.triggered.connect(self.addDistributionCenter)
        self.rmEmptyDCbtn.triggered.connect(self.removeEmptyDC)
        #set flags
        self.addDCbtn.setEnabled(False)
        self.rmEmptyDCbtn.setEnabled(False)
    def addDistributionCenter(self):
        """add 1 distribution center"""
        self.DClist.append(QLineEdit())
        self.DCLayout.addRow(QLabel("DC "+str(len(self.DClist))), self.DClist[len(self.DClist)-1])
    def removeEmptyDC(self):
        """remove empty DC text boxes"""
        index=0
        for i in range(len(self.DClist)):
            if(self.DClist[i].text()==""):   
                index=i
                break
        if(index>0):          
            del self.DClist[index]
            self.DCLayout.removeRow(index+1)
            
    def DeclareVehicle(self):
        """declare vehicle. This function must be activated before pressing calculate button"""
        #create table of vehicles
        self.VTable=QTableWidget()
        self.VTable.setRowCount(1)
        self.VTable.setColumnCount(4)
        self.VTable.setHorizontalHeaderLabels(['Name','Size','Weight','Qty'])
        for i in range(self.VTable.rowCount()):
            for j in range(4):
                self.VTable.setItem(i,j,QTableWidgetItem("_"))
    
class rightconfigwidget(QWidget):

    def __init__(self):
        super(rightconfigwidget,self).__init__()
        self.mainlayout=QVBoxLayout()
        self.undoStack = QUndoStack(self)
        self.createvehicletable()                
        self.mainlayout.addWidget(self.toolbar)
        self.mainlayout.addWidget(self.vehicletable)
        self.setLayout(self.mainlayout)
        return
    def createvehicletable(self):
        self.vehicletable=QTableWidget(self)
        #detect item changed
        self.vehicletable.itemChanged.connect(self.itemChanged)
        self.vehicletable.currentItemChanged.connect(self.getcurrent)
        self.flag=False

        self.createcorrtools()
    def createcorrtools(self):
        self.toolbar=QToolBar()
        #create buttons
        self.addrowbtn=QAction(QIcon("image/add.bmp"),"addrow")
        self.rmrowbtn=QAction(QIcon("image/minus.bmp"),"remove selected row")
        self.undobtn=QAction(QIcon("image/undo.bmp"),"undo")
        self.redobtn=QAction(QIcon("image/redo.bmp"),"redo")
        self.applybtn=QAction(QIcon("image/check.bmp"),"apply")
        #add action
        self.toolbar.addAction(self.addrowbtn)
        self.toolbar.addAction(self.rmrowbtn)
        self.toolbar.addAction(self.undobtn)
        self.toolbar.addAction(self.redobtn)
        self.toolbar.addAction(self.applybtn)
        #set action
        self.addrowbtn.triggered.connect(self.addrow)
        self.rmrowbtn.triggered.connect(self.remove1row)
        self.undobtn.triggered.connect(self.undoStack.undo)
        self.redobtn.triggered.connect(self.undoStack.redo)
        
        #set buttons disabled
        self.addrowbtn.setEnabled(False)
        self.rmrowbtn.setEnabled(False)
        self.undobtn.setEnabled(False)
        self.redobtn.setEnabled(False)
        self.applybtn.setEnabled(False)

        return
    def getcurrent(self,item):
        """get current item before edit"""
        self.textBeforeEdit=item.text()
        self.flag=True
        return
    def itemChanged(self,item):
        """get item after edit"""
        if self.flag==True:
            self.textAfterEdit=item.text() 
            #save to item stack for later use
            row=self.vehicletable.currentRow()
            col=self.vehicletable.currentColumn()
            command = CommandEdit(self.vehicletable, row,
                                  col,self.textBeforeEdit,self.textAfterEdit,"Rename item '{0}' to '{1}'".format(self.textBeforeEdit, self.textAfterEdit))
            self.undoStack.push(command)
        return
    def addrow(self):
        """add new row"""
        rowselected=self.vehicletable.rowCount()
        self.vehicletable.insertRow(rowselected)
        self.vehicletable.blockSignals(True)
        for i in range(self.vehicletable.columnCount()):
            self.vehicletable.setItem(rowselected,i,QTableWidgetItem(""))
        self.vehicletable.item(rowselected,0).setText("vehicle "+str(rowselected+1))
        self.vehicletable.item(rowselected,0).setFlags(Qt.ItemIsEnabled)
        self.vehicletable.item(rowselected,2).setFlags(Qt.ItemIsEnabled)
        self.vehicletable.item(rowselected,3).setFlags(Qt.ItemIsEnabled)
        self.vehicletable.blockSignals(False)
    def remove1row(self):
        """remove 1 selected row"""
        rowselected=self.vehicletable.currentRow()
        self.vehicletable.removeRow(rowselected)
        return    
class CommandEdit(QUndoCommand):
    """undo class for routing correction table"""
    def __init__(self, tblwidget, row, col, textBeforeEdit, textAfterEdit,description):
        super(CommandEdit, self).__init__(description)
        self.tblwidget = tblwidget
        self.textBeforeEdit = textBeforeEdit
        self.textAfterEdit = textAfterEdit
        self.row = row
        self.col= col

    def redo(self):
        self.tblwidget.blockSignals(True)
        self.tblwidget.item(self.row,self.col).setText(self.textAfterEdit)
        self.tblwidget.blockSignals(False)
    def undo(self):
        self.tblwidget.blockSignals(True)
        self.tblwidget.item(self.row,self.col).setText(self.textBeforeEdit)
        self.tblwidget.blockSignals(False)
class webview(QWebEngineView):
    """web display class"""
    def __init__(self,DC,route):
        super(webview,self).__init__()
        self.__DC="'"+DC+"'"
        self.__route=route
        self.__html='''
        <!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Waypoints in Directions</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
        width: 100%;
        height: 100%;
      }
      #directions-panel {
        position: absolute;
        z-index: 5;
        right: 0;
        //margin-top: 10px;
        background-color: #FFEE77;
        padding: 10px;
        overflow: scroll;
        height: 174px;
        width: 150px;
      }
    </style>
  </head>
  <body>
    <div id="directions-panel"></div>
	<div id="map"></div>
    <script>
      function initMap() {
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11,
          center: {lat: 10.8, lng: 106.7}
        });
        directionsDisplay.setMap(map);
          calculateAndDisplayRoute(directionsService, directionsDisplay);
      }

      function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        var wayptslist = '''+str(self.__route)+''';
        var waypts=[];
        for (var i = 0; i < wayptslist.length; i++) {
            waypts.push({
              location: wayptslist[i],
              stopover: true
            });
        }

        directionsService.route({
          origin: '''+self.__DC+''',
          destination: '''+self.__DC+''',
          waypoints: waypts,
          optimizeWaypoints: false,
          travelMode: 'DRIVING'
        }, function(response, status) {
          if (status === 'OK') {
            directionsDisplay.setDirections(response);
            var route = response.routes[0];
            var summaryPanel = document.getElementById('directions-panel');
            summaryPanel.innerHTML = '';
            // For each route, display summary information.
            for (var i = 0; i < route.legs.length; i++) {
              var routeSegment = i + 1;
              summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
                  '</b><br>';
              summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
              summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
              summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
            }
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDV8WkL5FcxNXI7AGp83YnI6rLuaKuO7r0&callback=initMap">
    </script>
  </body>
</html>
        '''
        #self.setUrl(QUrl(url))
        self.setHtml(self.__html)       
    def changeurl(self,DC,route):
        self.__DC="'"+DC+"'"
        self.__route=route
        self.__html='''
        <!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Waypoints in Directions</title>
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
        width: 100%;
        height: 100%;
      }
      #directions-panel {
        position: absolute;
        z-index: 5;
        right: 0;
        //margin-top: 10px;
        background-color: #FFEE77;
        padding: 10px;
        overflow: scroll;
        height: 174px;
        width: 150px;
      }
    </style>
  </head>
  <body>
    <div id="directions-panel"></div>
	<div id="map"></div>
    <script>
      function initMap() {
        var directionsService = new google.maps.DirectionsService;
        var directionsDisplay = new google.maps.DirectionsRenderer;
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 11,
          center: {lat: 10.8, lng: 106.7}
        });
        directionsDisplay.setMap(map);
          calculateAndDisplayRoute(directionsService, directionsDisplay);
      }

      function calculateAndDisplayRoute(directionsService, directionsDisplay) {
        var wayptslist = '''+str(self.__route)+''';
        var waypts=[];
        for (var i = 0; i < wayptslist.length; i++) {
            waypts.push({
              location: wayptslist[i],
              stopover: true
            });
        }

        directionsService.route({
          origin: '''+self.__DC+''',
          destination: '''+self.__DC+''',
          waypoints: waypts,
          optimizeWaypoints: false,
          travelMode: 'DRIVING'
        }, function(response, status) {
          if (status === 'OK') {
            directionsDisplay.setDirections(response);
            var route = response.routes[0];
            var summaryPanel = document.getElementById('directions-panel');
            summaryPanel.innerHTML = '';
            // For each route, display summary information.
            for (var i = 0; i < route.legs.length; i++) {
              var routeSegment = i + 1;
              summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
                  '</b><br>';
              summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
              summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
              summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
            }
          } else {
            window.alert('Directions request failed due to ' + status);
          }
        });
      }
    </script>
    <script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDV8WkL5FcxNXI7AGp83YnI6rLuaKuO7r0&callback=initMap">
    </script>
  </body>
</html>
        '''
        self.setHtml(self.__html)
class webdispwidget(QWidget):
    """web display widget class"""
    def __init__(self):
        super(webdispwidget,self).__init__()
        #add combobox
        self.VehicleCbox=QComboBox()
        self.DCCbox=QComboBox()
        self.mainLayout=QVBoxLayout()
        self.layout=QHBoxLayout()#create horizontal layout  
        self.ComboLayout=QHBoxLayout()
        self.ComboLayout.addWidget(self.DCCbox)  
        self.ComboLayout.addWidget(self.VehicleCbox)               
        self.setLayout(self.mainLayout)
    def addwebframe(self,DC,route):
        self.frame1=webview(DC,route)
        self.layout.addWidget(self.frame1)
        return
    def addcorrectedframe(self,DC,route):
        self.frame2=webview(DC,route)
        self.layout.addWidget(self.frame2)
        return
    def addCombobox(self,DCNumber,vNumber):
        for DCIndex in range(DCNumber):
            self.DCCbox.addItem("DC {0} ".format(DCIndex))
        for vIndex in range(vNumber):
            self.VehicleCbox.addItem("Vehicle {0} ".format(vIndex))
        self.mainLayout.addLayout(self.ComboLayout)
        self.mainLayout.addLayout(self.layout)
        return
    def getFrameNumber(self):
        return self.layout.count()
class MyProcess():
    def __init__(self,customerlist,VehicleList,distance,DCList,VRank,DRank,Psize,maxIter,CThold):
        self.customerlist=customerlist
        self.VehicleList=VehicleList
        self.distance=distance
        self.DCList=DCList
        self.VRank=VRank
        self.DRank=DRank
        self.Psize=Psize
        self.maxIter=maxIter
        self.CThold=CThold
        return
    def start(self):
        Solutions=[]
        with Pool(processes=4) as pool:
            results=[pool.apply_async(self.Calculate,(1,)) for i in range(4)]
            for res in results:
                Solutions.append(res.get())
        print(Solutions)        
        return self.getBestSolution(Solutions)
    def Calculate(self,a):
        GA=model_GA(self.customerlist,self.VehicleList,self.distance,self.DCList,self.VRank,self.DRank)
        LocGroup=GA.initGroup()
        GA.initpopulation(self.Psize,LocGroup)
        GA.mainloop(self.maxIter,self.CThold)
        return GA.getBestSolution()
    def getBestSolution(self,Solutions):
        min=Solutions[0]
        for res in Solutions:
            print(res.getTotalCost())
            if(res.getTotalCost()<min.getTotalCost()):
                min=res
        print("min={}".format(min.getTotalCost()))
        return copy.deepcopy(min)
class App(QMainWindow):
    
    def __init__(self):
        super(App,self).__init__()                
        self.initUI()
        self.show()
        #self.dialog_open()
        return
 
    def initUI(self):
        """ init main window"""
        title = 'Help me find a good title'
        left = 25 #left margin
        top = 50 #top margin
        width = 1280
        height = 720
        self.setWindowTitle(title)
        self.setGeometry(left, top, width, height)
        #create menu
        mainMenu = self.menuBar()
        #create file menu
        fileMenu = mainMenu.addMenu('File')
        opendatbutton = QAction( 'open data', self)#add open data button
        opendatbutton.setShortcut('Ctrl+O')
        opendatbutton.setStatusTip('open files containing data')
        opendatbutton.triggered.connect(self.fnamedialog)
        fileMenu.addAction(opendatbutton)

        opendatabasebtn=QAction('Import from database',self)
        opendatabasebtn.setShortcut('Ctrl+D')
        opendatabasebtn.setStatusTip('Import data from database')
        opendatabasebtn.triggered.connect(self.Opendtbdialog)
        fileMenu.addAction(opendatabasebtn)

        exitButton = QAction( 'Exit', self)#add exit button
        exitButton.setShortcut('Alt+F4')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        #create view menu
        viewMenu = mainMenu.addMenu('View')

        DatFormDockbutton = QAction( 'Data and Form', self)
        DatFormDockbutton.setStatusTip('Show / hide data and form dock')
        DatFormDockbutton.triggered.connect(self.ShowDataDock)
        viewMenu.addAction(DatFormDockbutton)

        CorrDockbutton = QAction( 'Correction dock', self)
        CorrDockbutton.setStatusTip('Show / hide Correction dock')
        CorrDockbutton.triggered.connect(self.ShowCorrDock)
        viewMenu.addAction(CorrDockbutton)
        #create tools menu        
        toolsMenu = mainMenu.addMenu('Tools')
        
        #create help menu
        helpMenu = mainMenu.addMenu('Help')

        #set main layout
        layout=QHBoxLayout()
        #create table dock
        self.leftwidget=leftwidget()
        #create calculate button for DC form widget
        self.calcbutton=QPushButton("calculate",self)
        self.calcbutton.setToolTip("calculate based on data and input algoritm")
        self.calcbutton.clicked.connect(self.calculate)
        self.calcbutton.setEnabled(False)
        self.leftwidget.formwidget.layout.addWidget(self.calcbutton)
        #create data dock
        self.leftdock=QDockWidget("Data", self)
        self.leftdock.setFloating(False)
        self.leftdock.setWidget(self.leftwidget)
        self.setCorner(Qt.BottomLeftCorner,Qt.LeftDockWidgetArea)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftdock)
        #create web view
        self.webdisp=webdispwidget()
        self.setCentralWidget(self.webdisp)
        #create correction dock
        self.corrwidget=rightconfigwidget()
        self.rightcorrdock=QDockWidget("Route", self)
        self.rightcorrdock.setFloating(False)
        self.rightcorrdock.setWidget(self.corrwidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.rightcorrdock)        
        self.corrwidget.applybtn.triggered.connect(self.apply)
        self.setLayout(layout)
    @pyqtSlot()
    def ShowDataDock(self):
        if(self.leftdock.isVisible()==False):
            self.leftdock.show()
        else:
            self.leftdock.hide()
        return
    @pyqtSlot()
    def ShowCorrDock(self):
        if(self.rightcorrdock.isVisible()==False):
            self.rightcorrdock.show()
        else:
            self.rightcorrdock.hide()
        return
    @pyqtSlot()
    def Opendtbdialog(self):
        dtbdialog=DTBDialog()
        if(dtbdialog.exec_()):
            print("accept")
            print(dtbdialog.IP.text())
            print(dtbdialog.Name.text())
            print(dtbdialog.Password.text())
            print(dtbdialog.Database.text())
            #connect to database
            conn=MySQLdb.connect(host=dtbdialog.IP.text(),user=dtbdialog.Name.text(),passwd=dtbdialog.Password.text(),db=dtbdialog.Database.text())
            #unsafe query execution
            conn.close()
     
        else:
            print("reject")  
    @pyqtSlot()
    def fnamedialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"open data file", 
                                                  "","All Files (*);;csv files (*.csv)", options=options)
        if fileName:
            #using pandas to load data frame
            self.customerlist=[]
            self.origins=[]
            list=pd.read_csv(fileName,encoding='utf-8-sig')
            header=list.columns.tolist()#create header list
            row=list.shape[0]
            col=list.shape[1]
            self.setdatatable(row=row,column=col,data=list,header=header)
            for i in range(len(list.index)):
                #if no quantity and handling time columns
                if(len(header)==4):
                    self.customerlist.append(customer(id=i,name=list[header[0]][i],volume=list[header[1]][i],weight=list[header[2]][i],
                                                  quantity=1,address=list[header[3]][i],handlingTime=0))
                #if no handling time column
                elif(len(header)==5):                
                    self.customerlist.append(customer(id=i,name=list[header[0]][i],volume=list[header[1]][i],weight=list[header[2]][i],
                                                  quantity=list[header[3]][i],address=list[header[4]][i],handlingTime=0))
                else:
                    self.customerlist.append(customer(id=i,name=list[header[0]][i],volume=list[header[1]][i],weight=list[header[2]][i],
                                                  quantity=list[header[3]][i],address=list[header[4]][i],handlingTime=list[header[5]][i]))
                self.origins.append(self.customerlist[i].getLocation()) #add customer locations to origin list
        #set buttons enabled
        self.leftwidget.addDCbtn.setEnabled(True)
        self.leftwidget.rmEmptyDCbtn.setEnabled(True)
        self.calcbutton.setEnabled(True)
        return
    def setdatatable(self,row,column,data,header):
        """set customer orders into table widget"""
        print(row)
        self.leftwidget.datatable.setRowCount(row)
        self.leftwidget.datatable.setColumnCount(column)
        for i in range(row):
            for j in range(column):
                item=QTableWidgetItem(str(data.iat[i,j]))
                item.setFlags(Qt.ItemIsEnabled)
                self.leftwidget.datatable.setItem(i,j, item)
        self.leftwidget.datatable.setHorizontalHeaderLabels(header)        
        #set hide button enabled
        self.leftwidget.hidebtn.setEnabled(True)
        return
    @pyqtSlot()
    def calculate(self):
        self.DCList=[]
        self.VehicleList=[]
        #get DC list
        for i in range(len(self.leftwidget.DClist)):
            address=self.leftwidget.DClist[i].text()
            if(address):                
                self.DCList.append(DistributionCenter(address,i+len(self.customerlist)))
                self.origins.append(self.DCList[i].getCoord()) #add DC to origin list
            else:
                print("Error: DC is null")
                return 1
        #get distance matrix
        distance=loc.dist_matrix(self.origins,self.origins)
        distance.get_approxdistance()
        #check Vehicle list
        for i in range(self.leftwidget.VTable.rowCount()):
            self.VehicleList.append([])
            #get vehicle name
            if(self.leftwidget.VTable.item(i,0).text()):
                VehicleName=self.leftwidget.VTable.item(i,0).text()
                self.VehicleList[i].append(VehicleName)
            else:
                print("Error: Vehicle Name is null")
                return 1
            #get and convert vehicle size, weight and quantity parameters to integer
            try:
                VehicleSize=float(self.leftwidget.VTable.item(i,1).text())
                VehicleWeight=float(self.leftwidget.VTable.item(i,2).text())
                VehicleQuantity=int(self.leftwidget.VTable.item(i,3).text())
                if(VehicleSize>0)and(VehicleWeight>0)and(VehicleQuantity>0):
                    self.VehicleList[i].append(VehicleSize)
                    self.VehicleList[i].append(VehicleWeight)
                    self.VehicleList[i].append(VehicleQuantity)
                else:
                    print("Size, Weight and quantity must be positive integers!")
                    return 1
            except:
                print("error when converting. Size and Weight must be positive numbers, quantity must be positive integers!")
                return 1
        #parameters for algorithm
        AlgoIndex=self.leftwidget.algorithm.currentIndex()
        maxIter=int(self.leftwidget.AlgorithmParamTbl.item(0,1).text())
        VRank=float(self.leftwidget.AlgorithmParamTbl.item(2,1).text())
        DRank=float(self.leftwidget.AlgorithmParamTbl.item(3,1).text())
        Psize=int(self.leftwidget.AlgorithmParamTbl.item(1,1).text())
        CThold=float(self.leftwidget.AlgorithmParamTbl.item(4,1).text())
        #calculation module

        worker=MyProcess(self.customerlist,self.VehicleList,distance,self.DCList,VRank,DRank,Psize,maxIter,CThold)
        self.BestSolution=worker.start()
        self.corrBestSolution=copy.deepcopy(self.BestSolution)
        #create list of DC-Vehicle dictionary
        self.result()
        return
    def result(self):
        #get vehicle number
        number=0
        for DCIndex in range(len(self.BestSolution.DC)):
            number+=self.BestSolution.DC[DCIndex].GetNumberVehicles()
        #get max route number
        maxroutenumber=20
        self.CreateRoutes(number,maxroutenumber)
        #create google map display
        DC,route,corrRoute=self.createRouteList(0,0)
        if (self.webdisp.getFrameNumber()<1):
            #Add Combobox 
            self.webdisp.addCombobox(self.BestSolution.getDCNumber(),self.BestSolution.DC[0].GetNumberVehicles())               
            self.webdisp.DCCbox.currentIndexChanged.connect(self.onDCIndexChanged)
            self.webdisp.VehicleCbox.currentIndexChanged.connect(self.onVIndexChanged)
            self.webdisp.addwebframe(DC,route)
            self.webdisp.addcorrectedframe(DC,corrRoute)
        else:
            self.webdisp.frame1.changeurl(DC,route)
            self.webdisp.frame2.changeurl(DC,corrRoute)
        return
    def CreateRoutes(self,number,maxroutenumber):
        """create routing table based on the calculation."""
        self.corrwidget.vehicletable.setRowCount(number)
        self.corrwidget.vehicletable.setColumnCount(maxroutenumber+2)
        self.corrwidget.vehicletable.setHorizontalHeaderLabels(['Vehicle','DC','Volume','Weight'])
        #fill table with ""
        self.corrwidget.vehicletable.blockSignals(True)
        for row in range(self.corrwidget.vehicletable.rowCount()):
            for col in range(self.corrwidget.vehicletable.columnCount()):
                item=QTableWidgetItem("")
                self.corrwidget.vehicletable.setItem(row,col, item)
        #set Solution to vehicle table
        totalCustomer=0
        i=0  
        for DCIndex in range(len(self.DCList)):
            for vIndex in range(self.BestSolution.DC[DCIndex].GetNumberVehicles()):
                j=4
                vItem=QTableWidgetItem("vehicle "+str(i+1))
                self.corrwidget.vehicletable.setItem(i,0, vItem) #set vehicle and vehicle number item
                self.corrwidget.vehicletable.item(i,0).setFlags(Qt.ItemIsEnabled)
                DCItem=QTableWidgetItem(str(DCIndex+1))
                self.corrwidget.vehicletable.setItem(i,1, DCItem)
                volume=0
                weight=0                
                for cIndex in range(self.BestSolution.DC[DCIndex].VehicleList[vIndex].getNumberofRoutes()):
                    routeitem=QTableWidgetItem(str(self.BestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getID()))
                    #calc volume
                    volume+=self.BestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getVolume()*self.BestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getQuantity()
                    weight+=self.BestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getWeight()*self.BestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getQuantity()                    
                    self.corrwidget.vehicletable.setItem(i,j, routeitem)
                    j+=1
                totalCustomer+=self.BestSolution.DC[DCIndex].VehicleList[vIndex].getNumberofRoutes()
                volItem=QTableWidgetItem(str(volume))
                weightItem=QTableWidgetItem(str(weight))
                self.corrwidget.vehicletable.setItem(i,2, volItem)
                self.corrwidget.vehicletable.item(i,2).setFlags(Qt.ItemIsEnabled)
                self.corrwidget.vehicletable.setItem(i,3, weightItem)
                self.corrwidget.vehicletable.item(i,3).setFlags(Qt.ItemIsEnabled)
                i+=1
        print("Total Customer: {0}".format(totalCustomer))
        self.corrwidget.vehicletable.blockSignals(False)
        #set buttons enabled    
        self.corrwidget.addrowbtn.setEnabled(True)
        self.corrwidget.rmrowbtn.setEnabled(True)
        self.corrwidget.undobtn.setEnabled(True)
        self.corrwidget.redobtn.setEnabled(True)
        self.corrwidget.applybtn.setEnabled(True)
        #set column uneditable 
        return
    def apply(self):
        CountList=[[] for i in range(len(self.customerlist))]        
        Constraint=True
        self.corrwidget.vehicletable.blockSignals(True)                                
        #check for input
        if(self.InputValidation(CountList)==False):
            self.corrwidget.vehicletable.blockSignals(False)
            return        
        #check for redundant
        if(self.RedundantValidation(CountList)==True):
            self.corrwidget.vehicletable.blockSignals(False)
            return
        self.corrBestSolution=Solution(copy.deepcopy(self.DCList))
        #constraint validation
        for row in range(self.corrwidget.vehicletable.rowCount()):
            DCIndex=int(self.corrwidget.vehicletable.item(row,1).text())-1
            self.corrBestSolution.DC[DCIndex].addVehicle(
                self.VehicleList[0][0],self.VehicleList[0][1],self.VehicleList[0][2],self.VehicleList[0][3])
            weight=0
            volume=0
            for col in range(4,self.corrwidget.vehicletable.columnCount()):
                Text=self.corrwidget.vehicletable.item(row,col).text()                
                if(Text!=""):
                    vnumber=self.corrBestSolution.DC[DCIndex].GetNumberVehicles()-1
                    self.corrBestSolution.DC[DCIndex].appendRoute(vnumber,copy.deepcopy(self.customerlist[int(Text)]))
                    weight+=self.corrBestSolution.DC[DCIndex].VehicleList[vnumber].routing[col-4].getWeight()*self.corrBestSolution.DC[DCIndex].VehicleList[vnumber].routing[col-4].getQuantity()
                    volume+=self.corrBestSolution.DC[DCIndex].VehicleList[vnumber].routing[col-4].getVolume()*self.corrBestSolution.DC[DCIndex].VehicleList[vnumber].routing[col-4].getQuantity()
            self.corrwidget.vehicletable.item(row,2).setText(str(volume))
            self.corrwidget.vehicletable.item(row,3).setText(str(weight))
            if(weight>self.VehicleList[0][2]):
                Constraint=False
                self.corrwidget.vehicletable.item(row,3).setBackground(Qt.darkYellow)
            if(volume>0.9*self.VehicleList[0][1]):
                Constraint=False
                self.corrwidget.vehicletable.item(row,2).setBackground(Qt.darkYellow)
        #check for constraints
        if(Constraint==False):
            self.corrwidget.vehicletable.blockSignals(False)
            return
        #display
        for DCIndex in range(self.corrBestSolution.getDCNumber()):
            print("\nDistribution Center {0}".format(DCIndex))
            for vIndex in range(self.corrBestSolution.DC[DCIndex].GetNumberVehicles()):
                for cIndex in range(self.corrBestSolution.DC[DCIndex].VehicleList[vIndex].getNumberofRoutes()):
                    print("vehicle {0}: {1}".format(vIndex,self.corrBestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getID()))
        #set web frame
        DC,Route,CorrRoute=self.createRouteList(0,0)
        self.webdisp.frame1.changeurl(DC,Route)
        self.webdisp.frame2.changeurl(DC,CorrRoute)
        self.corrwidget.vehicletable.blockSignals(False)

        return
    #validating function
    def InputValidation(self,CountList):
        ValidInput=True
        for row in range(self.corrwidget.vehicletable.rowCount()):
            self.corrwidget.vehicletable.item(row,1).setBackground(Qt.white)
            self.corrwidget.vehicletable.item(row,2).setBackground(Qt.white)
            self.corrwidget.vehicletable.item(row,3).setBackground(Qt.white)
            #check DC column
            DC=self.corrwidget.vehicletable.item(row,1).text()
            try:
                if(int(DC)-1<0)or(int(DC)-1>=len(self.DCList)):
                    self.corrwidget.vehicletable.item(row,1).setBackground(Qt.red)
                    ValidInput=False
            except: #catch invalid inputs
                self.corrwidget.vehicletable.item(row,1).setBackground(Qt.red)
                ValidInput=False
            for col in range(4,self.corrwidget.vehicletable.columnCount()):
                self.corrwidget.vehicletable.item(row,col).setBackground(Qt.white)
                Text=self.corrwidget.vehicletable.item(row,col).text()
                if(Text!=""):
                    try:
                        if(int(Text)<0)or(int(Text)>=len(self.customerlist)):
                            self.corrwidget.vehicletable.item(row,col).setBackground(Qt.red)
                            ValidInput=False
                        else:
                            CountList[int(Text)].append({'row': row,'col':col,'value': Text})                            
                    except:
                        self.corrwidget.vehicletable.item(row,col).setBackground(Qt.red)
                        print("INVALID INPUT!!!")
                        ValidInput=False
        return ValidInput
    def RedundantValidation(self,CountList):
        Redundant=False
        for i in range(len(CountList)):
            if(len(CountList[i])>1):
                for j in range(len(CountList[i])):
                    self.corrwidget.vehicletable.item(CountList[i][j]['row'],CountList[i][j]['col']).setBackground(Qt.yellow)
                Redundant=True
        return Redundant
    #signal function
    def onDCIndexChanged(self,index):
        self.webdisp.VehicleCbox.blockSignals(True)
        self.webdisp.VehicleCbox.clear()        
        for vIndex in range(self.corrBestSolution.DC[index].GetNumberVehicles()):
            self.webdisp.VehicleCbox.addItem("Vehicle {0}".format(vIndex))
        DC,Route,CorrRoute=self.createRouteList(index,0)
        self.webdisp.frame1.changeurl(DC,Route)
        self.webdisp.frame2.changeurl(DC,CorrRoute)
        self.webdisp.VehicleCbox.blockSignals(False)
        return
    def onVIndexChanged(self,index):
        DCIndex=self.webdisp.DCCbox.currentIndex()
        DC,Route,CorrRoute=self.createRouteList(DCIndex,index)
        self.webdisp.frame1.changeurl(DC,Route)
        self.webdisp.frame2.changeurl(DC,CorrRoute)
        return
    #create function
    def createRouteList(self,DCIndex,vIndex):
        RList=[]
        CorrRList=[]
        DC=self.BestSolution.DC[DCIndex].getAddress()
        try:
            for cIndex in range(self.BestSolution.DC[DCIndex].VehicleList[vIndex].getNumberofRoutes()):
                RList.append(self.BestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getAddress())
        except:
            print("")
        for cIndex in range(self.corrBestSolution.DC[DCIndex].VehicleList[vIndex].getNumberofRoutes()):
            CorrRList.append(self.corrBestSolution.DC[DCIndex].VehicleList[vIndex].routing[cIndex].getAddress())      
        return DC,RList,CorrRList
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())