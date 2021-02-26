# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionOpenPackage = QAction(MainWindow)
        self.actionOpenPackage.setObjectName(u"actionOpenPackage")
        self.actionOpen_Recent = QAction(MainWindow)
        self.actionOpen_Recent.setObjectName(u"actionOpen_Recent")
        self.actionSave_Package = QAction(MainWindow)
        self.actionSave_Package.setObjectName(u"actionSave_Package")
        self.actionSave_Package_As = QAction(MainWindow)
        self.actionSave_Package_As.setObjectName(u"actionSave_Package_As")
        self.actionUse_Template = QAction(MainWindow)
        self.actionUse_Template.setObjectName(u"actionUse_Template")
        self.actionCreate_Template = QAction(MainWindow)
        self.actionCreate_Template.setObjectName(u"actionCreate_Template")
        self.actionClose = QAction(MainWindow)
        self.actionClose.setObjectName(u"actionClose")
        self.actionHelp = QAction(MainWindow)
        self.actionHelp.setObjectName(u"actionHelp")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.metadataTableView = QTableView(self.centralwidget)
        self.metadataTableView.setObjectName(u"metadataTableView")
        self.metadataTableView.setAlternatingRowColors(True)
        self.metadataTableView.horizontalHeader().setStretchLastSection(True)

        self.gridLayout.addWidget(self.metadataTableView, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout_2 = QGridLayout(self.dockWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.treeView = QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName(u"treeView")

        self.gridLayout_2.addWidget(self.treeView, 0, 0, 1, 1)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpenPackage)
        self.menuFile.addAction(self.actionOpen_Recent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Package)
        self.menuFile.addAction(self.actionSave_Package_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionHelp)
        self.toolBar.addAction(self.actionUse_Template)
        self.toolBar.addAction(self.actionCreate_Template)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpenPackage.setText(QCoreApplication.translate("MainWindow", u"Open Package", None))
        self.actionOpen_Recent.setText(QCoreApplication.translate("MainWindow", u"Open Recent", None))
        self.actionSave_Package.setText(QCoreApplication.translate("MainWindow", u"Save Package", None))
        self.actionSave_Package_As.setText(QCoreApplication.translate("MainWindow", u"Save Package As", None))
        self.actionUse_Template.setText(QCoreApplication.translate("MainWindow", u"Use Template", None))
        self.actionCreate_Template.setText(QCoreApplication.translate("MainWindow", u"Create Template", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close ", None))
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

