# This Python file uses the following encoding: utf-8
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenu
from PySide6.QtCore import QStandardPaths, QSettings, Slot
from PySide6.QtGui import QDesktopServices, QAction
import PySide6.QtCore
from typing import List

from metaforge.widgets.aboutdialogimpl import AboutDialogImpl
from metaforge.widgets.metaforge_preferences import MetaForgePreferencesDialog
from metaforge.common.metaforgestyledatahelper import MetaForgeStyleDataHelper
from metaforge.qt_models.qparsercomboboxmodel import QParserComboBoxModel
from metaforge.qt_models.qparsertablemodel import QParserTableModel
from metaforge.models.parsermodel import ParserModel

from metaforge.widgets.generated_6_5.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    K_MAX_RECENT_TEMPLATE_SIZE = 10
    K_MAX_RECENT_PACKAGE_SIZE = 10
    K_CLEAR_RECENT_TEMPLATES_STR = "Clear Recent Templates"
    K_CLEAR_RECENT_PACKAGES_STR = "Clear Recent Packages"
    K_SETTINGS_GEOMETRY_KEY = "geometry"
    K_SETTINGS_WINDOW_STATE_KEY = "window_state"
    K_SETTINGS_RECENT_TEMPLATES_KEY = "recent_templates"
    K_SETTINGS_RECENT_PACKAGES_KEY = "recent_packages"
    K_SETTINGS_PARSER_MODEL_KEY = "parser_model"

    def __init__(self, app: QApplication):
        super(MainWindow, self).__init__()
        
        self.style_sheet_helper: MetaForgeStyleDataHelper = MetaForgeStyleDataHelper(app)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tab_widget.setCurrentWidget(self.ui.CreateTemplateTab)
        self.preferences_dialog = MetaForgePreferencesDialog(self)
        self.ui.create_template_widget.ui.saveTemplateButton.clicked.connect(self.save_template)
        self.ui.actionHelp.triggered.connect(self.display_help)
        self.ui.actionAbout.triggered.connect(self.display_about)
        self.ui.actionOpenPackage.triggered.connect(self.open_package)
        self.ui.actionSave_Package.triggered.connect(self.save_package)
        self.ui.actionSave_Package_As_2.triggered.connect(self.save_package_as)
        self.ui.actionClose.triggered.connect(self.close)
        self.ui.actionSave_Template.triggered.connect(self.save_template)
        self.ui.actionSave_Template_As.triggered.connect(self.save_template_as)
        self.ui.actionOpen_Template.triggered.connect(self.open_template)
        self.saved_template_path: Path = None
        self.saved_package_path: Path = None

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

        # Read settings
        self.read_settings()

        # Create the ez parser model and the qt parser models, and set them into the widgets
        self.qparsers_cb_model = QParserComboBoxModel(self.ez_parser_model, self.ui.create_template_widget)
        self.qparser_table_model = QParserTableModel(self.ez_parser_model, self.preferences_dialog)
        self.qparser_table_model.model_about_to_change.connect(self.qparsers_cb_model.modelAboutToBeReset)
        self.qparser_table_model.model_changed.connect(self.qparsers_cb_model.modelReset)
        self.ui.create_template_widget.set_parsers_model(self.qparsers_cb_model)
        self.ui.use_template_widget.set_parsers_model(self.ez_parser_model)
        self.preferences_dialog.set_parsers_model(self.qparser_table_model)
    
    def read_settings(self):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        self.read_window_settings(settings)
        recent_templates = settings.value(self.K_SETTINGS_RECENT_TEMPLATES_KEY)
        recent_packages = settings.value(self.K_SETTINGS_RECENT_PACKAGES_KEY)

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
        
        parser_dir_model_json = settings.value(self.K_SETTINGS_PARSER_MODEL_KEY, defaultValue="", type=str)
        self.ez_parser_model = ParserModel()
        if parser_dir_model_json != "":
            self.ez_parser_model: ParserModel = ParserModel.from_json(parser_dir_model_json)

    def read_window_settings(self, settings):
        self.restoreGeometry(settings.value(self.K_SETTINGS_GEOMETRY_KEY))
        self.restoreState(settings.value(self.K_SETTINGS_WINDOW_STATE_KEY))

    def closeEvent(self, event):
        settings = QSettings(QApplication.organizationName(), QApplication.applicationName())
        settings.setValue(self.K_SETTINGS_GEOMETRY_KEY, self.saveGeometry())
        settings.setValue(self.K_SETTINGS_WINDOW_STATE_KEY, self.saveState())

        recent_template_list = [action.text() for action in self.recent_template_list]
        settings.setValue(self.K_SETTINGS_RECENT_TEMPLATES_KEY, recent_template_list)

        recent_package_list = [action.text() for action in self.recent_package_list]
        settings.setValue(self.K_SETTINGS_RECENT_PACKAGES_KEY, recent_package_list)

        model_json = self.ez_parser_model.to_json()
        settings.setValue(self.K_SETTINGS_PARSER_MODEL_KEY, model_json)

        self.ui.create_template_widget.close()
        self.ui.use_template_widget.close()
        self.preferences_dialog.close()

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
        self.preferences_dialog.exec()

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
            self.saved_template_path = Path(template_file_path)

    @Slot(str, result=None)
    def _open_template(self, file_path: str):
        self.ui.create_template_widget.load_template_file(template_file_path=Path(file_path))

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

    def _save_template(self, file_path: Path):
        self.ui.create_template_widget.save_template(str(file_path))
        self.ui.statusbar.showMessage(f"Template saved successfully to '{str(file_path)}'.", 10000)

    def save_template(self):
        if self.saved_template_path is None:
            self.save_template_as()
        else:
            self._save_template(self.saved_template_path)
    
    def save_template_as(self):
        dialog = QFileDialog(self, "Save Template", "", "Templates (*.ez)")
        dialog.setDefaultSuffix(".ez")
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_path = ""
        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
        if file_path != "":
            self.saved_template_path = Path(file_path)
            self._save_template(self.saved_template_path)

    def open_package(self):
        pkgpath = QFileDialog.getExistingDirectory(self, caption=self.tr("Select MetaForge Package"), dir=QStandardPaths.displayName(
            QStandardPaths.HomeLocation))
        if pkgpath != "":
            self._open_package(pkgpath)
            self.saved_package_path = Path(pkgpath)
    
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

    def _save_package(self, file_path: Path):
        self.ui.use_template_widget.save_package(file_path)
        self.ui.statusbar.showMessage(f"Package saved successfully to '{str(file_path)}'.", 10000)

    def save_package(self):
        if self.saved_package_path:
            self._save_package(self.saved_package_path)
        else:
            self.save_package_as()
    
    def save_package_as(self):
        result = QFileDialog.getSaveFileName(self, "Save File",
                                               "/Packages/",
                                               "Packages (*.ezp)")
        pkgpath = result[0]
        if pkgpath != "":
            self.saved_package_path = Path(pkgpath)
            self._save_package(self.saved_package_path)

