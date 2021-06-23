# This Python file uses the following encoding: utf-8

from ezmodel.ezmetadataentry import EzMetadataEntry
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QToolButton, QStyle, QProgressDialog
from PySide2.QtCore import QFile, QDir, Qt, QStandardPaths, QSortFilterProxyModel, Signal, QThread, QModelIndex, QEvent, QFileInfo, QUrl
from PySide2.QtGui import QCursor, QDesktopServices
from ui_mainwindow import Ui_MainWindow
from hyperthoughtdialogimpl import HyperthoughtDialogImpl
from qeztablemodel import QEzTableModel
from usetablemodel import TableModelU
from uselistmodel import ListModel
from treemodel import TreeModel
from qcreateeztablemodel import QCreateEzTableModel
from quseeztablemodel import QUseEzTableModel
from usefiledelegate import UseFileDelegate

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
        self.ui.otherDataFileSelect.clicked.connect(self.loadOtherDataFile)
        self.ui.hyperthoughtUploadButton.clicked.connect(
            self.uploadToHyperthought)
        self.setAcceptDrops(True)
        self.numCustoms = 0
        self.editableKeys = []

        # Setup the blank Create Template table
        self.setup_create_ez_table()

        # Setup the blank Create Template tree
        self.setup_create_ez_tree()

        # Setup the blank Use Template table
        self.setup_use_ez_table()

        # Setup the blank Use Template file list
        self.setup_use_ez_list()

        self.addAppendButton()
        self.ui.TabWidget.currentChanged.connect(self.movethedamnbutton)
        self.appendSourceFilesButton.clicked.connect(self.addFile)
        self.ui.appendCreateTableRowButton.clicked.connect(
            self.addCustomRowToCreateTable)
        self.ui.removeCreateTableRowButton.clicked.connect(self.handleRemoveCreate)
        self.ui.removeUseTableRowButton.clicked.connect(self.handleRemoveUse)
        self.ui.appendUseTableRowButton.clicked.connect(self.addUseTableRow)
        self.ui.hyperthoughtLocationButton.clicked.connect(
            self.hyperthoughtui.exec)
        self.ui.useTemplateListSearchBar.textChanged.connect(self.filter_use_table)
        self.ui.createTemplateListSearchBar.textChanged.connect(
            self.filter_create_table)
        self.ui.createTemplateTreeSearchBar.textChanged.connect(
            self.filterCreateTree)
        self.ui.addMetadataFileCheckBox.stateChanged.connect(self.checkFileList)

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
    
    def setup_create_ez_table(self, metadata_model: EzMetadataModel = EzMetadataModel()):
        self.create_ez_table_model = QEzTableModel(metadata_model=metadata_model, parent=self)
        self.create_ez_table_model_proxy = self.init_create_table_model_proxy(self.create_ez_table_model)
        self.ui.metadataTableView.setModel(self.create_ez_table_model_proxy)
        self.filter_create_table()
    
    def setup_use_ez_table(self, metadata_model: EzMetadataModel = EzMetadataModel()):
        self.use_ez_table_model = QEzTableModel(metadata_model, parent=self)
        self.use_ez_table_model_proxy = self.init_use_table_model_proxy(self.use_ez_table_model)
        self.ui.useTemplateTableView.setModel(self.use_ez_table_model_proxy)
        self.filter_use_table()

    def setup_create_ez_tree(self, metadata_model: EzMetadataModel = EzMetadataModel()):
        headers = [self.K_CREATE_TREE_HEADER]
        self.treeModel = TreeModel(headers, metadata_model, self)
        self.createTreeSearchFilterModel = QSortFilterProxyModel(self)
        self.createTreeSearchFilterModel.setSourceModel(self.treeModel)
        self.createTreeSearchFilterModel.setFilterKeyColumn(0)
        self.createTreeSearchFilterModel.setDynamicSortFilter(True)
        self.createTreeSearchFilterModel.setRecursiveFilteringEnabled(True)
        self.ui.metadataTreeView.setModel(self.createTreeSearchFilterModel)
        self.ui.metadataTreeView.expandAll()
        refresh_func = self.create_ez_table_model.refresh_entry
        self.treeModel.checkChanged.connect(refresh_func)
    
    def setup_use_ez_list(self, file_list: list = []):
        self.uselistmodel = ListModel(file_list, self)
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.uselistmodel.rowRemoved.connect(self.toggleButtons)
        self.uselistmodel.rowAdded.connect(self.toggleButtons)

        self.useFileDelegate = UseFileDelegate(self)
        self.ui.useTemplateListView.setItemDelegate(self.useFileDelegate)

        self.ui.useTemplateListView.clicked.connect(
            self.removeRowfromUsefileType)

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
        self.use_ez_table_model.addCustomRow(1)

    def checkFileList(self, checked):
        if checked == Qt.Checked:
          if self.ui.otherDataFileLineEdit.text() != "":
              self.uselistmodel.addRow(self.ui.otherDataFileLineEdit.text())
        elif checked == Qt.Unchecked:
            if self.ui.otherDataFileLineEdit.text() in self.uselistmodel.metadataList:
                rowIndex = self.uselistmodel.metadataList.index(self.ui.otherDataFileLineEdit.text())
                self.uselistmodel.removeRow(rowIndex)

    def closeEvent(self, event):
        self.mThread.quit()
        self.mThread.wait(250)

    def eventFilter(self, object, event):
        if object == self.ui.hyperthoughtTemplateLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
                    self.ui.hyperthoughtTemplateLineEdit.setText(event.mimeData().urls()[0].toLocalFile())
                    self.loadTemplateFile()
        if object == self.ui.otherDataFileLineEdit:
            if event.type() == QEvent.DragEnter:
                event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                event.acceptProposedAction()
                self.ui.otherDataFileLineEdit.setText(event.mimeData().urls()[0].toLocalFile())
                self.importMetadataFromDataFile()
        if object == self.ui.dataFileLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-6:-2] == ".ctf" or str(event.mimeData().urls()[0])[-6:-2] == ".ang":
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-6:-2] == ".ctf" or str(event.mimeData().urls()[0])[-6:-2] == ".ang":
                    event.acceptProposedAction()
                    self.selectFile(event.mimeData().urls()[0].toLocalFile())

        return QMainWindow.eventFilter(self, object,  event)

    def filter_create_table(self):
        proxy = self.create_ez_table_model_proxy
        text = self.ui.createTemplateListSearchBar.text()
        self.filter_proxy(proxy, text)

    def filter_use_table(self):
        proxy = self.use_ez_table_model_proxy
        text = self.ui.useTemplateListSearchBar.text()
        self.filter_proxy(proxy, text)

    def filter_proxy(self, proxy_model: QSortFilterProxyModel, filter_text: str):
        proxy_model.invalidate()
        proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy_model.setFilterWildcard(f'*{filter_text}*')

    def filterCreateTree(self):
        self.createTreeSearchFilterModel.invalidate()
        self.createTreeSearchFilterModel.setFilterCaseSensitivity(
            Qt.CaseInsensitive)
        self.createTreeSearchFilterModel.setFilterWildcard(
            "*"+self.ui.createTemplateTreeSearchBar.text()+"*")


    def getLocation(self):
        remoteDirPath = self.hyperthoughtui.getUploadDirectory()
        self.folderuuid = ht_requests.get_ht_id_path_from_ht_path(
            self.hyperthoughtui.authcontrol, ht_path=remoteDirPath)
        self.ui.hyperthoughtLocationLineEdit.setText(remoteDirPath)
        self.toggleButtons()

    def handleRemoveCreate(self):
        proxy_selected_rows = reversed(self.ui.metadataTableView.selectionModel().selectedRows())
        source_row = -1
        for index in proxy_selected_rows:
            source_row = (index.model().mapToSource(index)).row()
            entry = self.create_ez_table_model.metadata_model.entry(source_row)
            # Remove Custom Entries from the mode or just mark FILE sources as disabled.
            if entry is not None and entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                self.create_ez_table_model.beginRemoveRows(QModelIndex(), source_row, source_row)
                self.create_ez_table_model.metadata_model.remove_by_index(source_row)
                self.create_ez_table_model.endRemoveRows()
            elif entry is not None and entry.source_type is EzMetadataEntry.SourceType.FILE:
                self.treeModel.changeLeafCheck(entry.source_path)
        
        index0 = self.create_ez_table_model.index(0, 0)
        index1 = self.create_ez_table_model.index(self.create_ez_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
        self.create_ez_table_model.dataChanged.emit(index0, index1)
        # This toggle is for macOS Catalina to actual visually show the updated checkboxes.
        self.ui.metadataTreeView.setVisible(False)
        self.ui.metadataTreeView.setVisible(True)
        self.ui.metadataTreeView.update()
        self.ui.metadataTableView.update()
        # End stupid macOS Catalina workaround.

    def handleRemoveUse(self, source):
        proxy_selected_rows = reversed(self.ui.useTemplateTableView.selectionModel().selectedRows())
        source_row = -1
        for index in proxy_selected_rows:
            source_row = (index.model().mapToSource(index)).row()
            entry = self.use_ez_table_model.metadata_model.entry(source_row)
            if entry is not None and entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                self.use_ez_table_model.beginRemoveRows(QModelIndex(), source_row, source_row)
                self.use_ez_table_model.metadata_model.remove_by_index(source_row)
                self.use_ez_table_model.endRemoveRows()
            elif entry is not None and entry.source_type is EzMetadataEntry.SourceType.FILE:
                entry.enabled = False
        
        index0 = self.use_ez_table_model.index(0, 0)
        index1 = self.use_ez_table_model.index(self.use_ez_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
        self.use_ez_table_model.dataChanged.emit(index0, index1)
        # This toggle is for macOS Catalina to actual visually show the updated checkboxes.
        self.ui.useTemplateTableView.setVisible(False)
        self.ui.useTemplateTableView.setVisible(True)
        self.ui.useTemplateTableView.update()
        # End stupid macOS Catalina workaround.


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
            self.use_ez_table_model = TableModelU(self, [])
            self.use_ez_table_model.templatelist = self.templatedata
            self.use_ez_table_model.templatesources = templatesources
            self.ui.hyperthoughtTemplateLineEdit.setText(linetext)
            self.ui.useTemplateTableView.setModel(self.use_ez_table_model)
            self.uselistmodel = ListModel(self, self.use_ez_table_model, fileType)
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

            # Setup the Create Template table
            self.setup_create_ez_table(metadata_model=metadata_model)

            # Setup the Create Template tree
            self.setup_create_ez_tree(metadata_model=metadata_model)

    def init_create_table_model_proxy(self, source_model: QEzTableModel) -> QCreateEzTableModel:
        proxy = QCreateEzTableModel(self)
        proxy.setSourceModel(source_model)
        proxy.setFilterKeyColumn(1)
        proxy.setDynamicSortFilter(True)
        return proxy
    
    def init_use_table_model_proxy(self, source_model: QEzTableModel) -> QUseEzTableModel:
        proxy = QUseEzTableModel(self)
        proxy.setSourceModel(source_model)
        proxy.setFilterKeyColumn(1)
        proxy.setDynamicSortFilter(True)
        return proxy   

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
                json.dump(self.use_ez_table_model.templatelist, outfile)
                outfile.write("\n")
                json.dump(self.use_ez_table_model.templatesources, outfile)
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
                json.dump(self.use_ez_table_model.templatelist, outfile)
                outfile.write("\n")
                json.dump(self.use_ez_table_model.templatesources, outfile)
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
            
            # Setup the Create Template table
            self.setup_create_ez_table(metadata_model=metadata_model)

            # Setup the Create Template tree
            self.setup_create_ez_tree(metadata_model=metadata_model)

        self.toggleButtons()
        return True

    def selectTemplate(self):
        startLocation = self.ui.hyperthoughtTemplateLineEdit.text()
        if startLocation == "":
            startLocation = QStandardPaths.writableLocation(
                QStandardPaths.HomeLocation)

        templateFilePath = QFileDialog.getOpenFileName(self, self.tr(
            "Select File"), startLocation, self.tr("Files (*.ez)"))[0]

        self.ui.hyperthoughtTemplateLineEdit.setText(templateFilePath)
        self.loadTemplateFile()

    def loadTemplateFile(self):
        templateFilePath = self.ui.hyperthoughtTemplateLineEdit.text()

        if templateFilePath == "":
            return False

        # Load the EzMetadataModel from the json file (Template file)
        metadata_model = EzMetadataModel.from_json_file(templateFilePath)
        self.setup_use_ez_table(metadata_model)
        self.currentTemplate = templateFilePath.split("/")[-1]
        self.ui.displayedFileLabel.setText(templateFilePath.split("/")[-1])
        self.updateUseTableModel()

    def loadOtherDataFile(self):
        datafile_input_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), self.tr("Files (*"+self.fileType+")"))[0]
        self.ui.otherDataFileLineEdit.setText(datafile_input_path)
        self.importMetadataFromDataFile()

    def importMetadataFromDataFile(self):
        filePath = self.ui.otherDataFileLineEdit.text()
        self.setWindowTitle(filePath)
        self.ui.dataTypeText.setText(filePath.split(".")[1].upper())
        if self.ui.addMetadataFileCheckBox.checkState() == Qt.Checked:
            self.uselistmodel.removeAllRows()
            self.uselistmodel.addRow(filePath)
            self.toggleButtons()
        self.updateUseTableModel()


    def updateUseTableModel(self):
        templateFilePath = self.ui.hyperthoughtTemplateLineEdit.text()
        filePath = self.ui.otherDataFileLineEdit.text()

        if filePath == "" or templateFilePath == "":
            return
        
        # Load the dictionary from the newly inserted datafile
        if self.ui.fileParserCombo.findText(filePath.split(".")[1].upper()+" Parser") != -1:
            headerDict = {}
            self.ui.fileParserCombo.setCurrentIndex(
                self.ui.fileParserCombo.findText(filePath.split(".")[1].upper()+" Parser"))
        if filePath.split(".")[1].upper() == "CTF":
            headerDict = ctf.parse_header_as_dict(filePath)
        elif filePath.split(".")[1].upper() == "ANG":
            headerDict = ang.parse_header_as_dict(filePath)
        elif filePath.split(".")[1].upper() == "XML":
            print("XML Parser used")

        self.use_ez_table_model.metadata_model.update_model_values_from_dict(headerDict)
        self.use_ez_table_model_proxy.metadata_file_chosen = True

        index0 = self.use_ez_table_model.index(0, 0)
        index1 = self.use_ez_table_model.index(self.use_ez_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
        self.use_ez_table_model.dataChanged.emit(index0, index1)

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
        auth_control = htauthcontroller.HTAuthorizationController(self.accessKey)

        metadataJson = ht_utilities.ezmodel_to_ht_metadata(self.use_ez_table_model.metadata_model)
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
