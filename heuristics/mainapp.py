import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *

import pandas as pd
import location as loc
import vehicle
from customer import *
from model import model_GA
class VehicleDialog(QDialog): #may change layout to table if there are multiple weight and size vehicles
    """create declare vehicle dialog"""
    def __init__(self):
        super(VehicleDialog,self).__init__()
        self.createformbox()
        self.setWindowTitle('Specify Vehicle')
        # set flags
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        #create button
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
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
        self.Name=QLineEdit()
        self.Size=QLineEdit()
        self.Weight=QLineEdit()
        self.Quantity=QLineEdit()
        #create form layout
        layout = QFormLayout()
        layout.addRow(QLabel("Vehicle Name:"), self.Name)
        layout.addRow(QLabel("Size:"), self.Size)
        layout.addRow(QLabel("Weight:"), self.Weight)
        layout.addRow(QLabel("Number of Vehicle:"), self.Quantity)
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
        #create form layout
        self.DCLayout=QFormLayout()
        self.DClist=[QLineEdit()]
        self.DCLayout.addRow(QLabel("DC 1"), self.DClist[0])
        self.DCform.setLayout(self.DCLayout)
        #create Vehicle layout
        self.Vform=QGroupBox("Vehicle")
        self.DeclareVehicle()
        VehicleLayout=QVBoxLayout()
        VehicleLayout.addWidget(self.VTable)
        self.Vform.setLayout(VehicleLayout)
        #create algorithm form layout
        self.algoform = QGroupBox("algorithm")
        algolayout=QFormLayout()
        self.algorithm=QComboBox()
            #add item to combobox
        self.algorithm.addItem("Genetic Algorithm")
        self.algorithm.addItem("Other")
        algolayout.addRow(QLabel("algorithm"),self.algorithm)
        self.algoform.setLayout(algolayout)
        self.createformtools()
        #create form tab layout
        self.formwidget.layout=QVBoxLayout()
        self.formwidget.layout.addWidget(self.FormToolbar)
        self.formwidget.layout.addWidget(self.DCform)
        self.formwidget.layout.addWidget(self.Vform)
        self.formwidget.layout.addWidget(self.algoform)        
        self.formwidget.setLayout(self.formwidget.layout)
    def createformtools(self):
        """create DC form toolbar"""
        self.FormToolbar=QToolBar()
        #create buttons
        self.addDCbtn=QAction(QIcon("image/add.bmp"),"Add distribution center")                
        #add action
        self.FormToolbar.addAction(self.addDCbtn)
        #set action
        self.addDCbtn.triggered.connect(self.addDistributionCenter)
    def addDistributionCenter(self):
        """add 1 distribution center"""
        self.DClist.append(QLineEdit())
        self.DCLayout.addRow(QLabel("DC "+str(len(self.DClist))), self.DClist[len(self.DClist)-1])
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
        self.applybtn.triggered.connect(self.apply)
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
        self.textAfterEdit=item.text()
        if self.flag==True:
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
        self.vehicletable.blockSignals(False)
    def remove1row(self):
        """remove 1 selected row"""
        rowselected=self.vehicletable.currentRow()
        self.vehicletable.removeRow(rowselected)
        return    
    def apply(self):
        """apply changes"""

        return   #return updated list
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
    def __init__(self,url):
        super(webview,self).__init__()
        self.setUrl(QUrl(url))       
    def changeurl(self,url):
        self.setUrl(QUrl(url)) 

class webdispwidget(QWidget):
    """web display widget class"""
    def __init__(self):
        super(webdispwidget,self).__init__()
        self.layout=QHBoxLayout()#create horizontal layout
        self.setLayout(self.layout)
    def addwebframe(self,url):
        self.frame1=webview(url)
        self.layout.addWidget(self.frame1)
        return
    def addcorrectedframe(self,url):
        self.frame2=webview(url)
        self.layout.addWidget(self.frame2)
    def getFrameNumber(self):
        return self.layout.count()
class App(QMainWindow):
    
    def __init__(self):
        super(App,self).__init__()                
        self.initUI()
        self.show()
        #self.dialog_open()
        return
 
    def initUI(self):
        """ init main window"""
        title = 'GUI'
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

        exitButton = QAction( 'Exit', self)#add exit button
        exitButton.setShortcut('Alt+F4')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)
        
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

        self.leftdock=QDockWidget("left dock", self)
        self.leftdock.setFloating(False)
        self.leftdock.setWidget(self.leftwidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.leftdock)
        #create web view
        self.webdisp=webdispwidget()
        self.setCentralWidget(self.webdisp)
        #create correction dock
        self.corrwidget=rightconfigwidget()
        self.rightcorrdock=QDockWidget("correction", self)
        self.rightcorrdock.setFloating(False)
        self.rightcorrdock.setWidget(self.corrwidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.rightcorrdock)
        
        self.setLayout(layout)
  
    @pyqtSlot()
    def fnamedialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"open data file", 
                                                  "","All Files (*);;csv files (*.csv)", options=options)
        if fileName:
            print(fileName)
            #using pandas to load data frame
            self.customerlist=[]
            self.origins=[]
            list=pd.read_csv(fileName,encoding='utf-8-sig')
            header=list.columns.tolist()#create header list
            row=list.shape[0]
            col=list.shape[1]
            self.setdatatable(row=row,column=col,data=list,header=header)
            for i in range(len(list.index)):                
                self.customerlist.append(customer(i,list[header[0]][i],list[header[1]][i],list[header[2]][i],
                                                  list[header[3]][i],list[header[4]][i],0))
                self.origins.append(self.customerlist[i].getLocation()) #add customer locations to origin list
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
        self.leftwidget.datatable.setHorizontalHeaderLabels([header[0],header[1],header[2],header[3],header[4]])
        #set hide button enabled
        self.leftwidget.hidebtn.setEnabled(True)
        return
    @pyqtSlot()
    def calculate(self):
        self.DCList=[]
        VehicleList=[]
        #get DC list
        for i in range(len(self.leftwidget.DClist)):
            address=self.leftwidget.DClist[i].text()
            if(address):                
                self.DCList.append(DistributionCenter(address,i+len(self.customerlist)))
                self.origins.append(self.DCList[i].getCoord()) #add DC to origin list
                print(self.DCList[i].getID())
            else:
                print("Error: DC is null")
                return 1
        #get distance matrix
        distance=loc.dist_matrix(self.origins,self.origins)
        distance.get_approxdistance()
        #check Vehicle list
        for i in range(self.leftwidget.VTable.rowCount()):
            VehicleList.append([])
            #get vehicle name
            if(self.leftwidget.VTable.item(i,0).text()):
                VehicleName=self.leftwidget.VTable.item(i,0).text()
                VehicleList[i].append(VehicleName)
            else:
                print("Error: Vehicle Name is null")
                return 1
            #get and convert vehicle size, weight and quantity parameters to integer
            try:
                VehicleSize=float(self.leftwidget.VTable.item(i,1).text())
                VehicleWeight=float(self.leftwidget.VTable.item(i,2).text())
                VehicleQuantity=int(self.leftwidget.VTable.item(i,3).text())
                if(VehicleSize>0)and(VehicleWeight>0)and(VehicleQuantity>0):
                    VehicleList[i].append(VehicleSize)
                    VehicleList[i].append(VehicleWeight)
                    VehicleList[i].append(VehicleQuantity)
                else:
                    print("Size, Weight and quantity must be positive integers!")
                    return 1
            except:
                print("error when converting. Size and Weight must be positive numbers, quantity must be positive integers!")
                return 1
        #calculation module
        GA=model_GA(self.customerlist,VehicleList,distance,self.DCList,0.8,0.2)
        print("")
        LocGroup=GA.initGroup()
        GA.initpopulation(40,LocGroup)
        GA.mainloop(50,0.8)
        self.result()
        return
    def result(self):
        number=3
        maxroutenumber=3
        self.CreateRoutes(number,maxroutenumber)
        #create google map display
        if (self.webdisp.getFrameNumber()<1):
            self.webdisp.addwebframe("https://www.google.com/maps")
        else:
            self.webdisp.frame1.changeurl("https://www.google.com/")
        return
    def CreateRoutes(self,number,maxroutenumber):
        """create routing table based on the calculation."""
        self.corrwidget.vehicletable.setRowCount(number)
        self.corrwidget.vehicletable.setColumnCount(maxroutenumber+1)
        for i in range(number):
            rlist=["loc 1","loc 2","loc 3"]
            item=QTableWidgetItem("vehicle "+str(i+1))
            self.corrwidget.vehicletable.setItem(i,0, item) #set vehicle and vehicle number item
            for j in range(1,len(rlist)+1):
                routeitem=QTableWidgetItem(rlist[j-1])
                self.corrwidget.vehicletable.setItem(i,j, routeitem) #set route list item   
        #set buttons enabled    
        self.corrwidget.addrowbtn.setEnabled(True)
        self.corrwidget.rmrowbtn.setEnabled(True)
        self.corrwidget.undobtn.setEnabled(True)
        self.corrwidget.redobtn.setEnabled(True)
        self.corrwidget.applybtn.setEnabled(True) 
        return
    def apply(self):
        print("applied")
        return
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())