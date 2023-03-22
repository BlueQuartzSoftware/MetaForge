# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'createtemplatewidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from  . import resources_rc

class Ui_CreateTemplateWidget(object):
    def setupUi(self, CreateTemplateWidget):
        if not CreateTemplateWidget.objectName():
            CreateTemplateWidget.setObjectName(u"CreateTemplateWidget")
        CreateTemplateWidget.resize(1493, 840)
        self.gridLayout_2 = QGridLayout(CreateTemplateWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(-1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(8, -1, 8, 0)
        self.create_frame_2 = QFrame(CreateTemplateWidget)
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
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.metadataTreeView.sizePolicy().hasHeightForWidth())
        self.metadataTreeView.setSizePolicy(sizePolicy)
        self.metadataTreeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTreeView.setAlternatingRowColors(True)

        self.gridLayout_9.addWidget(self.metadataTreeView, 1, 0, 1, 1)


        self.horizontalLayout_6.addWidget(self.create_frame_2)

        self.create_frame_1 = QFrame(CreateTemplateWidget)
        self.create_frame_1.setObjectName(u"create_frame_1")
        self.create_frame_1.setMinimumSize(QSize(200, 0))
        self.create_frame_1.setFrameShape(QFrame.StyledPanel)
        self.create_frame_1.setFrameShadow(QFrame.Raised)
        self.gridLayout_8 = QGridLayout(self.create_frame_1)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.metadata_table_view = QTableView(self.create_frame_1)
        self.metadata_table_view.setObjectName(u"metadata_table_view")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.metadata_table_view.sizePolicy().hasHeightForWidth())
        self.metadata_table_view.setSizePolicy(sizePolicy1)
        self.metadata_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.metadata_table_view.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked)
        self.metadata_table_view.setProperty("showDropIndicator", False)
        self.metadata_table_view.setDragDropOverwriteMode(False)
        self.metadata_table_view.setAlternatingRowColors(True)
        self.metadata_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.metadata_table_view.setShowGrid(False)
        self.metadata_table_view.setSortingEnabled(True)
        self.metadata_table_view.setCornerButtonEnabled(False)
        self.metadata_table_view.horizontalHeader().setStretchLastSection(True)
        self.metadata_table_view.verticalHeader().setVisible(False)
        self.metadata_table_view.verticalHeader().setMinimumSectionSize(15)

        self.gridLayout_8.addWidget(self.metadata_table_view, 2, 0, 1, 3)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_8.addItem(self.horizontalSpacer_8, 3, 0, 1, 1)

        self.removeCreateTableRowButton = QPushButton(self.create_frame_1)
        self.removeCreateTableRowButton.setObjectName(u"removeCreateTableRowButton")
        self.removeCreateTableRowButton.setMinimumSize(QSize(40, 0))
        self.removeCreateTableRowButton.setMaximumSize(QSize(40, 16777215))
        icon = QIcon()
        icon.addFile(u":/resources/Images/delete@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeCreateTableRowButton.setIcon(icon)
        self.removeCreateTableRowButton.setFlat(True)

        self.gridLayout_8.addWidget(self.removeCreateTableRowButton, 3, 2, 1, 1)

        self.appendCreateTableRowButton = QPushButton(self.create_frame_1)
        self.appendCreateTableRowButton.setObjectName(u"appendCreateTableRowButton")
        self.appendCreateTableRowButton.setMinimumSize(QSize(40, 0))
        self.appendCreateTableRowButton.setMaximumSize(QSize(40, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/resources/Images/plus@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appendCreateTableRowButton.setIcon(icon1)
        self.appendCreateTableRowButton.setFlat(True)

        self.gridLayout_8.addWidget(self.appendCreateTableRowButton, 3, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.create_label_1 = QLabel(self.create_frame_1)
        self.create_label_1.setObjectName(u"create_label_1")

        self.horizontalLayout_4.addWidget(self.create_label_1)

        self.createTemplateListSearchBar = QLineEdit(self.create_frame_1)
        self.createTemplateListSearchBar.setObjectName(u"createTemplateListSearchBar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.createTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.createTemplateListSearchBar.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.createTemplateListSearchBar)


        self.gridLayout_8.addLayout(self.horizontalLayout_4, 1, 0, 1, 3)


        self.horizontalLayout_6.addWidget(self.create_frame_1)

        self.horizontalLayout_6.setStretch(0, 25)
        self.horizontalLayout_6.setStretch(1, 75)

        self.gridLayout_2.addLayout(self.horizontalLayout_6, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(9)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.data_file_label = QLabel(CreateTemplateWidget)
        self.data_file_label.setObjectName(u"data_file_label")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.data_file_label.sizePolicy().hasHeightForWidth())
        self.data_file_label.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.data_file_label)

        self.dataFileLineEdit = QLineEdit(CreateTemplateWidget)
        self.dataFileLineEdit.setObjectName(u"dataFileLineEdit")
        self.dataFileLineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.dataFileLineEdit)

        self.dataFileSelect = QPushButton(CreateTemplateWidget)
        self.dataFileSelect.setObjectName(u"dataFileSelect")

        self.horizontalLayout_2.addWidget(self.dataFileSelect)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.fileParserLabel = QLabel(CreateTemplateWidget)
        self.fileParserLabel.setObjectName(u"fileParserLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.fileParserLabel.sizePolicy().hasHeightForWidth())
        self.fileParserLabel.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.fileParserLabel)

        self.fileParserCombo = QComboBox(CreateTemplateWidget)
        self.fileParserCombo.setObjectName(u"fileParserCombo")

        self.horizontalLayout_3.addWidget(self.fileParserCombo)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 0, 8, 4)
        self.saveTemplateButton = QPushButton(CreateTemplateWidget)
        self.saveTemplateButton.setObjectName(u"saveTemplateButton")
        self.saveTemplateButton.setFlat(False)

        self.gridLayout_4.addWidget(self.saveTemplateButton, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(1227, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)

        self.clearCreateButton = QPushButton(CreateTemplateWidget)
        self.clearCreateButton.setObjectName(u"clearCreateButton")

        self.gridLayout_4.addWidget(self.clearCreateButton, 0, 0, 1, 1)

        self.error_label = QLabel(CreateTemplateWidget)
        self.error_label.setObjectName(u"error_label")

        self.gridLayout_4.addWidget(self.error_label, 1, 0, 1, 3)


        self.gridLayout_2.addLayout(self.gridLayout_4, 3, 0, 1, 1)


        self.retranslateUi(CreateTemplateWidget)

        self.saveTemplateButton.setDefault(False)


        QMetaObject.connectSlotsByName(CreateTemplateWidget)
    # setupUi

    def retranslateUi(self, CreateTemplateWidget):
        CreateTemplateWidget.setWindowTitle(QCoreApplication.translate("CreateTemplateWidget", u"Create Template Widget", None))
        self.create_label_2.setText(QCoreApplication.translate("CreateTemplateWidget", u"Search Table", None))
        self.createTemplateTreeSearchBar.setPlaceholderText(QCoreApplication.translate("CreateTemplateWidget", u"Search metadata keys using wildcard (*.*)", None))
#if QT_CONFIG(tooltip)
        self.metadataTreeView.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"The metadata structure found inside the Data File.  Checked metadata entries are chosen to be included in the new template file and will appear in the table on the right.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.metadata_table_view.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"The metadata chosen to be included in the new template file.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Remove a custom value from the template", None))
#endif // QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setText("")
#if QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Add a custom value to the template", None))
#endif // QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setText("")
        self.create_label_1.setText(QCoreApplication.translate("CreateTemplateWidget", u"Search Table", None))
        self.createTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("CreateTemplateWidget", u"Search table using wildcard (*.*)", None))
        self.data_file_label.setText(QCoreApplication.translate("CreateTemplateWidget", u"Data File", None))
#if QT_CONFIG(tooltip)
        self.dataFileLineEdit.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"This data file will be used as the model to create the template file.", None))
#endif // QT_CONFIG(tooltip)
        self.dataFileLineEdit.setText("")
        self.dataFileLineEdit.setPlaceholderText(QCoreApplication.translate("CreateTemplateWidget", u"Drag a file here or select one using the 'Select' button to the right===>", None))
#if QT_CONFIG(tooltip)
        self.dataFileSelect.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Select data file to use for metadata extraction", None))
#endif // QT_CONFIG(tooltip)
        self.dataFileSelect.setText(QCoreApplication.translate("CreateTemplateWidget", u"Select", None))
        self.fileParserLabel.setText(QCoreApplication.translate("CreateTemplateWidget", u"File Parser", None))
#if QT_CONFIG(tooltip)
        self.fileParserCombo.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"The parser used to parse and extract the metadata from the data file above. ", None))
#endif // QT_CONFIG(tooltip)
        self.fileParserCombo.setCurrentText("")
#if QT_CONFIG(tooltip)
        self.saveTemplateButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Save Values to a .ez template file. You can also use standard 'Save' Shortcut key", None))
#endif // QT_CONFIG(tooltip)
        self.saveTemplateButton.setText(QCoreApplication.translate("CreateTemplateWidget", u"Save Template as ...", None))
#if QT_CONFIG(tooltip)
        self.clearCreateButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Reset all 'Create Template' input fields. All fields will be reset to an empty state.", None))
#endif // QT_CONFIG(tooltip)
        self.clearCreateButton.setText(QCoreApplication.translate("CreateTemplateWidget", u"Reset All Fields", None))
        self.error_label.setText(QCoreApplication.translate("CreateTemplateWidget", u"TextLabel", None))
    # retranslateUi

