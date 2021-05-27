# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hyperthoughtdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_HyperthoughtDialog(object):
    def setupUi(self, HyperthoughtDialog):
        if not HyperthoughtDialog.objectName():
            HyperthoughtDialog.setObjectName(u"HyperthoughtDialog")
        HyperthoughtDialog.resize(734, 513)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HyperthoughtDialog.sizePolicy().hasHeightForWidth())
        HyperthoughtDialog.setSizePolicy(sizePolicy)
        HyperthoughtDialog.setModal(True)
        self.gridLayout = QGridLayout(HyperthoughtDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.apiKeyLabel = QLabel(HyperthoughtDialog)
        self.apiKeyLabel.setObjectName(u"apiKeyLabel")

        self.gridLayout.addWidget(self.apiKeyLabel, 0, 0, 1, 2)

        self.apiKeyLineEdit = QLineEdit(HyperthoughtDialog)
        self.apiKeyLineEdit.setObjectName(u"apiKeyLineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.apiKeyLineEdit.sizePolicy().hasHeightForWidth())
        self.apiKeyLineEdit.setSizePolicy(sizePolicy1)
        self.apiKeyLineEdit.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.apiKeyLineEdit, 0, 2, 1, 2)

        self.apiKeyButton = QPushButton(HyperthoughtDialog)
        self.apiKeyButton.setObjectName(u"apiKeyButton")

        self.gridLayout.addWidget(self.apiKeyButton, 0, 4, 1, 1)

        self.frame = QFrame(HyperthoughtDialog)
        self.frame.setObjectName(u"frame")
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.directoryLabel = QLabel(self.frame)
        self.directoryLabel.setObjectName(u"directoryLabel")

        self.horizontalLayout.addWidget(self.directoryLabel)

        self.horizontalSpacer_2 = QSpacerItem(569, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.parentDirectoryButton = QToolButton(self.frame)
        self.parentDirectoryButton.setObjectName(u"parentDirectoryButton")

        self.horizontalLayout.addWidget(self.parentDirectoryButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.newFolderButton = QToolButton(self.frame)
        self.newFolderButton.setObjectName(u"newFolderButton")
        icon = QIcon()
        iconThemeName = u"SP_FileDialogNewFolder"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        
        self.newFolderButton.setIcon(icon)

        self.horizontalLayout.addWidget(self.newFolderButton)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.gridLayout.addWidget(self.frame, 1, 0, 1, 5)

        self.listView = QListView(HyperthoughtDialog)
        self.listView.setObjectName(u"listView")

        self.gridLayout.addWidget(self.listView, 2, 0, 1, 5)

        self.locationLabel = QLabel(HyperthoughtDialog)
        self.locationLabel.setObjectName(u"locationLabel")

        self.gridLayout.addWidget(self.locationLabel, 3, 0, 1, 1)

        self.locationLineEdit = QLineEdit(HyperthoughtDialog)
        self.locationLineEdit.setObjectName(u"locationLineEdit")

        self.gridLayout.addWidget(self.locationLineEdit, 3, 1, 1, 4)

        self.horizontalSpacer = QSpacerItem(380, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 2, 1, 1)

        self.buttonBox = QDialogButtonBox(HyperthoughtDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 3, 1, 2)


        self.retranslateUi(HyperthoughtDialog)
        self.buttonBox.accepted.connect(HyperthoughtDialog.accept)
        self.buttonBox.rejected.connect(HyperthoughtDialog.reject)

        QMetaObject.connectSlotsByName(HyperthoughtDialog)
    # setupUi

    def retranslateUi(self, HyperthoughtDialog):
        HyperthoughtDialog.setWindowTitle("")
        self.apiKeyLabel.setText(QCoreApplication.translate("HyperthoughtDialog", u"Hyperthought API Key:", None))
        self.apiKeyButton.setText(QCoreApplication.translate("HyperthoughtDialog", u"Submit", None))
        self.directoryLabel.setText(QCoreApplication.translate("HyperthoughtDialog", u"/", None))
        self.parentDirectoryButton.setText(QCoreApplication.translate("HyperthoughtDialog", u"...", None))
        self.newFolderButton.setText(QCoreApplication.translate("HyperthoughtDialog", u"...", None))
        self.locationLabel.setText(QCoreApplication.translate("HyperthoughtDialog", u"Location:", None))
    # retranslateUi

