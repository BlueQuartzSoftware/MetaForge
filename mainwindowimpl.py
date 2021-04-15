# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QButtonGroup, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame, QHeaderView
from PySide2.QtCore import QFile, QIODevice, Qt, QStandardPaths, QSortFilterProxyModel, QObject, Signal, Slot
from ui_mainwindow import Ui_MainWindow
from createtablemodel	import TableModelC
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from filterModel import FilterModel
from trashdelegate import TrashDelegate

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

#        self.ui.actionUseTemplate.toggle.connect(


        aTree={"Somefile.xml":
            {"States":
                {"SEMEColumnState":
                    {"Date":"Tue Aug 22 03:09:35 2017", "TimeStamp":1503385775.990084,"ScanMode":"Resolution"}}}}
        self.createtablemodel = TableModelC(aTree,self)
        self.filterModel = FilterModel(self)
        self.filterModel.setSourceModel(self.createtablemodel)
        self.ui.metadataTableView.setModel(self.filterModel)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(2,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(3,QHeaderView.ResizeToContents)
        self.trashDelegate = TrashDelegate()
        self.ui.metadataTableView.setItemDelegateForColumn(8, self.trashDelegate)
        self.ui.metadataTableView.setColumnWidth(8,self.width()*.05)


        self.treeModel = TreeModel(["Available File Metadata"],aTree,self.createtablemodel)
        self.ui.metadataTreeView.setModel(self.treeModel)
        self.treeModel.checkChanged.connect(self.filterModel.checkList)
        self.trashDelegate.pressed.connect(self.treeModel.changeLeafCheck)

        self.usetablemodel = TableModelU(self.filterModel,self)
        self.ui.useTemplateTableView.setModel(self.usetablemodel)
        self.ui.useTemplateTableView.setColumnWidth(0,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(1,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(2,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(3,self.width()*.25)

        self.uselistmodel = ListModel(self)
        self.ui.useTemplateListView.setModel(self.uselistmodel)
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
            self.setWindowTitle(linetext)
            self.ui.dataFileLineEdit.setText(linetext)
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

            self.createtablemodel = TableModelC(headerDict,self)
            self.filterModel.setSourceModel(self.createtablemodel)
            self.ui.metadataTableView.setModel(self.filterModel)
            self.treeModel = TreeModel(["Available File Metadata"],headerDict,self.usetablemodel)
            self.ui.metadataTreeView.setModel(self.treeModel)
            self.treeModel.checkChanged.connect(self.filterModel.checkList)
            self.trashDelegate.pressed.connect(self.treeModel.changeLeafCheck)

        return True


