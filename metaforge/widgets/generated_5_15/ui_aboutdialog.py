# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'aboutdialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

from  . import resources_rc
from  . import resources_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(510, 175)
        icon = QIcon()
        icon.addFile(u":/resources/Images/applicationIcon.png", QSize(), QIcon.Normal, QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.gridLayout = QGridLayout(AboutDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(24)
        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QSize(128, 128))
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setPixmap(QPixmap(u":/resources/Images/MetaForge.icns"))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)

        self.gridLayout.addWidget(self.label, 0, 0, 2, 1)

        self.ApplicationNameLabel = QLabel(AboutDialog)
        self.ApplicationNameLabel.setObjectName(u"ApplicationNameLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ApplicationNameLabel.sizePolicy().hasHeightForWidth())
        self.ApplicationNameLabel.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ApplicationNameLabel.setFont(font)
        self.ApplicationNameLabel.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.gridLayout.addWidget(self.ApplicationNameLabel, 0, 1, 1, 1)

        self.aboutDetailsLabel = QLabel(AboutDialog)
        self.aboutDetailsLabel.setObjectName(u"aboutDetailsLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.aboutDetailsLabel.sizePolicy().hasHeightForWidth())
        self.aboutDetailsLabel.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(11)
        self.aboutDetailsLabel.setFont(font1)
        self.aboutDetailsLabel.setAlignment(Qt.AlignJustify|Qt.AlignTop)

        self.gridLayout.addWidget(self.aboutDetailsLabel, 1, 1, 2, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)


        self.retranslateUi(AboutDialog)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle("")
        self.label.setText("")
        self.ApplicationNameLabel.setText(QCoreApplication.translate("AboutDialog", u"--", None))
        self.aboutDetailsLabel.setText(QCoreApplication.translate("AboutDialog", u"--", None))
    # retranslateUi

