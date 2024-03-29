# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'metaforge_preferences.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QDialog,
    QDialogButtonBox, QGridLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableView, QWidget)
from . import resources_rc

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
        self.removeBtn = QPushButton(MetaForgePreferences)
        self.removeBtn.setObjectName(u"removeBtn")
        self.removeBtn.setMinimumSize(QSize(24, 24))
        self.removeBtn.setMaximumSize(QSize(24, 24))
        icon = QIcon()
        icon.addFile(u":/resources/Images/close-pushed@2x.png", QSize(), QIcon.Normal, QIcon.Off)
        self.removeBtn.setIcon(icon)
        self.removeBtn.setIconSize(QSize(24, 24))
        self.removeBtn.setFlat(True)

        self.gridLayout_2.addWidget(self.removeBtn, 4, 3, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 5, 3, 1, 1)

        self.searchLineEdit = QLineEdit(MetaForgePreferences)
        self.searchLineEdit.setObjectName(u"searchLineEdit")

        self.gridLayout_2.addWidget(self.searchLineEdit, 1, 1, 1, 1)

        self.addBtn = QPushButton(MetaForgePreferences)
        self.addBtn.setObjectName(u"addBtn")
        self.addBtn.setMinimumSize(QSize(24, 24))
        self.addBtn.setMaximumSize(QSize(24, 24))
        icon1 = QIcon()
        icon1.addFile(u":/resources/Images/plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.addBtn.setIcon(icon1)
        self.addBtn.setIconSize(QSize(24, 24))
        self.addBtn.setFlat(True)

        self.gridLayout_2.addWidget(self.addBtn, 2, 3, 2, 1)

        self.parser_directories_label = QLabel(MetaForgePreferences)
        self.parser_directories_label.setObjectName(u"parser_directories_label")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.parser_directories_label.setFont(font)

        self.gridLayout_2.addWidget(self.parser_directories_label, 0, 0, 1, 4)

        self.parser_directories_table = QTableView(MetaForgePreferences)
        self.parser_directories_table.setObjectName(u"parser_directories_table")
        self.parser_directories_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.parser_directories_table.verticalHeader().setVisible(False)

        self.gridLayout_2.addWidget(self.parser_directories_table, 2, 0, 4, 3)

        self.label = QLabel(MetaForgePreferences)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(MetaForgePreferences)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


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
        self.searchLineEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.searchLineEdit.setPlaceholderText(QCoreApplication.translate("MetaForgePreferences", u"Search for parsers by name here", None))
#if QT_CONFIG(tooltip)
        self.addBtn.setToolTip(QCoreApplication.translate("MetaForgePreferences", u"Use this button to move an array up in the \"Selected Data Arrays\" column", None))
#endif // QT_CONFIG(tooltip)
        self.addBtn.setText("")
        self.parser_directories_label.setText(QCoreApplication.translate("MetaForgePreferences", u"Parsers", None))
        self.label.setText(QCoreApplication.translate("MetaForgePreferences", u"Search", None))
    # retranslateUi

