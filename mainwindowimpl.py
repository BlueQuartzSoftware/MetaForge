# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame
from PySide2.QtCore import QFile, QIODevice, Qt, QStandardPaths
from ui_mainwindow import Ui_MainWindow
from tablemodel	import TableModel
from treemodel import TreeModel
import ctf
import ang

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionOpen_Recent.triggered.connect(self.openRecent)
        self.ui.actionOpenPackage.triggered.connect(self.openPackage)
        self.ui.actionSave_Package.triggered.connect(self.savePackage)
        self.ui.actionSave_Package_As.triggered.connect(self.savePackageAs)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.dataFileSelect.clicked.connect(self.selectFile)

        aTree={"Somefile.xml":
            {"States":
                {"SEMEColumnState":
                    {"Date":"Tue Aug 22 03:09:35 2017", "TimeStamp":1503385775.990084,"ScanMode":"Resolution"}}}}

        self.ui.metadataTableView.setModel(TableModel(aTree))
        self.ui.metadataTableView.setColumnWidth(0,self.width()*.05)
        self.ui.metadataTableView.setColumnWidth(1,self.width()*.3)
        self.ui.metadataTableView.setColumnWidth(2,self.width()*.3)
        self.ui.metadataTableView.setColumnWidth(3,self.width()*.3)
        self.ui.metadataTableView.setColumnWidth(4,self.width()*.3)
        self.ui.metadataTableView.setColumnWidth(5,self.width()*.2)
        self.ui.metadataTableView.setColumnWidth(6,self.width()*.05)
        self.ui.metadataTableView.setColumnWidth(7,self.width()*.05)
        self.ui.metadataTableView.setColumnWidth(8,self.width()*.05)

#        frameOption = QStyleOptionFrame()
#        self.ui.metadataTableView.setItemDelegateForColumn(2,frameOption)

        self.treeModel = TreeModel(["Available File Metadata"],aTree)
        self.ui.metadataTreeView.setModel(self.treeModel)



    def help(self):
        print("Help")

    def openRecent(self):
        print("Clicked Open Recent.")

    def openPackage(self):
        print("Clicked Open Package.")

    def savePackage(self):
        print("Save Package")

    def savePackageAs(self):
        print("Save Package As")

    def selectFile(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ctf *.xml *.ang)"))[0]
        if linetext != "":
            self.ui.datafileLineEdit.setText(linetext)
            self.ui.dataTypeText.setText(linetext.split(".")[1].upper())
            if self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser") != -1:
                headerDict= {}
                self.ui.fileParserCombo.setCurrentIndex(self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser"))
            if linetext.split(".")[1].upper() == "CTF":
                headerDict =ctf.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "ANG":
                headerDict =ang.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "XML":
                print("XML Parser used")
            self.treeModel = TreeModel(["Available File Metadata"],headerDict)
            self.ui.metadataTreeView.setModel(self.treeModel)
            self.ui.metadataTableView.setModel(TableModel(headerDict))



        return True


