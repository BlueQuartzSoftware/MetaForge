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
        self.gridLayout = QGridLayout(CreateTemplateWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.dataFileParserWidget = QWidget(CreateTemplateWidget)
        self.dataFileParserWidget.setObjectName(u"dataFileParserWidget")
        self.gridLayout_2 = QGridLayout(self.dataFileParserWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.fileParserLabel = QLabel(self.dataFileParserWidget)
        self.fileParserLabel.setObjectName(u"fileParserLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileParserLabel.sizePolicy().hasHeightForWidth())
        self.fileParserLabel.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.fileParserLabel)

        self.fileParserCombo = QComboBox(self.dataFileParserWidget)
        self.fileParserCombo.setObjectName(u"fileParserCombo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.fileParserCombo.sizePolicy().hasHeightForWidth())
        self.fileParserCombo.setSizePolicy(sizePolicy1)
        self.fileParserCombo.setMaxCount(2147483647)
        self.fileParserCombo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.fileParserCombo.setMinimumContentsLength(0)
        self.fileParserCombo.setIconSize(QSize(16, 16))

        self.horizontalLayout.addWidget(self.fileParserCombo)

        self.parser_path_label = QLabel(self.dataFileParserWidget)
        self.parser_path_label.setObjectName(u"parser_path_label")

        self.horizontalLayout.addWidget(self.parser_path_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 0, 1, 3)

        self.data_file_label = QLabel(self.dataFileParserWidget)
        self.data_file_label.setObjectName(u"data_file_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.data_file_label.sizePolicy().hasHeightForWidth())
        self.data_file_label.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.data_file_label, 0, 0, 2, 1)

        self.dataFileSelect = QPushButton(self.dataFileParserWidget)
        self.dataFileSelect.setObjectName(u"dataFileSelect")

        self.gridLayout_2.addWidget(self.dataFileSelect, 0, 2, 2, 1)

        self.dataFileLineEdit = QLineEdit(self.dataFileParserWidget)
        self.dataFileLineEdit.setObjectName(u"dataFileLineEdit")
        self.dataFileLineEdit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.dataFileLineEdit, 0, 1, 2, 1)


        self.gridLayout.addWidget(self.dataFileParserWidget, 0, 0, 1, 1)

        self.splitter = QSplitter(CreateTemplateWidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.create_widget_2 = QWidget(self.splitter)
        self.create_widget_2.setObjectName(u"create_widget_2")
        self.gridLayout_9 = QGridLayout(self.create_widget_2)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_9.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, 0, 0)
        self.create_label_2 = QLabel(self.create_widget_2)
        self.create_label_2.setObjectName(u"create_label_2")

        self.horizontalLayout_5.addWidget(self.create_label_2)

        self.createTemplateTreeSearchBar = QLineEdit(self.create_widget_2)
        self.createTemplateTreeSearchBar.setObjectName(u"createTemplateTreeSearchBar")

        self.horizontalLayout_5.addWidget(self.createTemplateTreeSearchBar)


        self.gridLayout_9.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.metadataTreeView = QTreeView(self.create_widget_2)
        self.metadataTreeView.setObjectName(u"metadataTreeView")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.metadataTreeView.sizePolicy().hasHeightForWidth())
        self.metadataTreeView.setSizePolicy(sizePolicy3)
        self.metadataTreeView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadataTreeView.setAlternatingRowColors(True)

        self.gridLayout_9.addWidget(self.metadataTreeView, 1, 0, 1, 1)

        self.splitter.addWidget(self.create_widget_2)
        self.create_widget_1 = QWidget(self.splitter)
        self.create_widget_1.setObjectName(u"create_widget_1")
        self.create_widget_1.setMinimumSize(QSize(200, 0))
        self.gridLayout_8 = QGridLayout(self.create_widget_1)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setContentsMargins(1, 1, 1, 1)
        self.metadata_table_view = QTableView(self.create_widget_1)
        self.metadata_table_view.setObjectName(u"metadata_table_view")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.metadata_table_view.sizePolicy().hasHeightForWidth())
        self.metadata_table_view.setSizePolicy(sizePolicy4)
        self.metadata_table_view.setAcceptDrops(True)
        self.metadata_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.metadata_table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.metadata_table_view.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked)
        self.metadata_table_view.setProperty("showDropIndicator", True)
        self.metadata_table_view.setDragEnabled(True)
        self.metadata_table_view.setDragDropOverwriteMode(False)
        self.metadata_table_view.setDragDropMode(QAbstractItemView.InternalMove)
        self.metadata_table_view.setDefaultDropAction(Qt.MoveAction)
        self.metadata_table_view.setAlternatingRowColors(True)
        self.metadata_table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.metadata_table_view.setShowGrid(False)
        self.metadata_table_view.setSortingEnabled(True)
        self.metadata_table_view.setCornerButtonEnabled(False)
        self.metadata_table_view.horizontalHeader().setStretchLastSection(True)
        self.metadata_table_view.verticalHeader().setVisible(False)
        self.metadata_table_view.verticalHeader().setMinimumSectionSize(15)

        self.gridLayout_8.addWidget(self.metadata_table_view, 3, 0, 3, 6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, -1, 0, 0)
        self.create_label_1 = QLabel(self.create_widget_1)
        self.create_label_1.setObjectName(u"create_label_1")

        self.horizontalLayout_4.addWidget(self.create_label_1)

        self.createTemplateListSearchBar = QLineEdit(self.create_widget_1)
        self.createTemplateListSearchBar.setObjectName(u"createTemplateListSearchBar")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.createTemplateListSearchBar.sizePolicy().hasHeightForWidth())
        self.createTemplateListSearchBar.setSizePolicy(sizePolicy5)

        self.horizontalLayout_4.addWidget(self.createTemplateListSearchBar)

        self.appendCreateTableRowButton = QPushButton(self.create_widget_1)
        self.appendCreateTableRowButton.setObjectName(u"appendCreateTableRowButton")
        sizePolicy6 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.appendCreateTableRowButton.sizePolicy().hasHeightForWidth())
        self.appendCreateTableRowButton.setSizePolicy(sizePolicy6)
        self.appendCreateTableRowButton.setMinimumSize(QSize(40, 0))
        self.appendCreateTableRowButton.setMaximumSize(QSize(40, 16777215))
        icon = QIcon()
        icon.addFile(u":/resources/Images/plus@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.appendCreateTableRowButton.setIcon(icon)
        self.appendCreateTableRowButton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.appendCreateTableRowButton)

        self.removeCreateTableRowButton = QPushButton(self.create_widget_1)
        self.removeCreateTableRowButton.setObjectName(u"removeCreateTableRowButton")
        sizePolicy6.setHeightForWidth(self.removeCreateTableRowButton.sizePolicy().hasHeightForWidth())
        self.removeCreateTableRowButton.setSizePolicy(sizePolicy6)
        self.removeCreateTableRowButton.setMinimumSize(QSize(40, 0))
        self.removeCreateTableRowButton.setMaximumSize(QSize(40, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/resources/Images/trash_can@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeCreateTableRowButton.setIcon(icon1)
        self.removeCreateTableRowButton.setIconSize(QSize(18, 18))
        self.removeCreateTableRowButton.setFlat(True)

        self.horizontalLayout_4.addWidget(self.removeCreateTableRowButton)


        self.gridLayout_8.addLayout(self.horizontalLayout_4, 1, 0, 1, 6)

        self.gridLayout_8.setRowStretch(5, 1)
        self.splitter.addWidget(self.create_widget_1)

        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(8, 0, 8, 4)
        self.clearCreateButton = QPushButton(CreateTemplateWidget)
        self.clearCreateButton.setObjectName(u"clearCreateButton")

        self.gridLayout_4.addWidget(self.clearCreateButton, 0, 0, 1, 1)

        self.saveTemplateButton = QPushButton(CreateTemplateWidget)
        self.saveTemplateButton.setObjectName(u"saveTemplateButton")
        self.saveTemplateButton.setFlat(False)

        self.gridLayout_4.addWidget(self.saveTemplateButton, 0, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(1227, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)

        self.error_label = QLabel(CreateTemplateWidget)
        self.error_label.setObjectName(u"error_label")

        self.gridLayout_4.addWidget(self.error_label, 1, 0, 1, 3)


        self.gridLayout.addLayout(self.gridLayout_4, 2, 0, 1, 1)

        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(CreateTemplateWidget)

        self.saveTemplateButton.setDefault(False)


        QMetaObject.connectSlotsByName(CreateTemplateWidget)
    # setupUi

    def retranslateUi(self, CreateTemplateWidget):
        CreateTemplateWidget.setWindowTitle(QCoreApplication.translate("CreateTemplateWidget", u"Create Template Widget", None))
        self.fileParserLabel.setText(QCoreApplication.translate("CreateTemplateWidget", u"Parser:", None))
#if QT_CONFIG(tooltip)
        self.fileParserCombo.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"The parser used to parse and extract the metadata from the data file above. ", None))
#endif // QT_CONFIG(tooltip)
        self.fileParserCombo.setCurrentText("")
        self.parser_path_label.setText("")
        self.data_file_label.setText(QCoreApplication.translate("CreateTemplateWidget", u"Data File:", None))
#if QT_CONFIG(tooltip)
        self.dataFileSelect.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Select data file to use for metadata extraction", None))
#endif // QT_CONFIG(tooltip)
        self.dataFileSelect.setText(QCoreApplication.translate("CreateTemplateWidget", u"Select", None))
#if QT_CONFIG(tooltip)
        self.dataFileLineEdit.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"This data file will be used as the model to create the template file.", None))
#endif // QT_CONFIG(tooltip)
        self.dataFileLineEdit.setText("")
        self.dataFileLineEdit.setPlaceholderText(QCoreApplication.translate("CreateTemplateWidget", u"Drag a file here or select one using the 'Select' button to the right===>", None))
        self.create_label_2.setText(QCoreApplication.translate("CreateTemplateWidget", u"Search Table", None))
        self.createTemplateTreeSearchBar.setPlaceholderText(QCoreApplication.translate("CreateTemplateWidget", u"Search metadata keys using wildcard (*.*)", None))
#if QT_CONFIG(tooltip)
        self.metadataTreeView.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"The metadata structure found inside the Data File.  Checked metadata entries are chosen to be included in the new template file and will appear in the table on the right.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.metadata_table_view.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"The metadata chosen to be included in the new template file.", None))
#endif // QT_CONFIG(tooltip)
        self.create_label_1.setText(QCoreApplication.translate("CreateTemplateWidget", u"Search Table", None))
        self.createTemplateListSearchBar.setPlaceholderText(QCoreApplication.translate("CreateTemplateWidget", u"Search metadata items using wildcard (*.*)", None))
#if QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Add a Custom Value that will be included with every use of the template", None))
#endif // QT_CONFIG(tooltip)
        self.appendCreateTableRowButton.setText("")
#if QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Remove selected metadata items from the table", None))
#endif // QT_CONFIG(tooltip)
        self.removeCreateTableRowButton.setText("")
#if QT_CONFIG(tooltip)
        self.clearCreateButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Reset all 'Create Template' input fields. All fields will be reset to an empty state.", None))
#endif // QT_CONFIG(tooltip)
        self.clearCreateButton.setText(QCoreApplication.translate("CreateTemplateWidget", u"Reset All Fields", None))
#if QT_CONFIG(tooltip)
        self.saveTemplateButton.setToolTip(QCoreApplication.translate("CreateTemplateWidget", u"Save Values to a .ez template file. You can also use standard 'Save' Shortcut key", None))
#endif // QT_CONFIG(tooltip)
        self.saveTemplateButton.setText(QCoreApplication.translate("CreateTemplateWidget", u"Save Template", None))
        self.error_label.setText(QCoreApplication.translate("CreateTemplateWidget", u"TextLabel", None))
    # retranslateUi

