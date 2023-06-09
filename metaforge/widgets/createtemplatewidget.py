# This Python file uses the following encoding: utf-8
from typing import List
import json
from uuid import UUID

from pathlib import Path

from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Qt, QStandardPaths, QSortFilterProxyModel, QModelIndex, QEvent, QPersistentModelIndex
import PySide6.QtCore

from metaforge.parsers.metaforgeparser import MetaForgeParser
from metaforge.models.metadataentry import MetadataEntry
from metaforge.models.metadatamodel import MetadataModel, TemplateModel_V1, TemplateModel, load_template
from metaforge.qt_models.qeztablemodel import QEzTableModel
from metaforge.models.treemodel import TreeModel
from metaforge.delegates.trashdelegate import TrashDelegate
from metaforge.delegates.checkboxdelegate import CheckBoxDelegate
from metaforge.qt_models.qcreateeztablemodel import QCreateEzTableModel
from metaforge.common.metaforgestyledatahelper import MetaForgeStyleDataHelper
from metaforge.qt_models.qparsercomboboxmodel import QParserComboBoxModel
from metaforge.qt_models.qproxyparsercomboboxmodel import QProxyParserComboBoxModel
from metaforge.widgets.utilities.widget_utilities import notify_error_message, notify_no_errors

from metaforge.widgets.generated_6_5.ui_createtemplatewidget import Ui_CreateTemplateWidget


class CreateTemplateWidget(QWidget):
    K_CREATE_TREE_HEADER = "Available File Metadata"
    K_DATA_FILE_KEY = 'data_file_path'
    K_PARSER_UUID_KEY = 'parser_uuid'
    K_MODEL_ENTRIES_KEY = 'entries'
    
    def __init__(self, parent):
        super(CreateTemplateWidget, self).__init__(parent)
        
        self.style_sheet_helper: MetaForgeStyleDataHelper = MetaForgeStyleDataHelper(self)
        self.ui = Ui_CreateTemplateWidget()
        self.ui.setupUi(self)
        self.dialog_start_location = QStandardPaths.displayName(QStandardPaths.HomeLocation)
        self.qparsers_cb_model: QParserComboBoxModel = None
        self.proxy_parsers_model = QProxyParserComboBoxModel(self)
        self.metadata_model: MetadataModel = MetadataModel()
        self.ui.dataFileSelect.clicked.connect(self.select_input_data_file)
        self.ui.clearCreateButton.clicked.connect(self.clear)
        self.last_valid_parser: MetaForgeParser = None
        self.numCustoms = 0
        self.cb_saved_parser_path = None

        # Setup the blank Create Template table and tree
        self.load_metadata_entries(metadata_model=self.metadata_model)

        notify_no_errors(self.ui.error_label)

        self.ui.appendCreateTableRowButton.clicked.connect(self.add_custom_row_to_table)
        self.ui.removeCreateTableRowButton.clicked.connect(self.remove_row_btn_clicked_slot)
    
        self.ui.createTemplateListSearchBar.textChanged.connect(self.filter_metadata_table)
        self.ui.createTemplateTreeSearchBar.textChanged.connect(self.filter_tree)

        # Setup the Combo Box with all of the parsers that we know about
        self.ui.dataFileLineEdit.installEventFilter(self)

    def setup_metadata_table(self, metadata_model: MetadataModel = MetadataModel()):
        self.trash_delegate = TrashDelegate(stylehelper=self.style_sheet_helper)
        self.checkbox_delegate = CheckBoxDelegate()
        self.metadata_table_model = QEzTableModel(metadata_model=metadata_model, parent=self)
        self.metadata_table_model_proxy = self.init_table_model_proxy(self.metadata_table_model)
        self.ui.metadata_table_view.setModel(self.metadata_table_model_proxy)
        # centered_box_proxy = CenteredBoxProxy()
        # self.ui.metadata_table_view.setStyle(centered_box_proxy)
        self.filter_metadata_table()
        self.ui.metadata_table_view.setItemDelegateForColumn(self.metadata_table_model.K_REMOVE_COL_INDEX, self.trash_delegate)
        self.trash_delegate.pressed.connect(self.remove_table_entry)
        self.ui.metadata_table_view.setItemDelegateForColumn(self.metadata_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.checkbox_delegate)
        self.ui.metadata_table_view.setItemDelegateForColumn(self.metadata_table_model.K_EDITABLE_COL_INDEX, self.checkbox_delegate)
        self.ui.metadata_table_view.setWordWrap(True)
        self.ui.metadata_table_view.setRowHeight(21, 35)
        self.polish_metadata_table()
    
    def polish_metadata_table(self):
        self.ui.metadata_table_view.resizeColumnsToContents()
        self.ui.metadata_table_view.setColumnWidth(self.metadata_table_model.K_HTANNOTATION_COL_INDEX, self.width() * .1)
        self.ui.metadata_table_view.setColumnWidth(self.metadata_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.width() * .125)
        self.ui.metadata_table_view.horizontalHeader().setStretchLastSection(True)

    def setup_metadata_tree(self, metadata_model: MetadataModel = MetadataModel()):
        headers = [self.K_CREATE_TREE_HEADER]
        self.metadata_tree_model = TreeModel(headers, metadata_model, self)
        self.tree_search_filter_model = QSortFilterProxyModel(self)
        self.tree_search_filter_model.setSourceModel(self.metadata_tree_model)
        self.tree_search_filter_model.setFilterKeyColumn(0)
        self.tree_search_filter_model.setDynamicSortFilter(True)
        self.tree_search_filter_model.setRecursiveFilteringEnabled(True)
        self.ui.metadataTreeView.setModel(self.tree_search_filter_model)
        self.ui.metadataTreeView.expandAll()
        refresh_func = self.metadata_table_model.refresh_entry
        self.metadata_tree_model.checkChanged.connect(refresh_func)

    def clear(self):
        self.ui.dataFileLineEdit.setText("")
        self.ui.createTemplateListSearchBar.setText("")
        self.ui.createTemplateTreeSearchBar.setText("")
        self.clear_models()
        self.last_valid_parser = None
        self.ui.fileParserCombo.setCurrentIndex(-1)
    
    def clear_models(self):
        self.metadata_model = MetadataModel()
        self.load_metadata_entries(self.metadata_model)

    def add_custom_row_to_table(self):
        self.metadata_table_model.addCustomRow(self.numCustoms)
        self.numCustoms += 1
        self.ui.metadata_table_view.scrollToBottom()

        # Reload table view
        self.filter_metadata_table()
        self.polish_metadata_table()

    def eventFilter(self, object, event):
        if object == self.ui.dataFileLineEdit:
            accepted_ext = ['.ang', '.ctf', '.tiff' , '.tif' , '.ini']
            if event.type() == QEvent.DragEnter:
                file_ext = str(event.mimeData().urls()[0])[-6:-2]
                event.acceptProposedAction()
            if (event.type() == QEvent.Drop):
                file_ext = str(event.mimeData().urls()[0])[-6:-2]
                event.acceptProposedAction()
                self.select_input_data_file(event.mimeData().urls()[0].toLocalFile())              

        return QWidget.eventFilter(self, object,  event)

    def filter_metadata_table(self):
        proxy = self.metadata_table_model_proxy
        text = self.ui.createTemplateListSearchBar.text()
        self.filter_proxy_model(proxy, text)

    def filter_proxy_model(self, proxy_model: QSortFilterProxyModel, filter_text: str):
        proxy_model.invalidate()
        proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        proxy_model.setFilterWildcard(f'*{filter_text}*')

    def filter_tree(self):
        self.tree_search_filter_model.invalidate()
        self.tree_search_filter_model.setFilterCaseSensitivity(
            Qt.CaseInsensitive)
        self.tree_search_filter_model.setFilterWildcard(
            "*"+self.ui.createTemplateTreeSearchBar.text()+"*")
    
    def load_template_file(self, template_file_path: Path):
        notify_no_errors(self.ui.error_label)

        data_file_path, parser_uuid, metadata_model, err_msg = load_template(template_file_path)

        if err_msg is not None:
            self._notify_error_message(err_msg)
            return

        self.load_template_data(data_file_path, parser_uuid, metadata_model)
    
    def load_template_data(self, data_file_path: Path, parser_uuid: UUID, metadata_model: MetadataModel):
        # Set the data file path
        self.ui.dataFileLineEdit.setText(str(data_file_path))

        # Set the entries data
        self.load_metadata_entries(metadata_model=metadata_model)

        # Set the parser
        parser_index = -1
        if parser_uuid is not None:
            parser, err_msg = self.qparsers_cb_model.find_parser_from_uuid(parser_uuid)
            if parser is None:
                parser, err_msg = self.qparsers_cb_model.find_parser_from_data_path(data_file_path)
                if parser is None:
                    self._notify_error_message(err_msg)
                    return
            parser_index = self.qparsers_cb_model.index_from_parser(parser)

        self.ui.fileParserCombo.blockSignals(True)
        self.ui.fileParserCombo.setCurrentIndex(parser_index)
        self.ui.fileParserCombo.blockSignals(False)

        self.last_valid_parser = parser
    
    def load_metadata_entries(self, metadata_model: MetadataModel = MetadataModel()):        
        # Setup the Create Template table
        self.setup_metadata_table(metadata_model=metadata_model)

        # Setup the Create Template tree
        self.setup_metadata_tree(metadata_model=metadata_model)

    def remove_row_btn_clicked_slot(self):
        selection_model = self.ui.metadata_table_view.selectionModel()
        selected_rows: List[QModelIndex] = selection_model.selectedRows()
        selected_rows: List[QModelIndex] = [QPersistentModelIndex(idx.model().mapToSource(idx)) for idx in selected_rows]
        for selected_row in selected_rows:
            if selected_row.isValid():
                self.remove_table_entry(selected_row)

    def remove_table_entry(self, source_index: QModelIndex):
        if not source_index.isValid() or source_index.row() >= self.metadata_table_model.metadata_model.size():
            return
        
        entry = self.metadata_table_model.metadata_model.entry(source_index.row())
        if entry is not None:
            if entry.source_type is MetadataEntry.SourceType.FILE and entry.loaded is True:
                self.metadata_tree_model.changeLeafCheck(entry)
            else:
                self.metadata_table_model.beginRemoveRows(QModelIndex(), source_index.row(), source_index.row())
                self.metadata_table_model.metadata_model.remove_by_index(source_index.row())
                self.metadata_table_model.endRemoveRows()
        
        self.metadata_table_model_proxy.invalidate()
        index0 = self.metadata_table_model.index(0, 0)
        index1 = self.metadata_table_model.index(self.metadata_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
        self.metadata_table_model_proxy.dataChanged.emit(index0, index1)
    
    def save_template(self, file_path: str):
        with open(file_path, 'w') as outfile:
            metadata_model = self.metadata_table_model.metadata_model
            parser_uuid = None
            if self.last_valid_parser:
                parser_uuid = str(self.last_valid_parser.uuid())
            template_model = TemplateModel.create_model(data_file_path=self.ui.dataFileLineEdit.text(), parser_uuid=parser_uuid, entries=metadata_model.entries)
            model_string = template_model.to_json(indent=4)
            outfile.write(model_string)

    def init_table_model_proxy(self, source_model: QEzTableModel) -> QCreateEzTableModel:
        proxy = QCreateEzTableModel(self)
        proxy.setSourceModel(source_model)
        proxy.setFilterKeyColumn(1)
        proxy.setDynamicSortFilter(True)
        return proxy

    def parser_combobox_changed_slot(self, index: int):
        notify_no_errors(self.ui.error_label)

        proxy_model_index = self.proxy_parsers_model.index(index, 0)
        model_index = self.proxy_parsers_model.mapToSource(proxy_model_index)
        if not model_index.isValid():
            self.ui.parser_path_label.clear()
            return

        parser_path = self.qparsers_cb_model.data(model_index, QParserComboBoxModel.ParserPath)
        self.ui.parser_path_label.setText(str(parser_path))

        if not self.ui.dataFileLineEdit.text():
            self._notify_error_message(f"'{self.ui.data_file_label.text()}' is empty!")
            return

        filePath = Path(self.ui.dataFileLineEdit.text())
        parser = self.qparsers_cb_model.data(model_index, QParserComboBoxModel.Parser)

        if not self.parse_data_file(filePath, parser):
            return

        self.last_valid_parser = parser
    
    def parse_data_file(self, file_path: Path, parser: MetaForgeParser) -> bool:
        if file_path == None:
            return False
        
        if not parser.accepts_extension(file_path.suffix):
            self._notify_error_message(f"Selected parser '{parser.human_label()}' is not usable with file '{file_path}': File extension not accepted.")
            return False

        # Parse the metadata dictionary from the input data file
        metadata_list = parser.parse_header(file_path)
        
        # Create an MetadataModel from the metadata dictionary
        metadata_model = MetadataModel.create_model(metadata_list, source_type=MetadataEntry.SourceType.FILE)

        # Merge the new MetadataModel with the existing MetadataModel
        self._merge_metadata_model(metadata_model=metadata_model)

        # Reload tree view
        self.metadata_tree_model.clearModel()
        self.metadata_tree_model.setupModelData(self.metadata_model)
        self.ui.metadataTreeView.expandAll()

        # Reload table view
        self.filter_metadata_table()
        self.polish_metadata_table()

        return True
    
    def _merge_metadata_model(self, metadata_model: MetadataModel):
        for entry in self.metadata_model.entries:
            if entry.source_type == MetadataEntry.SourceType.FILE:
                new_entry = metadata_model.entry_by_source(entry.source_path)
                if new_entry is None:
                    # Exists in current model but not in incoming model
                    # Mark the entry as not loaded because it's no longer an entry from the current file
                    entry.loaded = False
                    entry.source_value = ""
                else:
                    # Exists in both the current model and the incoming model
                    # Keep all settings the same for this entry, just replace the source value
                    entry.loaded = True
                    entry.source_value = new_entry.source_value

        for entry in metadata_model.entries:
            if entry.source_type == MetadataEntry.SourceType.FILE:
                if self.metadata_model.entry_by_source(entry.source_path) is None:
                    # Exists in incoming model, but not in current model
                    self.metadata_model.entries.append(entry)
                    self.metadata_table_model.refresh_entry(entry.source_path)

    
    def select_input_data_file(self, fileLink=None):
        notify_no_errors(self.ui.error_label)
        if fileLink == False:
            file_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), self.dialog_start_location, self.tr("Files (*.*)"))[0]
        else:
            file_path = fileLink

        if file_path != "":
            self.setWindowTitle(file_path)
            self.ui.dataFileLineEdit.setText(file_path)

            file_path = Path(file_path)
            self.dialog_start_location = str(file_path.parent)

            if self.ui.fileParserCombo.currentIndex() == -1:
                parser, err_msg = self.qparsers_cb_model.find_parser_from_data_path(file_path)
                if parser is None:
                    self._notify_error_message(err_msg)
                    return
            
                parser_index = self.qparsers_cb_model.index_from_parser(parser)
                self.ui.fileParserCombo.setCurrentIndex(parser_index)
            else:
                proxy_model_index = self.proxy_parsers_model.index(self.ui.fileParserCombo.currentIndex(), 0)
                model_index = self.proxy_parsers_model.mapToSource(proxy_model_index)
                parser = self.qparsers_cb_model.data(model_index, QParserComboBoxModel.Parser)
                if not self.parse_data_file(file_path, parser):
                    return
            
            self.last_valid_parser = parser
    
    def set_parsers_model(self, qparsers_cb_model: QParserComboBoxModel):
        self.qparsers_cb_model = qparsers_cb_model
        self.proxy_parsers_model.setSourceModel(self.qparsers_cb_model)
        self.proxy_parsers_model.sort(0)
        self.ui.fileParserCombo.setModel(self.proxy_parsers_model)
        self.ui.fileParserCombo.setCurrentIndex(-1)
        self.ui.fileParserCombo.currentIndexChanged.connect(self.parser_combobox_changed_slot)
        qparsers_cb_model.modelAboutToBeReset.connect(self._save_combo_box)
        qparsers_cb_model.modelReset.connect(self._update_combo_box)
    
    def _save_combo_box(self):
        idx = self.ui.fileParserCombo.currentIndex()
        if idx > 0:
            proxy_index = self.proxy_parsers_model.index(idx, 0)
            source_index = self.proxy_parsers_model.mapToSource(proxy_index)
            self.cb_saved_parser_path = self.qparsers_cb_model.data(source_index, QParserComboBoxModel.ParserPath)
    
    def _update_combo_box(self):
        self.proxy_parsers_model.invalidateFilter()

        if self.cb_saved_parser_path is None:
            self.ui.fileParserCombo.setCurrentIndex(-1)
            return
        
        idx = self.qparsers_cb_model.index_from_parser_path(self.cb_saved_parser_path)
        if idx < 0:
            self.ui.fileParserCombo.setCurrentIndex(idx)
        else:
            source_index = self.qparsers_cb_model.index(idx, 0)
            proxy_index = self.proxy_parsers_model.mapFromSource(source_index)
            self.ui.fileParserCombo.setCurrentIndex(proxy_index.row())
        self.cb_saved_parser_path = None

    def _notify_error_message(self, err_msg):
        notify_error_message(self.ui.error_label, err_msg)
