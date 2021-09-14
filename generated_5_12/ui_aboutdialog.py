# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/mjackson/Workspace4/MetaForge/aboutdialog.ui',
# licensing of '/Users/mjackson/Workspace4/MetaForge/aboutdialog.ui' applies.
#
# Created: Tue Sep 14 17:44:51 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(510, 175)
        AboutDialog.setWindowTitle("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/Images/applicationIcon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(AboutDialog)
        self.gridLayout.setHorizontalSpacing(24)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(128, 128))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/resources/Images/MetaForge.icns"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)
        self.ApplicationNameLabel = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ApplicationNameLabel.sizePolicy().hasHeightForWidth())
        self.ApplicationNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.ApplicationNameLabel.setFont(font)
        self.ApplicationNameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ApplicationNameLabel.setObjectName("ApplicationNameLabel")
        self.gridLayout.addWidget(self.ApplicationNameLabel, 0, 1, 1, 1)
        self.aboutDetailsLabel = QtWidgets.QLabel(AboutDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutDetailsLabel.sizePolicy().hasHeightForWidth())
        self.aboutDetailsLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.aboutDetailsLabel.setFont(font)
        self.aboutDetailsLabel.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.aboutDetailsLabel.setObjectName("aboutDetailsLabel")
        self.gridLayout.addWidget(self.aboutDetailsLabel, 1, 1, 2, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)

        self.retranslateUi(AboutDialog)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        self.ApplicationNameLabel.setText(QtWidgets.QApplication.translate("AboutDialog", "--", None, -1))
        self.aboutDetailsLabel.setText(QtWidgets.QApplication.translate("AboutDialog", "--", None, -1))

from . import resources_rc
