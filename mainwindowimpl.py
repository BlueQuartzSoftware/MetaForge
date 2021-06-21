# This Python file uses the following encoding: utf-8

from ezmodel.ezmetadataentry import EzMetadataEntry
from PySide2.QtWidgets import QApplication, QButtonGroup, QWidget, QMainWindow, QFileSystemModel, QFileDialog, QStyleOptionFrame, QHeaderView, QToolButton, QStyle, QProgressDialog, QDialog
from PySide2.QtCore import QFile, QDir, QIODevice, Qt, QStandardPaths, QSortFilterProxyModel, QObject, Signal, Slot, QRegExp, QThread, QModelIndex, QEvent
from PySide2.QtGui import QCloseEvent, QCursor, QDesktopServices
from ui_mainwindow import Ui_MainWindow
from hyperthoughtdialogimpl import HyperthoughtDialogImpl
from qeztablemodel import QEzTableModel
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from treemodelrestore import TreeModelR
from usetreemodel import TreeModelU
from qcreateeztablemodel import QCreateEzTableModel
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
import parsers.ang as ang
import json

from ezmodel.ezmetadatamodel import EzMetadataModel


class MainWindow(QMainWindow):
    K_CREATE_TREE_HEADER = "Available File Metadata"

    createUpload = Signal(
        list, htauthcontroller.HTAuthorizationController, str, list)

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
        self.ui.hyperthoughtUploadButton.clicked.connect(
            self.uploadToHyperthought)
        self.setAcceptDrops(True)
        self.numCustoms = 0

        self.create_ez_table_model = QEzTableModel(
            metadata_model=EzMetadataModel(), parent=self)
        self.create_ez_table_model_proxy = QCreateEzTableModel(self)
        self.create_ez_table_model_proxy.setSourceModel(
            self.create_ez_table_model)
        self.ui.metadataTableView.setModel(self.create_ez_table_model_proxy)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
            self.create_ez_table_model.K_SOURCE_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
            self.create_ez_table_model.K_HTNAME_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
            self.create_ez_table_model.K_SOURCEVAL_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
            self.create_ez_table_model.K_HTVALUE_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.metadataTableView.setColumnWidth(
            self.create_ez_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.width() * .1)

        self.checkboxDelegate = CheckBoxDelegate()
        self.createtrashDelegate = TrashDelegate()
        self.ui.metadataTableView.setItemDelegateForColumn(
            self.create_ez_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.checkboxDelegate)
        self.ui.metadataTableView.setItemDelegateForColumn(
            self.create_ez_table_model.K_EDITABLE_COL_INDEX, self.checkboxDelegate)
        self.ui.metadataTableView.setItemDelegateForColumn(
            self.create_ez_table_model.K_REMOVE_COL_INDEX, self.createtrashDelegate)
        self.ui.metadataTableView.setColumnWidth(
            self.create_ez_table_model.K_REMOVE_COL_INDEX, self.width() * .05)

        self.treeModel = TreeModel(
            [self.K_CREATE_TREE_HEADER], EzMetadataModel(), self.create_ez_table_model)
        self.ui.metadataTreeView.setModel(self.treeModel)
        self.treeModel.checkChanged.connect(
            self.create_ez_table_model_proxy.checkList)
        self.createtrashDelegate.pressed.connect(self.handleRemoveCreate)
        self.editableKeys = []

        self.usetablemodel = TableModelU(self, [], self.editableKeys)
        self.usefilterModel = FilterModelU(self)
        self.usefilterModel.setSourceModel(self.usetablemodel)
        self.ui.useTemplateTableView.setModel(self.usefilterModel)
        self.ui.useTemplateTableView.setColumnWidth(
            self.usetablemodel.K_HTKEY_COL_INDEX, self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(
            self.usetablemodel.K_HTVALUE_COL_INDEX, self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(
            self.usetablemodel.K_SOURCE_COL_INDEX, self.width()*.25)
        self.ui.useTemplateTableView.setColumnWidth(
            self.usetablemodel.K_OVERRIDESOURCEVALUE_COL_INDEX, self.width()*.1)
        self.ui.useTemplateTableView.setColumnWidth(
            self.usetablemodel.K_HTANNOTATION_COL_INDEX, self.width()*.1)
        self.usetrashDelegate = TrashDelegate()
        self.ui.useTemplateTableView.setItemDelegateForColumn(
            self.usetablemodel.K_OVERRIDESOURCEVALUE_COL_INDEX, self.checkboxDelegate)
        self.ui.useTemplateTableView.setItemDelegateForColumn(
            self.usetablemodel.K_REMOVE_COL_INDEX, self.usetrashDelegate)
        self.ui.useTemplateTableView.setColumnWidth(
            self.usetablemodel.K_REMOVE_COL_INDEX, self.width()*.075)
        self.usetrashDelegate.pressed.connect(self.handleRemoveUse)

        self.uselistmodel = ListModel(self, self.usetablemodel, [])
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.uselistmodel.rowRemoved.connect(self.toggleButtons)
        self.uselistmodel.rowAdded.connect(self.toggleButtons)

        self.useFileDelegate = UseFileDelegate(self)
        self.ui.useTemplateListView.setItemDelegate(self.useFileDelegate)

        self.ui.useTemplateListView.clicked.connect(
            self.removeRowfromUsefileType)

        self.addAppendButton()
        self.ui.TabWidget.currentChanged.connect(self.movethedamnbutton)
        self.appendSourceFilesButton.clicked.connect(self.addFile)
        self.ui.appendCreateTableRowButton.clicked.connect(
            self.addCustomRowToCreateTable)
        self.ui.appendUseTableRowButton.clicked.connect(self.addUseTableRow)
        self.ui.hyperthoughtLocationButton.clicked.connect(
            self.hyperthoughtui.exec)
        self.ui.usetableSearchBar.textChanged.connect(self.filterUseTable)
        self.ui.createTemplateListSearchBar.textChanged.connect(
            self.filterCreateTable)
        self.ui.createTemplateTreeSearchBar.textChanged.connect(
            self.filterCreateTree)

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

    def addCustomRowToCreateTable(self):
        self.create_ez_table_model.addCustomRow(self.numCustoms)
        self.numCustoms += 1

    def addFile(self):
        linetexts = QFileDialog.getOpenFileNames(self, self.tr("Select File"), QStandardPaths.displayName(
            QStandardPaths.HomeLocation), self.tr("Files (*.ctf *.xml *.ang)"))[0]
        for line in linetexts:
            self.uselistmodel.addRow(line)
        self.toggleButtons()

    def addAppendButton(self):
        self.appendSourceFilesButton = QToolButton(self.ui.useTemplateListView)
        icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)

    def addUseTableRow(self):
        self.usetablemodel.addEmptyRow()

    def closeEvent(self, event):
        self.mThread.quit()
        self.mThread.wait(250)

    def extractFile(self, fileLink=False):
        if fileLink == False:
            linetext = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), self.tr("Files (*"+self.fileType+")"))[0]
        else:
            linetext = fileLink
        if linetext != "":
            self.setWindowTitle(linetext)
            self.ui.dataTypeText.setText(linetext.split(".")[1].upper())
            self.ui.otherDataFileLineEdit.setText(linetext)
            if self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser") != -1:
                headerDict = {}
                self.ui.fileParserCombo.setCurrentIndex(
                    self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser"))
            if linetext.split(".")[1].upper() == "CTF":
                headerDict = ctf.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "ANG":
                headerDict = ang.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "XML":
                print("XML Parser used")

            if self.templatedata:
                self.usetablemodel.metadataList = []
                self.usefilterModel = FilterModelU(self)
                self.usefilterModel.setSourceModel(self.usetablemodel)
                self.unusedTreeModel = TreeModelU(
                    [self.K_CREATE_TREE_HEADER], headerDict, self.usetablemodel, self.editableKeys)
                self.templatelist = []
                self.templatesources = []
                for i in range(len(self.templatedata)):
                    self.templatelist.append(self.templatedata[i])
                    if "Custom Input" not in self.templatedata[i]["Source"]:
                        self.templatesources.append(
                            "/".join(self.templatedata[i]['Source'].split("/")[1:]))
                    else:
                        self.usetablemodel.addRow(self.templatedata[i])
                self.usesearchFilterModel = QSortFilterProxyModel(self)
                self.usesearchFilterModel.setSourceModel(self.usefilterModel)
                self.usesearchFilterModel.setFilterKeyColumn(0)
                self.usesearchFilterModel.setDynamicSortFilter(True)
                self.ui.useTemplateTableView.setModel(
                    self.usesearchFilterModel)

        self.toggleButtons()

    def eventFilter(self, object, event):
        if object == self.ui.hyperthoughtTemplateLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
                    self.loadTemplateFile(
                        event.mimeData().urls()[0].toLocalFile())
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
        self.create_ez_table_model_proxy.invalidate()
        self.create_ez_table_model_proxy.setFilterCaseSensitivity(
            Qt.CaseInsensitive)
        self.create_ez_table_model_proxy.setFilterWildcard(
            "*"+self.ui.createTemplateListSearchBar.text()+"*")

    def filterCreateTree(self):
        self.createTreeSearchFilterModel.invalidate()
        self.createTreeSearchFilterModel.setFilterCaseSensitivity(
            Qt.CaseInsensitive)
        self.createTreeSearchFilterModel.setFilterWildcard(
            "*"+self.ui.createTemplateTreeSearchBar.text()+"*")

    def filterUseTable(self):
        self.usesearchFilterModel.invalidate()
        self.usesearchFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.usesearchFilterModel.setFilterWildcard(
            "*"+self.ui.usetableSearchBar.text()+"*")

    def getLocation(self):
        remoteDirPath = self.hyperthoughtui.getUploadDirectory()
        self.folderuuid = ht_requests.get_ht_id_path_from_ht_path(
            self.hyperthoughtui.authcontrol, ht_path=remoteDirPath)
        self.ui.hyperthoughtLocationLineEdit.setText(remoteDirPath)
        self.toggleButtons()

    def handleRemoveCreate(self, source):
        if "Custom Input" in source:
            for i in range(len(self.create_ez_table_model.metadataList)):
                if self.create_ez_table_model.metadataList[i]["Source"] == source:
                    self.create_ez_table_model.beginRemoveRows(
                        QModelIndex(), i, i)
                    del self.create_ez_table_model.metadataList[i]
                    self.create_ez_table_model.endRemoveRows()
                    break
        else:
            self.treeModel.changeLeafCheck(source)

    def handleRemoveUse(self, source):
        for i in range(len(self.usetablemodel.metadataList)):
            if self.usetablemodel.metadataList[i]["Source"] == source:
                self.usetablemodel.beginRemoveRows(QModelIndex(), i, i)
                del self.usetablemodel.metadataList[i]
                self.usetablemodel.endRemoveRows()
                break
        for i in range(len(self.usefilterModel.displayed)):
            if self.usefilterModel.displayed[i]["Source"] == source:
                self.usefilterModel.beginRemoveRows(QModelIndex(), i, i)
                del self.usefilterModel.displayed[i]
                self.usefilterModel.endRemoveRows()
                break

    def help(self):
        QDesktopServices.openUrl("http://www.bluequartz.net/")

    def movethedamnbutton(self):
        self.appendSourceFilesButton.move(self.ui.useTemplateListView.width() - self.appendSourceFilesButton.width(
        ) - 15, self.ui.useTemplateListView.height() - self.appendSourceFilesButton.height())

    def openRecent(self):
        print("Clicked Open Recent.")

    def openPackage(self):
        linetext = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
            QStandardPaths.HomeLocation), self.tr("Files (*.ez)"))[0]
        if linetext != "":
            self.currentTemplate = linetext.split("/")[-1]
            self.ui.displayedFileLabel.setText(linetext.split("/")[-1])
            infile = open(linetext, "r")
            self.templatedata = infile.readline()
            self.templatedata = json.loads(self.templatedata)
            templatesources = json.loads(infile.readline())
            self.fileType = json.loads(infile.readline())
            fileType = infile.readline()
            fileType = json.loads(fileType)
            editables = infile.readline()
            self.editable = json.loads(editables)
            self.usetablemodel = TableModelU(self, [])
            self.usetablemodel.templatelist = self.templatedata
            self.usetablemodel.templatesources = templatesources
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            self.ui.useTemplateTableView.setModel(self.usetablemodel)
            self.uselistmodel = ListModel(self, self.usetablemodel, fileType)
            self.ui.useTemplateListView.setModel(self.uselistmodel)
            self.toggleButtons()
            infile.close()

    def saveTemplate(self):
        dialog = QFileDialog(self, "Save File", "", "Templates (*.ez)")
        dialog.setDefaultSuffix(".ez")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        fileName = ""
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]
        if fileName != "":
            with open(fileName, 'w') as outfile:
                model_string = self.create_ez_table_model.metadata_model.to_json_string()
                outfile.write(model_string)

    def restoreTemplate(self):
        # open template
        template_file_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
            QStandardPaths.HomeLocation), self.tr("Files (*.ez)"))[0]
        if template_file_path != "":
            metadata_model = EzMetadataModel.from_json_file(template_file_path)

            self.create_ez_table_model = QEzTableModel(metadata_model=metadata_model,
                                                       parent=self)

            self.treeModel = TreeModel(
                [self.K_CREATE_TREE_HEADER], metadata_model)
            self.ui.metadataTreeView.setModel(self.treeModel)

            self.init_create_table_model_proxy(
                self.create_ez_table_model, template_file_path)

            self.ui.metadataTableView.setModel(
                self.create_ez_table_model_proxy)

            self.treeModel.checkChanged.connect(
                self.create_ez_table_model_proxy.checkList)
            self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
                self.create_ez_table_model.K_SOURCE_COL_INDEX, QHeaderView.ResizeToContents)
            self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
                self.create_ez_table_model.K_HTNAME_COL_INDEX, QHeaderView.ResizeToContents)
            self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
                self.create_ez_table_model.K_SOURCEVAL_COL_INDEX, QHeaderView.ResizeToContents)
            self.ui.metadataTableView.horizontalHeader().setSectionResizeMode(
                self.create_ez_table_model.K_HTVALUE_COL_INDEX, QHeaderView.ResizeToContents)
            self.ui.metadataTableView.setColumnWidth(
                self.create_ez_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.width() * .1)

    def init_create_table_model_proxy(self, source_model: QEzTableModel, linetext: str):
        self.create_ez_table_model_proxy = QCreateEzTableModel(self)
        self.create_ez_table_model_proxy.displayed = []
        self.create_ez_table_model_proxy.setSourceModel(source_model)
        self.create_ez_table_model_proxy.fileType.append(linetext)
        self.create_ez_table_model_proxy.setFilterKeyColumn(1)
        self.create_ez_table_model_proxy.setDynamicSortFilter(True)
        self.filterCreateTable()

    def removeRowfromUsefileType(self, index):
        if self.ui.useTemplateListView.width() - 64 < self.ui.useTemplateListView.mapFromGlobal(QCursor.pos()).x():
            # this is where to remove the row
            self.uselistmodel.removeRow(index.row())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.movethedamnbutton()

    def savePackage(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File",
                                               "/Packages/",
                                               "Packages (*.ez)")
        if fileName != "":
            myDir = QDir()
            myDir.mkpath(fileName[0])
            for file in self.uselistmodel.metadataList:
                QFile.copy(file, fileName[0]+"/"+file.split("/")[-1])
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
        if fileName != "":
            myDir = QDir()
            myDir.mkpath(fileName[0])
            for file in self.uselistmodel.metadataList:
                QFile.copy(file, fileName[0]+"/"+file.split("/")[-1])
            with open(fileName[0]+"/"+self.currentTemplate, 'w') as outfile:
                json.dump(self.usetablemodel.templatelist, outfile)
                outfile.write("\n")
                json.dump(self.usetablemodel.templatesources, outfile)
                outfile.write("\n")
                json.dump(self.create_ez_table_model.editableList, outfile)
                outfile.write("\n")
                json.dump(self.fileType, outfile)
                outfile.write("\n")
                json.dump(self.uselistmodel.metadataList, outfile)
                outfile.write("\n")
                json.dump(self.editableKeys, outfile)

    def selectFile(self, fileLink=None):
        if fileLink == False:
            linetext = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), self.tr("Files (*.*)"))[0]
        else:
            linetext = fileLink
        if linetext != "":
            self.setWindowTitle(linetext)
            self.ui.dataFileLineEdit.setText(linetext)
            self.ui.dataTypeText.setText(linetext.split(".")[1].upper())
            if self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser") != -1:
                headerDict = {}
                self.ui.fileParserCombo.setCurrentIndex(
                    self.ui.fileParserCombo.findText(linetext.split(".")[1].upper()+" Parser"))
            if linetext.split(".")[1].upper() == "CTF":
                headerDict = ctf.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "ANG":
                headerDict = ang.parse_header_as_dict(linetext)
            elif linetext.split(".")[1].upper() == "XML":
                print("XML Parser used")

            metadata_model = EzMetadataModel.create_model(headerDict,
                                                          linetext,
                                                          source_type=EzMetadataEntry.SourceType.FILE)
            self.create_ez_table_model = QEzTableModel(
                metadata_model=metadata_model, parent=self)
            self.init_create_table_model_proxy(
                self.create_ez_table_model, linetext)

            self.ui.metadataTableView.setModel(
                self.create_ez_table_model_proxy)
            self.treeModel = TreeModel(
                [self.K_CREATE_TREE_HEADER], headerDict, self.create_ez_table_model)
            self.createTreeSearchFilterModel = QSortFilterProxyModel(self)
            self.createTreeSearchFilterModel.setSourceModel(self.treeModel)
            self.createTreeSearchFilterModel.setFilterKeyColumn(0)
            self.createTreeSearchFilterModel.setDynamicSortFilter(True)
            self.createTreeSearchFilterModel.setRecursiveFilteringEnabled(True)
            self.ui.metadataTreeView.setModel(self.createTreeSearchFilterModel)
            self.treeModel.checkChanged.connect(
                self.create_ez_table_model_proxy.checkList)
            self.createtrashDelegate.pressed.connect(self.handleRemoveCreate)

        self.toggleButtons()
        return True

    def selectTemplate(self):
        startLocation = self.ui.hyperthoughtTemplateLineEdit.text()
        if startLocation == "":
            startLocation = QStandardPaths.writableLocation(
                QStandardPaths.HomeLocation)

        templateFilePath = QFileDialog.getOpenFileName(self, self.tr(
            "Select File"), startLocation, self.tr("Files (*.ez)"))[0]
        self.loadTemplateFile(templateFilePath)

    def loadTemplateFile(self, templateFilePath=None):
        if templateFilePath == "":
            return False

        # Load the EzMetadataModel from the json file (Template file)
        ez_metadata_model = EzMetadataModel.from_json_file(templateFilePath)

        ez_qtable_model = QEzTableModel(ez_metadata_model)
        self.ui.useTemplateTableView.setModel(ez_qtable_model)

        self.currentTemplate = templateFilePath.split("/")[-1]
        self.ui.displayedFileLabel.setText(templateFilePath.split("/")[-1])
        self.ui.hyperthoughtTemplateLineEdit.setText(templateFilePath)
        self.ui.otherDataFileLineEdit.setText("")

        # infile = open(templateFilePath,"r")
        # data = infile.readline()
        # fileType = infile.readline()
        # fileType = json.loads(fileType)
        # self.fileType = fileType[0][-4:]
        # editables = infile.readline()
        # self.editableKeys = json.loads(editables)
        # self.usetablemodel.editableKeys = self.editableKeys
        # self.toggleButtons()
        # self.templatedata = json.loads(data)
        # self.usetablemodel.addTemplateList(self.templatedata)
        # self.usefilterModel.setFilterRegExp(QRegExp())
        # infile.close()

        return True

    def showEvent(self, event):
        super().showEvent(event)
        self.movethedamnbutton()

    def toggleButtons(self):
        if (self.ui.hyperthoughtTemplateLineEdit.text() != "" and
            self.ui.otherDataFileLineEdit.text() != "" and
            self.ui.useTemplateListView.model().rowCount() > 0 and
                self.ui.hyperthoughtLocationLineEdit.text() != ""):

            self.ui.hyperthoughtUploadButton.setEnabled(True)

    def uploadToHyperthought(self):
        auth_control = htauthcontroller.HTAuthorizationController(
            self.accessKey)
        metadataJson = ht_utilities.dict_to_ht_metadata(
            self.usefilterModel.displayed)
        progress = QProgressDialog("Uploading files...", "Abort Upload", 0, len(
            self.uselistmodel.metadataList), self)

        progress.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        progress.setAttribute(Qt.WA_DeleteOnClose)
        self.createUpload.emit(
            self.uselistmodel.metadataList, auth_control, self.folderuuid, metadataJson)
        self.uploader.currentUploadDone.connect(progress.setValue)
        self.uploader.currentlyUploading.connect(progress.setLabelText)
        self.uploader.allUploadsDone.connect(progress.accept)
        progress.canceled.connect(lambda: self.uploader.interruptUpload())
        progress.setFixedSize(500, 100)
        progress.exec()
