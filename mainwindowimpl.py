# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QButtonGroup, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame, QHeaderView, QToolButton, QStyle
from PySide2.QtCore import QFile, QDir ,QIODevice, Qt, QStandardPaths, QSortFilterProxyModel, QObject, Signal, Slot
from ui_mainwindow import Ui_MainWindow
from createtablemodel	import TableModelC
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from filterModel import FilterModel
from trashdelegate import TrashDelegate

import ctf
import ang
import json

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
        self.ui.actionSave_Template.triggered.connect(self.saveTemplate)
        self.ui.dataFileSelect.clicked.connect(self.selectFile)
        self.ui.hyperthoughtTemplateSelect.clicked.connect(self.selectTemplate)
        self.ui.saveTemplateButton.clicked.connect(self.saveTemplate)
        self.ui.otherDataFileSelect.clicked.connect(self.extractFile)
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

        self.usetablemodel = TableModelU(self,[])
        self.ui.useTemplateTableView.setModel(self.usetablemodel)
        self.ui.useTemplateTableView.setColumnWidth(0,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(1,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(2,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(3,self.width()*.25)

        self.uselistmodel = ListModel(self, self.usetablemodel,"")
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.addAppendButton()
        self.ui.TabWidget.currentChanged.connect(self.movethedamnbutton)
        self.appendSourceFilesButton.clicked.connect(self.addFile)
        self.appendCreateTableRowButton.clicked.connect(self.addCreateTableRow)
        self.appendUseTableRowButton.clicked.connect(self.addUseTableRow)


    def addCreateTableRow(self):
        self.createtablemodel.addEmptyRow()


    def addFile(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ctf *.xml *.ang)"))[0]
        if linetext != "":
            self.setWindowTitle(linetext)
            self.uselistmodel.addRow(linetext)


    def addAppendButton(self):

        self.appendSourceFilesButton= QToolButton(self.ui.useTemplateListView)
        icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)
        self.appendSourceFilesButton.setIcon(icon)
        self.appendSourceFilesButton.resize(32,32)

        self.appendUseTableRowButton = QToolButton(self.ui.UseTemplateTab)
        icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)
        self.appendUseTableRowButton.setIcon(icon)
        self.appendUseTableRowButton.resize(24,24)

        self.appendCreateTableRowButton = QToolButton(self.ui.CreateTemplateTab)
        icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)
        self.appendCreateTableRowButton.setIcon(icon)
        self.appendCreateTableRowButton.resize(24,24)

    def addUseTableRow(self):
        self.usetablemodel.addEmptyRow()


    def extractFile(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ctf *.xml *.ang)"))[0]
        if linetext != "":
            self.setWindowTitle(linetext)
            self.ui.dataFileLineEdit.setText(linetext)
            self.ui.dataTypeText.setText(linetext.split(".")[1].upper())
            self.ui.otherDataFileLineEdit.setText(linetext)
            if self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser") != -1:
                headerDict= {}
                self.ui.fileParserCombo.setCurrentIndex(self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser"))
            if linetext.split(".")[1].upper() == "CTF":
                headerDict =ctf.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "ANG":
                headerDict =ang.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "XML":
                print("XML Parser used")
            self.unusedTreeModel = TreeModel(["Available File Metadata"],headerDict,self.usetablemodel)
                #self.uselistmodel.addRow(linetext)


    def help(self):
        print("Help")

    def movethedamnbutton(self):
        self.appendSourceFilesButton.move(self.ui.useTemplateListView.width() - self.appendSourceFilesButton.width(),self.ui.useTemplateListView.height() - self.appendSourceFilesButton.height())
        self.appendUseTableRowButton.move(self.ui.useTemplateTableView.width() + self.appendUseTableRowButton.width(), self.ui.displayedFileLabel.y() - 2)
        self.appendCreateTableRowButton.move(self.ui.metadataTableView.width() + self.appendCreateTableRowButton.width(), self.ui.label.y() - 2)


    def openRecent(self):
        print("Clicked Open Recent.")

    def openPackage(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ez)"))[0]
        if linetext != "":
            self.currentTemplate= linetext.split("/")[-1]
            self.ui.displayedFileLabel.setText(linetext.split("/")[-1])
            infile = open(linetext,"r")
            data= infile.readline()
            fileList = infile.readline()
            fileList= json.loads(fileList)
            self.usetablemodel = TableModelU(self,json.loads(data))
            self.ui.useTemplateTableView.setModel(self.usetablemodel)
            self.uselistmodel = ListModel(self, self.usetablemodel, fileList)
            self.ui.useTemplateListView.setModel(self.uselistmodel)
            infile.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        print("resizeEvent was called")
        self.movethedamnbutton()


    def savePackage(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "/Packages/",
                                   "Packages (*)")
        if fileName != "":
            myDir= QDir()
            myDir.mkpath(fileName[0])
            for file in self.uselistmodel.metadataList:
                print(QFile.copy( file, fileName[0]+"/"+file.split("/")[-1]))
            with open(fileName[0]+"/"+self.currentTemplate, 'w') as outfile:
                json.dump(self.usetablemodel.metadataList, outfile)
                outfile.write("\n")
                json.dump(self.uselistmodel.metadataList, outfile)
                print(self.currentTemplate)



    def savePackageAs(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "/Packages/",
                                   "Packages (*.ez)")
    def saveTemplate(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "",
                                   "Templates (*.ez)")
        if fileName != "":
            with open(fileName[0]+".ez", 'w') as outfile:
                json.dump(self.filterModel.displayed, outfile)
                outfile.write("\n")
                json.dump(self.filterModel.fileList, outfile)


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
            self.filterModel.displayed=[]
            self.filterModel.setSourceModel(self.createtablemodel)
            self.filterModel.fileList.append(linetext)
            self.ui.metadataTableView.setModel(self.filterModel)
            self.treeModel = TreeModel(["Available File Metadata"],headerDict,self.createtablemodel)
            self.ui.metadataTreeView.setModel(self.treeModel)
            self.treeModel.checkChanged.connect(self.filterModel.checkList)
            self.trashDelegate.pressed.connect(self.treeModel.changeLeafCheck)

        return True

    def selectTemplate(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ez)"))[0]
        if linetext != "":
            self.currentTemplate= linetext.split("/")[-1]
            self.ui.displayedFileLabel.setText(linetext.split("/")[-1])
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            infile = open(linetext,"r")
            data= infile.readline()
            fileList = infile.readline()
            fileList= json.loads(fileList)
            self.usetablemodel = TableModelU(self,json.loads(data))
            self.ui.useTemplateTableView.setModel(self.usetablemodel)
#            self.uselistmodel = ListModel(self, self.usetablemodel, fileList)
            self.ui.useTemplateListView.setModel(self.uselistmodel)
            infile.close()

        return True

    def showEvent(self, event):
        super().showEvent(event)
        self.movethedamnbutton()



