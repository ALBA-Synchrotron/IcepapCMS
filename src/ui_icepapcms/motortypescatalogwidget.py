import sys
from PyQt4 import Qt, QtCore, QtGui
from xml.dom import minidom,Node


################################################################################
# Motor Types Catalog Widget
# based on http://doc.trolltech.com/4.2/itemviews-basicsortfiltermodel.html
#
################################################################################

CATALOG_PARAMS = ['MOTPHASES','MOTPOLES','MREGMODE','NVOLT','IVOLT','NCURR'
                  ,'CURRGAIN','MREGP','MREGI','MREGD','ANTURN','ANSTEP']
## 080731: jlidon considers that ICURR and BCURR are not needed and ANTURN,ANSTEP are needed

class MotorTypesCatalogWidget(QtGui.QDialog):

    def __init__(self,catalog_file,pageipapdriver,parent=None):

        QtGui.QDialog.__init__(self,parent,QtCore.Qt.Window)

        self.pageipapdriver = pageipapdriver

        self.buildCatalog(catalog_file)

        self.proxyModel = QtGui.QSortFilterProxyModel()
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.createModel())

        self.proxyGroupBox = QtGui.QGroupBox()
        self.proxyGroupBox.setFlat(True)

        self.proxyView = QtGui.QTreeView()
        self.proxyView.setRootIsDecorated(False)
        self.proxyView.setAlternatingRowColors(True)
        self.proxyView.setModel(self.proxyModel)
        self.proxyView.setSortingEnabled(True)
        # AT THE ISG LAB, THIS METHOD IS NOT AVAILABLE...
        #self.proxyView.setWordWrap(True)

        self.filterPatternLineEdit = QtGui.QLineEdit()
        self.filterPatternLabel = QtGui.QLabel("&Filter pattern:")
        self.filterPatternLabel.setBuddy(self.filterPatternLineEdit)
        self.connect(self.filterPatternLineEdit,
                     QtCore.SIGNAL("textChanged(const QString)"),self.filterRegExpChanged)

        
        self.filterColumnComboBox = QtGui.QComboBox()
        # ITEMS HAVE BEEN FILLED AT THE self.buildCatalog CALL
        model = self.proxyModel.sourceModel()
        for column in range(model.columnCount()):
            self.filterColumnComboBox.addItem(model.horizontalHeaderItem(column).text())
        self.filterColumnLabel = QtGui.QLabel("Filter &column:")
        self.filterColumnLabel.setBuddy(self.filterColumnComboBox)
        self.connect(self.filterColumnComboBox,
                     QtCore.SIGNAL("currentIndexChanged(int)"),self.filterColumnChanged)

        self.btnSelectMotor = QtGui.QPushButton("Select")
        self.connect(self.btnSelectMotor,
                     QtCore.SIGNAL('clicked()'),self.applySelection)

        self.chkAutoClose = QtGui.QCheckBox("Auto close")
        self.chkAutoClose.setChecked(True)

        self.proxyLayout = QtGui.QGridLayout()

        self.proxyLayout.addWidget(self.filterColumnLabel, 0, 0)
        self.proxyLayout.addWidget(self.filterColumnComboBox, 0, 1)
        self.proxyLayout.addWidget(self.filterPatternLineEdit, 0, 2)
        self.proxyLayout.addWidget(self.btnSelectMotor,0,3)
        self.proxyLayout.addWidget(self.chkAutoClose,0,4)

        self.proxyLayout.addWidget(self.proxyView, 1, 0, 1, 5)


        self.proxyGroupBox.setLayout(self.proxyLayout)
        
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.proxyGroupBox)
        self.setLayout(self.mainLayout)
        
        self.setWindowTitle("IcepaCMS MotorTypes Catalog")
        self.resize(750, 600)
        
        self.proxyView.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.proxyView.setColumnWidth(0,220)

        self.filterColumnComboBox.setCurrentIndex(0)
        
        self.filterPatternLineEdit.setText("")


    def buildCatalog(self,catalog):
        self.catalog = {}
        doc = minidom.parse(catalog)
        root = doc.documentElement
        for motor_node in root.getElementsByTagName('motor'):
            motor_type = motor_node.attributes.get('motor_type').value
            params = {}
            description = ""
            desc_node = motor_node.getElementsByTagName('description')[0].firstChild
            if desc_node != None:
                description = str(desc_node.data)
            params['description'] = description
        
            for param in CATALOG_PARAMS:
                try:
                    value = motor_node.attributes.get(param).value
                    if param in ['MREGMODE','CURRGAIN']:
                        value = str(value)
                    elif param in ['MOTPHASES','MOTPOLES']:
                        value = int(value)
                    else:
                        value = float(value)
                    params[param] = value
                except:
                    #print "could not retrieve param",param,"from the catalog"
                    pass
            self.catalog[str(motor_type)] = params


    def createModel(self,parent=None):
        model = QtGui.QStandardItemModel(0,2,self)
        model.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.QVariant("Motor type"))
        model.setHeaderData(1, QtCore.Qt.Horizontal, QtCore.QVariant("Description"))
    
        for motor_type in self.catalog.keys():
            self.addMotorType(model,motor_type,self.catalog[motor_type]['description'])
            
        return model

    
    def addMotorType(self,model,motor_type,description):
        model.insertRow(0)
        model.setData(model.index(0, 0), QtCore.QVariant(motor_type))
        model.setData(model.index(0, 1), QtCore.QVariant(description))
        model.item(0,0).setFlags(Qt.Qt.ItemIsSelectable)
        model.item(0,1).setFlags(Qt.Qt.ItemIsSelectable)


    def filterRegExpChanged(self):
        caseSensitivity = QtCore.Qt.CaseInsensitive
        syntax = QtCore.QRegExp.PatternSyntax(QtCore.QRegExp.RegExp)
        regExp = QtCore.QRegExp(self.filterPatternLineEdit.text(),
                                caseSensitivity,syntax)
        self.proxyModel.setFilterRegExp(regExp)
        # In case of just one match, auto-select it
        if self.proxyView.model().rowCount() == 1:
            self.proxyView.selectAll()
        else:
            self.proxyView.selectionModel().clear()
 

    def filterColumnChanged(self):
        self.proxyModel.setFilterKeyColumn(
            self.filterColumnComboBox.currentIndex())


    def applySelection(self):
        indexes = self.proxyView.selectedIndexes()
        if len(indexes) > 0:
            motor_type = str(indexes[0].data().toString())
            params = self.catalog.get(motor_type)
            self.pageipapdriver.setMotorTypeParams(motor_type,params)

            if self.chkAutoClose.isChecked():
                self.close()


    def closeEvent(self, event):
        self.close()
        event.accept()

