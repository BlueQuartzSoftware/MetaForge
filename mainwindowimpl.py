# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QButtonGroup, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame, QHeaderView, QToolButton, QStyle, QProgressDialog, QDialog
from PySide2.QtCore import QFile, QDir ,QIODevice, Qt, QStandardPaths, QSortFilterProxyModel, QObject, Signal, Slot, QRegExp, QThread
from PySide2.QtGui import QCloseEvent
from ui_mainwindow import Ui_MainWindow
from hyperthoughtdialogimpl import HyperthoughtDialogImpl
from createtablemodel	import TableModelC
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from usetreemodel import TreeModelU
from filterModel import FilterModel
from usefiltermodel import FilterModelU
from trashdelegate import TrashDelegate
from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests
from tqdm import tqdm
from uploader import Uploader

import ctf
import ang
import json

class MainWindow(QMainWindow):
    createUpload = Signal(list,htauthcontroller.HTAuthorizationController, str, list)
    def __init__(self):
        super(MainWindow, self).__init__()
        self.hyperthoughtui = HyperthoughtDialogImpl()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.TabWidget.setCurrentWidget(self.ui.CreateTemplateTab)
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
        self.ui.hyperthoughtUploadButton.clicked.connect(self.uploadToHyperthought)
        self.setAcceptDrops(True)

        aTree={}
        self.createtablemodel = TableModelC(aTree,self)
        self.filterModel = FilterModel(self)
        self.filterModel.setSourceModel(self.createtablemodel)
        self.ui.metadataTableView.setModel(self.filterModel)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_SOURCE_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_HTNAME_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_SOURCEVAL_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_HTVALUE_COL_INDEX,QHeaderView.ResizeToContents)
        self.trashDelegate = TrashDelegate()
        self.ui.metadataTableView.setItemDelegateForColumn(9, self.trashDelegate)
        self.ui.metadataTableView.setColumnWidth(9,self.width()*.05)


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
        #self.ui.useTemplateTableView.setColumnWidth(3,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(4,self.width()*.25)

        self.uselistmodel = ListModel(self, self.usetablemodel,[])
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.addAppendButton()
        self.ui.TabWidget.currentChanged.connect(self.movethedamnbutton)
        self.appendSourceFilesButton.clicked.connect(self.addFile)
        self.ui.appendCreateTableRowButton.clicked.connect(self.addCreateTableRow)
        self.ui.appendUseTableRowButton.clicked.connect(self.addUseTableRow)
        self.ui.hyperthoughtLocationButton.clicked.connect(self.hyperthoughtui.exec)
        self.ui.usetableSearchBar.textChanged.connect(self.filterUseTable)
        self.ui.createTemplateListSearchBar.textChanged.connect(self.filterCreateTable)
        self.ui.createTemplateTreeSearchBar.textChanged.connect(self.filterCreateTree)



        self.fileType = ""
        self.accessKey = ""
        self.folderuuid = ""
        self.mThread = QThread()
        self.uploader = Uploader()
        self.uploader.moveToThread(self.mThread)
        self.mThread.start()

        self.createUpload.connect(self.uploader.performUpload)
        self.hyperthoughtui.apiSubmitted.connect(self.acceptKey)
        self.hyperthoughtui.finished.connect(self.getLocation)


    def acceptKey(self, apikey):
        self.accessKey = apikey


    def addCreateTableRow(self):
        self.createtablemodel.addEmptyRow()


    def addFile(self):
        linetexts = QFileDialog.getOpenFileNames(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ctf *.xml *.ang)"))[0]
        for line in linetexts:
            self.uselistmodel.addRow(line)
        self.toggleButtons()


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

    def closeEvent(self, event):
        self.mThread.quit()
        self.mThread.wait(250)


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
                self.usetablemodel.metadataList = []
                self.usefilterModel = FilterModelU(self)
                self.usefilterModel.setSourceModel(self.usetablemodel)
                self.unusedTreeModel = TreeModelU(["Available File Metadata"],headerDict,self.usetablemodel,self.requireds)

                self.usesearchFilterModel = QSortFilterProxyModel(self)
                self.usesearchFilterModel.setSourceModel(self.usefilterModel)
                self.usesearchFilterModel.setFilterKeyColumn(0)
                self.usesearchFilterModel.setDynamicSortFilter(True)
                self.ui.useTemplateTableView.setModel(self.usesearchFilterModel)

    def filterCreateTable(self):
        self.createTableSearchFilterModel.invalidate()
        self.createTableSearchFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.createTableSearchFilterModel.setFilterWildcard("*"+self.ui.createTemplateListSearchBar.text()+"*")

    def filterCreateTree(self):
        self.createTreeSearchFilterModel.invalidate()
        self.createTreeSearchFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.createTreeSearchFilterModel.setFilterWildcard("*"+self.ui.createTemplateTreeSearchBar.text()+"*")

    def filterUseTable(self):
        self.usesearchFilterModel.invalidate()
        self.usesearchFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.usesearchFilterModel.setFilterWildcard("*"+self.ui.usetableSearchBar.text()+"*")

    def getLocation(self):
        location = self.hyperthoughtui.promptui.locationLineEdit.text()
        locationindex = self.hyperthoughtui.stringlistmodel.directoryList.index(location)
        self.ui.hyperthoughtLocationLineEdit.setText(location)
        self.toggleButtons()

        self.folderuuid = self.hyperthoughtui.path + self.hyperthoughtui.stringlistmodel.uuidList[locationindex] + ","

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
            self.templatedata = infile.readline()
            self.templatedata = json.loads(self.templatedata)
            templatesources = json.loads(infile.readline())
            self.fileType = json.loads(infile.readline())
            fileList = infile.readline()
            fileList = json.loads(fileList)
            requireds = infile.readline()
            self.requireds = json.loads(requireds)
            self.usetablemodel = TableModelU(self,[])
            self.usetablemodel.templatelist = self.templatedata
            self.usetablemodel.templatesources = templatesources
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            self.ui.useTemplateTableView.setModel(self.usetablemodel)
            self.uselistmodel = ListModel(self, self.usetablemodel, fileList)
            self.ui.useTemplateListView.setModel(self.uselistmodel)
            self.toggleButtons()
            infile.close()


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.movethedamnbutton()


    def savePackage(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "/Packages/",
                                   "Packages (*.ez)")
        if fileName != "":
            myDir= QDir()
            myDir.mkpath(fileName[0])
            for file in self.uselistmodel.metadataList:
                QFile.copy( file, fileName[0]+"/"+file.split("/")[-1])
            with open(fileName[0]+"/"+self.currentTemplate, 'w') as outfile:
                json.dump(self.usetablemodel.templatelist, outfile)
                outfile.write("\n")
                json.dump(self.usetablemodel.templatesources, outfile)
                outfile.write("\n")
                json.dump(self.fileType, outfile)
                outfile.write("\n")
                json.dump(self.uselistmodel.metadataList, outfile)
                outfile.write("\n")
                json.dump(self.requireds, outfile)

    def savePackageAs(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "/Packages/",
                                   "Packages (*)")
        if fileName != "":
            myDir= QDir()
            myDir.mkpath(fileName[0])
            for file in self.uselistmodel.metadataList:
                QFile.copy( file, fileName[0]+"/"+file.split("/")[-1])
            with open(fileName[0]+"/"+self.currentTemplate, 'w') as outfile:
                json.dump(self.usetablemodel.templatelist, outfile)
                outfile.write("\n")
                json.dump(self.usetablemodel.templatesources, outfile)
                outfile.write("\n")
                son.dump(self.createtablemodel.requiredList, outfile)
                outfile.write("\n")
                json.dump(self.fileType, outfile)
                outfile.write("\n")
                json.dump(self.uselistmodel.metadataList, outfile)
                outfile.write("\n")
                json.dump(self.requireds, outfile)

    def saveTemplate(self):
        dialog = QFileDialog(self, "Save File","", "Templates (*.ez)")
        dialog.setDefaultSuffix(".ez");
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        if  dialog.exec():
            fileName  = dialog.selectedFiles()[0]
        if fileName != "":
            with open(fileName, 'w') as outfile:
                json.dump(self.filterModel.displayed, outfile)
                outfile.write("\n")
                json.dump(self.filterModel.fileList, outfile)
                outfile.write("\n")
                json.dump(self.createtablemodel.requiredList, outfile)

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
            self.createTableSearchFilterModel = QSortFilterProxyModel(self)
            self.createTableSearchFilterModel.setSourceModel(self.filterModel)
            self.createTableSearchFilterModel.setFilterKeyColumn(1)
            self.createTableSearchFilterModel.setDynamicSortFilter(True)
            self.ui.metadataTableView.setModel(self.createTableSearchFilterModel)
            self.treeModel = TreeModel(["Available File Metadata"],headerDict,self.createtablemodel)
            self.createTreeSearchFilterModel = QSortFilterProxyModel(self)
            self.createTreeSearchFilterModel.setSourceModel(self.treeModel)
            self.createTreeSearchFilterModel.setFilterKeyColumn(0)
            self.createTreeSearchFilterModel.setDynamicSortFilter(True)
            self.createTreeSearchFilterModel.setRecursiveFilteringEnabled(True)
            self.ui.metadataTreeView.setModel(self.createTreeSearchFilterModel)
            self.treeModel.checkChanged.connect(self.filterModel.checkList)
            self.trashDelegate.pressed.connect(self.treeModel.changeLeafCheck)

        return True

    def selectTemplate(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ez)"))[0]
        if linetext != "":
            self.usetablemodel.metadataList = []
            self.usefilterModel.displayed = []
            self.currentTemplate= linetext.split("/")[-1]
            self.ui.displayedFileLabel.setText(linetext.split("/")[-1])
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            self.ui.otherDataFileLineEdit.setText("")
            infile = open(linetext,"r")
            data= infile.readline()
            fileType = infile.readline()
            fileType= json.loads(fileType)
            self.fileType = fileType[0][-4:]
            requireds = infile.readline()
            self.requireds = json.loads(requireds)
            self.toggleButtons()
            self.templatedata = json.loads(data)
            self.usetablemodel.addTemplateList(self.templatedata)
            self.usefilterModel.setFilterRegExp(QRegExp())
            infile.close()

        return True

    def showEvent(self, event):
        super().showEvent(event)
        self.movethedamnbutton()

    def toggleButtons(self):
        self.ui.otherDataFileSelect.setEnabled(self.fileType != "")
        self.ui.hyperthoughtLocationButton.setEnabled(self.uselistmodel.metadataList != [])
        self.ui.hyperthoughtUploadButton.setEnabled(self.ui.hyperthoughtLocationLineEdit.text() != "")

    def uploadToHyperthought(self):
        auth_control = htauthcontroller.HTAuthorizationController(self.accessKey)
        metadataJson = ht_utilities.dict_to_ht_metadata(self.usefilterModel.displayed)
        progress = QProgressDialog("Uploading files...", "Abort Upload", 0, len(self.uselistmodel.metadataList), self)
        self.createUpload.emit(self.uselistmodel.metadataList, auth_control, self.folderuuid, metadataJson)
        self.uploader.currentUploadDone.connect(progress.setValue)
        self.uploader.currentlyUploading.connect(progress.setLabelText)
        self.uploader.allUploadsDone.connect(progress.accept)
        progress.canceled.connect(lambda: self.uploader.interruptUpload())
        progress.exec()


    def dragEnterEven(event):
        print("YES I GET HERE TOO 2")
        event.acceptProposedAction()

    def dragMoveEvent(event):
        print("YES I GET HERE TOO 3")
        self.event.setDropAction(Qt.MoveAction);
        event.accept()

    def dropEvent(event):
        print("YES I GET HERE TOO")
        event.accept()




