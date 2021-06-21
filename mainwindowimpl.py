# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QApplication, QButtonGroup, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame, QHeaderView, QToolButton, QStyle, QProgressDialog, QDialog
from PySide2.QtCore import QFile, QDir ,QIODevice, Qt, QStandardPaths, QSortFilterProxyModel, QObject, Signal, Slot, QRegExp, QThread,QModelIndex, QEvent
from PySide2.QtGui import QCloseEvent, QCursor, QDesktopServices
from ui_mainwindow import Ui_MainWindow
from hyperthoughtdialogimpl import HyperthoughtDialogImpl
from createtablemodel	import TableModelC
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from treemodelrestore import TreeModelR
from usetreemodel import TreeModelU
from filterModel import FilterModel
from usefiltermodel import FilterModelU
from checkboxdelegate import CheckBoxDelegate
from usefiledelegate import UseFileDelegate
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
        self.ui.actionOpen_Template.triggered.connect(self.restoreTemplate)
        self.ui.dataFileSelect.clicked.connect(self.selectFile)
        self.ui.hyperthoughtTemplateSelect.clicked.connect(self.selectTemplate)
        self.ui.saveTemplateButton.clicked.connect(self.saveTemplate)
        self.ui.otherDataFileSelect.clicked.connect(self.extractFile)
        self.ui.hyperthoughtUploadButton.clicked.connect(self.uploadToHyperthought)
        self.setAcceptDrops(True)
        self.numCustoms = 0

        aTree={}
        self.createtablemodel = TableModelC(aTree,self)
        self.filterModel = FilterModel(self)
        self.filterModel.setSourceModel(self.createtablemodel)
        self.ui.metadataTableView.setModel(self.filterModel)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_SOURCE_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_HTNAME_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_SOURCEVAL_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(self.createtablemodel.K_HTVALUE_COL_INDEX,QHeaderView.ResizeToContents)
        self.ui.metadataTableView.setColumnWidth(self.createtablemodel.K_USESOURCE_COL_INDEX, self.width() * .1)

        self.checkboxDelegate = CheckBoxDelegate()
        self.createtrashDelegate = TrashDelegate()
        self.ui.metadataTableView.setItemDelegateForColumn(self.createtablemodel.K_USESOURCE_COL_INDEX, self.checkboxDelegate)
        self.ui.metadataTableView.setItemDelegateForColumn(self.createtablemodel.K_EDITABLE_COL_INDEX, self.checkboxDelegate)
        self.ui.metadataTableView.setItemDelegateForColumn(self.createtablemodel.K_REMOVE_COL_INDEX, self.createtrashDelegate)
        self.ui.metadataTableView.setColumnWidth(self.createtablemodel.K_REMOVE_COL_INDEX,self.width() * .05)

        self.treeModel = TreeModel(["Available File Metadata"],aTree,self.createtablemodel)
        self.ui.metadataTreeView.setModel(self.treeModel)
        self.treeModel.checkChanged.connect(self.filterModel.checkList)
        self.createtrashDelegate.pressed.connect(self.handleRemoveCreate)
        self.editableKeys = []

        self.usetablemodel = TableModelU(self,[],self.editableKeys)
        self.usefilterModel = FilterModelU(self)
        self.usefilterModel.setSourceModel(self.usetablemodel)
        self.ui.useTemplateTableView.setModel(self.usefilterModel)
        self.ui.useTemplateTableView.setColumnWidth(self.usetablemodel.K_HTKEY_COL_INDEX,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(self.usetablemodel.K_HTVALUE_COL_INDEX,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(self.usetablemodel.K_SOURCE_COL_INDEX,self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(self.usetablemodel.K_USESOURCE_COL_INDEX,self.width()*.1)
        self.ui.useTemplateTableView.setColumnWidth(self.usetablemodel.K_HTANNOTATION_COL_INDEX,self.width()*.1)
        self.usetrashDelegate = TrashDelegate()
        self.ui.useTemplateTableView.setItemDelegateForColumn(self.usetablemodel.K_USESOURCE_COL_INDEX, self.checkboxDelegate)
        self.ui.useTemplateTableView.setItemDelegateForColumn(self.usetablemodel.K_REMOVE_COL_INDEX, self.usetrashDelegate)
        self.ui.useTemplateTableView.setColumnWidth(self.usetablemodel.K_REMOVE_COL_INDEX,self.width()*.075)
        self.usetrashDelegate.pressed.connect(self.handleRemoveUse)


        self.uselistmodel = ListModel(self, self.usetablemodel,[])
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.uselistmodel.rowRemoved.connect(self.toggleButtons)
        self.uselistmodel.rowAdded.connect(self.toggleButtons)

        self.useFileDelegate = UseFileDelegate(self)
        self.ui.useTemplateListView.setItemDelegate(self.useFileDelegate)

        self.ui.useTemplateListView.clicked.connect(self.removeRowfromUsefileType)

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
        self.ui.hyperthoughtTemplateLineEdit.installEventFilter(self)
        self.ui.otherDataFileLineEdit.installEventFilter(self)
        self.ui.dataFileLineEdit.installEventFilter(self)


    def acceptKey(self, apikey):
        self.accessKey = apikey


    def addCreateTableRow(self):
        self.createtablemodel.addEmptyRow(self.numCustoms)
        self.numCustoms+=1


    def addFile(self):
        linetexts = QFileDialog.getOpenFileNames(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ctf *.xml *.ang)"))[0]
        for line in linetexts:
            self.uselistmodel.addRow(line)
        self.toggleButtons()


    def addAppendButton(self):
        self.appendSourceFilesButton= QToolButton(self.ui.useTemplateListView)
        icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)


    def addUseTableRow(self):
        self.usetablemodel.addEmptyRow()

    def closeEvent(self, event):
        self.mThread.quit()
        self.mThread.wait(250)


    def extractFile(self, fileLink = False):
        if fileLink == False:
            linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
            QStandardPaths.HomeLocation),self.tr("Files (*"+self.fileType+")"))[0]
        else:
            linetext = fileLink
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
                self.unusedTreeModel = TreeModelU(["Available File Metadata"],headerDict,self.usetablemodel,self.editableKeys)
                self.templatelist = []
                self.templatesources = []
                for i in range(len(self.templatedata)):
                    self.templatelist.append(self.templatedata[i])
                    if "Custom Input" not in self.templatedata[i]["Source"]:
                        self.templatesources.append("/".join(self.templatedata[i]['Source'].split("/")[1:]))
                    else:
                        self.usetablemodel.addExistingRow(self.templatedata[i])
                self.usesearchFilterModel = QSortFilterProxyModel(self)
                self.usesearchFilterModel.setSourceModel(self.usefilterModel)
                self.usesearchFilterModel.setFilterKeyColumn(0)
                self.usesearchFilterModel.setDynamicSortFilter(True)
                self.ui.useTemplateTableView.setModel(self.usesearchFilterModel)
        
        self.toggleButtons()

    def eventFilter(self, object, event):
        if object == self.ui.hyperthoughtTemplateLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
                    self.loadTemplateFile(event.mimeData().urls()[0].toLocalFile())
        if object == self.ui.otherDataFileLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-6:-2] == self.fileType:
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-6:-2] == self.fileType:
                    event.acceptProposedAction()
                    self.extractFile(event.mimeData().urls()[0].toLocalFile())
        if object == self.ui.dataFileLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-6:-2] == ".ctf" or str(event.mimeData().urls()[0])[-6:-2] == ".ang":
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-6:-2] == ".ctf" or str(event.mimeData().urls()[0])[-6:-2] == ".ang":
                    event.acceptProposedAction()
                    self.selectFile(event.mimeData().urls()[0].toLocalFile())


        return QMainWindow.eventFilter(self, object,  event)


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
        remoteDirPath = self.hyperthoughtui.getUploadDirectory()
        self.folderuuid = ht_requests.get_ht_id_path_from_ht_path(self.hyperthoughtui.authcontrol, ht_path=remoteDirPath)
        self.ui.hyperthoughtLocationLineEdit.setText(remoteDirPath)
        self.toggleButtons()

    def handleRemoveCreate(self, source):
        if "Custom Input" in source:
            for i in range(len(self.createtablemodel.metadataList)):
                if self.createtablemodel.metadataList[i]["Source"] == source:
                    self.createtablemodel.beginRemoveRows(QModelIndex(),i,i)
                    del self.createtablemodel.metadataList[i]
                    self.createtablemodel.endRemoveRows()
                    break
        else:
            self.treeModel.changeLeafCheck(source)

    def handleRemoveUse(self, source):
        for i in range(len(self.usetablemodel.metadataList)):
            if self.usetablemodel.metadataList[i]["Source"] == source:
                self.usetablemodel.beginRemoveRows(QModelIndex(),i,i)
                del self.usetablemodel.metadataList[i]
                self.usetablemodel.endRemoveRows()
                break
        for i in range(len(self.usefilterModel.displayed)):
            if self.usefilterModel.displayed[i]["Source"] == source:
                self.usefilterModel.beginRemoveRows(QModelIndex(),i,i)
                del self.usefilterModel.displayed[i]
                self.usefilterModel.endRemoveRows()
                break

    def help(self):
        QDesktopServices.openUrl("http://www.bluequartz.net/")

    def movethedamnbutton(self):
        self.appendSourceFilesButton.move(self.ui.useTemplateListView.width() - self.appendSourceFilesButton.width() - 15,self.ui.useTemplateListView.height() - self.appendSourceFilesButton.height())

    def openRecent(self):
        print("Clicked Open Recent.")

    def openPackage(self):
        linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ezpak)"))[0]
        if linetext != "":
            self.currentTemplate= linetext.split("/")[-1]
            self.ui.displayedFileLabel.setText(linetext.split("/")[-1])
            infile = open(linetext,"r")
            self.templatedata = infile.readline()
            self.templatedata = json.loads(self.templatedata)
            templatesources = json.loads(infile.readline())
            self.fileType = json.loads(infile.readline())
            fileType = infile.readline()
            fileType = json.loads(fileType)
            editables = infile.readline()
            self.editable = json.loads(editables)
            self.usetablemodel = TableModelU(self,[])
            self.usetablemodel.templatelist = self.templatedata
            self.usetablemodel.templatesources = templatesources
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            self.ui.useTemplateTableView.setModel(self.usetablemodel)
            self.uselistmodel = ListModel(self, self.usetablemodel, fileType)
            self.ui.useTemplateListView.setModel(self.uselistmodel)
            self.toggleButtons()
            infile.close()

    def restoreTemplate(self):
        #Clear data on create side
        self.createtablemodel.metadataList = []
        self.createtablemodel.hiddenList = []
        self.filterModel.displayed = []
        #open template
        linetext = QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
        QStandardPaths.HomeLocation),self.tr("Files (*.ez)"))[0]
        if linetext != "":
            infile = open(linetext,"r")
            infile.readline()
            fileType = infile.readline()
            self.fileType = json.loads(fileType)
            infile.readline()
            newList = infile.readline()
            newList = json.loads(newList)
            newDict = infile.readline()
            newDict = json.loads(newDict)
            self.ui.dataFileLineEdit.setText(self.fileType[0])
            self.createtablemodel = TableModelC(newDict,self)
            self.filterModel.displayed = []
            self.filterModel.setSourceModel(self.createtablemodel)
            self.filterModel.fileType = self.fileType
            self.createTableSearchFilterModel = QSortFilterProxyModel(self)
            self.createTableSearchFilterModel.setSourceModel(self.filterModel)
            self.createTableSearchFilterModel.setFilterKeyColumn(1)
            self.createTableSearchFilterModel.setDynamicSortFilter(True)
            self.ui.metadataTableView.setModel(self.createTableSearchFilterModel)
            self.treeModel = TreeModelR(["Available File Metadata"],newDict,self.createtablemodel, newList,self.filterModel)


            for i in range(len(newList)):
                if "Custom Input" in newList[i]["Source"]:
                    self.createtablemodel.beginInsertRows(self.createtablemodel.index(len(self.createtablemodel.metadataList), 0), i, i)
                    self.createtablemodel.metadataList.append(newList[i])
                    self.createtablemodel.endInsertRows()

            self.createTreeSearchFilterModel = QSortFilterProxyModel(self)
            self.createTreeSearchFilterModel.setSourceModel(self.treeModel)
            self.createTreeSearchFilterModel.setFilterKeyColumn(0)
            self.createTreeSearchFilterModel.setDynamicSortFilter(True)
            self.createTreeSearchFilterModel.setRecursiveFilteringEnabled(True)
            self.ui.metadataTreeView.setModel(self.createTreeSearchFilterModel)
            self.treeModel.checkChanged.connect(self.filterModel.checkList)
            self.createtrashDelegate.pressed.connect(self.handleRemoveCreate)

    def removeRowfromUsefileType(self, index):
        if self.ui.useTemplateListView.width() - 64 < self.ui.useTemplateListView.mapFromGlobal(QCursor.pos()).x():
            #this is where to remove the row
            self.uselistmodel.removeRow(index.row())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.movethedamnbutton()


    def savePackage(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "/Packages/",
                                   "Packages (*.ez)")
        dialog.setDefaultSuffix(".ezpak")
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
                json.dump(self.editableKeys, outfile)

    def savePackageAs(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                   "/Packages/",
                                   "Packages (*)")
        dialog.setDefaultSuffix(".ezpak")
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
                son.dump(self.createtablemodel.editableList, outfile)
                outfile.write("\n")
                json.dump(self.fileType, outfile)
                outfile.write("\n")
                json.dump(self.uselistmodel.metadataList, outfile)
                outfile.write("\n")
                json.dump(self.editableKeys, outfile)

    def saveTemplate(self):
        dialog = QFileDialog(self, "Save File","", "Templates (*.ez)")
        dialog.setDefaultSuffix(".ez")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        fileName = ""
        if dialog.exec():
            fileName  = dialog.selectedFiles()[0]
        if fileName != "":
            with open(fileName, 'w') as outfile:
                json.dump(self.filterModel.displayed, outfile)
                outfile.write("\n")
                json.dump(self.filterModel.fileType, outfile)
                outfile.write("\n")
                self.createtablemodel.editableList = []
                for i in range(len(self.createtablemodel.metadataList)):
                    if self.createtablemodel.metadataList[i]["Editable"] == 2 and (self.createtablemodel.metadataList[i]["Checked"] == 2 or self.createtablemodel.metadataList[i]["Checked"] == 1):
                        self.createtablemodel.editableList.append(self.createtablemodel.metadataList[i]["Key"])
                json.dump(self.createtablemodel.editableList, outfile)
                outfile.write("\n")
                json.dump(self.createtablemodel.metadataList, outfile)
                outfile.write("\n")
                json.dump(self.treeModel.treeDict, outfile)

    def selectFile(self, fileLink = None):
        if fileLink == False:
            linetext=QFileDialog.getOpenFileName(self,self.tr("Select File"),QStandardPaths.displayName(
            QStandardPaths.HomeLocation),self.tr("Files (*.*)"))[0]
        else:
            linetext = fileLink
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
            self.filterModel.fileType.append(linetext)
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
            self.createtrashDelegate.pressed.connect(self.handleRemoveCreate)
        
        self.toggleButtons()
        return True

    def selectTemplate(self):
        startLocation = self.ui.hyperthoughtTemplateLineEdit.text()
        if startLocation == "":
            startLocation = QStandardPaths.writableLocation(QStandardPaths.HomeLocation)

        templateFilePath = QFileDialog.getOpenFileName(self, self.tr("Select File"), startLocation, self.tr("Files (*.ez)") )[0]
        self.loadTemplateFile(templateFilePath)


    def loadTemplateFile(self, templateFilePath = None):
        if templateFilePath == "":
            return False

        self.usetablemodel.metadataList = []
        self.usefilterModel.displayed = []
        self.currentTemplate= templateFilePath.split("/")[-1]
        self.ui.displayedFileLabel.setText(templateFilePath.split("/")[-1])
        self.ui.hyperthoughtTemplateLineEdit.setText(templateFilePath)
        self.ui.otherDataFileLineEdit.setText("")
        infile = open(templateFilePath,"r")
        data = infile.readline()
        fileType = infile.readline()
        fileType = json.loads(fileType)
        self.fileType = fileType[0][-4:]
        editables = infile.readline()
        self.editableKeys = json.loads(editables)
        self.usetablemodel.editableKeys = self.editableKeys
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
        if (self.ui.hyperthoughtTemplateLineEdit.text() != "" and
            self.ui.otherDataFileLineEdit.text() != "" and
            self.ui.useTemplateListView.model().rowCount() > 0 and
            self.ui.hyperthoughtLocationLineEdit.text() != "") :
            
            self.ui.hyperthoughtUploadButton.setEnabled(True)

    def uploadToHyperthought(self):
        auth_control = htauthcontroller.HTAuthorizationController(self.accessKey)
        metadataJson = ht_utilities.dict_to_ht_metadata(self.usefilterModel.displayed)
        progress = QProgressDialog("Uploading files...", "Abort Upload", 0, len(self.uselistmodel.metadataList), self)

        progress.setWindowFlags( Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint )
        progress.setAttribute(Qt.WA_DeleteOnClose)
        self.createUpload.emit(self.uselistmodel.metadataList, auth_control, self.folderuuid, metadataJson)
        self.uploader.currentUploadDone.connect(progress.setValue)
        self.uploader.currentlyUploading.connect(progress.setLabelText)
        self.uploader.allUploadsDone.connect(progress.accept)
        progress.canceled.connect(lambda: self.uploader.interruptUpload())
        progress.setFixedSize( 500, 100 )
        progress.exec()



