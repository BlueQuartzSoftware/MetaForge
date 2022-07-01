# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'usetemplatewidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_UseTemplateWidget(object):
    def setupUi(self, UseTemplateWidget):
        if not UseTemplateWidget.objectName():
            UseTemplateWidget.setObjectName(u"UseTemplateWidget")
        UseTemplateWidget.resize(1493, 840)
        self.gridLayout_2 = QGridLayout(UseTemplateWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(-1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 8)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, 10, 10)
        self.label_3 = QLabel(UseTemplateWidget)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_3)

        self.hyperThoughtServer = QLabel(UseTemplateWidget)
        self.hyperThoughtServer.setObjectName(u"hyperThoughtServer")
        font1 = QFont()
        font1.setItalic(True)
        self.hyperThoughtServer.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtServer)

        self.horizontalSpacer_9 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_9)

        self.label_4 = QLabel(UseTemplateWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_4)

        self.hyperThoughtProject = QLabel(UseTemplateWidget)
        self.hyperThoughtProject.setObjectName(u"hyperThoughtProject")
        self.hyperThoughtProject.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtProject)

        self.horizontalSpacer_10 = QSpacerItem(12, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_10)

        self.label_5 = QLabel(UseTemplateWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)

        self.horizontalLayout_7.addWidget(self.label_5)

        self.hyperThoughtUploadPath = QLabel(UseTemplateWidget)
        self.hyperThoughtUploadPath.setObjectName(u"hyperThoughtUploadPath")
        self.hyperThoughtUploadPath.setFont(font1)

        self.horizontalLayout_7.addWidget(self.hyperThoughtUploadPath)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_6)

        self.hyperthoughtLocationButton = QPushButton(UseTemplateWidget)
        self.hyperthoughtLocationButton.setObjectName(u"hyperthoughtLocationButton")
        self.hyperthoughtLocationButton.setEnabled(True)

        self.horizontalLayout_7.addWidget(self.hyperthoughtLocationButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_7, 5, 0, 1, 2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, -1, 0, 0)
        self.list_progress_label = QLabel(UseTemplateWidget)
        self.list_progress_label.setObjectName(u"list_progress_label")

        self.gridLayout_3.addWidget(self.list_progress_label, 2, 0, 1, 1)

        self.hyperthoughtUploadButton = QPushButton(UseTemplateWidget)
        self.hyperthoughtUploadButton.setObjectName(u"hyperthoughtUploadButton")
        self.hyperthoughtUploadButton.setEnabled(False)

        self.gridLayout_3.addWidget(self.hyperthoughtUploadButton, 1, 2, 3, 1)

        self.file_progress_bar_label = QLabel(UseTemplateWidget)
        self.file_progress_bar_label.setObjectName(u"file_progress_bar_label")

        self.gridLayout_3.addWidget(self.file_progress_bar_label, 1, 1, 1, 1)

        self.file_progress_bar = QProgressBar(UseTemplateWidget)
        self.file_progress_bar.setObjectName(u"file_progress_bar")
        self.file_progress_bar.setValue(0)
        self.file_progress_bar.setOrientation(Qt.Horizontal)
        self.file_progress_bar.setInvertedAppearance(False)

        self.gridLayout_3.addWidget(self.file_progress_bar, 1, 0, 1, 1)

        self.list_progress_bar_label = QLabel(UseTemplateWidget)
        self.list_progress_bar_label.setObjectName(u"list_progress_bar_label")

        self.gridLayout_3.addWidget(self.list_progress_bar_label, 3, 1, 1, 1)

        self.list_progress_bar = QProgressBar(UseTemplateWidget)
        self.list_progress_bar.setObjectName(u"list_progress_bar")
        self.list_progress_bar.setValue(0)
        self.list_progress_bar.setOrientation(Qt.Horizontal)
        self.list_progress_bar.setInvertedAppearance(False)

        self.gridLayout_3.addWidget(self.list_progress_bar, 3, 0, 1, 1)

        self.file_progress_label = QLabel(UseTemplateWidget)
        self.file_progress_label.setObjectName(u"file_progress_label")

        self.gridLayout_3.addWidget(self.file_progress_label, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 6, 0, 1, 1)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, -1, -1, -1)
        self.use_frame_3 = QFrame(UseTemplateWidget)
        self.use_frame_3.setObjectName(u"use_frame_3")
        self.use_frame_3.setFrameShape(QFrame.StyledPanel)
        self.use_frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_10 = QGridLayout(self.use_frame_3)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.addUploadFilesBtn = QPushButton(self.use_frame_3)
        self.addUploadFilesBtn.setObjectName(u"addUploadFilesBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addUploadFilesBtn.sizePolicy().hasHeightForWidth())
        self.addUploadFilesBtn.setSizePolicy(sizePolicy)
        self.addUploadFilesBtn.setMinimumSize(QSize(40, 0))
        self.addUploadFilesBtn.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_10.addWidget(self.addUploadFilesBtn, 2, 0, 1, 1)

        self.clearUploadFilesBtn = QPushButton(self.use_frame_3)
        self.clearUploadFilesBtn.setObjectName(u"clearUploadFilesBtn")
        sizePolicy.setHeightForWidth(self.clearUploadFilesBtn.sizePolicy().hasHeightForWidth())
        self.clearUploadFilesBtn.setSizePolicy(sizePolicy)
        self.clearUploadFilesBtn.setMinimumSize(QSize(40, 0))
        self.clearUploadFilesBtn.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_10.addWidget(self.clearUploadFilesBtn, 2, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_10.addItem(self.horizontalSpacer_4, 2, 2, 1, 1)

        self.useTemplateListView = QListView(self.use_frame_3)
        self.useTemplateListView.setObjectName(u"useTemplateListView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.useTemplateListView.sizePolicy().hasHeightForWidth())
        self.useTemplateListView.setSizePolicy(sizePolicy1)
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
        self.use_frame_1 = QFrame(UseTemplateWidget)
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
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.use_label_1.sizePolicy().hasHeightForWidth())
        self.use_label_1.setSizePolicy(sizePolicy2)

        self.gridLayout_7.addWidget(self.use_label_1, 0, 0, 1, 1)

        self.hyperthoughtTemplateLineEdit = QLineEdit(self.use_frame_1)
        self.hyperthoughtTemplateLineEdit.setObjectName(u"hyperthoughtTemplateLineEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(2)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.hyperthoughtTemplateLineEdit.sizePolicy().hasHeightForWidth())
        self.hyperthoughtTemplateLineEdit.setSizePolicy(sizePolicy3)
        self.hyperthoughtTemplateLineEdit.setReadOnly(True)

        self.gridLayout_7.addWidget(self.hyperthoughtTemplateLineEdit, 0, 1, 1, 1)

        self.use_label_2 = QLabel(self.use_frame_1)
        self.use_label_2.setObjectName(u"use_label_2")
        sizePolicy2.setHeightForWidth(self.use_label_2.sizePolicy().hasHeightForWidth())
        self.use_label_2.setSizePolicy(sizePolicy2)

        self.gridLayout_7.addWidget(self.use_label_2, 1, 0, 1, 1)

        self.hyperthoughtTemplateSelect = QPushButton(self.use_frame_1)
        self.hyperthoughtTemplateSelect.setObjectName(u"hyperthoughtTemplateSelect")

        self.gridLayout_7.addWidget(self.hyperthoughtTemplateSelect, 0, 2, 1, 1)

        self.otherDataFileLineEdit = QLineEdit(self.use_frame_1)
        self.otherDataFileLineEdit.setObjectName(u"otherDataFileLineEdit")
        sizePolicy3.setHeightForWidth(self.otherDataFileLineEdit.sizePolicy().hasHeightForWidth())
        self.otherDataFileLineEdit.setSizePolicy(sizePolicy3)
        self.otherDataFileLineEdit.setReadOnly(True)

        self.gridLayout_7.addWidget(self.otherDataFileLineEdit, 1, 1, 1, 1)

        self.addMetadataFileCheckBox = QCheckBox(self.use_frame_1)
        self.addMetadataFileCheckBox.setObjectName(u"addMetadataFileCheckBox")
        self.addMetadataFileCheckBox.setChecked(True)

        self.gridLayout_7.addWidget(self.addMetadataFileCheckBox, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.use_frame_1)

        self.use_frame_2 = QFrame(UseTemplateWidget)
        self.use_frame_2.setObjectName(u"use_frame_2")
        self.use_frame_2.setFrameShape(QFrame.StyledPanel)
        self.use_frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.use_frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.removeUseTableRowButton = QPushButton(self.use_frame_2)
        self.removeUseTableRowButton.setObjectName(u"removeUseTableRowButton")
        sizePolicy.setHeightForWidth(self.removeUseTableRowButton.sizePolicy().hasHeightForWidth())
        self.removeUseTableRowButton.setSizePolicy(sizePolicy)
        self.removeUseTableRowButton.setMinimumSize(QSize(40, 0))
        self.removeUseTableRowButton.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_6.addWidget(self.removeUseTableRowButton, 2, 3, 1, 1)

        self.useTemplateTableView = QTableView(self.use_frame_2)
        self.useTemplateTableView.setObjectName(u"useTemplateTableView")
        self.useTemplateTableView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.useTemplateTableView.setAlternatingRowColors(True)
        self.useTemplateTableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.useTemplateTableView.setShowGrid(False)
        self.useTemplateTableView.setGridStyle(Qt.SolidLine)
        self.useTemplateTableView.setSortingEnabled(True)
        self.useTemplateTableView.setCornerButtonEnabled(False)
        self.useTemplateTableView.horizontalHeader().setStretchLastSection(True)
        self.useTemplateTableView.verticalHeader().setMinimumSectionSize(15)

        self.gridLayout_6.addWidget(self.useTemplateTableView, 1, 0, 1, 4)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_7, 2, 0, 1, 2)

        self.useTemplateListSearchBar = QLineEdit(self.use_frame_2)
        self.useTemplateListSearchBar.setObjectName(u"useTemplateListSearchBar")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(2)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.useTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.useTemplateListSearchBar.setSizePolicy(sizePolicy4)
        self.useTemplateListSearchBar.setReadOnly(False)

        self.gridLayout_6.addWidget(self.useTemplateListSearchBar, 0, 1, 1, 3)

        self.use_label_3 = QLabel(self.use_frame_2)
        self.use_label_3.setObjectName(u"use_label_3")

        self.gridLayout_6.addWidget(self.use_label_3, 0, 0, 1, 1)

        self.appendUseTableRowButton = QPushButton(self.use_frame_2)
        self.appendUseTableRowButton.setObjectName(u"appendUseTableRowButton")
        sizePolicy.setHeightForWidth(self.appendUseTableRowButton.sizePolicy().hasHeightForWidth())
        self.appendUseTableRowButton.setSizePolicy(sizePolicy)
        self.appendUseTableRowButton.setMinimumSize(QSize(40, 0))
        self.appendUseTableRowButton.setMaximumSize(QSize(40, 16777215))

        self.gridLayout_6.addWidget(self.appendUseTableRowButton, 2, 2, 1, 1)


        self.verticalLayout.addWidget(self.use_frame_2)


        self.horizontalLayout_13.addLayout(self.verticalLayout)

        self.horizontalLayout_13.setStretch(1, 100)

        self.gridLayout_2.addLayout(self.horizontalLayout_13, 4, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, -1, 0)
        self.clearUseButton = QPushButton(UseTemplateWidget)
        self.clearUseButton.setObjectName(u"clearUseButton")

        self.horizontalLayout.addWidget(self.clearUseButton)

        self.error_label = QLabel(UseTemplateWidget)
        self.error_label.setObjectName(u"error_label")

        self.horizontalLayout.addWidget(self.error_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 7, 0, 1, 2)


        self.retranslateUi(UseTemplateWidget)

        QMetaObject.connectSlotsByName(UseTemplateWidget)
    # setupUi

    def retranslateUi(self, UseTemplateWidget):
        UseTemplateWidget.setWindowTitle(QCoreApplication.translate("UseTemplateWidget", u"Use Template Widget", None))
        self.label_3.setText(QCoreApplication.translate("UseTemplateWidget", u"Server:", None))
        self.hyperThoughtServer.setText(QCoreApplication.translate("UseTemplateWidget", u"Server Not Selected", None))
        self.label_4.setText(QCoreApplication.translate("UseTemplateWidget", u"Project:", None))
        self.hyperThoughtProject.setText(QCoreApplication.translate("UseTemplateWidget", u"Project Not Selected", None))
        self.label_5.setText(QCoreApplication.translate("UseTemplateWidget", u"Project Directory Path:", None))
        self.hyperThoughtUploadPath.setText(QCoreApplication.translate("UseTemplateWidget", u"Folder Not Selected", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtLocationButton.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Allows user to set their API key from HyperThought and set a remote location on the HyperThought server to upload the data files", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtLocationButton.setText(QCoreApplication.translate("UseTemplateWidget", u"Select Remote Folder", None))
        self.list_progress_label.setText("")
#if QT_CONFIG(tooltip)
        self.hyperthoughtUploadButton.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Upload all files to the HyperThought server", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtUploadButton.setText(QCoreApplication.translate("UseTemplateWidget", u"Upload Files", None))
        self.file_progress_bar_label.setText(QCoreApplication.translate("UseTemplateWidget", u"0%", None))
        self.list_progress_bar_label.setText(QCoreApplication.translate("UseTemplateWidget", u"0%", None))
        self.file_progress_label.setText("")
#if QT_CONFIG(tooltip)
        self.addUploadFilesBtn.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Add files to the upload list", None))
#endif // QT_CONFIG(tooltip)
        self.addUploadFilesBtn.setText("")
#if QT_CONFIG(tooltip)
        self.clearUploadFilesBtn.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Clear *all* the files from the list", None))
#endif // QT_CONFIG(tooltip)
        self.clearUploadFilesBtn.setText("")
        self.label.setText(QCoreApplication.translate("UseTemplateWidget", u"Files to be Uploaded:", None))
#if QT_CONFIG(tooltip)
        self.otherDataFileSelect.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Select a data file to extract meta-data", None))
#endif // QT_CONFIG(tooltip)
        self.otherDataFileSelect.setText(QCoreApplication.translate("UseTemplateWidget", u"Select", None))
        self.use_label_1.setText(QCoreApplication.translate("UseTemplateWidget", u"Template File: ", None))
        self.hyperthoughtTemplateLineEdit.setPlaceholderText(QCoreApplication.translate("UseTemplateWidget", u"Drag a template file here or select one using the 'Select' button to the right===>", None))
        self.use_label_2.setText(QCoreApplication.translate("UseTemplateWidget", u"File To Extract Metadata From: ", None))
#if QT_CONFIG(tooltip)
        self.hyperthoughtTemplateSelect.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Select the template file for this upload(*.ez)", None))
#endif // QT_CONFIG(tooltip)
        self.hyperthoughtTemplateSelect.setText(QCoreApplication.translate("UseTemplateWidget", u"Select", None))
        self.addMetadataFileCheckBox.setText(QCoreApplication.translate("UseTemplateWidget", u"Add Extracted Metadata File To File List", None))
#if QT_CONFIG(tooltip)
        self.removeUseTableRowButton.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Removes the selected rows from the table", None))
#endif // QT_CONFIG(tooltip)
        self.removeUseTableRowButton.setText("")
        self.useTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("UseTemplateWidget", u"Search table using wildcard (*.*)", None))
        self.use_label_3.setText(QCoreApplication.translate("UseTemplateWidget", u"Search Table", None))
#if QT_CONFIG(tooltip)
        self.appendUseTableRowButton.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Add a Custom Value that is only going to be used for this upload", None))
#endif // QT_CONFIG(tooltip)
        self.appendUseTableRowButton.setText("")
#if QT_CONFIG(tooltip)
        self.clearUseButton.setToolTip(QCoreApplication.translate("UseTemplateWidget", u"Reset all 'Create Template' input fields. All fields will be reset to an empty state.", None))
#endif // QT_CONFIG(tooltip)
        self.clearUseButton.setText(QCoreApplication.translate("UseTemplateWidget", u"Reset All Fields", None))
        self.error_label.setText(QCoreApplication.translate("UseTemplateWidget", u"TextLabel", None))
    # retranslateUi

