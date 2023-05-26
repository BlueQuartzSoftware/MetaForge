# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from metaforge.widgets.createtemplatewidget import CreateTemplateWidget
from metaforge.widgets.usetemplatewidget import UseTemplateWidget

from  . import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1606, 879)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.actionOpenPackage = QAction(MainWindow)
        self.actionOpenPackage.setObjectName(u"actionOpenPackage")
        self.actionOpenPackage.setEnabled(True)
        self.actionSave_Package = QAction(MainWindow)
        self.actionSave_Package.setObjectName(u"actionSave_Package")
        self.actionSave_Package.setEnabled(True)
        self.actionSave_Package_As = QAction(MainWindow)
        self.actionSave_Package_As.setObjectName(u"actionSave_Package_As")
        self.actionSave_Package_As.setEnabled(True)
        self.actionUse_Template = QAction(MainWindow)
        self.actionUse_Template.setObjectName(u"actionUse_Template")
        self.actionUse_Template.setCheckable(True)
        self.actionUse_Template.setEnabled(True)
        self.actionCreate_Template = QAction(MainWindow)
        self.actionCreate_Template.setObjectName(u"actionCreate_Template")
        self.actionCreate_Template.setCheckable(True)
        self.actionCreate_Template.setChecked(True)
        self.actionCreate_Template.setEnabled(True)
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName(u"actionHelp")
        self.actionSave_Template = QAction(MainWindow)
        self.actionSave_Template.setObjectName(u"actionSave_Template")
        self.actionOpen_Template = QAction(MainWindow)
        self.actionOpen_Template.setObjectName(u"actionOpen_Template")
        self.actionPackages = QAction(MainWindow)
        self.actionPackages.setObjectName(u"actionPackages")
        self.actionPackages.setCheckable(True)
        self.actionPackages.setChecked(True)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.action_clear_recent_templates = QAction(MainWindow)
        self.action_clear_recent_templates.setObjectName(u"action_clear_recent_templates")
        self.action_clear_recent_packages = QAction(MainWindow)
        self.action_clear_recent_packages.setObjectName(u"action_clear_recent_packages")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 12, 2, 2)
        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.CreateTemplateTab = QWidget()
        self.CreateTemplateTab.setObjectName(u"CreateTemplateTab")
        self.gridLayout_5 = QGridLayout(self.CreateTemplateTab)
#ifndef Q_OS_MAC
        self.gridLayout_5.setSpacing(-1)
#endif
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.create_template_widget = CreateTemplateWidget(self.CreateTemplateTab)
        self.create_template_widget.setObjectName(u"create_template_widget")

        self.gridLayout_5.addWidget(self.create_template_widget, 0, 0, 1, 1)

        self.tab_widget.addTab(self.CreateTemplateTab, "")
        self.UseTemplateTab = QWidget()
        self.UseTemplateTab.setObjectName(u"UseTemplateTab")
        self.gridLayout_3 = QGridLayout(self.UseTemplateTab)
#ifndef Q_OS_MAC
        self.gridLayout_3.setSpacing(-1)
#endif
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.use_template_widget = UseTemplateWidget(self.UseTemplateTab)
        self.use_template_widget.setObjectName(u"use_template_widget")

        self.gridLayout_3.addWidget(self.use_template_widget, 0, 0, 1, 1)

        self.tab_widget.addTab(self.UseTemplateTab, "")

        self.gridLayout_4.addWidget(self.tab_widget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1606, 24))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menu_recent_templates = QMenu(self.menuFile)
        self.menu_recent_templates.setObjectName(u"menu_recent_templates")
        self.menu_recent_packages = QMenu(self.menuFile)
        self.menu_recent_packages.setObjectName(u"menu_recent_packages")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Template)
        self.menuFile.addAction(self.actionOpenPackage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menu_recent_templates.menuAction())
        self.menuFile.addAction(self.menu_recent_packages.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Template)
        self.menuFile.addAction(self.actionSave_Package)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.actionOpenPackage.setText(QCoreApplication.translate("MainWindow", u"Open Package", None))
#if QT_CONFIG(shortcut)
        self.actionOpenPackage.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_Package.setText(QCoreApplication.translate("MainWindow", u"Save Package", None))
#if QT_CONFIG(shortcut)
        self.actionSave_Package.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_Package_As.setText(QCoreApplication.translate("MainWindow", u"Save Package As", None))
        self.actionUse_Template.setText(QCoreApplication.translate("MainWindow", u"Use Template", None))
        self.actionCreate_Template.setText(QCoreApplication.translate("MainWindow", u"Create Template", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close ", None))
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"Help", None))
#if QT_CONFIG(shortcut)
        self.actionHelp.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+H", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_Template.setText(QCoreApplication.translate("MainWindow", u"Save Template", None))
#if QT_CONFIG(shortcut)
        self.actionSave_Template.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen_Template.setText(QCoreApplication.translate("MainWindow", u"Open Template", None))
#if QT_CONFIG(shortcut)
        self.actionOpen_Template.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionPackages.setText(QCoreApplication.translate("MainWindow", u"Packages", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.action_clear_recent_templates.setText(QCoreApplication.translate("MainWindow", u"Clear Recent Templates", None))
        self.action_clear_recent_packages.setText(QCoreApplication.translate("MainWindow", u"Clear Recent Packages", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.CreateTemplateTab), QCoreApplication.translate("MainWindow", u"Create Template", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.UseTemplateTab), QCoreApplication.translate("MainWindow", u"Use Template", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menu_recent_templates.setTitle(QCoreApplication.translate("MainWindow", u"Recent Templates", None))
        self.menu_recent_packages.setTitle(QCoreApplication.translate("MainWindow", u"Recent Packages", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

