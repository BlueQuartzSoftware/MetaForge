# This Python file uses the following encoding: utf-8
from importlib.metadata import metadata
from pyexpat import model
from typing import List
import json
from uuid import UUID

from pathlib import Path

from PySide2.QtWidgets import QWidget, QFileDialog
from PySide2.QtCore import Qt, QStandardPaths, QSortFilterProxyModel, QModelIndex, QEvent, QPersistentModelIndex
import PySide2.QtCore

from metaforge.parsers.metaforgeparser import MetaForgeParser
from metaforge.ez_models.ezmetadataentry import EzMetadataEntry
from metaforge.ez_models.ezmetadatamodel import EzMetadataModel, TemplateModel_V1, TemplateModel
from metaforge.qt_models.qeztablemodel import QEzTableModel
from metaforge.models.treemodel import TreeModel
from metaforge.delegates.trashdelegate import TrashDelegate
from metaforge.delegates.checkboxdelegate import CheckBoxDelegate
from metaforge.qt_models.qcreateeztablemodel import QCreateEzTableModel
from metaforge.utilities.metaforgestyledatahelper import MetaForgeStyleDataHelper
from metaforge.models.available_parsers_model import AvailableParsersModel
from metaforge.widgets.utilities.widget_utilities import notify_error_message, notify_no_errors

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from metaforge.widgets.generated_5_12.ui_createtemplatewidget import Ui_CreateTemplateWidget
elif qt_version[1] == 15:
    from metaforge.widgets.generated_5_15.ui_createtemplatewidget import Ui_CreateTemplateWidget


class CreateTemplateWidget(QWidget):
    K_CREATE_TREE_HEADER = "Available File Metadata"
    K_TEMPLATE_VERSION_KEY = 'template_version'
    K_DATA_FILE_KEY = 'data_file_path'
    K_PARSER_UUID_KEY = 'parser_uuid'
    K_MODEL_ENTRIES_KEY = 'entries'
    
    def __init__(self, parent):
        super(CreateTemplateWidget, self).__init__(parent)
        
        self.style_sheet_helper: MetaForgeStyleDataHelper = MetaForgeStyleDataHelper(self)
        self.ui = Ui_CreateTemplateWidget()
        self.ui.setupUi(self)
        self.available_parsers_model = None
        self.ui.dataFileSelect.clicked.connect(self.select_input_data_file)
        self.ui.clearCreateButton.clicked.connect(self.clear)
        self.setAcceptDrops(True)
        self.numCustoms = 0

        # Setup the blank Create Template table and tree
        self.load_metadata_entries()

        notify_no_errors(self.ui.error_label)

        self.ui.appendCreateTableRowButton.clicked.connect(self.add_custom_row_to_table)
        self.ui.removeCreateTableRowButton.clicked.connect(self.remove_row_btn_clicked_slot)
    
        self.ui.createTemplateListSearchBar.textChanged.connect(self.filter_metadata_table)
        self.ui.createTemplateTreeSearchBar.textChanged.connect(self.filter_tree)

        # Setup the Combo Box with all of the parsers that we know about
        self.ui.fileParserCombo.currentIndexChanged.connect(self.parser_combobox_changed_slot)

        self.ui.dataFileLineEdit.installEventFilter(self)

    def setup_metadata_table(self, metadata_model: EzMetadataModel = EzMetadataModel()):
        self.trash_delegate = TrashDelegate(stylehelper=self.style_sheet_helper)
        self.checkbox_delegate = CheckBoxDelegate()
        self.metadata_table_model = QEzTableModel(metadata_model=metadata_model, parent=self)
        self.metadata_table_model_proxy = self.init_table_model_proxy(self.metadata_table_model)
        self.ui.metadata_table_view.setModel(self.metadata_table_model_proxy)
        self.filter_metadata_table()
        self.ui.metadata_table_view.setItemDelegateForColumn(self.metadata_table_model.K_REMOVE_COL_INDEX, self.trash_delegate)
        self.trash_delegate.pressed.connect(self.remove_table_entry)
        self.ui.metadata_table_view.setItemDelegateForColumn(self.metadata_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.checkbox_delegate)
        self.ui.metadata_table_view.setItemDelegateForColumn(self.metadata_table_model.K_EDITABLE_COL_INDEX, self.checkbox_delegate)
        self.polish_metadata_table()
    
    def polish_metadata_table(self):
        self.ui.metadata_table_view.resizeColumnsToContents()
        self.ui.metadata_table_view.setColumnWidth(self.metadata_table_model.K_HTANNOTATION_COL_INDEX, self.width() * .1)
        self.ui.metadata_table_view.setColumnWidth(self.metadata_table_model.K_OVERRIDESOURCEVALUE_COL_INDEX, self.width() * .125)
        self.ui.metadata_table_view.horizontalHeader().setStretchLastSection(True)

    def setup_metadata_tree(self, metadata_model: EzMetadataModel = EzMetadataModel()):
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
    
    def clear_models(self):
        self.load_metadata_entries()

    def add_custom_row_to_table(self):
        self.metadata_table_model.addCustomRow(self.numCustoms)
        self.numCustoms += 1
        self.ui.metadata_table_view.scrollToBottom()

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
    
    def load_template(self, template_file_path: Path):
        notify_no_errors(self.ui.error_label)
        with template_file_path.open('r') as json_file:
            template_json = json.load(json_file)
            template_version: str = template_json[self.K_TEMPLATE_VERSION_KEY]
            if template_version == '1.0':
                self._load_template_v1(template_json)
            elif template_version == '2.0':
                self._load_template(template_json)
            else:
                self._notify_error_message(f"Unable to load template file '{str(template_file_path)}'. Unrecognizable template version.")
    
    def _load_template_v1(self, template_json: dict):
        model: TemplateModel_V1 = TemplateModel_V1.from_dict(template_json)
        data_file_path, metadata_model = model.extract_data()
        self.load_template_data(data_file_path, None, metadata_model)

    def _load_template(self, template_json: dict):
        template_model: TemplateModel = TemplateModel.from_dict(template_json)
        data_file_path, parser_uuid, metadata_model = template_model.extract_data()
        self.load_template_data(data_file_path, parser_uuid, metadata_model)
    
    def load_template_data(self, data_file_path: Path, parser_uuid: UUID, metadata_model: EzMetadataModel):
        # Set the data file path
        self.ui.dataFileLineEdit.setText(str(data_file_path))

        # Set the entries data
        self.load_metadata_entries(metadata_model=metadata_model)

        # Set the parser
        parser_index, parser = self.available_parsers_model.find_parser_from_uuid(parser_uuid)
        if parser is None:
            parser_index, parser = self.available_parsers_model.find_compatible_parser(data_file_path, self._notify_error_message)
            if (parser is None):
                return
        
        self.ui.fileParserCombo.blockSignals(True)
        self.ui.fileParserCombo.setCurrentIndex(parser_index)
        self.ui.fileParserCombo.blockSignals(False)
    
    def load_metadata_entries(self, metadata_model: EzMetadataModel = EzMetadataModel()):        
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
        if entry is not None and entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
            self.metadata_table_model.beginRemoveRows(QModelIndex(), source_index.row(), source_index.row())
            self.metadata_table_model.metadata_model.remove_by_index(source_index.row())
            self.metadata_table_model.endRemoveRows()
        elif entry is not None and entry.source_type is EzMetadataEntry.SourceType.FILE:
            self.metadata_tree_model.changeLeafCheck(entry)
        
        self.metadata_table_model_proxy.invalidate()
        index0 = self.metadata_table_model.index(0, 0)
        index1 = self.metadata_table_model.index(self.metadata_table_model.rowCount() - 1, QEzTableModel.K_COL_COUNT)
        self.metadata_table_model_proxy.dataChanged.emit(index0, index1)
    
    def save_template(self, file_path: str):
        with open(file_path, 'w') as outfile:
            metadata_model = self.metadata_table_model.metadata_model
            parser_model_index = self.available_parsers_model.index(self.ui.fileParserCombo.currentIndex(), 0)
            parser: MetaForgeParser = self.available_parsers_model.data(parser_model_index, AvailableParsersModel.Parser)
            template_model = TemplateModel.create_model(data_file_path=self.ui.dataFileLineEdit.text(), parser_uuid=parser.uuid(), entries=metadata_model.entries)
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
        self.clear_models()
        if not self.ui.dataFileLineEdit.text():
            self._notify_error_message(f"'{self.ui.data_file_label.text()}' is empty!")
            return

        filePath = Path(self.ui.dataFileLineEdit.text())
        model_index = self.available_parsers_model.index(index, 0)
        parser = self.available_parsers_model.data(model_index, AvailableParsersModel.Parser)

        if not self.parse_data_file(filePath, parser):
            return
    
    def parse_data_file(self, file_path: Path, parser: MetaForgeParser) -> bool:
        if file_path == None:
            return False
        
        if not parser.accepts_extension(file_path.suffix):
            self._notify_error_message(f"Selected parser '{parser.human_label()}' is not usable with file '{file_path}': File extension not accepted.")
            return False

        # parse the metadata from the input data file
        headerDict = parser.parse_header_as_dict(file_path)


        metadata_model = EzMetadataModel.create_model_from_dict(model_dict=headerDict, source_type=EzMetadataEntry.SourceType.FILE)

        self.load_metadata_entries(metadata_model=metadata_model)

        self.ui.metadata_table_view.setWordWrap(True)
        self.ui.metadata_table_view.setRowHeight(21, 35)
        self.polish_metadata_table()

        return True
    
    def select_input_data_file(self, fileLink=None):
        notify_no_errors(self.ui.error_label)
        if fileLink == False:
            file_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
                QStandardPaths.HomeLocation), self.tr("Files (*.*)"))[0]
        else:
            file_path = fileLink

        if file_path != "":
            self.setWindowTitle(file_path)
            self.ui.dataFileLineEdit.setText(file_path)

            file_path = Path(file_path)

            self.clear_models()

            if self.ui.fileParserCombo.currentIndex() == -1:
                parser_index, parser = self.available_parsers_model.find_compatible_parser(file_path, self._notify_error_message)
                if (parser is None):
                    return
            
                self.ui.fileParserCombo.setCurrentIndex(parser_index)
            else:
                model_index = self.available_parsers_model.index(self.ui.fileParserCombo.currentIndex(), 0)
                parser = self.available_parsers_model.data(model_index, AvailableParsersModel.Parser)
                if not self.parse_data_file(file_path, parser):
                    return
    
    def set_parsers_model(self, model: AvailableParsersModel):
        self.available_parsers_model = model
        self.ui.fileParserCombo.setModel(model)
        self.ui.fileParserCombo.setCurrentIndex(-1)
    
    def _notify_error_message(self, err_msg):
        notify_error_message(self.ui.error_label, err_msg)
