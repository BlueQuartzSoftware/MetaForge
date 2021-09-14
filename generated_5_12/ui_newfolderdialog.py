# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/mjackson/Workspace4/MetaForge/newfolderdialog.ui',
# licensing of '/Users/mjackson/Workspace4/MetaForge/newfolderdialog.ui' applies.
#
# Created: Tue Sep 14 17:44:51 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_NewFolderDialog(object):
    def setupUi(self, NewFolderDialog):
        NewFolderDialog.setObjectName("NewFolderDialog")
        NewFolderDialog.resize(448, 96)
        NewFolderDialog.setWindowTitle("")
        self.gridLayout = QtWidgets.QGridLayout(NewFolderDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.folderNameLabel = QtWidgets.QLabel(NewFolderDialog)
        self.folderNameLabel.setObjectName("folderNameLabel")
        self.gridLayout.addWidget(self.folderNameLabel, 0, 0, 1, 1)
        self.folderNameLineEdit = QtWidgets.QLineEdit(NewFolderDialog)
        self.folderNameLineEdit.setObjectName("folderNameLineEdit")
        self.gridLayout.addWidget(self.folderNameLineEdit, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewFolderDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(NewFolderDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewFolderDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewFolderDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFolderDialog)

    def retranslateUi(self, NewFolderDialog):
        self.folderNameLabel.setText(QtWidgets.QApplication.translate("NewFolderDialog", "Folder Name:", None, -1))

