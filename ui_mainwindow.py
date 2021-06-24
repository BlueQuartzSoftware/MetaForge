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

import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1328, 749)
        MainWindow.setMinimumSize(QSize(0, 0))
        self.actionOpenPackage = QAction(MainWindow)
        self.actionOpenPackage.setObjectName(u"actionOpenPackage")
        self.actionOpenPackage.setEnabled(True)
        self.actionOpen_Recent = QAction(MainWindow)
        self.actionOpen_Recent.setObjectName(u"actionOpen_Recent")
        self.actionOpen_Recent.setEnabled(False)
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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setSpacing(4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(2, 12, 2, 2)
        self.TabWidget = QTabWidget(self.centralwidget)
        self.TabWidget.setObjectName(u"TabWidget")
        self.CreateTemplateTab = QWidget()
        self.CreateTemplateTab.setObjectName(u"CreateTemplateTab")
        self.gridLayout_5 = QGridLayout(self.CreateTemplateTab)
        self.gridLayout_5.setSpacing(2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, -1, 4, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(9)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.CreateTemplateTab)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.dataFileLineEdit = QLineEdit(self.CreateTemplateTab)
        self.dataFileLineEdit.setObjectName(u"dataFileLineEdit")
        self.dataFileLineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.dataFileLineEdit)

        self.dataFileSelect = QPushButton(self.CreateTemplateTab)
        self.dataFileSelect.setObjectName(u"dataFileSelect")

        self.horizontalLayout_2.addWidget(self.dataFileSelect)


        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dataTypeLabel = QLabel(self.CreateTemplateTab)
        self.dataTypeLabel.setObjectName(u"dataTypeLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dataTypeLabel.sizePolicy().hasHeightForWidth())
        self.dataTypeLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.dataTypeLabel)

        self.dataTypeText = QLabel(self.CreateTemplateTab)
        self.dataTypeText.setObjectName(u"dataTypeText")

        self.horizontalLayout_3.addWidget(self.dataTypeText)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileParserLabel = QLabel(self.CreateTemplateTab)
        self.fileParserLabel.setObjectName(u"fileParserLabel")
        sizePolicy1.setHeightForWidth(self.fileParserLabel.sizePolicy().hasHeightForWidth())
        self.fileParserLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.fileParserLabel)

        self.fileParserCombo = QComboBox(self.CreateTemplateTab)
        self.fileParserCombo.addItem("")
        self.fileParserCombo.addItem("")
        self.fileParserCombo.addItem("")
        self.fileParserCombo.setObjectName(u"fileParserCombo")

        self.horizontalLayout.addWidget(self.fileParserCombo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.appendCreateTableRowButton = QToolButton(self.CreateTemplateTab)
        self.appendCreateTableRowButton.setObjectName(u"appendCreateTableRowButton")
        icon = QIcon()
        icon.addFile(u":/resources/plus@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appendCreateTableRowButton.setIcon(icon)
        self.appendCreateTableRowButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.appendCreateTableRowButton)

        self.removeCreateTableRowButton = QToolButton(self.CreateTemplateTab)
        self.removeCreateTableRowButton.setObjectName(u"removeCreateTableRowButton")
        icon1 = QIcon()
        icon1.addFile(u":/resources/delete@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeCreateTableRowButton.setIcon(icon1)
        self.removeCreateTableRowButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout.addWidget(self.removeCreateTableRowButton)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.gridLayout_5.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.widget_3 = QWidget(self.CreateTemplateTab)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_9 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_5.addWidget(self.widget_3, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.metadataTreeView = QTreeView(self.CreateTemplateTab)
        self.metadataTreeView.setObjectName(u"metadataTreeView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.metadataTreeView.sizePolicy().hasHeightForWidth())
        self.metadataTreeView.setSizePolicy(sizePolicy2)
        self.metadataTreeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTreeView.setAlternatingRowColors(True)

        self.gridLayout.addWidget(self.metadataTreeView, 1, 0, 1, 1)

        self.metadataTableView = QTableView(self.CreateTemplateTab)
        self.metadataTableView.setObjectName(u"metadataTableView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.metadataTableView.sizePolicy().hasHeightForWidth())
        self.metadataTableView.setSizePolicy(sizePolicy3)
        self.metadataTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTableView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked)
        self.metadataTableView.setProperty("showDropIndicator", False)
        self.metadataTableView.setDragDropOverwriteMode(False)
        self.metadataTableView.setAlternatingRowColors(True)
        self.metadataTableView.setSortingEnabled(True)
        self.metadataTableView.setCornerButtonEnabled(False)
        self.metadataTableView.horizontalHeader().setStretchLastSection(False)
        self.metadataTableView.verticalHeader().setVisible(False)
        self.metadataTableView.verticalHeader().setMinimumSectionSize(15)

        self.gridLayout.addWidget(self.metadataTableView, 1, 1, 1, 1)

        self.createTemplateListSearchBar = QLineEdit(self.CreateTemplateTab)
        self.createTemplateListSearchBar.setObjectName(u"createTemplateListSearchBar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.createTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.createTemplateListSearchBar.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.createTemplateListSearchBar, 0, 1, 1, 1)

        self.createTemplateTreeSearchBar = QLineEdit(self.CreateTemplateTab)
        self.createTemplateTreeSearchBar.setObjectName(u"createTemplateTreeSearchBar")

        self.gridLayout.addWidget(self.createTemplateTreeSearchBar, 0, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout, 3, 1, 1, 1)

        self.widget = QWidget(self.CreateTemplateTab)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_11 = QHBoxLayout(self.widget)
        self.horizontalLayout_11.setSpacing(2)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(2, 2, 2, 2)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 0))
        self.horizontalLayout_10 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(4, 4, 4, 4)
        self.horizontalSpacer_5 = QSpacerItem(1227, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.saveTemplateButton = QPushButton(self.widget_2)
        self.saveTemplateButton.setObjectName(u"saveTemplateButton")

        self.horizontalLayout_10.addWidget(self.saveTemplateButton)


        self.horizontalLayout_11.addWidget(self.widget_2)


        self.gridLayout_5.addWidget(self.widget, 4, 0, 1, 2)

        self.TabWidget.addTab(self.CreateTemplateTab, "")
        self.UseTemplateTab = QWidget()
        self.UseTemplateTab.setObjectName(u"UseTemplateTab")
        self.gridLayout_3 = QGridLayout(self.UseTemplateTab)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(10)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, -1, 0, 0)
        self.label = QLabel(self.UseTemplateTab)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.useTemplateListView = QListView(self.UseTemplateTab)
        self.useTemplateListView.setObjectName(u"useTemplateListView")
        sizePolicy2.setHeightForWidth(self.useTemplateListView.sizePolicy().hasHeightForWidth())
        self.useTemplateListView.setSizePolicy(sizePolicy2)
        self.useTemplateListView.setMinimumSize(QSize(325, 0))
        self.useTemplateListView.setAcceptDrops(True)
        self.useTemplateListView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.useTemplateListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.useTemplateListView.setAlternatingRowColors(False)

        self.verticalLayout_2.addWidget(self.useTemplateListView)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setSpacing(2)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, -1, 0, 0)
        self.addUploadFilesBtn = QPushButton(self.UseTemplateTab)
        self.addUploadFilesBtn.setObjectName(u"addUploadFilesBtn")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.addUploadFilesBtn.sizePolicy().hasHeightForWidth())
        self.addUploadFilesBtn.setSizePolicy(sizePolicy5)
        self.addUploadFilesBtn.setIcon(icon)

        self.horizontalLayout_14.addWidget(self.addUploadFilesBtn)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_4)

        self.clearUploadFilesBtn = QPushButton(self.UseTemplateTab)
        self.clearUploadFilesBtn.setObjectName(u"clearUploadFilesBtn")
        sizePolicy5.setHeightForWidth(self.clearUploadFilesBtn.sizePolicy().hasHeightForWidth())
        self.clearUploadFilesBtn.setSizePolicy(sizePolicy5)

        self.horizontalLayout_14.addWidget(self.clearUploadFilesBtn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_13.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.hyperthoughtTemplateLabel = QLabel(self.UseTemplateTab)
        self.hyperthoughtTemplateLabel.setObjectName(u"hyperthoughtTemplateLabel")
        sizePolicy6 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.hyperthoughtTemplateLabel.sizePolicy().hasHeightForWidth())
        self.hyperthoughtTemplateLabel.setSizePolicy(sizePolicy6)

        self.horizontalLayout_5.addWidget(self.hyperthoughtTemplateLabel)

        self.hyperthoughtTemplateLineEdit = QLineEdit(self.UseTemplateTab)
        self.hyperthoughtTemplateLineEdit.setObjectName(u"hyperthoughtTemplateLineEdit")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(2)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.hyperthoughtTemplateLineEdit.sizePolicy().hasHeightForWidth())
        self.hyperthoughtTemplateLineEdit.setSizePolicy(sizePolicy7)
        self.hyperthoughtTemplateLineEdit.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.hyperthoughtTemplateLineEdit)

        self.hyperthoughtTemplateSelect = QPushButton(self.UseTemplateTab)
        self.hyperthoughtTemplateSelect.setObjectName(u"hyperthoughtTemplateSelect")

        self.horizontalLayout_5.addWidget(self.hyperthoughtTemplateSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.UseTemplateTab)
        self.label_6.setObjectName(u"label_6")
        sizePolicy6.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy6)

        self.horizontalLayout_6.addWidget(self.label_6)

        self.otherDataFileLineEdit = QLineEdit(self.UseTemplateTab)
        self.otherDataFileLineEdit.setObjectName(u"otherDataFileLineEdit")
        sizePolicy7.setHeightForWidth(self.otherDataFileLineEdit.sizePolicy().hasHeightForWidth())
        self.otherDataFileLineEdit.setSizePolicy(sizePolicy7)
        self.otherDataFileLineEdit.setReadOnly(True)

        self.horizontalLayout_6.addWidget(self.otherDataFileLineEdit)

        self.otherDataFileSelect = QPushButton(self.UseTemplateTab)
        self.otherDataFileSelect.setObjectName(u"otherDataFileSelect")
        self.otherDataFileSelect.setEnabled(True)

        self.horizontalLayout_6.addWidget(self.otherDataFileSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.useTemplateListSearchBar = QLineEdit(self.UseTemplateTab)
        self.useTemplateListSearchBar.setObjectName(u"useTemplateListSearchBar")
        sizePolicy8 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.useTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.useTemplateListSearchBar.setSizePolicy(sizePolicy8)
        self.useTemplateListSearchBar.setReadOnly(False)

        self.horizontalLayout_12.addWidget(self.useTemplateListSearchBar)

        self.addMetadataFileCheckBox = QCheckBox(self.UseTemplateTab)
        self.addMetadataFileCheckBox.setObjectName(u"addMetadataFileCheckBox")
        self.addMetadataFileCheckBox.setChecked(True)

        self.horizontalLayout_12.addWidget(self.addMetadataFileCheckBox)

        self.displayedFileLabel = QLabel(self.UseTemplateTab)
        self.displayedFileLabel.setObjectName(u"displayedFileLabel")
        self.displayedFileLabel.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.displayedFileLabel)

        self.appendUseTableRowButton = QToolButton(self.UseTemplateTab)
        self.appendUseTableRowButton.setObjectName(u"appendUseTableRowButton")
        icon2 = QIcon()
        icon2.addFile(u":/resources/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appendUseTableRowButton.setIcon(icon2)
        self.appendUseTableRowButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_12.addWidget(self.appendUseTableRowButton)

        self.removeUseTableRowButton = QToolButton(self.UseTemplateTab)
        self.removeUseTableRowButton.setObjectName(u"removeUseTableRowButton")
        self.removeUseTableRowButton.setIcon(icon1)
        self.removeUseTableRowButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.horizontalLayout_12.addWidget(self.removeUseTableRowButton)


        self.verticalLayout.addLayout(self.horizontalLayout_12)

        self.useTemplateTableView = QTableView(self.UseTemplateTab)
        self.useTemplateTableView.setObjectName(u"useTemplateTableView")
        self.useTemplateTableView.setAlternatingRowColors(True)
        self.useTemplateTableView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.useTemplateTableView.horizontalHeader().setStretchLastSection(False)
        self.useTemplateTableView.verticalHeader().setMinimumSectionSize(15)

        self.verticalLayout.addWidget(self.useTemplateTableView)


        self.horizontalLayout_13.addLayout(self.verticalLayout)

        self.horizontalLayout_13.setStretch(0, 10)
        self.horizontalLayout_13.setStretch(1, 100)

        self.gridLayout_3.addLayout(self.horizontalLayout_13, 0, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(12)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.UseTemplateTab)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_7.addWidget(self.label_3)

        self.hyperThoughtUrl = QLabel(self.UseTemplateTab)
        self.hyperThoughtUrl.setObjectName(u"hyperThoughtUrl")
        font = QFont()
        font.setItalic(True)
        self.hyperThoughtUrl.setFont(font)

        self.horizontalLayout_7.addWidget(self.hyperThoughtUrl)

        self.hyperthoughtLocationLineEdit = QLineEdit(self.UseTemplateTab)
        self.hyperthoughtLocationLineEdit.setObjectName(u"hyperthoughtLocationLineEdit")

        self.horizontalLayout_7.addWidget(self.hyperthoughtLocationLineEdit)

        self.hyperthoughtLocationButton = QPushButton(self.UseTemplateTab)
        self.hyperthoughtLocationButton.setObjectName(u"hyperthoughtLocationButton")
        self.hyperthoughtLocationButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.hyperthoughtLocationButton)


        self.gridLayout_3.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.hyperthoughtUploadButton = QPushButton(self.UseTemplateTab)
        self.hyperthoughtUploadButton.setObjectName(u"hyperthoughtUploadButton")
        self.hyperthoughtUploadButton.setEnabled(False)

        self.gridLayout_2.addWidget(self.hyperthoughtUploadButton, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 2, 0, 1, 1)

        self.TabWidget.addTab(self.UseTemplateTab, "")

        self.gridLayout_4.addWidget(self.TabWidget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1328, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpenPackage)
        self.menuFile.addAction(self.actionOpen_Template)
        self.menuFile.addAction(self.actionOpen_Recent)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Package)
        self.menuFile.addAction(self.actionSave_Package_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Template)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionHelp)

        self.retranslateUi(MainWindow)

        self.TabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.actionOpenPackage.setText(QCoreApplication.translate("MainWindow", u"Open Package", None))
        self.actionOpen_Recent.setText(QCoreApplication.translate("MainWindow", u"Open Recent", None))
        self.actionSave_Package.setText(QCoreApplication.translate("MainWindow", u"Save Package", None))
        self.actionSave_Package_As.setText(QCoreApplication.translate("MainWindow", u"Save Package As", None))
        self.actionUse_Template.setText(QCoreApplication.translate("MainWindow", u"Use Template", None))
        self.actionCreate_Template.setText(QCoreApplication.translate("MainWindow", u"Create Template", None))
        self.actionClose.setText(QCoreApplication.translate("MainWindow", u"Close ", None))
        self.actionHelp.setText(QCoreApplication.translate("MainWindow", u"Help", None))
        self.actionSave_Template.setText(QCoreApplication.translate("MainWindow", u"Save Template", None))
        self.actionOpen_Template.setText(QCoreApplication.translate("MainWindow", u"Restore Template", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Data File:", None))
        self.dataFileLineEdit.setText("")
#if QT_CONFIG(tooltip)
        self.dataFileSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select data file to use for meta-data extraction", None))
#endif // QT_CONFIG(tooltip)
        self.dataFileSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.dataTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Data Type Detected:", None))
        self.dataTypeText.setText(QCoreApplication.translate("MainWindow", u"None Selected", None))
        self.fileParserLabel.setText(QCoreApplication.translate("MainWindow", u"File Parser:", None))
        self.fileParserCombo.setItemText(0, QCoreApplication.translate("MainWindow", u"CTF Parser", None))
        self.fileParserCombo.setItemText(1, QCoreApplication.translate("MainWindow", u"ANG Parser", None))
        self.fileParserCombo.setItemText(2, QCoreApplication.translate("MainWindow", u"Custom Parser", None))

        self.fileParserCombo.setCurrentText(QCoreApplication.translate("MainWindow", u"CTF Parser", None))
#if QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a custom value to the template", None))
#endif // QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setText(QCoreApplication.translate("MainWindow", u"Add Custom Value", None))
#if QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a custom value to the template", None))
#endif // QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setText(QCoreApplication.translate("MainWindow", u"Remove Value", None))
        self.createTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type to search for key", None))
        self.createTemplateTreeSearchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Type to search for key", None))
        self.saveTemplateButton.setText(QCoreApplication.translate("MainWindow", u"Save Template as ...", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.CreateTemplateTab), QCoreApplication.translate("MainWindow", u"Create Template", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Files to be Uploaded:", None))
        self.addUploadFilesBtn.setText("")
        self.clearUploadFilesBtn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.hyperthoughtTemplateLabel.setText(QCoreApplication.translate("MainWindow", u"Template File: ", None))
        self.hyperthoughtTemplateLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"example.ez", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtTemplateSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select the template file for this upload(*.ez)", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtTemplateSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"File To Extract Metadata From: ", None))
#if QT_CONFIG(tooltip)
        self.otherDataFileSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select a data file to extract meta-data", None))
#endif // QT_CONFIG(tooltip)
        self.otherDataFileSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.useTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search For HT Key", None))
        self.addMetadataFileCheckBox.setText(QCoreApplication.translate("MainWindow", u"Add Extracted Metadata File To File List", None))
        self.displayedFileLabel.setText(QCoreApplication.translate("MainWindow", u"No File Selected", None))
#if QT_CONFIG(tooltip)
        self.appendUseTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a Custom Value that is only going to be used for this upload", None))
#endif // QT_CONFIG(tooltip)
        self.appendUseTableRowButton.setText(QCoreApplication.translate("MainWindow", u"Add Custom Value", None))
#if QT_CONFIG(tooltip)
        self.removeUseTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a Custom Value that is only going to be used for this upload", None))
#endif // QT_CONFIG(tooltip)
        self.removeUseTableRowButton.setText(QCoreApplication.translate("MainWindow", u"Remove Value", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Remote HyperThought Folder Path:", None))
        self.hyperThoughtUrl.setText(QCoreApplication.translate("MainWindow", u"https://hyperthought.url", None))
        self.hyperthoughtLocationLineEdit.setText("")
        self.hyperthoughtLocationLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Use the 'Select Remote Folder' button to set the remote location for the data --->", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtLocationButton.setToolTip(QCoreApplication.translate("MainWindow", u"Allows user to set their API key from HyperThought and set a remote location on the HyperThought server to upload the data files", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtLocationButton.setText(QCoreApplication.translate("MainWindow", u"Select Remote Folder", None))
        self.hyperthoughtUploadButton.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.UseTemplateTab), QCoreApplication.translate("MainWindow", u"Use Template", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

