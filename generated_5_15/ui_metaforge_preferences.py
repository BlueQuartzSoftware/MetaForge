# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'metaforge_preferences.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
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
        self.buttonBox = QDialogButtonBox(MetaForgePreferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.removeBtn = QPushButton(MetaForgePreferences)
        self.removeBtn.setObjectName(u"removeBtn")
        self.removeBtn.setIconSize(QSize(24, 24))
        self.removeBtn.setFlat(False)

        self.gridLayout_2.addWidget(self.removeBtn, 0, 3, 1, 1)

        self.parser_locations_label = QLabel(MetaForgePreferences)
        self.parser_locations_label.setObjectName(u"parser_locations_label")

        self.gridLayout_2.addWidget(self.parser_locations_label, 0, 0, 1, 1)

        self.addBtn = QPushButton(MetaForgePreferences)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setIconSize(QSize(24, 24))
        self.addBtn.setFlat(False)

        self.gridLayout_2.addWidget(self.addBtn, 0, 2, 1, 1)

        self.parser_locations_list = QListWidget(MetaForgePreferences)
        self.parser_locations_list.setObjectName(u"parser_locations_list")

        self.gridLayout_2.addWidget(self.parser_locations_list, 1, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

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
        self.removeBtn.setText(QCoreApplication.translate("MetaForgePreferences", u"Remove Folders", None))
        self.parser_locations_label.setText(QCoreApplication.translate("MetaForgePreferences", u"Parser Locations", None))
#if QT_CONFIG(tooltip)
        self.addBtn.setToolTip(QCoreApplication.translate("MetaForgePreferences", u"Use this button to move an array up in the \"Selected Data Arrays\" column", None))
#endif // QT_CONFIG(tooltip)
        self.addBtn.setText(QCoreApplication.translate("MetaForgePreferences", u"Add Folders", None))
        self.error_string.setText(QCoreApplication.translate("MetaForgePreferences", u"ERROR_STRING", None))
    # retranslateUi

