# This Python file uses the following encoding: utf-8
from pathlib import Path
import yaml

from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QAction, QMenu, QDialog
from PySide2.QtCore import QStandardPaths, QSettings, Slot
from PySide2.QtGui import QDesktopServices
import PySide2.QtCore
from typing import List

from aboutdialogimpl import AboutDialogImpl
from metaforge_preferences import MetaForgePreferencesDialog, MetaForgePreferences
from metaforgestyledatahelper import MetaForgeStyleDataHelper
from available_parsers_model import AvailableParsersModel

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from generated_5_12.ui_mainwindow import Ui_MainWindow
elif qt_version[1] == 15:
    from generated_5_15.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    K_MAX_RECENT_TEMPLATE_SIZE = 10
    K_MAX_RECENT_PACKAGE_SIZE = 10
    K_CLEAR_RECENT_TEMPLATES_STR = "Clear Recent Templates"
    K_CLEAR_RECENT_PACKAGES_STR = "Clear Recent Packages"
    K_PARSER_YAML_FILE_NAME = "parsers.yaml"
    K_PARSER_YAML_KEY = "metaforge-parsers"

    def __init__(self, app: QApplication):
        super(MainWindow, self).__init__()
        
        self.style_sheet_helper: MetaForgeStyleDataHelper = MetaForgeStyleDataHelper(app)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tab_widget.setCurrentWidget(self.ui.CreateTemplateTab)
        self.preferences_dialog = MetaForgePreferencesDialog(self)
        self.available_parsers_model = AvailableParsersModel(self)
        self.ui.create_template_widget.ui.saveTemplateButton.clicked.connect(self.save_template)
        self.ui.actionHelp.triggered.connect(self.display_help)
        self.ui.actionAbout.triggered.connect(self.display_about)
        self.ui.actionOpenPackage.triggered.connect(self.open_package)
        self.ui.actionSave_Package.triggered.connect(self.save_package)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionSave_Template.triggered.connect(self.save_template)
        self.ui.actionOpen_Template.triggered.connect(self.open_template)

        self.action_recent_templates_separator: QAction = self.ui.menu_recent_templates.addSeparator()
        self.action_recent_templates: QAction = self.ui.menu_recent_templates.addAction(self.K_CLEAR_RECENT_TEMPLATES_STR, self.clear_recent_templates)
        self.action_recent_packages_separator: QAction = self.ui.menu_recent_packages.addSeparator()
        self.action_recent_packages: QAction = self.ui.menu_recent_packages.addAction(self.K_CLEAR_RECENT_PACKAGES_STR, self.clear_recent_packages)
        self.recent_template_list: List[QAction] = []
        self.recent_package_list: List[QAction] = []

        self.action_preferences: QAction = QAction("Preferences")
        self.action_preferences.triggered.connect(self.display_preferences)
        self.action_preferences.setMenuRole(QAction.PreferencesRole)
        self.ui.menuFile.addAction(self.action_preferences)

        # Load the parsers
        parser_file_paths = self._parser_file_paths()
        self.available_parsers_model.load_parsers(parser_file_paths)

        # Set the parsers model down into the Create Template and Use Template widgets
        self.ui.create_template_widget.set_parsers_model(self.available_parsers_model)
        self.ui.use_template_widget.set_parsers_model(self.available_parsers_model)

        # Read settings
        self.read_settings()
    
    def read_settings(self):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        self.read_window_settings(settings)
        recent_templates = settings.value("recent_templates")
        recent_packages = settings.value("recent_packages")

        if recent_templates is not None:
            for file_path in recent_templates:
                action = QAction(file_path)
                action.triggered.connect(lambda triggered=False, file_path=file_path: self._open_template(file_path))
                self.add_recent_action(self.ui.menu_recent_templates, self.recent_template_list, self.action_recent_templates_separator, self.ui.action_clear_recent_templates, action)

        if recent_packages is not None:
            for file_path in recent_packages:
                action = QAction(file_path)
                action.triggered.connect(lambda triggered=False, pkg_file_path=Path(file_path): self.ui.use_template_widget.open_package(pkg_file_path))
                self.add_recent_action(self.ui.menu_recent_packages, self.recent_package_list, self.action_recent_packages_separator, self.ui.action_clear_recent_packages, action)

    def read_window_settings(self, settings):
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("window_state"))

    def closeEvent(self, event):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("window_state", self.saveState())

        recent_template_list = [action.text() for action in self.recent_template_list]
        settings.setValue("recent_templates", recent_template_list)

        recent_package_list = [action.text() for action in self.recent_package_list]
        settings.setValue("recent_packages", recent_package_list)

        self.ui.create_template_widget.close()
        self.ui.use_template_widget.close()

        super().closeEvent(event)
    
    def add_recent_action(self, recent_menu: QMenu, recent_list: List[QAction], separator_action: QAction, clear_action: QAction, action: QAction, index: int = -1):
        if index == -1 or (index == 0 and len(recent_list) == 0):
            index = len(recent_list)
            before_action = separator_action
        else:
            before_action = recent_list[index]
        recent_list.insert(index, action)
        recent_menu.insertAction(before_action, action)
        if len(recent_list) > 0:
            clear_action.setEnabled(True)
    
    def remove_recent_action(self, recent_menu: QMenu, recent_list: List[QAction], clear_action: QAction, action: QAction):
        recent_menu.removeAction(action)
        recent_list.remove(action)

        if len(recent_list) == 0:
            clear_action.setDisabled(True)
    
    def clear_recent_templates(self):
        [self.ui.menu_recent_templates.removeAction(action) for action in self.recent_template_list]
        self.recent_template_list.clear()
        self.ui.action_clear_recent_templates.setDisabled(True)
    
    def clear_recent_packages(self):
        [self.ui.menu_recent_packages.removeAction(action) for action in self.recent_package_list]
        self.recent_package_list.clear()
        self.ui.action_clear_recent_packages.setDisabled(True)
    
    def display_preferences(self):
        result: QDialog.DialogCode = self.preferences_dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            parser_file_paths = self._parser_file_paths()

            self.available_parsers_model.clear_parsers()
            self.available_parsers_model.load_parsers(parser_file_paths)
    
    def _parser_file_paths(self) -> List[Path]:
        prefs: MetaForgePreferences = self.preferences_dialog.preferences()
        parser_folder_paths = [Path(path) for path in prefs.parser_folder_paths]
        parser_file_paths = []
        for parser_folder_path in parser_folder_paths:
            parser_file_paths = parser_file_paths + self._find_parser_files(parser_folder_path)
        return parser_file_paths

    def _find_parser_files(self, parser_folder_path: Path) -> List[Path]:
        yaml_file_path = parser_folder_path / self.K_PARSER_YAML_FILE_NAME
        with yaml_file_path.open("r") as yml:
            yaml_data: dict = yaml.safe_load(yml)
            return [parser_folder_path / file_name for file_name in yaml_data[self.K_PARSER_YAML_KEY]]

    def display_about(self):
        aboutDialog = AboutDialogImpl(self)
        aboutDialog.exec()

    def display_help(self):
        QDesktopServices.openUrl("http://www.bluequartz.net/")
    
    def open_template(self):
        # open template
        template_file_path = QFileDialog.getOpenFileName(self, self.tr("Select File"), QStandardPaths.displayName(
            QStandardPaths.HomeLocation), self.tr("Files (*.ez)"))[0]
        if template_file_path != "":
            self._open_template(template_file_path)

    @Slot(str, result=None)
    def _open_template(self, file_path: str):
        self.ui.create_template_widget.load_template(template_file_path=Path(file_path))

        # Find action in the list and remove it (if it's there)
        for action in self.recent_template_list:
            if action.text() == file_path:
                self.remove_recent_action(self.ui.menu_recent_templates, self.recent_template_list, self.ui.action_clear_recent_templates, action)

        # Add action to the top of the list
        action = QAction(file_path)
        action.triggered.connect(lambda triggered=False, file_path=file_path: self._open_template(file_path))
        self.add_recent_action(self.ui.menu_recent_templates, self.recent_template_list, self.action_recent_templates_separator, self.ui.action_clear_recent_templates, action, 0)

        # Remove last action if the action list is greater than the max
        if len(self.recent_template_list) > self.K_MAX_RECENT_TEMPLATE_SIZE:
            action = self.recent_template_list[len(self.recent_template_list) - 1]
            self.remove_recent_action(self.ui.menu_recent_templates, self.recent_template_list, self.ui.action_clear_recent_templates, action)
        
        # Change the tab to the "Create Template" section
        self.ui.tab_widget.setCurrentIndex(0)

    def save_template(self):
        dialog = QFileDialog(self, "Save File", "", "Templates (*.ez)")
        dialog.setDefaultSuffix(".ez")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_path = ""
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
        if file_path != "":
            self.ui.create_template_widget.save_template(file_path)
            self.ui.statusbar.showMessage(f"Template saved successfully to '{file_path}'.", 10000)

    def open_package(self):
        pkgpath = QFileDialog.getExistingDirectory(self, caption=self.tr("Select MetaForge Package"), dir=QStandardPaths.displayName(
            QStandardPaths.HomeLocation))
        if pkgpath != "":
            self._open_package(pkgpath)
    
    @Slot(str, result=None)
    def _open_package(self, pkgpath: str):
        pkgpath = Path(pkgpath)
        self.ui.use_template_widget.open_package(pkgpath)

        # Find action in the list and remove it (if it's there)
        for action in self.recent_package_list:
            if action.text() == str(pkgpath):
                self.remove_recent_action(self.ui.menu_recent_packages, self.recent_package_list, self.ui.action_clear_recent_packages, action)

        # Add action to the top of the list
        action = QAction(str(pkgpath))
        action.triggered.connect(lambda triggered=False, file_path=str(pkgpath): self._open_package(file_path))
        self.add_recent_action(self.ui.menu_recent_packages, self.recent_package_list, self.action_recent_packages_separator, self.ui.action_clear_recent_packages, action, 0)

        # Remove last action if the action list is greater than the max
        if len(self.recent_package_list) > self.K_MAX_RECENT_PACKAGE_SIZE:
            action = self.recent_package_list[len(self.recent_package_list) - 1]
            self.remove_recent_action(self.ui.menu_recent_packages, self.recent_package_list, self.ui.action_clear_recent_packages, action)
        
        # Change the tab to the "Use Template" section
        self.ui.tab_widget.setCurrentIndex(1)

    def save_package(self):
        result = QFileDialog.getSaveFileName(self, "Save File",
                                               "/Packages/",
                                               "Packages (*.ezp)")
        pkgpath = result[0]
        if pkgpath != "":
            self.ui.use_template_widget.save_package(Path(pkgpath))

