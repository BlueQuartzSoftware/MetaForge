from pathlib import Path
import yaml
import copy
import subprocess
import sys
from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QApplication, QHeaderView
import PySide2.QtCore
from PySide2.QtCore import QSettings, QModelIndex, QPersistentModelIndex, QFileSystemWatcher, QItemSelection

from metaforge.ez_models.ezparserdirectory import EzParserDirectory
from metaforge.qt_models.qparsersmodel import QParsersModel
from metaforge.delegates.geardelegate import GearDelegate
from metaforge.delegates.checkboxdelegate import CheckBoxDelegate
from metaforge.common.constants import METAFORGE_PKG_ROOT, K_PARSER_YAML_FILE_NAME
from metaforge.qt_models.qparserdirectoriesmodel import QParserDirectoriesModel
from metaforge.ez_models.ezparserdirectoriesmodel import EzParserDirectoriesModel, EzParserDirectory
from metaforge.widgets.utilities.widget_utilities import notify_no_errors, notify_error_message
from metaforge.utilities.parser_utilities import create_parser_directory

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from metaforge.widgets.generated_5_12.ui_metaforge_preferences import Ui_MetaForgePreferences
elif qt_version[1] == 15:
    from metaforge.widgets.generated_5_15.ui_metaforge_preferences import Ui_MetaForgePreferences

class MetaForgePreferencesDialog(QDialog):
    K_SETTINGS_USE_DEFAULT_PARSER_LOCATION_KEY = "use_default_parser_location"
    K_SETTINGS_PARSER_DIR_MODEL_KEY = "parser_directories_model"
    K_PARSER_YAML_KEY = "metaforge-parsers"
    K_NO_ERRORS_STR = "No errors."

    def __init__(self, parent=None):
        super(MetaForgePreferencesDialog, self).__init__(parent)
        self.ui = Ui_MetaForgePreferences()
        self.ui.setupUi(self)
        self.current_directory = Path("")
        self.parsers_model = None
        self.parser_directories_model: EzParserDirectoriesModel = EzParserDirectoriesModel()
        self.file_watcher = QFileSystemWatcher(parent=self)
        self.default_parsers_dir_path = METAFORGE_PKG_ROOT / 'parsers'

        self._read_settings()

        self._init_file_watcher()

        self.staged_parser_directories_model = copy.deepcopy(self.parser_directories_model)
        
        self.qparser_directories_model = QParserDirectoriesModel(self.staged_parser_directories_model)
        self.gear_delegate = GearDelegate()
        self.checkbox_delegate = CheckBoxDelegate()
        self.gear_delegate.pressed.connect(self._open_parser_config_file)
        self.ui.parser_directories_table.setItemDelegateForColumn(self.qparser_directories_model.K_ENABLED_COL_INDEX, self.checkbox_delegate)
        self.ui.parser_directories_table.setItemDelegateForColumn(self.qparser_directories_model.K_CONFIGURE_COL_INDEX, self.gear_delegate)
        self.ui.parser_directories_table.setModel(self.qparser_directories_model)
        self.ui.parser_directories_table.selectionModel().selectionChanged.connect(self._handle_parser_directories_selection_changed)
        self._polish_parser_directories_table()

        self.ui.addBtn.pressed.connect(self._add_files)
        self.ui.removeBtn.pressed.connect(self._remove_selected_files)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).pressed.connect(self.accept)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).pressed.connect(self.reject)

        notify_no_errors(self.ui.error_string)
    
    def _read_settings(self):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())

        parser_dir_model_json = settings.value(self.K_SETTINGS_PARSER_DIR_MODEL_KEY, defaultValue="", type=str)
        if parser_dir_model_json != "":
            self.parser_directories_model: EzParserDirectoriesModel = EzParserDirectoriesModel.from_json(parser_dir_model_json)
                
        # Insert the default directory
        default_parsers_directory: EzParserDirectory = create_parser_directory(self.default_parsers_dir_path)
        default_parsers_directory.default = True
        default_parsers_directory.enabled = settings.value(self.K_SETTINGS_USE_DEFAULT_PARSER_LOCATION_KEY, defaultValue=True, type=bool)
        self.parser_directories_model.insert_directory(0, default_parsers_directory)
    
    def _init_file_watcher(self):
        self.file_watcher = QFileSystemWatcher(parent=self)
        self.file_watcher.fileChanged.connect(self._handle_parser_directory_config_file_changed)
        [self.file_watcher.addPath(str(directory.directory_path / K_PARSER_YAML_FILE_NAME)) for directory in self.parser_directories_model.parser_directories]
    
    def _handle_parser_directory_config_file_changed(self, config_file_path: str):
        config_file_path = Path(config_file_path)
        directory: EzParserDirectory = create_parser_directory(config_file_path.parent)
        matched_directory = self.staged_parser_directories_model.directory_from_path(directory.directory_path)
        if matched_directory is not None:
            matched_directory.parser_paths = directory.parser_paths
            directory_row = self.staged_parser_directories_model.index_from_directory(matched_directory)
            index = self.qparser_directories_model.index(directory_row, self.qparser_directories_model.K_PARSERS_LOADED_COL_INDEX)
            self.qparser_directories_model.dataChanged.emit(index, index)

            directory_paths = [directory.directory_path for directory in self.parser_directories_model.parser_directories if directory.enabled]
            if directory.directory_path in directory_paths:
                self._update_parsers_list_from_config_file(config_file_path)
    
    def _handle_parser_directories_changed(self, parent: QModelIndex, first: int, last: int):
        self._update_parsers_list()
    
    def _handle_parser_directories_selection_changed(self, selected: QItemSelection, deselected: QItemSelection):
        model_indexes: List[QModelIndex] = self.ui.parser_directories_table.selectionModel().selectedRows()
        for model_index in model_indexes:
            directory = self.staged_parser_directories_model.directory(model_index.row())
            if directory.default:
                self.ui.removeBtn.setDisabled(True)
                return
        
        self.ui.removeBtn.setEnabled(True)
    
    def _open_parser_config_file(self, source_index: QModelIndex):
        directory: EzParserDirectory = self.staged_parser_directories_model.directory(source_index.row())
        config_path = directory.directory_path / K_PARSER_YAML_FILE_NAME

        if sys.platform == "win32":
            os.startfile(str(config_path))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(config_path)])
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", str(config_path)])
        else:
            self.ui.error_string.setText(f"Unable to open config file - unsupported operating system '{sys.platform}'.")
    
    def closeEvent(self, event):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())

        default_directory = self.staged_parser_directories_model.directory_from_path(self.default_parsers_dir_path)
        if default_directory is not None:
            settings.setValue(self.K_SETTINGS_USE_DEFAULT_PARSER_LOCATION_KEY, default_directory.enabled)
            self.parser_directories_model.remove(self.default_parsers_dir_path)

        parser_dir_model_json = self.parser_directories_model.to_json(indent=4)
        settings.setValue(self.K_SETTINGS_PARSER_DIR_MODEL_KEY, parser_dir_model_json)

        super().closeEvent(event)
    
    def _add_files(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Directory', str(self.current_directory))
        if dir_path != "":
            self.current_directory = Path(dir_path)
            self.qparser_directories_model.addRow(self.current_directory)
            self.file_watcher.addPath(str(self.current_directory / K_PARSER_YAML_FILE_NAME))
            self.validate()

    def _remove_selected_files(self):
        selected_rows: List[QModelIndex] = self.ui.parser_directories_table.selectionModel().selectedRows()
        persistent_rows: List[QPersistentModelIndex] = [QPersistentModelIndex(row) for row in selected_rows]
        for persistent_row in persistent_rows:
            directory = self.staged_parser_directories_model.directory(persistent_row.row())
            self.file_watcher.removePath(str(directory.directory_path))
            self.qparser_directories_model.removeRow(persistent_row.row())
        
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.validate())

    def parser_file_paths(self) -> List[Path]:
        parser_paths: List[Path] = []
        for directory in self.parser_directories_model.parser_directories:
            if directory.enabled:
                parser_paths += [parser_path for parser_path in directory.parser_paths]
        return parser_paths
    
    def validate(self) -> bool:
        parser_directory: EzParserDirectory
        for parser_directory in self.staged_parser_directories_model.parser_directories:
            yaml_file_path = parser_directory.directory_path / K_PARSER_YAML_FILE_NAME
            if not yaml_file_path.exists():
                notify_error_message(self.ui.error_string, f'Yaml file not found at path \"{str(yaml_file_path)}\"!')
                self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                return False

            with yaml_file_path.open("r") as yml:
                try:
                    yaml_data: dict = yaml.safe_load(yml)
                except yaml.YAMLError as exc:
                    notify_error_message(self.ui.error_string, f'Unable to read yaml file \"{str(yaml_file_path)}\" - {exc}')
                    self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    return False
                
                if self.K_PARSER_YAML_KEY not in yaml_data:
                    notify_error_message(self.ui.error_string, f'No key named \"{self.K_PARSER_YAML_KEY}\" in yaml file \"{str(yaml_file_path)}\"!')
                    self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    return False
        
        notify_no_errors(self.ui.error_string)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        return True

    def _polish_parser_directories_table(self):
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserDirectoriesModel.K_PARSER_DIR_COL_INDEX, QHeaderView.Stretch)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserDirectoriesModel.K_PARSERS_LOADED_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.horizontalHeader().setSectionResizeMode(QParserDirectoriesModel.K_CONFIGURE_COL_INDEX, QHeaderView.ResizeToContents)
        self.ui.parser_directories_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
    
    def _update_parsers_list_from_config_file(self, config_file_path: Path):
        directory: EzParserDirectory = create_parser_directory(config_file_path.parent)
        indexes: List[QPersistentModelIndex] = [QPersistentModelIndex(self.parsers_model.index(row, 0)) for row in range(self.parsers_model.rowCount())]
        for index in indexes:
            matched_path = next((parser_path for parser_path in directory.parser_paths if self.parsers_model._parsers[index.row()].parser_path == parser_path), None)
            if matched_path is None:
                self.parsers_model.removeRow(index.row())

        self.parsers_model.load_parsers(directory.parser_paths)
    
    def _update_parsers_list(self):
        self.parsers_model.clear_parsers()
        self.parsers_model.load_parsers(self.parser_file_paths())
    
    def set_parsers_model(self, model: QParsersModel):
        self.parsers_model = model
        self._handle_parser_directories_changed(QModelIndex(), 0, len(self.parser_directories_model.parser_directories) - 1)

    def accept(self):
        self.parser_directories_model.parser_directories = copy.deepcopy(self.staged_parser_directories_model.parser_directories)
        self.parsers_model.clear_parsers()
        self.parsers_model.load_parsers(self.parser_file_paths())
        super().accept()

    def reject(self):
        self.staged_parser_directories_model.parser_directories = copy.deepcopy(self.parser_directories_model.parser_directories)
        self._polish_parser_directories_table()
        for file_path in self.file_watcher.files():
            matching_directory = next((directory for directory in self.parser_directories_model.parser_directories if file_path == str(directory.directory_path / K_PARSER_YAML_FILE_NAME)), None)
            if matching_directory is None:
                self.file_watcher.removePath(file_path)
        super().reject()