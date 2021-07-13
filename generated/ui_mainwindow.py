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
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(4, 12, 4, 4)
        self.create_frame_3 = QFrame(self.CreateTemplateTab)
        self.create_frame_3.setObjectName(u"create_frame_3")
        self.create_frame_3.setFrameShape(QFrame.StyledPanel)
        self.create_frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.create_frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(9)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.create_frame_3)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.dataFileLineEdit = QLineEdit(self.create_frame_3)
        self.dataFileLineEdit.setObjectName(u"dataFileLineEdit")
        self.dataFileLineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.dataFileLineEdit)

        self.dataFileSelect = QPushButton(self.create_frame_3)
        self.dataFileSelect.setObjectName(u"dataFileSelect")

        self.horizontalLayout_2.addWidget(self.dataFileSelect)


        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dataTypeLabel = QLabel(self.create_frame_3)
        self.dataTypeLabel.setObjectName(u"dataTypeLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dataTypeLabel.sizePolicy().hasHeightForWidth())
        self.dataTypeLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.dataTypeLabel)

        self.dataTypeText = QLabel(self.create_frame_3)
        self.dataTypeText.setObjectName(u"dataTypeText")

        self.horizontalLayout_3.addWidget(self.dataTypeText)

        self.horizontalSpacer_2 = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.fileParserLabel = QLabel(self.create_frame_3)
        self.fileParserLabel.setObjectName(u"fileParserLabel")
        sizePolicy1.setHeightForWidth(self.fileParserLabel.sizePolicy().hasHeightForWidth())
        self.fileParserLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.fileParserLabel)

        self.fileParserCombo = QComboBox(self.create_frame_3)
        self.fileParserCombo.setObjectName(u"fileParserCombo")

        self.horizontalLayout_3.addWidget(self.fileParserCombo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)


        self.gridLayout_5.addWidget(self.create_frame_3, 0, 0, 1, 2)

        self.create_frame_4 = QFrame(self.CreateTemplateTab)
        self.create_frame_4.setObjectName(u"create_frame_4")
        self.create_frame_4.setFrameShape(QFrame.StyledPanel)
        self.create_frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.create_frame_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.clearCreateButton = QPushButton(self.create_frame_4)
        self.clearCreateButton.setObjectName(u"clearCreateButton")

        self.horizontalLayout.addWidget(self.clearCreateButton)

        self.horizontalSpacer_5 = QSpacerItem(1227, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_5)

        self.saveTemplateButton = QPushButton(self.create_frame_4)
        self.saveTemplateButton.setObjectName(u"saveTemplateButton")
        self.saveTemplateButton.setFlat(False)

        self.horizontalLayout.addWidget(self.saveTemplateButton)


        self.gridLayout_5.addWidget(self.create_frame_4, 5, 0, 1, 2)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, 0, 0)
        self.create_frame_2 = QFrame(self.CreateTemplateTab)
        self.create_frame_2.setObjectName(u"create_frame_2")
        self.create_frame_2.setFrameShape(QFrame.StyledPanel)
        self.create_frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_9 = QGridLayout(self.create_frame_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, 0)
        self.create_label_2 = QLabel(self.create_frame_2)
        self.create_label_2.setObjectName(u"create_label_2")

        self.horizontalLayout_5.addWidget(self.create_label_2)

        self.createTemplateTreeSearchBar = QLineEdit(self.create_frame_2)
        self.createTemplateTreeSearchBar.setObjectName(u"createTemplateTreeSearchBar")

        self.horizontalLayout_5.addWidget(self.createTemplateTreeSearchBar)


        self.gridLayout_9.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.metadataTreeView = QTreeView(self.create_frame_2)
        self.metadataTreeView.setObjectName(u"metadataTreeView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.metadataTreeView.sizePolicy().hasHeightForWidth())
        self.metadataTreeView.setSizePolicy(sizePolicy2)
        self.metadataTreeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTreeView.setAlternatingRowColors(True)

        self.gridLayout_9.addWidget(self.metadataTreeView, 1, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.create_frame_2)

        self.create_frame_1 = QFrame(self.CreateTemplateTab)
        self.create_frame_1.setObjectName(u"create_frame_1")
        self.create_frame_1.setMinimumSize(QSize(200, 0))
        self.create_frame_1.setFrameShape(QFrame.StyledPanel)
        self.create_frame_1.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.create_frame_1)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.metadataTableView = QTableView(self.create_frame_1)
        self.metadataTableView.setObjectName(u"metadataTableView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.metadataTableView.sizePolicy().hasHeightForWidth())
        self.metadataTableView.setSizePolicy(sizePolicy3)
        self.metadataTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.metadataTableView.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked)
        self.metadataTableView.setProperty("showDropIndicator", False)
        self.metadataTableView.setDragDropOverwriteMode(False)
        self.metadataTableView.setAlternatingRowColors(True)
        self.metadataTableView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.metadataTableView.setShowGrid(False)
        self.metadataTableView.setSortingEnabled(True)
        self.metadataTableView.setCornerButtonEnabled(False)
        self.metadataTableView.horizontalHeader().setStretchLastSection(True)
        self.metadataTableView.verticalHeader().setVisible(False)
        self.metadataTableView.verticalHeader().setMinimumSectionSize(15)

        self.gridLayout_8.addWidget(self.metadataTableView, 2, 0, 1, 3)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_8, 3, 0, 1, 1)

        self.removeCreateTableRowButton = QPushButton(self.create_frame_1)
        self.removeCreateTableRowButton.setObjectName(u"removeCreateTableRowButton")
        self.removeCreateTableRowButton.setMinimumSize(QSize(40, 0))
        self.removeCreateTableRowButton.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_8.addWidget(self.removeCreateTableRowButton, 3, 2, 1, 1)

        self.appendCreateTableRowButton = QPushButton(self.create_frame_1)
        self.appendCreateTableRowButton.setObjectName(u"appendCreateTableRowButton")
        self.appendCreateTableRowButton.setMinimumSize(QSize(40, 0))
        self.appendCreateTableRowButton.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_8.addWidget(self.appendCreateTableRowButton, 3, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.create_label_1 = QLabel(self.create_frame_1)
        self.create_label_1.setObjectName(u"create_label_1")

        self.horizontalLayout_4.addWidget(self.create_label_1)

        self.createTemplateListSearchBar = QLineEdit(self.create_frame_1)
        self.createTemplateListSearchBar.setObjectName(u"createTemplateListSearchBar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.createTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.createTemplateListSearchBar.setSizePolicy(sizePolicy4)

        self.horizontalLayout_4.addWidget(self.createTemplateListSearchBar)


        self.gridLayout_8.addLayout(self.horizontalLayout_4, 1, 0, 1, 3)


        self.horizontalLayout_6.addWidget(self.create_frame_1)

        self.horizontalLayout_6.setStretch(0, 25)
        self.horizontalLayout_6.setStretch(1, 75)

        self.gridLayout_5.addLayout(self.horizontalLayout_6, 1, 0, 1, 2)

        self.TabWidget.addTab(self.CreateTemplateTab, "")
        self.UseTemplateTab = QWidget()
        self.UseTemplateTab.setObjectName(u"UseTemplateTab")
        self.gridLayout_3 = QGridLayout(self.UseTemplateTab)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(4, 12, 4, 4)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.use_frame_3 = QFrame(self.UseTemplateTab)
        self.use_frame_3.setObjectName(u"use_frame_3")
        self.use_frame_3.setFrameShape(QFrame.StyledPanel)
        self.use_frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.use_frame_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.addUploadFilesBtn = QPushButton(self.use_frame_3)
        self.addUploadFilesBtn.setObjectName(u"addUploadFilesBtn")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.addUploadFilesBtn.sizePolicy().hasHeightForWidth())
        self.addUploadFilesBtn.setSizePolicy(sizePolicy5)
        self.addUploadFilesBtn.setMinimumSize(QSize(40, 0))
        self.addUploadFilesBtn.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_10.addWidget(self.addUploadFilesBtn, 2, 0, 1, 1)

        self.clearUploadFilesBtn = QPushButton(self.use_frame_3)
        self.clearUploadFilesBtn.setObjectName(u"clearUploadFilesBtn")
        sizePolicy5.setHeightForWidth(self.clearUploadFilesBtn.sizePolicy().hasHeightForWidth())
        self.clearUploadFilesBtn.setSizePolicy(sizePolicy5)
        self.clearUploadFilesBtn.setMinimumSize(QSize(40, 0))
        self.clearUploadFilesBtn.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_10.addWidget(self.clearUploadFilesBtn, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_4, 2, 2, 1, 1)

        self.useTemplateListView = QListView(self.use_frame_3)
        self.useTemplateListView.setObjectName(u"useTemplateListView")
        sizePolicy2.setHeightForWidth(self.useTemplateListView.sizePolicy().hasHeightForWidth())
        self.useTemplateListView.setSizePolicy(sizePolicy2)
        self.useTemplateListView.setMinimumSize(QSize(325, 0))
        self.useTemplateListView.setAcceptDrops(True)
        self.useTemplateListView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.useTemplateListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.useTemplateListView.setAlternatingRowColors(True)
        self.useTemplateListView.setUniformItemSizes(True)

        self.gridLayout_10.addWidget(self.useTemplateListView, 1, 0, 1, 3)

        self.label = QLabel(self.use_frame_3)
        self.label.setObjectName(u"label")

        self.gridLayout_10.addWidget(self.label, 0, 0, 1, 3)


        self.horizontalLayout_13.addWidget(self.use_frame_3)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.use_frame_1 = QFrame(self.UseTemplateTab)
        self.use_frame_1.setObjectName(u"use_frame_1")
        self.use_frame_1.setAutoFillBackground(False)
        self.use_frame_1.setStyleSheet(u"")
        self.use_frame_1.setFrameShape(QFrame.StyledPanel)
        self.use_frame_1.setFrameShadow(QFrame.Sunken)
        self.gridLayout_7 = QGridLayout(self.use_frame_1)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.otherDataFileSelect = QPushButton(self.use_frame_1)
        self.otherDataFileSelect.setObjectName(u"otherDataFileSelect")
        self.otherDataFileSelect.setEnabled(True)

        self.gridLayout_7.addWidget(self.otherDataFileSelect, 1, 2, 1, 1)

        self.use_label_1 = QLabel(self.use_frame_1)
        self.use_label_1.setObjectName(u"use_label_1")
        sizePolicy6 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(1)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.use_label_1.sizePolicy().hasHeightForWidth())
        self.use_label_1.setSizePolicy(sizePolicy6)

        self.gridLayout_7.addWidget(self.use_label_1, 0, 0, 1, 1)

        self.hyperthoughtTemplateLineEdit = QLineEdit(self.use_frame_1)
        self.hyperthoughtTemplateLineEdit.setObjectName(u"hyperthoughtTemplateLineEdit")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(2)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.hyperthoughtTemplateLineEdit.sizePolicy().hasHeightForWidth())
        self.hyperthoughtTemplateLineEdit.setSizePolicy(sizePolicy7)
        self.hyperthoughtTemplateLineEdit.setReadOnly(True)

        self.gridLayout_7.addWidget(self.hyperthoughtTemplateLineEdit, 0, 1, 1, 1)

        self.use_label_2 = QLabel(self.use_frame_1)
        self.use_label_2.setObjectName(u"use_label_2")
        sizePolicy6.setHeightForWidth(self.use_label_2.sizePolicy().hasHeightForWidth())
        self.use_label_2.setSizePolicy(sizePolicy6)

        self.gridLayout_7.addWidget(self.use_label_2, 1, 0, 1, 1)

        self.hyperthoughtTemplateSelect = QPushButton(self.use_frame_1)
        self.hyperthoughtTemplateSelect.setObjectName(u"hyperthoughtTemplateSelect")

        self.gridLayout_7.addWidget(self.hyperthoughtTemplateSelect, 0, 2, 1, 1)

        self.otherDataFileLineEdit = QLineEdit(self.use_frame_1)
        self.otherDataFileLineEdit.setObjectName(u"otherDataFileLineEdit")
        sizePolicy7.setHeightForWidth(self.otherDataFileLineEdit.sizePolicy().hasHeightForWidth())
        self.otherDataFileLineEdit.setSizePolicy(sizePolicy7)
        self.otherDataFileLineEdit.setReadOnly(True)

        self.gridLayout_7.addWidget(self.otherDataFileLineEdit, 1, 1, 1, 1)

        self.addMetadataFileCheckBox = QCheckBox(self.use_frame_1)
        self.addMetadataFileCheckBox.setObjectName(u"addMetadataFileCheckBox")
        self.addMetadataFileCheckBox.setChecked(True)

        self.gridLayout_7.addWidget(self.addMetadataFileCheckBox, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.use_frame_1)

        self.use_frame_2 = QFrame(self.UseTemplateTab)
        self.use_frame_2.setObjectName(u"use_frame_2")
        self.use_frame_2.setFrameShape(QFrame.StyledPanel)
        self.use_frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.use_frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.useTemplateTableView = QTableView(self.use_frame_2)
        self.useTemplateTableView.setObjectName(u"useTemplateTableView")
        self.useTemplateTableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.useTemplateTableView.setAlternatingRowColors(True)
        self.useTemplateTableView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.useTemplateTableView.setShowGrid(False)
        self.useTemplateTableView.setGridStyle(Qt.SolidLine)
        self.useTemplateTableView.setSortingEnabled(True)
        self.useTemplateTableView.setCornerButtonEnabled(False)
        self.useTemplateTableView.horizontalHeader().setStretchLastSection(True)
        self.useTemplateTableView.verticalHeader().setMinimumSectionSize(15)

        self.gridLayout_6.addWidget(self.useTemplateTableView, 1, 0, 1, 4)

        self.use_label_3 = QLabel(self.use_frame_2)
        self.use_label_3.setObjectName(u"use_label_3")

        self.gridLayout_6.addWidget(self.use_label_3, 0, 0, 1, 1)

        self.removeUseTableRowButton = QPushButton(self.use_frame_2)
        self.removeUseTableRowButton.setObjectName(u"removeUseTableRowButton")
        sizePolicy5.setHeightForWidth(self.removeUseTableRowButton.sizePolicy().hasHeightForWidth())
        self.removeUseTableRowButton.setSizePolicy(sizePolicy5)
        self.removeUseTableRowButton.setMinimumSize(QSize(40, 0))
        self.removeUseTableRowButton.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_6.addWidget(self.removeUseTableRowButton, 2, 3, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_7, 2, 0, 1, 2)

        self.appendUseTableRowButton = QPushButton(self.use_frame_2)
        self.appendUseTableRowButton.setObjectName(u"appendUseTableRowButton")
        sizePolicy5.setHeightForWidth(self.appendUseTableRowButton.sizePolicy().hasHeightForWidth())
        self.appendUseTableRowButton.setSizePolicy(sizePolicy5)
        self.appendUseTableRowButton.setMinimumSize(QSize(40, 0))
        self.appendUseTableRowButton.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_6.addWidget(self.appendUseTableRowButton, 2, 2, 1, 1)

        self.useTemplateListSearchBar = QLineEdit(self.use_frame_2)
        self.useTemplateListSearchBar.setObjectName(u"useTemplateListSearchBar")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy8.setHorizontalStretch(2)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.useTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.useTemplateListSearchBar.setSizePolicy(sizePolicy8)
        self.useTemplateListSearchBar.setReadOnly(False)

        self.gridLayout_6.addWidget(self.useTemplateListSearchBar, 0, 1, 1, 3)


        self.verticalLayout.addWidget(self.use_frame_2)


        self.horizontalLayout_13.addLayout(self.verticalLayout)

        self.horizontalLayout_13.setStretch(1, 100)

        self.gridLayout_3.addLayout(self.horizontalLayout_13, 1, 0, 1, 1)

        self.use_frame_4 = QFrame(self.UseTemplateTab)
        self.use_frame_4.setObjectName(u"use_frame_4")
        self.use_frame_4.setFrameShape(QFrame.StyledPanel)
        self.use_frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_11 = QGridLayout(self.use_frame_4)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.clearUseButton = QPushButton(self.use_frame_4)
        self.clearUseButton.setObjectName(u"clearUseButton")

        self.gridLayout_11.addWidget(self.clearUseButton, 2, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_3, 2, 1, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, 10, 10)
        self.label_3 = QLabel(self.use_frame_4)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_3)

        self.hyperThoughtServer = QLabel(self.use_frame_4)
        self.hyperThoughtServer.setObjectName(u"hyperThoughtServer")
        font1 = QFont()
        font1.setItalic(True)
        self.hyperThoughtServer.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtServer)

        self.horizontalSpacer_9 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.label_4 = QLabel(self.use_frame_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.hyperThoughtProject = QLabel(self.use_frame_4)
        self.hyperThoughtProject.setObjectName(u"hyperThoughtProject")
        self.hyperThoughtProject.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtProject)

        self.horizontalSpacer_10 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_10)

        self.label_5 = QLabel(self.use_frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.hyperThoughtUploadPath = QLabel(self.use_frame_4)
        self.hyperThoughtUploadPath.setObjectName(u"hyperThoughtUploadPath")
        self.hyperThoughtUploadPath.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtUploadPath)

        self.horizontalSpacer_11 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.label_6 = QLabel(self.use_frame_4)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_6)

        self.hyperThoughtExpiresIn = QLabel(self.use_frame_4)
        self.hyperThoughtExpiresIn.setObjectName(u"hyperThoughtExpiresIn")
        self.hyperThoughtExpiresIn.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtExpiresIn)

        self.horizontalSpacer_12 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_12)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)

        self.hyperthoughtLocationButton = QPushButton(self.use_frame_4)
        self.hyperthoughtLocationButton.setObjectName(u"hyperthoughtLocationButton")
        self.hyperthoughtLocationButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.hyperthoughtLocationButton)

        self.hyperthoughtUploadButton = QPushButton(self.use_frame_4)
        self.hyperthoughtUploadButton.setObjectName(u"hyperthoughtUploadButton")
        self.hyperthoughtUploadButton.setEnabled(False)

        self.horizontalLayout_7.addWidget(self.hyperthoughtUploadButton)


        self.gridLayout_11.addLayout(self.horizontalLayout_7, 0, 0, 1, 2)


        self.gridLayout_3.addWidget(self.use_frame_4, 2, 0, 1, 1)

        self.TabWidget.addTab(self.UseTemplateTab, "")

        self.gridLayout_4.addWidget(self.TabWidget, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1606, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuOpen_Recent = QMenu(self.menuFile)
        self.menuOpen_Recent.setObjectName(u"menuOpen_Recent")
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
        self.menuFile.addAction(self.menuOpen_Recent.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Template)
        self.menuFile.addAction(self.actionSave_Package)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)

        self.TabWidget.setCurrentIndex(0)
        self.saveTemplateButton.setDefault(False)


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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Data File:", None))
        self.dataFileLineEdit.setText("")
#if QT_CONFIG(tooltip)
        self.dataFileSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select data file to use for meta-data extraction", None))
#endif // QT_CONFIG(tooltip)
        self.dataFileSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.dataTypeLabel.setText(QCoreApplication.translate("MainWindow", u"Data Type Detected:", None))
        self.dataTypeText.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.fileParserLabel.setText(QCoreApplication.translate("MainWindow", u"File Parser:", None))
        self.fileParserCombo.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.clearCreateButton.setToolTip(QCoreApplication.translate("MainWindow", u"Reset all 'Create Template' input fields. All fields will be reset to an empty state.", None))
#endif // QT_CONFIG(tooltip)
        self.clearCreateButton.setText(QCoreApplication.translate("MainWindow", u"Reset All Fields", None))
#if QT_CONFIG(tooltip)
        self.saveTemplateButton.setToolTip(QCoreApplication.translate("MainWindow", u"Save Values to a .ez template file. You can also use standard 'Save' Shortcut key", None))
#endif // QT_CONFIG(tooltip)
        self.saveTemplateButton.setText(QCoreApplication.translate("MainWindow", u"Save Template as ...", None))
        self.create_label_2.setText(QCoreApplication.translate("MainWindow", u"Search Table", None))
        self.createTemplateTreeSearchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search metadata keys using wildcard (*.*)", None))
#if QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a custom value to the template", None))
#endif // QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setText("")
#if QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a custom value to the template", None))
#endif // QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setText("")
        self.create_label_1.setText(QCoreApplication.translate("MainWindow", u"Search Table", None))
        self.createTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search table using wildcard (*.*)", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.CreateTemplateTab), QCoreApplication.translate("MainWindow", u"Create Template", None))
#if QT_CONFIG(tooltip)
        self.addUploadFilesBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Add files to the upload list", None))
#endif // QT_CONFIG(tooltip)
        self.addUploadFilesBtn.setText("")
#if QT_CONFIG(tooltip)
        self.clearUploadFilesBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Clear *all* the files from the list", None))
#endif // QT_CONFIG(tooltip)
        self.clearUploadFilesBtn.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Files to be Uploaded:", None))
#if QT_CONFIG(tooltip)
        self.otherDataFileSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select a data file to extract meta-data", None))
#endif // QT_CONFIG(tooltip)
        self.otherDataFileSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.use_label_1.setText(QCoreApplication.translate("MainWindow", u"Template File: ", None))
        self.hyperthoughtTemplateLineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Drag a template file here or select one using the 'Select' button to the right===>", None))
        self.use_label_2.setText(QCoreApplication.translate("MainWindow", u"File To Extract Metadata From: ", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtTemplateSelect.setToolTip(QCoreApplication.translate("MainWindow", u"Select the template file for this upload(*.ez)", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtTemplateSelect.setText(QCoreApplication.translate("MainWindow", u"Select", None))
        self.addMetadataFileCheckBox.setText(QCoreApplication.translate("MainWindow", u"Add Extracted Metadata File To File List", None))
        self.use_label_3.setText(QCoreApplication.translate("MainWindow", u"Search Table", None))
#if QT_CONFIG(tooltip)
        self.removeUseTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Removes the selected rows from the table", None))
#endif // QT_CONFIG(tooltip)
        self.removeUseTableRowButton.setText("")
#if QT_CONFIG(tooltip)
        self.appendUseTableRowButton.setToolTip(QCoreApplication.translate("MainWindow", u"Add a Custom Value that is only going to be used for this upload", None))
#endif // QT_CONFIG(tooltip)
        self.appendUseTableRowButton.setText("")
        self.useTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search table using wildcard (*.*)", None))
#if QT_CONFIG(tooltip)
        self.clearUseButton.setToolTip(QCoreApplication.translate("MainWindow", u"Reset all 'Create Template' input fields. All fields will be reset to an empty state.", None))
#endif // QT_CONFIG(tooltip)
        self.clearUseButton.setText(QCoreApplication.translate("MainWindow", u"Reset All Fields", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Server:", None))
        self.hyperThoughtServer.setText(QCoreApplication.translate("MainWindow", u"Server Not Selected", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Project:", None))
        self.hyperThoughtProject.setText(QCoreApplication.translate("MainWindow", u"Project Not Selected", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Project Directory Path:", None))
        self.hyperThoughtUploadPath.setText(QCoreApplication.translate("MainWindow", u"Folder Not Selected", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Token Expires At:", None))
        self.hyperThoughtExpiresIn.setText(QCoreApplication.translate("MainWindow", u"Not Authenticated", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtLocationButton.setToolTip(QCoreApplication.translate("MainWindow", u"Allows user to set their API key from HyperThought and set a remote location on the HyperThought server to upload the data files", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtLocationButton.setText(QCoreApplication.translate("MainWindow", u"Select Remote Folder", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtUploadButton.setToolTip(QCoreApplication.translate("MainWindow", u"Upload all files to the HyperThought server", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtUploadButton.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.UseTemplateTab), QCoreApplication.translate("MainWindow", u"Use Template", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuOpen_Recent.setTitle(QCoreApplication.translate("MainWindow", u"Open Recent", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

