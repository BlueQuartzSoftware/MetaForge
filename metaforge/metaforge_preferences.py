from pathlib import Path
import yaml
import metaforge.widget_utilities as widget_utils
from typing import List
from dataclasses import dataclass
from dataclasses_json import dataclass_json

from PySide2.QtWidgets import QDialog, QDialogButtonBox, QListWidgetItem, QFileDialog, QApplication
import PySide2.QtCore
from PySide2.QtCore import QSettings

from metaforge.definitions import ROOT_DIR

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from metaforge.generated_5_12.ui_metaforge_preferences import Ui_MetaForgePreferences
elif qt_version[1] == 15:
    from metaforge.generated_5_15.ui_metaforge_preferences import Ui_MetaForgePreferences

@dataclass
@dataclass_json
class MetaForgePreferences():
    def __init__(self, default_parser_path, parser_folder_paths):
        self.default_parser_path: str = default_parser_path
        self.parser_folder_paths: List[str] = parser_folder_paths

class MetaForgePreferencesDialog(QDialog):
    K_SETTINGS_USE_DEFAULT_PARSER_LOCATION_KEY = "use_default_parser_location"
    K_SETTINGS_PARSER_PATHS_KEY = "parser_paths"
    K_PARSER_YAML_FILE_NAME = "parsers.yaml"
    K_PARSER_YAML_KEY = "metaforge-parsers"
    K_NO_ERRORS_STR = "No errors."

    def __init__(self, parent=None):
        super(MetaForgePreferencesDialog, self).__init__(parent)
        self.ui = Ui_MetaForgePreferences()
        self.ui.setupUi(self)
        self.current_directory = ''

        self._set_default_parser_location()
        self._read_settings()

        self.ui.addBtn.pressed.connect(self._add_files)
        self.ui.removeBtn.pressed.connect(self._remove_selected_files)
        self.ui.include_default_parser_location.stateChanged.connect(self._toggle_default_parser_location)

        self.ui.buttonBox.button(QDialogButtonBox.Ok).pressed.connect(self.accept)
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).pressed.connect(self.reject)

        widget_utils.notify_no_errors(self.ui.error_string)
    
    def _set_default_parser_location(self):
        default_location = Path(ROOT_DIR) / 'parsers'
        self.ui.include_default_parser_location.setText(str(default_location))
    
    def _toggle_default_parser_location(self, state: PySide2.QtCore.Qt.CheckState):
        if state == PySide2.QtCore.Qt.CheckState.Checked:
            self.staged_prefs.default_parser_path = self.ui.include_default_parser_location.text()
        else:
            self.staged_prefs.default_parser_path = None
    
    def _read_settings(self):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        parser_folder_paths: List[str] = []
        use_default_location = settings.value(self.K_SETTINGS_USE_DEFAULT_PARSER_LOCATION_KEY, defaultValue=True, type=bool)
        self.ui.include_default_parser_location.setChecked(use_default_location)
        default_parser_path = None
        if use_default_location:
            default_parser_path = self.ui.include_default_parser_location.text()

        parser_folder_size = settings.beginReadArray(self.K_SETTINGS_PARSER_PATHS_KEY)
        for i in range(parser_folder_size):
            settings.setArrayIndex(i)
            parser_path = settings.value(f'{i}')
            parser_folder_paths.append(parser_path)
        settings.endArray()

        self.ui.parser_locations_list.addItems(parser_folder_paths)
        self.prefs = MetaForgePreferences(default_parser_path, parser_folder_paths)
        self.staged_prefs = MetaForgePreferences(default_parser_path, parser_folder_paths)
    
    def closeEvent(self, event):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        settings.setValue(self.K_SETTINGS_USE_DEFAULT_PARSER_LOCATION_KEY, self.ui.include_default_parser_location.isChecked())

        parser_folder_paths = self.prefs.parser_folder_paths
        settings.beginWriteArray(self.K_SETTINGS_PARSER_PATHS_KEY)
        for i in range(len(parser_folder_paths)):
            parser_path = parser_folder_paths[i]
            settings.setArrayIndex(i)
            settings.setValue(f'{i}', parser_path)
        settings.endArray()

        super().closeEvent(event)
    
    def exec(self) -> int:
        self.ui.parser_locations_list.clear()
        [self.ui.parser_locations_list.addItem(path) for path in self.prefs.parser_folder_paths]

        return super().exec_()
    
    def _add_files(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Open Directory', self.current_directory)
        if dir_path != "":
            self.current_directory = dir_path
            self.ui.parser_locations_list.addItem(dir_path)
            self.staged_prefs.parser_folder_paths.append(dir_path)

            self.validate()

    def _remove_selected_files(self):
        selected_items: List[QListWidgetItem] = self.ui.parser_locations_list.selectedItems()
        for item in selected_items:
            self.ui.parser_locations_list.takeItem(self.ui.parser_locations_list.row(item))
            self.staged_prefs.parser_folder_paths.remove(item.text())
        
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.validate())
    
    def preferences(self) -> MetaForgePreferences:
        return self.prefs
    
    def validate(self) -> bool:
        for parser_folder_path in self.staged_prefs.parser_folder_paths:
            parser_folder_path = Path(parser_folder_path)
            yaml_file_path = parser_folder_path / self.K_PARSER_YAML_FILE_NAME
            if not yaml_file_path.exists():
                widget_utils.notify_error_message(self.ui.error_string, f'Yaml file not found at path \"{str(yaml_file_path)}\"!')
                self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                return False

            with yaml_file_path.open("r") as yml:
                try:
                    yaml_data: dict = yaml.safe_load(yml)
                except yaml.YAMLError as exc:
                    widget_utils.notify_error_message(self.ui.error_string, f'Unable to read yaml file \"{str(yaml_file_path)}\" - {exc}')
                    self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    return False
                
                if self.K_PARSER_YAML_KEY not in yaml_data:
                    widget_utils.notify_error_message(self.ui.error_string, f'No key named \"{self.K_PARSER_YAML_KEY}\" in yaml file \"{str(yaml_file_path)}\"!')
                    self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                    return False
        
        widget_utils.notify_no_errors(self.ui.error_string)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        return True

    def accept(self):
        self.prefs = self.staged_prefs
        super().accept()

    def reject(self):
        self.staged_prefs = self.prefs
        super().reject()