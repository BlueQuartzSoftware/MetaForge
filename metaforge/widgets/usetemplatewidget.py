# This Python file uses the following encoding: utf-8
import shutil
from typing import List
import json
from pathlib import Path
import hyperthought as ht
from uuid import UUID

from PySide2.QtWidgets import QMainWindow, QFileDialog, QDialog, QWidget, QStackedWidget, QListView, QLineEdit
from PySide2.QtCore import QFile, Qt, QStandardPaths, QSortFilterProxyModel, Signal, QThread, QModelIndex, QEvent, QSize
from PySide2.QtGui import QCursor, QIcon
import PySide2.QtCore

from metaforge.parsers.metaforgeparser import MetaForgeParser
from metaforge.ht_helpers.ht_uploader import HyperThoughtUploader
from metaforge.models.metadatamodel import MetadataModel, load_template
from metaforge.widgets.hyperthoughtdialogimpl import HyperthoughtDialogImpl
from metaforge.qt_models.qeztablemodel import QEzTableModel
from metaforge.models.uselistmodel import ListModel
from metaforge.delegates.trashdelegate import TrashDelegate
from metaforge.qt_models.quseeztablemodel import QUseEzTableModel
from metaforge.delegates.usefiledelegate import UseFileDelegate
from metaforge.common.metaforgestyledatahelper import MetaForgeStyleDataHelper
from metaforge.models.parsermodel import ParserModel
from metaforge.widgets.utilities.widget_utilities import notify_error_message, notify_no_errors
from metaforge.utilities.ht_utilities import ezmodel_to_ht_metadata

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from metaforge.widgets.generated_5_12.ui_usetemplatewidget import Ui_UseTemplateWidget
elif qt_version[1] == 15:
    from metaforge.widgets.generated_5_15.ui_usetemplatewidget import Ui_UseTemplateWidget


class UseTemplateWidget(QWidget):
    K_MODEL_JSON_FILE_NAME = '.model.json'
    K_MODEL_KEY_NAME = 'model'
    K_FILELIST_KEY_NAME = 'file_list'
    K_TEMPLATEFILE_KEY_NAME = 'template_file'
    K_FILETOEXTRACT_KEY_NAME = 'file_to_extract'
    K_MISSINGENTRIES_KEY_NAME = 'missing_entries'
    K_METADATAFILECHOSEN_KEY_NAME = 'metadata_file_chosen'
    K_NO_ERRORS = "No errors."
    K_OTHER_DATA_FILE_PLACEHOLDER_REPLACE_SYMBOL = "@EXTENSION_LIST@"
    K_OTHER_DATA_FILE_PLACEHOLDER = f"Drag a file ({K_OTHER_DATA_FILE_PLACEHOLDER_REPLACE_SYMBOL}) here or select one using the 'Select' button to the right ===>"

    createUpload = Signal(list, ht.auth.Authorization, str, str, list)
    
    def __init__(self, parent):
        super(UseTemplateWidget, self).__init__(parent)
        
        self.style_sheet_helper: MetaForgeStyleDataHelper = MetaForgeStyleDataHelper(self)
        self.ui = Ui_UseTemplateWidget()
        self.ui.setupUi(self)
        self.parsers_model: ParserModel = None
        self.template_specified_parser_uuid: UUID = None
        self.hyperthoughtui = HyperthoughtDialogImpl()
        self.ui.hyperthoughtTemplateSelect.clicked.connect(self.select_template)
        self.ui.otherDataFileSelect.clicked.connect(self.load_other_data_file)
        self.ui.hyperthoughtUploadButton.clicked.connect(self.upload_to_hyperthought)
        self.ui.clearUseButton.clicked.connect(self.clear)
        self.setAcceptDrops(True)

        notify_no_errors(self.ui.error_label)

        # Setup the icons
        self.setup_icons()

        # Setup the blank Use Template table
        self.setup_metadata_table()

        # Setup the blank Use Template file list
        self.setup_file_upload_list()

        self.ui.addUploadFilesBtn.clicked.connect(self.add_upload_files)
        self.ui.clearUploadFilesBtn.clicked.connect(self.clear_upload_files)
        self.ui.removeUseTableRowButton.clicked.connect(self.remove_model_entry)
        self.ui.appendUseTableRowButton.clicked.connect(self.add_metadata_table_row)
        self.ui.hyperthoughtLocationButton.clicked.connect(self.authenticate_to_hyperthought)
    
        self.ui.useTemplateListSearchBar.textChanged.connect(self.filter_metadata_table)
        self.ui.addMetadataFileCheckBox.stateChanged.connect(self.check_file_list)

        self.fileType = ""
        self.folderuuid = ""
        self.uploader = HyperThoughtUploader()
        self.mThread = QThread()
        self.uploader.moveToThread(self.mThread)
        self.mThread.start()

        self.createUpload.connect(self.uploader.performUpload)
        self.ui.hyperthoughtTemplateLineEdit.installEventFilter(self)
        self.ui.otherDataFileLineEdit.installEventFilter(self)
    
    def setup_icons(self):
        icon = QIcon()
        icon.addFile(u":/resources/Images/trash_can.png", QSize(), QIcon.Normal, QIcon.Off)
        # icon.addFile(u":/resources/Images/trash_can@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui.clearUploadFilesBtn.setIcon(icon)
        self.ui.removeUseTableRowButton.setIcon(icon)

    def setup_metadata_table(self, metadata_model: MetadataModel = MetadataModel()):
        self.usetrashDelegate = TrashDelegate(stylehelper=self.style_sheet_helper)
        self.use_ez_table_model = QEzTableModel(metadata_model, parent=self)
        self.use_ez_table_model_proxy = self.init_table_model_proxy(self.use_ez_table_model)
        self.ui.useTemplateTableView.setModel(self.use_ez_table_model_proxy)
        self.filter_metadata_table()
        self.ui.useTemplateTableView.setItemDelegateForColumn(self.use_ez_table_model_proxy.K_REMOVE_COL_INDEX, self.usetrashDelegate)
        self.usetrashDelegate.pressed.connect(self.remove_model_entry)
        self.polish_metadata_table()

    def polish_metadata_table(self):
        self.ui.useTemplateTableView.resizeColumnsToContents()
        self.ui.useTemplateTableView.setColumnWidth(self.use_ez_table_model.K_HTANNOTATION_COL_INDEX, self.width() * .1)
        self.ui.useTemplateTableView.setColumnWidth(self.use_ez_table_model.K_HTUNITS_COL_INDEX, self.width() * .1)
        self.ui.useTemplateTableView.horizontalHeader().setStretchLastSection(True)
    
    def setup_file_upload_list(self, file_list: list = []):
        self.uselistmodel = ListModel(file_list, self)
        self.ui.useTemplateListView.setModel(self.uselistmodel)
        self.uselistmodel.rowRemoved.connect(self.toggle_buttons)
        self.uselistmodel.rowAdded.connect(self.toggle_buttons)

        self.useFileDelegate = UseFileDelegate(self, stylehelper=self.style_sheet_helper)
        self.ui.useTemplateListView.setItemDelegate(self.useFileDelegate)

        self.ui.useTemplateListView.clicked.connect(
            self.removeRowfromUsefileType)
    
    def closeEvent(self, event):
        self.mThread.quit()
        self.mThread.wait(250)

        super().closeEvent(event)

    def clear(self):
        self.ui.hyperthoughtTemplateLineEdit.setText("")
        self.ui.otherDataFileLineEdit.setText("")
        self.ui.useTemplateListSearchBar.setText("")
        self.ui.addMetadataFileCheckBox.setChecked(True)
        self.setup_metadata_table()
        self.clear_upload_files()
        self.template_specified_parser_uuid = None
        self.ui.otherDataFileLineEdit.setPlaceholderText("")
        notify_no_errors(self.ui.error_label)

    def add_upload_files(self):
        linetexts = self._getOpenFilesAndDirs(self, self.tr("Select File"), QStandardPaths.displayName(
            QStandardPaths.HomeLocation), self.tr("Files (*.ctf *.xml *.ang *.tif *.tiff *.ini);;All Files (*.*)"))
        for line in linetexts:
            self.uselistmodel.addRow(Path(line))
        self.toggle_buttons()
    
    def _getOpenFilesAndDirs(self, parent=None, caption='', directory='', filter='', initialFilter='', options=None):
        def updateText():
            # update the contents of the line edit widget with the selected files
            selected = []
            for index in view.selectionModel().selectedRows():
                selected.append('"{}"'.format(index.data()))
            lineEdit.setText(' '.join(selected))

        dialog = QFileDialog(parent, windowTitle=caption)
        dialog.setFileMode(dialog.ExistingFiles)
        if options:
            dialog.setOptions(options)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        if directory:
            dialog.setDirectory(directory)
        if filter:
            dialog.setNameFilter(filter)
            if initialFilter:
                dialog.selectNameFilter(initialFilter)

        # by default, if a directory is opened in file listing mode, 
        # QFileDialog.accept() shows the contents of that directory, but we 
        # need to be able to "open" directories as we can do with files, so we 
        # just override accept() with the default QDialog implementation which 
        # will just return exec_()
        dialog.accept = lambda: QDialog.accept(dialog)

        stackedWidget = dialog.findChild(QStackedWidget)
        view = stackedWidget.findChild(QListView)
        view.selectionModel().selectionChanged.connect(updateText)

        lineEdit = dialog.findChild(QLineEdit)
        # clear the line edit contents whenever the current directory changes
        dialog.directoryEntered.connect(lambda: lineEdit.setText(''))

        dialog.exec_()
        return dialog.selectedFiles()

    def clear_upload_files(self):
        self.uselistmodel.removeAllRows()

    def add_metadata_table_row(self):
        self.use_ez_table_model.addCustomRow(1)

    def check_file_list(self, checked):
        if checked == Qt.Checked:
          if self.ui.otherDataFileLineEdit.text() != "":
              self.uselistmodel.addRow(Path(self.ui.otherDataFileLineEdit.text()))
        elif checked == Qt.Unchecked:
            path = Path(self.ui.otherDataFileLineEdit.text())
            if path in self.uselistmodel.metadataList:
                rowIndex = self.uselistmodel.metadataList.index(path)
                self.uselistmodel.removeRow(rowIndex)

    def eventFilter(self, object, event):
        if object == self.ui.hyperthoughtTemplateLineEdit:
            if event.type() == QEvent.DragEnter:
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                if str(event.mimeData().urls()[0])[-5:-2] == ".ez":
                    event.acceptProposedAction()
                    self.ui.hyperthoughtTemplateLineEdit.setText(event.mimeData().urls()[0].toLocalFile())
                    self.load_template_file()
        if object == self.ui.otherDataFileLineEdit:
            if event.type() == QEvent.DragEnter:
                file_path = Path(event.mimeData().urls()[0].toLocalFile())
                if self.template_specified_parser:
                    if file_path.suffix in self.template_specified_parser.supported_file_extensions():
                        event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                file_path = Path(event.mimeData().urls()[0].toLocalFile())
                if self.template_specified_parser:
                    if file_path.suffix in self.template_specified_parser.supported_file_extensions():
                        event.acceptProposedAction()
                        self.ui.otherDataFileLineEdit.setText(str(file_path))
                        self.import_metadata_from_data_file()

        return QMainWindow.eventFilter(self, object,  event)

    def filter_metadata_table(self):
        proxy = self.use_ez_table_model_proxy
        text = self.ui.useTemplateListSearchBar.text()
        self.filter_proxy(proxy, text)

    def filter_proxy(self, proxy_model: QSortFilterProxyModel, filter_text: str):
        proxy_model.invalidate()
        proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy_model.setFilterWildcard(f'*{filter_text}*')

    def remove_model_entry(self, source_index = QModelIndex()):
        if source_index.isValid():
            entry = self.use_ez_table_model.metadata_model.entry(source_index.row())
            if entry is not None:
                self.use_ez_table_model.beginRemoveRows(QModelIndex(), source_index.row(), source_index.row())
                self.use_ez_table_model.metadata_model.remove_by_index(source_index.row())
                self.use_ez_table_model.endRemoveRows()
        else:
            proxy_selected_rows = reversed(self.ui.useTemplateTableView.selectionModel().selectedRows())
            for index in proxy_selected_rows:
                source_row = (index.model().mapToSource(index)).row()
                entry = self.use_ez_table_model.metadata_model.entry(source_row)
                if entry is not None:
                    self.use_ez_table_model.beginRemoveRows(QModelIndex(), source_row, source_row)
                    self.use_ez_table_model.metadata_model.remove_by_index(source_row)
                    self.use_ez_table_model.endRemoveRows()
        
        self.use_ez_table_model_proxy.invalidate()
        index0 = self.use_ez_table_model_proxy.index(0, 0)
        index1 = self.use_ez_table_model_proxy.index(self.use_ez_table_model_proxy.rowCount() - 1, self.use_ez_table_model_proxy.K_COL_COUNT)
        self.use_ez_table_model_proxy.dataChanged.emit(index0, index1)
        # This toggle is for macOS Catalina to actual visually show the updated checkboxes.
        self.ui.useTemplateTableView.setVisible(False)
        self.ui.useTemplateTableView.setVisible(True)
        self.ui.useTemplateTableView.update()
        # End stupid macOS Catalina workaround.

    def open_package(self, pkgpath: Path):
        # Load model
        model_input_path = pkgpath / self.K_MODEL_JSON_FILE_NAME

        with model_input_path.open('r') as infile:
            model_dict = json.load(infile)

            metadata_model = MetadataModel.from_dict(model_dict[self.K_MODEL_KEY_NAME])
            self.setup_metadata_table(metadata_model=metadata_model)

            # Load file list
            upload_file_paths = model_dict[self.K_FILELIST_KEY_NAME]
            for file_path in upload_file_paths:
                self.uselistmodel.metadataList.append(Path(file_path))
            
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
    
    def init_table_model_proxy(self, source_model: QEzTableModel) -> QUseEzTableModel:
        proxy = QUseEzTableModel(self)
        proxy.setSourceModel(source_model)
        proxy.setFilterKeyColumn(1)
        proxy.setDynamicSortFilter(True)
        return proxy

    def removeRowfromUsefileType(self, index):
        if self.ui.useTemplateListView.width() - 64 < self.ui.useTemplateListView.mapFromGlobal(QCursor.pos()).x():
            # this is where to remove the row
            self.uselistmodel.removeRow(index.row())

    def save_package(self, pkgpath: Path):
        # Create package
        if pkgpath.exists():
            shutil.rmtree(str(pkgpath))
            
        pkgpath.mkdir(parents=True)

        # Copy file list to package
        newfilepaths: List[str] = []
        for filepath in self.uselistmodel.metadataList:
            filename = filepath.name
            newfilepath = pkgpath / filename
            newfilepaths.append(str(newfilepath))
            QFile.copy(str(filepath), str(newfilepath))
        
        # Copy template file to package
        template_file_path = self.ui.hyperthoughtTemplateLineEdit.text()
        if template_file_path != "":
            template_file_path = Path(template_file_path)
            template_file_name = template_file_path.name
            new_template_file_path = pkgpath / template_file_name
            QFile.copy(str(template_file_path), str(new_template_file_path))

        # Copy "file to extract metadata from" to package
        extraction_file_path = self.ui.otherDataFileLineEdit.text()
        if extraction_file_path != "":
            extraction_file_path = Path(extraction_file_path)
            extraction_file_name = extraction_file_path.name
            new_extraction_file_path = pkgpath / extraction_file_name
            QFile.copy(str(extraction_file_path), str(new_extraction_file_path))

        # Save model, file list, template file, file_to_extract,
        # metadata_file_chosen, and missing_entries to json file
        model_dict = {}
        model_dict[self.K_MODEL_KEY_NAME] = self.use_ez_table_model.metadata_model.to_dict()

        model_dict[self.K_FILELIST_KEY_NAME] = newfilepaths
        model_dict[self.K_TEMPLATEFILE_KEY_NAME] = str(new_template_file_path)
        model_dict[self.K_FILETOEXTRACT_KEY_NAME] = str(new_extraction_file_path)
        model_dict[self.K_METADATAFILECHOSEN_KEY_NAME] = self.use_ez_table_model_proxy.metadata_file_chosen
        missing_entries: List[str] = []
        for missing_entry in self.use_ez_table_model_proxy.missing_entries:
            missing_entries.append(missing_entry.source_path)
        model_dict[self.K_MISSINGENTRIES_KEY_NAME] = missing_entries
        paths_output_path = pkgpath / self.K_MODEL_JSON_FILE_NAME
        with paths_output_path.open('w') as outfile:
            json.dump(model_dict, outfile, indent=4)

    def select_template(self):
        startLocation = self.ui.hyperthoughtTemplateLineEdit.text()
        if startLocation == "":
            startLocation = QStandardPaths.writableLocation(
                QStandardPaths.HomeLocation)

        templateFilePath = QFileDialog.getOpenFileName(self, self.tr(
            "Select File"), startLocation, self.tr("Files (*.ez)"))[0]

        self.ui.hyperthoughtTemplateLineEdit.setText(templateFilePath)
        self.load_template_file()

    def load_template_file(self):
        templateFilePath = self.ui.hyperthoughtTemplateLineEdit.text()

        if templateFilePath == "":
            return False

        # Load the MetadataModel from the json file (Template file)
        data_file_path, self.template_specified_parser_uuid, metadata_model, err_msg = load_template(Path(templateFilePath))

        if err_msg is not None:
            self._notify_error_message(err_msg)
            return
        
        self.template_specified_parser, err_msg = self.parsers_model.find_parser_from_uuid(self.template_specified_parser_uuid)
        if err_msg is not None:
            self._notify_error_message(err_msg)
            return
        
        placeholder_text = self.K_OTHER_DATA_FILE_PLACEHOLDER
        placeholder_text = placeholder_text.replace(self.K_OTHER_DATA_FILE_PLACEHOLDER_REPLACE_SYMBOL, ', '.join(self.template_specified_parser.supported_file_extensions()))
        self.ui.otherDataFileLineEdit.setPlaceholderText(placeholder_text)
        
        self.setup_metadata_table(metadata_model)
        self.update_metadata_table_model()
        self.polish_metadata_table()

    def load_other_data_file(self):
        file_filter = "All Files(*.*)"
        if self.template_specified_parser:
            file_filter = f"Data Files ({'*' + ' *'.join(self.template_specified_parser.supported_file_extensions())});;" + file_filter

        datafile_input_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), file_filter)[0]
        if datafile_input_path != "":
            self.ui.otherDataFileLineEdit.setText(datafile_input_path)
            self.import_metadata_from_data_file()

    def import_metadata_from_data_file(self):
        if not self.update_metadata_table_model():
            return
        
        filePath = Path(self.ui.otherDataFileLineEdit.text())
        self.setWindowTitle(str(filePath))

        if self.ui.addMetadataFileCheckBox.checkState() == Qt.Checked:
            self.uselistmodel.removeAllRows()
            self.uselistmodel.addRow(filePath)
            self.toggle_buttons()


    def update_metadata_table_model(self) -> bool:
        templateFilePath = self.ui.hyperthoughtTemplateLineEdit.text()
        file_path = self.ui.otherDataFileLineEdit.text()

        if file_path == "" or templateFilePath == "":
            self.use_ez_table_model_proxy.metadata_file_chosen = False
            index0 = self.use_ez_table_model.index(0, 0)
            index1 = self.use_ez_table_model.index(self.use_ez_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
            self.use_ez_table_model.dataChanged.emit(index0, index1)
            return True
        
        self.template_specified_parser, err_msg = self.parsers_model.find_parser_from_uuid(self.template_specified_parser_uuid)
        if err_msg is not None:
            self._notify_error_message(err_msg)
            return False

        if Path(file_path).suffix not in self.template_specified_parser.supported_file_extensions():
            self._notify_error_message(f"Unable to parse data file - Data file '{Path(file_path).name}' is not compatible with the parser used by the template!  The supported file extensions are: {self.template_specified_parser.supported_file_extensions()}")
            return False
        
        file_path = Path(file_path)
        templateFilePath = Path(templateFilePath)
        
        # Load the dictionary from the newly inserted datafile
        metadata_list = self.template_specified_parser.parse_header(file_path)

        self.use_ez_table_model_proxy.missing_entries = self.use_ez_table_model.metadata_model.update_model_values(metadata_list)
        self.use_ez_table_model_proxy.metadata_file_chosen = True

        index0 = self.use_ez_table_model_proxy.index(0, 0)
        index1 = self.use_ez_table_model_proxy.index(self.use_ez_table_model_proxy.rowCount() - 1, QUseEzTableModel.K_COL_COUNT)
        self.use_ez_table_model_proxy.dataChanged.emit(index0, index1)

        notify_no_errors(self.ui.error_label)
        return True

    def toggle_buttons(self):
        if (self.ui.hyperthoughtTemplateLineEdit.text() != "" and
            self.ui.useTemplateListView.model().rowCount() > 0 and
                self.ui.hyperThoughtUploadPath.text() != ""):

            self.ui.hyperthoughtUploadButton.setEnabled(True)

    def upload_to_hyperthought(self):
        original_btn_text = self.ui.hyperthoughtUploadButton.text()
        metadataJson = ezmodel_to_ht_metadata(self.use_ez_table_model.metadata_model,
                                                           self.use_ez_table_model_proxy.missing_entries,
                                                           self.use_ez_table_model_proxy.metadata_file_chosen)
        auth_control = self.hyperthoughtui.get_auth_control()
        ht_upload_path = ','
        if self.chosen_ht_folder is not None:
            ht_upload_path = self.chosen_ht_folder['path'] + self.chosen_ht_folder['pk'] + ','
        self.createUpload.emit(self.uselistmodel.metadataList, 
                    auth_control, 
                    self.chosen_ht_workspace["id"],
                    ht_upload_path,
                    metadataJson)
        self.uploader.notify_file_progress_text.connect(self._update_file_progress_label)
        self.uploader.notify_file_progress.connect(self._update_file_progress)
        self.uploader.notify_list_progress_text.connect(self._update_list_progress_label)
        self.uploader.notify_list_progress.connect(self._update_list_progress)
        self.ui.hyperthoughtUploadButton.pressed.connect(self.uploader.interruptUpload)
        self.uploader.all_uploads_done.connect(lambda: self.ui.hyperthoughtUploadButton.setText(original_btn_text))
        self.ui.hyperthoughtUploadButton.setText('Cancel Upload')
    
    def _update_file_progress(self, progress: int):
        self.ui.file_progress_bar.setValue(progress)
        self.ui.file_progress_bar_label.setText(f"{progress}%")

    def _update_file_progress_label(self, progress_text: str):
        self.ui.file_progress_label.setText(progress_text)
    
    def _update_list_progress(self, progress: int):
        self.ui.list_progress_bar.setValue(progress)
        self.ui.list_progress_bar_label.setText(f"{progress}%")
    
    def _update_list_progress_label(self, progress_text: str):
        self.ui.list_progress_label.setText(progress_text)

    def authenticate_to_hyperthought(self):
        ret = self.hyperthoughtui.exec()
        if ret == int(QDialog.Accepted):
            self.chosen_ht_workspace = self.hyperthoughtui.get_workspace()
            self.chosen_ht_folder = self.hyperthoughtui.get_chosen_folder()
            if self.chosen_ht_folder is None:
                self.ui.hyperThoughtUploadPath.setText('/')
            else:
                self.ui.hyperThoughtUploadPath.setText(self.chosen_ht_folder['path_string'])
            self.toggle_buttons()

            htUrl = self.hyperthoughtui.ui.ht_server_url.text()
            if htUrl == "":
                self.ui.hyperThoughtServer.setText("https://hyperthought.url")
            else:
                self.ui.hyperThoughtServer.setText(htUrl)
                self.ui.hyperThoughtProject.setText(self.chosen_ht_workspace["name"])
    
    def set_parsers_model(self, parsers_model: ParserModel):
        self.parsers_model = parsers_model
    
    def _notify_error_message(self, err_msg):
        notify_error_message(self.ui.error_label, err_msg)