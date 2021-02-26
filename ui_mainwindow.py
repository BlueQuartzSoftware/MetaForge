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
        MainWindow.resize(1231, 683)
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
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.dateFileLabel = QLabel(self.centralwidget)
        self.dateFileLabel.setObjectName(u"dateFileLabel")

        self.horizontalLayout_2.addWidget(self.dateFileLabel)

        self.datafileLineEdit = QLineEdit(self.centralwidget)
        self.datafileLineEdit.setObjectName(u"datafileLineEdit")

        self.horizontalLayout_2.addWidget(self.datafileLineEdit)

        self.dataFileSelect = QPushButton(self.centralwidget)
        self.dataFileSelect.setObjectName(u"dataFileSelect")

        self.horizontalLayout_2.addWidget(self.dataFileSelect)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dataTypeLabel = QLabel(self.centralwidget)
        self.dataTypeLabel.setObjectName(u"dataTypeLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataTypeLabel.sizePolicy().hasHeightForWidth())
        self.dataTypeLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.dataTypeLabel)

        self.dataTypeText = QLabel(self.centralwidget)
        self.dataTypeText.setObjectName(u"dataTypeText")

        self.horizontalLayout_3.addWidget(self.dataTypeText)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileParserLabel = QLabel(self.centralwidget)
        self.fileParserLabel.setObjectName(u"fileParserLabel")

        self.horizontalLayout.addWidget(self.fileParserLabel)

        self.fileParserCombo = QComboBox(self.centralwidget)
        self.fileParserCombo.addItem("")
        self.fileParserCombo.addItem("")
        self.fileParserCombo.addItem("")
        self.fileParserCombo.setObjectName(u"fileParserCombo")

        self.horizontalLayout.addWidget(self.fileParserCombo)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.metadataTableView = QTableView(self.centralwidget)
        self.metadataTableView.setObjectName(u"metadataTableView")
        self.metadataTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTableView.setAlternatingRowColors(True)
        self.metadataTableView.horizontalHeader().setStretchLastSection(False)

        self.gridLayout.addWidget(self.metadataTableView, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1231, 22))
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
        self.gridLayout_3 = QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.treeView = QTreeView(self.dockWidgetContents)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.gridLayout_3.addWidget(self.treeView, 0, 0, 1, 1)

        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget_3 = QDockWidget(MainWindow)
        self.dockWidget_3.setObjectName(u"dockWidget_3")
        self.dockWidget_3.setMinimumSize(QSize(364, 100))
        self.dockWidgetContents_3 = QWidget()
        self.dockWidgetContents_3.setObjectName(u"dockWidgetContents_3")
        self.gridLayout_2 = QGridLayout(self.dockWidgetContents_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.hyperthoughtLabel = QLabel(self.dockWidgetContents_3)
        self.hyperthoughtLabel.setObjectName(u"hyperthoughtLabel")

        self.gridLayout_2.addWidget(self.hyperthoughtLabel, 0, 0, 1, 1)

        self.hyperthoughtLineEdit = QLineEdit(self.dockWidgetContents_3)
        self.hyperthoughtLineEdit.setObjectName(u"hyperthoughtLineEdit")

        self.gridLayout_2.addWidget(self.hyperthoughtLineEdit, 0, 1, 1, 1)

        self.hyperthoughtSelectButton = QPushButton(self.dockWidgetContents_3)
        self.hyperthoughtSelectButton.setObjectName(u"hyperthoughtSelectButton")

        self.gridLayout_2.addWidget(self.hyperthoughtSelectButton, 0, 2, 1, 1)

        self.hyperthoughtUploadButton = QPushButton(self.dockWidgetContents_3)
        self.hyperthoughtUploadButton.setObjectName(u"hyperthoughtUploadButton")

        self.gridLayout_2.addWidget(self.hyperthoughtUploadButton, 1, 2, 1, 1)

        self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidget_3)

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
        self.dateFileLabel.setText(QCoreApplication.translate("MainWindow", u"Date File:", None))
        self.datafileLineEdit.setText(QCoreApplication.translate("MainWindow", u"/Users/Somebody/Desktop/SomeFile.xml ", None))
        self.dataFileSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.dataTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Data Type Detected:", None))
        self.dataTypeText.setText(QCoreApplication.translate("MainWindow", u"XML", None))
        self.fileParserLabel.setText(QCoreApplication.translate("MainWindow", u"File Parser:", None))
        self.fileParserCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"XML Parser", None))
        self.fileParserCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"ANG Parser", None))
        self.fileParserCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"Custom Parser", None))

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
        self.hyperthoughtLabel.setText(QCoreApplication.translate("MainWindow", u"Hyperthought Upload Path:", None))
        self.hyperthoughtLineEdit.setText(QCoreApplication.translate("MainWindow", u"Please select a path to upload to Hyperthought.", None))
        self.hyperthoughtSelectButton.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.hyperthoughtUploadButton.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
    # retranslateUi

