# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hyperthoughtdialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

from metaforge.widgets.deselectable_table_view import DeselectableTableView
from . import resources_rc

class Ui_HyperthoughtDialog(object):
    def setupUi(self, HyperthoughtDialog):
        if not HyperthoughtDialog.objectName():
            HyperthoughtDialog.setObjectName(u"HyperthoughtDialog")
        HyperthoughtDialog.resize(867, 497)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HyperthoughtDialog.sizePolicy().hasHeightForWidth())
        HyperthoughtDialog.setSizePolicy(sizePolicy)
        HyperthoughtDialog.setModal(True)
        self.gridLayout = QGridLayout(HyperthoughtDialog)
        self.gridLayout.setSpacing(4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.label = QLabel(HyperthoughtDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.ht_server_url = QLabel(HyperthoughtDialog)
        self.ht_server_url.setObjectName(u"ht_server_url")

        self.horizontalLayout_3.addWidget(self.ht_server_url)

        self.label_3 = QLabel(HyperthoughtDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.ht_username = QLabel(HyperthoughtDialog)
        self.ht_username.setObjectName(u"ht_username")

        self.horizontalLayout_3.addWidget(self.ht_username)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 7)

        self.horizontalSpacer = QSpacerItem(380, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 5, 0, 1, 4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.parentDirectoryButton = QPushButton(HyperthoughtDialog)
        self.parentDirectoryButton.setObjectName(u"parentDirectoryButton")
        icon = QIcon()
        icon.addFile(u":/resources/Images/arrow-top.png", QSize(), QIcon.Normal, QIcon.Off)
        self.parentDirectoryButton.setIcon(icon)
        self.parentDirectoryButton.setIconSize(QSize(16, 16))

        self.horizontalLayout_5.addWidget(self.parentDirectoryButton)

        self.breadcrumbLabel = QLabel(HyperthoughtDialog)
        self.breadcrumbLabel.setObjectName(u"breadcrumbLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.breadcrumbLabel.sizePolicy().hasHeightForWidth())
        self.breadcrumbLabel.setSizePolicy(sizePolicy1)
        self.breadcrumbLabel.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_5.addWidget(self.breadcrumbLabel)

        self.show_files = QCheckBox(HyperthoughtDialog)
        self.show_files.setObjectName(u"show_files")

        self.horizontalLayout_5.addWidget(self.show_files)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.newFolderButton = QPushButton(HyperthoughtDialog)
        self.newFolderButton.setObjectName(u"newFolderButton")
        icon1 = QIcon()
        icon1.addFile(u":/resources/Images/folder@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.newFolderButton.setIcon(icon1)
        self.newFolderButton.setIconSize(QSize(16, 16))

        self.horizontalLayout_5.addWidget(self.newFolderButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)

        self.label_4 = QLabel(HyperthoughtDialog)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.locationLabel = QLabel(HyperthoughtDialog)
        self.locationLabel.setObjectName(u"locationLabel")
        self.locationLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.locationLabel)

        self.selectedFolderLabel = QLineEdit(HyperthoughtDialog)
        self.selectedFolderLabel.setObjectName(u"selectedFolderLabel")

        self.horizontalLayout.addWidget(self.selectedFolderLabel)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.workspaceListView = QListWidget(HyperthoughtDialog)
        self.workspaceListView.setObjectName(u"workspaceListView")

        self.gridLayout_2.addWidget(self.workspaceListView, 1, 0, 2, 1)

        self.folderListView = DeselectableTableView(HyperthoughtDialog)
        self.folderListView.setObjectName(u"folderListView")
        self.folderListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.folderListView.setAlternatingRowColors(False)
        self.folderListView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.folderListView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.folderListView.setShowGrid(False)
        self.folderListView.setCornerButtonEnabled(False)
        self.folderListView.horizontalHeader().setCascadingSectionResizes(True)
        self.folderListView.horizontalHeader().setMinimumSectionSize(100)
        self.folderListView.horizontalHeader().setStretchLastSection(True)
        self.folderListView.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.folderListView, 1, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 33)
        self.gridLayout_2.setColumnStretch(1, 100)

        self.gridLayout.addLayout(self.gridLayout_2, 2, 0, 1, 7)

        self.buttonBox = QDialogButtonBox(HyperthoughtDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy2)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 4, 1, 3)

        self.apiKeyButton = QPushButton(HyperthoughtDialog)
        self.apiKeyButton.setObjectName(u"apiKeyButton")
        sizePolicy.setHeightForWidth(self.apiKeyButton.sizePolicy().hasHeightForWidth())
        self.apiKeyButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.apiKeyButton, 0, 6, 1, 1)

        self.pasteFromClipboardBtn = QPushButton(HyperthoughtDialog)
        self.pasteFromClipboardBtn.setObjectName(u"pasteFromClipboardBtn")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pasteFromClipboardBtn.sizePolicy().hasHeightForWidth())
        self.pasteFromClipboardBtn.setSizePolicy(sizePolicy3)
        self.pasteFromClipboardBtn.setMinimumSize(QSize(34, 34))
        self.pasteFromClipboardBtn.setMaximumSize(QSize(34, 34))
        icon2 = QIcon()
        icon2.addFile(u":/resources/Images/key@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pasteFromClipboardBtn.setIcon(icon2)
        self.pasteFromClipboardBtn.setIconSize(QSize(16, 16))

        self.gridLayout.addWidget(self.pasteFromClipboardBtn, 0, 5, 1, 1)

        self.apiKeyLabel = QLabel(HyperthoughtDialog)
        self.apiKeyLabel.setObjectName(u"apiKeyLabel")

        self.gridLayout.addWidget(self.apiKeyLabel, 0, 0, 1, 1)

        self.apiKeyLineEdit = QLineEdit(HyperthoughtDialog)
        self.apiKeyLineEdit.setObjectName(u"apiKeyLineEdit")
        sizePolicy1.setHeightForWidth(self.apiKeyLineEdit.sizePolicy().hasHeightForWidth())
        self.apiKeyLineEdit.setSizePolicy(sizePolicy1)
        self.apiKeyLineEdit.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.apiKeyLineEdit, 0, 1, 1, 4)


        self.retranslateUi(HyperthoughtDialog)
        self.buttonBox.accepted.connect(HyperthoughtDialog.accept)
        self.buttonBox.rejected.connect(HyperthoughtDialog.reject)

        QMetaObject.connectSlotsByName(HyperthoughtDialog)
    # setupUi

    def retranslateUi(self, HyperthoughtDialog):
        HyperthoughtDialog.setWindowTitle("")
        self.label.setText(QCoreApplication.translate("HyperthoughtDialog", u"Server:", None))
        self.ht_server_url.setText(QCoreApplication.translate("HyperthoughtDialog", u"Not Authenticated", None))
        self.label_3.setText(QCoreApplication.translate("HyperthoughtDialog", u"User:", None))
        self.ht_username.setText(QCoreApplication.translate("HyperthoughtDialog", u"Not Authenticated", None))
#if QT_CONFIG(tooltip)
        self.parentDirectoryButton.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"Move Up a Directory", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.parentDirectoryButton.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.parentDirectoryButton.setText(QCoreApplication.translate("HyperthoughtDialog", u"Up", None))
        self.breadcrumbLabel.setText(QCoreApplication.translate("HyperthoughtDialog", u"/Some/Path/to/Store/Data", None))
#if QT_CONFIG(tooltip)
        self.show_files.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"Show files in the viewer", None))
#endif // QT_CONFIG(tooltip)
        self.show_files.setText(QCoreApplication.translate("HyperthoughtDialog", u"Show Files", None))
#if QT_CONFIG(tooltip)
        self.newFolderButton.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"Create Remote Folder", None))
#endif // QT_CONFIG(tooltip)
        self.newFolderButton.setText(QCoreApplication.translate("HyperthoughtDialog", u"New Remote Folder", None))
        self.label_4.setText(QCoreApplication.translate("HyperthoughtDialog", u"Workspace List:", None))
        self.locationLabel.setText(QCoreApplication.translate("HyperthoughtDialog", u"Folder:", None))
#if QT_CONFIG(tooltip)
        self.selectedFolderLabel.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"The name of the remote folder that you want to upload your files/folders to", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.workspaceListView.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"The list of available workspaces that your HyperThought account can access.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.folderListView.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"Select the directory that you would like to upload your files/folders to", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.apiKeyButton.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"<html><head/><body><p>Authenticates your API key with HyperThought and connects MetaForge to your HyperThought instance.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.apiKeyButton.setText(QCoreApplication.translate("HyperthoughtDialog", u"Authenticate", None))
#if QT_CONFIG(tooltip)
        self.pasteFromClipboardBtn.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"Click to paste your API key that is on the clipboard", None))
#endif // QT_CONFIG(tooltip)
        self.pasteFromClipboardBtn.setText("")
        self.apiKeyLabel.setText(QCoreApplication.translate("HyperthoughtDialog", u"Hyperthought API Key:", None))
#if QT_CONFIG(tooltip)
        self.apiKeyLineEdit.setToolTip(QCoreApplication.translate("HyperthoughtDialog", u"Put your HyperThought API key here.  It can be found on the HyperThought website, under your account information.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

