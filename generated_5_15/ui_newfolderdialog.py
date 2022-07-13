# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'newfolderdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_NewFolderDialog(object):
    def setupUi(self, NewFolderDialog):
        if not NewFolderDialog.objectName():
            NewFolderDialog.setObjectName(u"NewFolderDialog")
        NewFolderDialog.resize(448, 96)
        self.gridLayout = QGridLayout(NewFolderDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.folderNameLabel = QLabel(NewFolderDialog)
        self.folderNameLabel.setObjectName(u"folderNameLabel")

        self.gridLayout.addWidget(self.folderNameLabel, 0, 0, 1, 1)

        self.folderNameLineEdit = QLineEdit(NewFolderDialog)
        self.folderNameLineEdit.setObjectName(u"folderNameLineEdit")

        self.gridLayout.addWidget(self.folderNameLineEdit, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(NewFolderDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)


        self.retranslateUi(NewFolderDialog)
        self.buttonBox.accepted.connect(NewFolderDialog.accept)
        self.buttonBox.rejected.connect(NewFolderDialog.reject)

        QMetaObject.connectSlotsByName(NewFolderDialog)
    # setupUi

    def retranslateUi(self, NewFolderDialog):
        NewFolderDialog.setWindowTitle("")
        self.folderNameLabel.setText(QCoreApplication.translate("NewFolderDialog", u"Folder Name:", None))
    # retranslateUi

