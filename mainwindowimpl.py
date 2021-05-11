# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QButtonGroup, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame, QHeaderView, QToolButton, QStyle
from PySide2.QtCore import QFile, QDir ,QIODevice, Qt, QStandardPaths, QSortFilterProxyModel, QObject, Signal, Slot, QRegExp
from ui_mainwindow import Ui_MainWindow
from createtablemodel	import TableModelC
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from usetreemodel import TreeModelU
from filterModel import FilterModel
from usefiltermodel import FilterModelU
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


        aTree={}
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
        self.usefilterModel = FilterModelU(self)
        self.usefilterModel.setSourceModel(self.usetablemodel)
        self.ui.useTemplateTableView.setModel(self.usefilterModel)
        self.ui.useTemplateTableView.setColumnWidth(0,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(1,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(2,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(3,self.width()*.25)

        self.uselistmodel = ListModel(self, self.usetablemodel,"")
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.addAppendButton()
        self.ui.TabWidget.currentChanged.connect(self.movethedamnbutton)
        self.appendSourceFilesButton.clicked.connect(self.addFile)
        self.ui.appendCreateTableRowButton.clicked.connect(self.addCreateTableRow)
        self.ui.appendUseTableRowButton.clicked.connect(self.addUseTableRow)


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


        icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)
        self.ui.appendUseTableRowButton.setIcon(icon)
        self.ui.appendUseTableRowButton.resize(24,24)

        self.ui.appendCreateTableRowButton.setIcon(icon)
        self.ui.appendCreateTableRowButton.resize(24,24)


    def addUseTableRow(self):
        self.usetablemodel.addEmptyRow()


    def extractFile(self):
        if self.fileType:
            linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
            QStandardPaths.HomeLocation),self.tr("Files (*"+self.fileType+")"))[0]
        if linetext != "":
            self.setWindowTitle(linetext)
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

            if self.templatedata:
                self.usefilterModel = FilterModelU(self)
                self.usefilterModel.setSourceModel(self.usetablemodel)
                self.unusedTreeModel = TreeModelU(["Available File Metadata"],headerDict,self.usetablemodel)
                self.ui.useTemplateTableView.setModel(self.usefilterModel)



    def help(self):
        print("Help")

    def movethedamnbutton(self):
        self.appendSourceFilesButton.move(self.ui.useTemplateListView.width() - self.appendSourceFilesButton.width(),self.ui.useTemplateListView.height() - self.appendSourceFilesButton.height())




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
            self.usetablemodel.metadataList=[]
            self.currentTemplate= linetext.split("/")[-1]
            self.ui.displayedFileLabel.setText(linetext.split("/")[-1])
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            self.ui.otherDataFileLineEdit.setText("")
            infile = open(linetext,"r")
            data= infile.readline()
            fileType = infile.readline()
            fileType= json.loads(fileType)
            self.fileType = fileType[0][-4:]

            self.toggleButtons()
            self.templatedata= json.loads(data)
            self.usetablemodel.addTemplateList(self.templatedata)
            self.usefilterModel.setFilterRegExp(QRegExp())
            infile.close()

        return True

    def showEvent(self, event):
        super().showEvent(event)
        self.movethedamnbutton()

    def toggleButtons(self):
        self.ui.otherDataFileSelect.setEnabled(self.fileType!="")



