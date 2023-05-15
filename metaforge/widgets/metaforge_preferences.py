from pathlib import Path
from typing import List

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QHeaderView, QUndoStack
import PySide2.QtCore
from PySide2.QtCore import QModelIndex, QItemSelection, QSortFilterProxyModel, Qt

from metaforge.undo_stack_commands.load_parsers_command import LoadParsersCommand
from metaforge.undo_stack_commands.remove_parsers_command import RemoveParsersCommand
from metaforge.qt_models.qparsertablemodel import QParserTableModel
from metaforge.delegates.checkboxdelegate import CheckBoxDelegate
from metaforge.widgets.utilities.widget_utilities import notify_no_errors

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from metaforge.widgets.generated_5_12.ui_metaforge_preferences import Ui_MetaForgePreferences
    from metaforge.widgets.generated_5_12.ui_metaforge_preferences import Ui_MetaForgePreferences
elif qt_version[1] == 15:
    from metaforge.widgets.generated_5_15.ui_metaforge_preferences import Ui_MetaForgePreferences

class MetaForgePreferencesDialog(QDialog):
    K_NO_ERRORS_STR = "No errors."

    def __init__(self, parent=None):
        super(MetaForgePreferencesDialog, self).__init__(parent)
        self.ui = Ui_MetaForgePreferences()
        self.ui.setupUi(self)
        self.current_directory = Path("")
        self.qparser_table_model: QParserTableModel = None
        self.qproxy_parser_table_model: QSortFilterProxyModel = QSortFilterProxyModel(self)
        self.undo_stack: QUndoStack = QUndoStack(self)
        
        self.checkbox_delegate = CheckBoxDelegate(self.undo_stack)
        self.ui.parser_directories_table.setItemDelegateForColumn(QParserTableModel.K_ENABLED_COL_INDEX, self.checkbox_delegate)

        self.ui.addBtn.pressed.connect(self._add_files)
        self.ui.removeBtn.pressed.connect(self._remove_selected_files)
        self.ui.searchLineEdit.textChanged.connect(self.qproxy_parser_table_model.setFilterFixedString)

        self.ui.parser_directories_table.setSortingEnabled(True)
        self.qproxy_parser_table_model.setFilterKeyColumn(QParserTableModel.K_PARSER_NAME_COL_INDEX)
        self.qproxy_parser_table_model.setFilterCaseSensitivity(Qt.CaseInsensitive)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).pressed.connect(self.accept)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).pressed.connect(self.reject)

        notify_no_errors(self.ui.error_string)
    
    def _handle_parser_directories_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        proxy_indexes: List[QModelIndex] = self.ui.parser_directories_table.selectionModel().selectedRows()
        for proxy_index in proxy_indexes:
            is_default = self.qproxy_parser_table_model.data(proxy_index, QParserTableModel.Default)
            if is_default:
                self.ui.removeBtn.setDisabled(True)
                return
        
        self.ui.removeBtn.setEnabled(True)
    
    def _add_files(self):
        result = QFileDialog.getOpenFileNames(self, 'Open Parser File(s)', str(self.current_directory), "MetaForge Parsers (*.py)")
        file_paths = result[0]
        if len(file_paths) > 0:
            self.current_directory = Path(file_paths[0]).parent
            file_paths = [Path(file_path) for file_path in file_paths]
            load_parsers_command = LoadParsersCommand(self.qparser_table_model, file_paths)
            self.undo_stack.push(load_parsers_command)

    def _remove_selected_files(self):
        selected_rows: List[QModelIndex] = self.ui.parser_directories_table.selectionModel().selectedRows()
        selected_rows = [index.row() for index in selected_rows]
        remove_parsers_command = RemoveParsersCommand(self.qparser_table_model, selected_rows)
        self.undo_stack.push(remove_parsers_command)
        
        notify_no_errors(self.ui.error_string)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def _setup_parser_directories_table(self):
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserTableModel.K_ENABLED_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserTableModel.K_PARSER_NAME_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserTableModel.K_PARSER_LOCATION_COL_INDEX, QHeaderView.Stretch)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserTableModel.K_PARSER_SUPPORTED_EXTS_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserTableModel.K_PARSER_VERSION_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserTableModel.K_PARSER_MESSAGES_COL_INDEX, QHeaderView.Stretch)
        self.ui.parser_directories_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.setWordWrap(True)
    
    def set_parsers_model(self, model: QParserTableModel):
        self.qparser_table_model = model
        self.qproxy_parser_table_model.setSourceModel(model)
        self.ui.parser_directories_table.setModel(self.qproxy_parser_table_model)
        self.ui.parser_directories_table.selectionModel().selectionChanged.connect(self._handle_parser_directories_selection_changed)
        self._setup_parser_directories_table()

    def accept(self):
        self.undo_stack.clear()
        self.qparser_table_model.update_watched_parsers()
        self.qparser_table_model.model_about_to_change.emit()
        self.qparser_table_model.model_changed.emit()
        super().accept()

    def reject(self):
        while self.undo_stack.canUndo():
            self.undo_stack.undo()
        super().reject()