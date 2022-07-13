# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'metaforge_preferences.ui'
##
## Created by: Qt User Interface Compiler version 5.15.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc

class Ui_MetaForgePreferences(object):
    def setupUi(self, MetaForgePreferences):
        if not MetaForgePreferences.objectName():
            MetaForgePreferences.setObjectName(u"MetaForgePreferences")
        MetaForgePreferences.resize(777, 528)
        self.gridLayout = QGridLayout(MetaForgePreferences)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(4)
        self.gridLayout_2.setVerticalSpacing(-1)
        self.gridLayout_2.setContentsMargins(-1, 0, 0, -1)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 6, 2, 1, 1)

        self.removeBtn = QPushButton(MetaForgePreferences)
        self.removeBtn.setObjectName(u"removeBtn")
        self.removeBtn.setMinimumSize(QSize(24, 24))
        self.removeBtn.setMaximumSize(QSize(24, 24))
        icon = QIcon()
        icon.addFile(u":/resources/Images/close-pushed@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeBtn.setIcon(icon)
        self.removeBtn.setIconSize(QSize(24, 24))
        self.removeBtn.setFlat(True)

        self.gridLayout_2.addWidget(self.removeBtn, 5, 2, 1, 1)

        self.addBtn = QPushButton(MetaForgePreferences)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMinimumSize(QSize(24, 24))
        self.addBtn.setMaximumSize(QSize(24, 24))
        icon1 = QIcon()
        icon1.addFile(u":/resources/Images/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.addBtn.setIcon(icon1)
        self.addBtn.setIconSize(QSize(24, 24))
        self.addBtn.setFlat(True)

        self.gridLayout_2.addWidget(self.addBtn, 3, 2, 2, 1)

        self.parser_locations_label = QLabel(MetaForgePreferences)
        self.parser_locations_label.setObjectName(u"parser_locations_label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.parser_locations_label.setFont(font)

        self.gridLayout_2.addWidget(self.parser_locations_label, 0, 0, 1, 3)

        self.parser_locations_list = QListWidget(MetaForgePreferences)
        self.parser_locations_list.setObjectName(u"parser_locations_list")

        self.gridLayout_2.addWidget(self.parser_locations_list, 3, 0, 4, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 0, 0, -1)
        self.include_default_parser_location = QCheckBox(MetaForgePreferences)
        self.include_default_parser_location.setObjectName(u"include_default_parser_location")

        self.horizontalLayout.addWidget(self.include_default_parser_location)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 2)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(MetaForgePreferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.error_string = QLabel(MetaForgePreferences)
        self.error_string.setObjectName(u"error_string")

        self.gridLayout.addWidget(self.error_string, 1, 0, 1, 1)


        self.retranslateUi(MetaForgePreferences)
        self.buttonBox.accepted.connect(MetaForgePreferences.accept)
        self.buttonBox.rejected.connect(MetaForgePreferences.reject)

        QMetaObject.connectSlotsByName(MetaForgePreferences)
    # setupUi

    def retranslateUi(self, MetaForgePreferences):
        MetaForgePreferences.setWindowTitle(QCoreApplication.translate("MetaForgePreferences", u"Preferences", None))
#if QT_CONFIG(tooltip)
        self.removeBtn.setToolTip(QCoreApplication.translate("MetaForgePreferences", u"Use this button to remove non-existant arrays out of the \"Selected Data Arrays\" column", None))
#endif // QT_CONFIG(tooltip)
        self.removeBtn.setText("")
#if QT_CONFIG(tooltip)
        self.addBtn.setToolTip(QCoreApplication.translate("MetaForgePreferences", u"Use this button to move an array up in the \"Selected Data Arrays\" column", None))
#endif // QT_CONFIG(tooltip)
        self.addBtn.setText("")
        self.parser_locations_label.setText(QCoreApplication.translate("MetaForgePreferences", u"Parser Locations", None))
        self.include_default_parser_location.setText("")
        self.error_string.setText(QCoreApplication.translate("MetaForgePreferences", u"ERROR_STRING", None))
    # retranslateUi

