# This Python file uses the following encoding: utf-8

from ezmodel.ezmetadataentry import EzMetadataEntry
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QProgressDialog, QDialog
from PySide2.QtCore import QFile, QDir, Qt, QStandardPaths, QSortFilterProxyModel, Signal, QThread, QModelIndex, QEvent, QSettings
from PySide2.QtGui import QCursor, QDesktopServices
from generated.ui_mainwindow import Ui_MainWindow
from hyperthoughtdialogimpl import HyperthoughtDialogImpl
from aboutdialogimpl import AboutDialogImpl
from qeztablemodel import QEzTableModel
from uselistmodel import ListModel
from treemodel import TreeModel
from trashdelegate import TrashDelegate
from checkboxdelegate import CheckBoxDelegate
from qcreateeztablemodel import QCreateEzTableModel
from quseeztablemodel import QUseEzTableModel
from usefiledelegate import UseFileDelegate

from ht_requests.ht_requests import ht_utilities
from ht_requests.ht_requests import htauthcontroller
from ht_requests.ht_requests import ht_requests

from tqdm import tqdm
from uploader import Uploader
import os

import parsers.ctf as ctf
import parsers.ang as ang
import json
from typing import List
from datetime import datetime

from ezmodel.ezmetadatamodel import EzMetadataModel


class MainWindow(QMainWindow):
    K_CREATE_TREE_HEADER = "Available File Metadata"
    K_MODEL_JSON_FILE_NAME = '.model.json'
    K_MODEL_KEY_NAME = 'model'
    K_FILELIST_KEY_NAME = 'file_list'
    K_TEMPLATEFILE_KEY_NAME = 'template_file'
    K_FILETOEXTRACT_KEY_NAME = 'file_to_extract'
    K_MISSINGENTRIES_KEY_NAME = 'missing_entries'
    K_METADATAFILECHOSEN_KEY_NAME = 'metadata_file_chosen'

    createUpload = Signal(list, htauthcontroller.HTAuthorizationController, str, str, list)

    def __init__(self):
        super(MainWindow, self).__init__()
        self.hyperthoughtui = HyperthoughtDialogImpl()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.TabWidget.setCurrentWidget(self.ui.CreateTemplateTab)
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionAbout.triggered.connect(self.displayAbout)
        self.ui.actionOpenPackage.triggered.connect(self.openPackage)
        self.ui.actionSave_Package.triggered.connect(self.savePackage)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionSave_Template.triggered.connect(self.saveTemplate)
        self.ui.actionOpen_Template.triggered.connect(self.restoreTemplate)
        self.ui.dataFileSelect.clicked.connect(self.selectFile)
        self.ui.hyperthoughtTemplateSelect.clicked.connect(self.selectTemplate)
        self.ui.saveTemplateButton.clicked.connect(self.saveTemplate)
        self.ui.otherDataFileSelect.clicked.connect(self.loadOtherDataFile)
        self.ui.hyperthoughtUploadButton.clicked.connect(
            self.uploadToHyperthought)
        self.ui.clearCreateButton.clicked.connect(self.clearCreate)
        self.ui.clearUseButton.clicked.connect(self.clearUse)
        self.hyperthoughtui.currentTokenExpired.connect(lambda:  self.ui.hyperThoughtExpiresIn.setText(self.hyperthoughtui.K_EXPIRED_STR))
        self.setAcceptDrops(True)
        self.numCustoms = 0
        self.editableKeys = []

        # Read window settings
        self.read_window_settings()

        # Setup the blank Create Template table
        self.setup_create_ez_table()

        # Setup the blank Create Template tree
        self.setup_create_ez_tree()

        # Setup the blank Use Template table
        self.setup_use_ez_table()

        # Setup the blank Use Template file list
        self.setup_use_ez_list()

        self.ui.addUploadFilesBtn.clicked.connect(self.addUploadFiles)
        self.ui.clearUploadFilesBtn.clicked.connect(self.clearUploadFiles)
        self.ui.appendCreateTableRowButton.clicked.connect(
            self.addCustomRowToCreateTable)
        self.ui.removeCreateTableRowButton.clicked.connect(self.handleRemoveCreate)
        self.ui.removeUseTableRowButton.clicked.connect(self.handleRemoveUse)
        self.ui.appendUseTableRowButton.clicked.connect(self.addUseTableRow)
        self.ui.hyperthoughtLocationButton.clicked.connect(self.authenticateToHyperThought)
    
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
        self.ui.hyperthoughtTemplateLineEdit.installEventFilter(self)
        self.ui.otherDataFileLineEdit.installEventFilter(self)
        self.ui.dataFileLineEdit.installEventFilter(self)
    
    def setup_create_ez_table(self, metadata_model: EzMetadataModel = EzMetadataModel()):
        self.createtrashDelegate = TrashDelegate()
        self.checkboxDelegate = CheckBoxDelegate()
        self.create_ez_table_model = QEzTableModel(metadata_model=metadata_model, parent=self)
        self.create_ez_table_model_proxy = self.init_create_table_model_proxy(self.create_ez_table_model)
        self.ui.metadataTableView.setModel(self.create_ez_table_model_proxy)
        self.filter_create_table()
        self.ui.metadataTableView.setItemDelegateForColumn(self.create_ez_table_model.K_REMOVE_COL_INDEX, self.createtrashDelegate)
        self.createtrashDelegate.pressed.connect(self.handleRemoveCreate)
        self.ui.metadataTableView.setItemDelegateForColumn(self.create_ez_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.checkboxDelegate)
        self.ui.metadataTableView.setItemDelegateForColumn(self.create_ez_table_model.K_EDITABLE_COL_INDEX, self.checkboxDelegate)
        self.polish_create_ez_table()
    
    def polish_create_ez_table(self):
        self.ui.metadataTableView.resizeColumnsToContents()
        self.ui.metadataTableView.setColumnWidth(self.create_ez_table_model.K_HTANNOTATION_COL_INDEX, self.width() * .1)
        self.ui.metadataTableView.setColumnWidth(self.create_ez_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.width() * .125)
        self.ui.metadataTableView.horizontalHeader().setStretchLastSection(True)

    def setup_use_ez_table(self, metadata_model: EzMetadataModel = EzMetadataModel()):
        self.usetrashDelegate = TrashDelegate()
        self.use_ez_table_model = QEzTableModel(metadata_model, parent=self)
        self.use_ez_table_model_proxy = self.init_use_table_model_proxy(self.use_ez_table_model)
        self.ui.useTemplateTableView.setModel(self.use_ez_table_model_proxy)
        self.filter_use_table()
        self.ui.useTemplateTableView.setItemDelegateForColumn(self.use_ez_table_model_proxy.K_REMOVE_COL_INDEX, self.usetrashDelegate)
        self.usetrashDelegate.pressed.connect(self.handleRemoveUse)
        self.polish_use_ez_table()

    def polish_use_ez_table(self):
        self.ui.useTemplateTableView.resizeColumnsToContents()
        self.ui.useTemplateTableView.setColumnWidth(self.use_ez_table_model.K_HTANNOTATION_COL_INDEX, self.width() * .1)
        self.ui.useTemplateTableView.setColumnWidth(self.use_ez_table_model.K_HTUNITS_COL_INDEX, self.width() * .1)
        self.ui.useTemplateTableView.horizontalHeader().setStretchLastSection(True)

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

    def clearCreate(self):
        self.ui.dataFileLineEdit.setText("")
        self.ui.dataTypeText.setText("None Selected")
        self.ui.createTemplateListSearchBar.setText("")
        self.ui.createTemplateTreeSearchBar.setText("")
        self.setup_create_ez_table()
        self.setup_create_ez_tree()

    def clearUse(self):
        self.ui.hyperthoughtTemplateLineEdit.setText("")
        self.ui.otherDataFileLineEdit.setText("")
        self.ui.useTemplateListSearchBar.setText("")
        self.ui.displayedFileLabel.setText("No File Selected")
        self.ui.addMetadataFileCheckBox.setChecked(True)
        self.setup_use_ez_table()
        self.clearUploadFiles()

    def read_window_settings(self):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("window_state"))

    def acceptKey(self, apikey):
        self.accessKey = apikey

    def addCustomRowToCreateTable(self):
        self.create_ez_table_model.addCustomRow(self.numCustoms)
        self.numCustoms += 1

    def addUploadFiles(self):
        linetexts = QFileDialog.getOpenFileNames(self, self.tr("Select File"), QStandardPaths.displayName(
            QStandardPaths.HomeLocation), self.tr("Files (*.ctf *.xml *.ang)"))[0]
        for line in linetexts:
            self.uselistmodel.addRow(line)
        self.toggleButtons()

    def clearUploadFiles(self):
        self.uselistmodel.removeAllRows()

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
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())

        self.mThread.quit()
        self.mThread.wait(250)

        super().closeEvent(event)

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

    def displayAbout(self):
        aboutDialog = AboutDialogImpl(self)
        aboutDialog.exec()


    def getLocation(self):
        remoteDirPath = self.hyperthoughtui.getUploadDirectory()
        
        self.folderuuid = ht_requests.get_ht_id_path_from_ht_path(self.hyperthoughtui.authcontrol, 
                                                    ht_path=remoteDirPath, 
                                                    ht_space = 'project', ht_space_id=self.hyperthoughtui.current_project["content"]["pk"])
        self.ui.hyperThoughtUploadPath.setText(remoteDirPath)
        self.toggleButtons()

    def handleRemoveCreate(self, source_row = -1):
        if source_row != -1:
            entry = self.create_ez_table_model.metadata_model.entry(source_row)
            if entry is not None and entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                self.create_ez_table_model.beginRemoveRows(QModelIndex(), source_row, source_row)
                self.create_ez_table_model.metadata_model.remove_by_index(source_row)
                self.create_ez_table_model.endRemoveRows()
            elif entry is not None and entry.source_type is EzMetadataEntry.SourceType.FILE:
                self.treeModel.changeLeafCheck(entry.source_path)
        else:

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
        
        self.create_ez_table_model_proxy.invalidate()
        index0 = self.create_ez_table_model.index(0, 0)
        index1 = self.create_ez_table_model.index(self.create_ez_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
        self.create_ez_table_model_proxy.dataChanged.emit(index0, index1)


    def handleRemoveUse(self, source_row = -1):
        if source_row != -1:
            entry = self.use_ez_table_model.metadata_model.entry(source_row)
            if entry is not None and entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                self.use_ez_table_model.beginRemoveRows(QModelIndex(), source_row, source_row)
                self.use_ez_table_model.metadata_model.remove_by_index(source_row)
                self.use_ez_table_model.endRemoveRows()
            elif entry is not None and entry.source_type is EzMetadataEntry.SourceType.FILE:
                entry.enabled = False
        else:
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
        
        self.use_ez_table_model_proxy.invalidate()
        index0 = self.use_ez_table_model_proxy.index(0, 0)
        index1 = self.use_ez_table_model_proxy.index(self.use_ez_table_model_proxy.rowCount() - 1, self.use_ez_table_model_proxy.K_COL_COUNT)
        self.use_ez_table_model_proxy.dataChanged.emit(index0, index1)
        # This toggle is for macOS Catalina to actual visually show the updated checkboxes.
        self.ui.useTemplateTableView.setVisible(False)
        self.ui.useTemplateTableView.setVisible(True)
        self.ui.useTemplateTableView.update()
        # End stupid macOS Catalina workaround.


    def help(self):
        QDesktopServices.openUrl("http://www.bluequartz.net/")

    def openPackage(self):
        pkgpath = QFileDialog.getExistingDirectory(self, caption=self.tr("Select MetaForge Package"), dir=QStandardPaths.displayName(
            QStandardPaths.HomeLocation))
        if pkgpath != "":
            # Load model
            model_input_path = os.path.join(pkgpath, self.K_MODEL_JSON_FILE_NAME)

            with open(model_input_path, 'r') as infile:
                model_dict = json.load(infile)

                self.use_ez_table_model.metadata_model = EzMetadataModel.from_json_dict(model_dict[self.K_MODEL_KEY_NAME])

                # Load file list
                upload_file_paths = model_dict[self.K_FILELIST_KEY_NAME]
                for file_path in upload_file_paths:
                    self.uselistmodel.metadataList.append(file_path)
                
                index0 = self.uselistmodel.index(0, 0)
                index1 = self.uselistmodel.index(len(self.uselistmodel.metadataList) - 1, 0)
                self.uselistmodel.dataChanged.emit(index0, index1)

                # Load template file
                template_file_path = model_dict[self.K_TEMPLATEFILE_KEY_NAME]
                self.ui.hyperthoughtTemplateLineEdit.setText(template_file_path)

                # Load file to extract metadata from
                extraction_file_path = model_dict[self.K_FILETOEXTRACT_KEY_NAME]
                self.ui.otherDataFileLineEdit.setText(extraction_file_path)
            
                # Load missing entries and metadata_file_chosen boolean
                missing_entry_srcs = model_dict[self.K_MISSINGENTRIES_KEY_NAME]
                metadata_model = self.use_ez_table_model.metadata_model
                missing_entries = []
                for missing_entry_src in missing_entry_srcs:
                    metadata_entry = metadata_model.entry_by_source(missing_entry_src)
                    missing_entries.append(metadata_entry)
                self.use_ez_table_model_proxy.missing_entries = missing_entries
                self.use_ez_table_model_proxy.metadata_file_chosen = model_dict[self.K_METADATAFILECHOSEN_KEY_NAME]

            self.use_ez_table_model_proxy.invalidate()
            self.ui.menuOpen_Recent.addAction(pkgpath)

    def saveTemplate(self):
        dialog = QFileDialog(self, "Save File", "", "Templates (*.ez)")
        dialog.setDefaultSuffix(".ez")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        fileName = ""
        if dialog.exec():
            fileName = dialog.selectedFiles()[0]
        if fileName != "":
            self._saveTemplate(fileName)
    
    def _saveTemplate(self, file_path: str):
        with open(file_path, 'w') as outfile:
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

    def savePackage(self):
        result = QFileDialog.getSaveFileName(self, "Save File",
                                               "/Packages/",
                                               "Packages (*.ezp)")
        pkgpath = result[0]
        if pkgpath != "":
            # Create package
            myDir = QDir()
            myDir.mkpath(pkgpath)

            # Copy file list to package
            newfilepaths = []
            for filepath in self.uselistmodel.metadataList:
                filename = filepath.split("/")[-1]
                newfilepath = os.path.join(pkgpath, filename)
                newfilepaths.append(newfilepath)
                QFile.copy(filepath, newfilepath)
            
            # Copy template file to package
            template_file_path = self.ui.hyperthoughtTemplateLineEdit.text()
            new_template_file_path = ""
            if template_file_path != "":
                template_file_name = template_file_path.split("/")[-1]
                new_template_file_path = os.path.join(pkgpath, template_file_name)
                QFile.copy(template_file_path, new_template_file_path)

            # Copy "file to extract metadata from" to package
            extraction_file_path = self.ui.otherDataFileLineEdit.text()
            new_extraction_file_path = ""
            if extraction_file_path != "":
                extraction_file_name = extraction_file_path.split("/")[-1]
                new_extraction_file_path = os.path.join(pkgpath, extraction_file_name)
                QFile.copy(extraction_file_path, new_extraction_file_path)

            # Save model, file list, template file, file_to_extract,
            # metadata_file_chosen, and missing_entries to json file
            model_dict = {}
            model_dict[self.K_MODEL_KEY_NAME] = self.use_ez_table_model.metadata_model.to_json_dict()

            model_dict[self.K_FILELIST_KEY_NAME] = newfilepaths
            model_dict[self.K_TEMPLATEFILE_KEY_NAME] = new_template_file_path
            model_dict[self.K_FILETOEXTRACT_KEY_NAME] = new_extraction_file_path
            model_dict[self.K_METADATAFILECHOSEN_KEY_NAME] = self.use_ez_table_model_proxy.metadata_file_chosen
            missing_entries = []
            for missing_entry in self.use_ez_table_model_proxy.missing_entries:
                missing_entries.append(missing_entry.source_path)
            model_dict[self.K_MISSINGENTRIES_KEY_NAME] = missing_entries
            paths_output_path = os.path.join(pkgpath, self.K_MODEL_JSON_FILE_NAME)
            with open(paths_output_path, 'w') as outfile:
                json.dump(model_dict, outfile, indent=4)

    def selectFile(self, fileLink=None):
        if fileLink == False:
            filePath = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), self.tr("Files (*.*)"))[0]
        else:
            filePath = fileLink
        if filePath != "":
            self.setWindowTitle(filePath)
            self.ui.dataFileLineEdit.setText(filePath)

            split = os.path.splitext(filePath)
            ext = split[1].replace('.', '')

            self.ui.dataTypeText.setText(ext.upper())
            if self.ui.fileParserCombo.findText(f'{ext.upper()} Parser') != -1:
                self.ui.fileParserCombo.setCurrentIndex(
                    self.ui.fileParserCombo.findText(f'{ext.upper()} Parser'))
            headerDict = {}
            if ext.upper() == "CTF":
                headerDict = ctf.parse_header_as_dict(filePath)
            elif ext.upper() == "ANG":
                headerDict = ang.parse_header_as_dict(filePath)
            # elif ext.upper() == "XML":
            #     print("XML Parser used")
            else:
                raise RuntimeError('No parser available for selected file.')

            metadata_model = EzMetadataModel.create_model(headerDict,
                                                          filePath,
                                                          source_type=EzMetadataEntry.SourceType.FILE)
            
            # Setup the Create Template table
            self.setup_create_ez_table(metadata_model=metadata_model)

            # Setup the Create Template tree
            self.setup_create_ez_tree(metadata_model=metadata_model)

            self.ui.metadataTableView.setWordWrap(True)
            # self.ui.metadataTableView.setColumnWidth(1, 200)
            self.ui.metadataTableView.setRowHeight(21, 35)
            self.polish_create_ez_table()

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
        self.updateUseTableModel()
        self.polish_use_ez_table()

    def loadOtherDataFile(self):
        datafile_input_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), self.tr("Files (*"+self.fileType+")"))[0]
        if datafile_input_path != "":
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
            self.use_ez_table_model_proxy.metadata_file_chosen = False
            index0 = self.use_ez_table_model.index(0, 0)
            index1 = self.use_ez_table_model.index(self.use_ez_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
            self.use_ez_table_model.dataChanged.emit(index0, index1)
            return
        
        # Load the dictionary from the newly inserted datafile
        split = os.path.splitext(filePath)
        ext = split[1].replace('.', '')
        if self.ui.fileParserCombo.findText(f'{ext.upper()} Parser') != -1:
            self.ui.fileParserCombo.setCurrentIndex(
                self.ui.fileParserCombo.findText(f'{ext.upper()} Parser'))
        headerDict = {}
        if ext.upper() == "CTF":
            headerDict = ctf.parse_header_as_dict(filePath)
        elif ext.upper() == "ANG":
            headerDict = ang.parse_header_as_dict(filePath)
        # elif ext.upper() == "XML":
        #     print("XML Parser used")
        else:
            raise RuntimeError('No parser available for selected file.')

        self.use_ez_table_model_proxy.missing_entries = self.use_ez_table_model.metadata_model.update_model_values_from_dict(headerDict)
        self.use_ez_table_model_proxy.metadata_file_chosen = True

        index0 = self.use_ez_table_model_proxy.index(0, 0)
        index1 = self.use_ez_table_model_proxy.index(self.use_ez_table_model_proxy.rowCount() - 1, QUseEzTableModel.K_COL_COUNT)
        self.use_ez_table_model_proxy.dataChanged.emit(index0, index1)

    def toggleButtons(self):
        if (self.ui.hyperthoughtTemplateLineEdit.text() != "" and
            self.ui.useTemplateListView.model().rowCount() > 0 and
                self.ui.hyperThoughtUploadPath.text() != ""):

            self.ui.hyperthoughtUploadButton.setEnabled(True)

    def uploadToHyperthought(self):
        auth_control = htauthcontroller.HTAuthorizationController(self.accessKey)

        metadataJson = ht_utilities.ezmodel_to_ht_metadata(self.use_ez_table_model.metadata_model,
                                                           self.use_ez_table_model_proxy.missing_entries,
                                                           self.use_ez_table_model_proxy.metadata_file_chosen)
        progress = QProgressDialog("Uploading files...", "Abort Upload", 0, len(
            self.uselistmodel.metadataList), self)

        progress.setWindowFlags(
            Qt.Window | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        progress.setAttribute(Qt.WA_DeleteOnClose)
        self.createUpload.emit(self.uselistmodel.metadataList, 
                    auth_control, 
                    self.hyperthoughtui.current_project["content"]["pk"],
                    self.folderuuid, 
                    metadataJson)
        self.uploader.currentUploadDone.connect(progress.setValue)
        self.uploader.currentlyUploading.connect(progress.setLabelText)
        self.uploader.allUploadsDone.connect(progress.accept)
        progress.canceled.connect(lambda: self.uploader.interruptUpload())
        progress.setFixedSize(500, 100)
        progress.exec()

    def authenticateToHyperThought(self):
        ret = self.hyperthoughtui.exec()
        if ret == int(QDialog.Accepted):
            self.getLocation()
            htUrl = self.hyperthoughtui.ui.ht_server_url.text()
            if htUrl == "":
                self.ui.hyperThoughtServer.setText("https://hyperthought.url")
            else:
                self.ui.hyperThoughtServer.setText(htUrl)
                self.ui.hyperThoughtProject.setText(self.hyperthoughtui.current_project["content"]["title"])
                self.ui.hyperThoughtUploadPath.setText(self.hyperthoughtui.getUploadDirectory())
        
        if self.hyperthoughtui.authcontrol is not None:
            datetime_obj = datetime.strptime(self.hyperthoughtui.authcontrol.expires_at, '%Y-%m-%dT%X%z')
            expires_at = datetime_obj.strftime("%m/%d/%Y %I:%M:%S %p")
            self.ui.hyperThoughtExpiresIn.setText(expires_at)

