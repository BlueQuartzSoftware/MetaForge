from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle


class TableModelU(QAbstractTableModel):

    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """
    # Total Number of Columns
    K_COL_COUNT = 7

    # These are some misc strings that are used.
    K_CUSTOM_INPUT = "Custom Input"
    K_FROM_SOURCE = "--SOURCE--"

    # These are the keys to the Meta Data Dictionary that stores each row of data in the table.
    K_KEY_META_KEY = "Key"
    K_VALUE_META_KEY = "Value"
    K_SOURCE_META_KEY = "Source"
    K_HTNAME_META_KEY = "HT Name"
    K_HTVALUE_META_KEY = "HT Value"
    K_ANNOTATION_META_KEY = "Annotation"
    K_UNITS_META_KEY = "Units"
    K_EDITABLE_META_KEY = "Editable"
    K_USESOURCE_META_KEY = "Default"

    # These are the user facing header and the index of each column in the table.
    K_SOURCE_COL_NAME = "Source"
    K_SOURCE_COL_INDEX = 0

    K_USESOURCE_COL_NAME = "Use Source Value"
    K_USESOURCE_COL_INDEX = 1

    K_HTKEY_COL_NAME = "HT Name"
    K_HTKEY_COL_INDEX = 2

    K_HTVALUE_COL_NAME = "HT Value"
    K_HTVALUE_COL_INDEX = 3

    K_HTANNOTATION_COL_NAME = "HT Annotation"
    K_HTANNOTATION_COL_INDEX = 4

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 5

    K_REMOVE_COL_NAME = "Remove Row"
    K_REMOVE_COL_INDEX = 6


#    K_EDITABLE_COL_NAME = "Editable"
#    K_EDITABLE_COL_INDEX = 7

    def __init__(self, data, metadataList, editables, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.metadataList = metadataList
        self.treeDict = metadataList
        self.templatelist = []
        self.templatesources = []
        self.newmetadataList = []
        self.newmetadatasources = []

        self.hiddenList = []
        self.editableKeys = editables

    def addTemplateList(self, newList):
        self.metadataList = []
        self.templatelist = []
        self.templatesources = []

        for i in range(len(newList)):
            self.templatelist.append(newList[i])
            if "Custom Input" not in newList[i]["Source"]:
                self.templatesources.append("/".join(newList[i]['Source'].split("/")[1:]))

    def rowCount(self, parent=QModelIndex()):
        return len(self.metadataList)

    def columnCount(self, parent=QModelIndex()):
        return 7

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == self.K_HTKEY_COL_INDEX:
                return self.metadataList[index.row()][self.K_KEY_META_KEY]

            elif index.column() == self.K_HTVALUE_COL_INDEX:
                return str(self.metadataList[index.row()][self.K_VALUE_META_KEY])

            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return self.metadataList[index.row()][self.K_ANNOTATION_META_KEY]

            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return self.metadataList[index.row()][self.K_UNITS_META_KEY]

            elif index.column() == self.K_SOURCE_COL_INDEX:
                return self.metadataList[index.row()][self.K_SOURCE_META_KEY]
                
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_USESOURCE_COL_INDEX:
                return self.metadataList[index.row()][self.K_USESOURCE_META_KEY]

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == self.K_HTKEY_COL_INDEX:
                return self.K_HTKEY_COL_NAME
            elif section == self.K_HTVALUE_COL_INDEX:
                return self.K_HTVALUE_COL_NAME
            elif section == self.K_HTANNOTATION_COL_INDEX:
                return self.K_HTANNOTATION_COL_NAME
            elif section == self.K_HTUNITS_COL_INDEX:
                return self.K_HTUNITS_COL_NAME
            elif section == self.K_SOURCE_COL_INDEX:
                return self.K_SOURCE_COL_NAME
            elif section == self.K_REMOVE_COL_INDEX:
                return self.K_REMOVE_COL_NAME
            elif section == self.K_USESOURCE_COL_INDEX:
                return self.K_USESOURCE_COL_NAME

            return None

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            if not index.isValid():
                return False
            elif index.column() == self.K_HTKEY_COL_INDEX:
                if self.metadataList[index.row()][self.K_SOURCE_META_KEY] == self.K_CUSTOM_INPUT:
                    self.metadataList[index.row(
                    )][self.K_KEY_META_KEY] = value
                    self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if self.metadataList[index.row()][self.K_SOURCE_META_KEY] == self.K_CUSTOM_INPUT:
                    self.metadataList[index.row(
                    )][self.K_VALUE_META_KEY] = value
                    self.dataChanged.emit(index, index)
                else:
                    self.metadataList[index.row(
                    )][self.K_VALUE_META_KEY] = value
                    self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                self.metadataList[index.row(
                )][self.K_ANNOTATION_META_KEY] = value
                self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                self.metadataList[index.row()][self.K_UNITS_META_KEY] = value
                self.dataChanged.emit(index, index)

            return True
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_USESOURCE_COL_INDEX:
                pass
            #self.dataChanged.emit(index, index)
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == self.K_REMOVE_COL_INDEX:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        elif index.column() == self.K_SOURCE_COL_INDEX or index.column() == self.K_USESOURCE_COL_INDEX:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) ^ Qt.ItemIsEnabled)
        else:
            if index.data() == "" or self.metadataList[index.row()]["Editable"] == 2:
                return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
            else:
                return Qt.ItemIsEnabled

    def prepRow(self, dataDict, source, value):
        self.newmetadataList.append(
            {self.K_KEY_META_KEY: value, self.K_VALUE_META_KEY: dataDict[value], self.K_SOURCE_META_KEY: source+value})
        newsource = source+value
        self.newmetadatasources.append("/".join(newsource.split("/")[1:]))

    def addRow(self, row):
        self.beginInsertRows(self.index(len(self.metadataList), 0), len(
            self.metadataList), len(self.metadataList))

        units = ""
        annotation = ""
        for i in range(len(self.templatelist)):
            if self.templatelist[i][self.K_KEY_META_KEY] == row[self.K_KEY_META_KEY]:
                units = self.templatelist[i][self.K_UNITS_META_KEY]
                annotation = self.templatelist[i][self.K_ANNOTATION_META_KEY]
        if row[self.K_KEY_META_KEY] in self.editableKeys:
            self.metadataList.append(
                {self.K_KEY_META_KEY: row[self.K_KEY_META_KEY],
                 self.K_VALUE_META_KEY: row[self.K_VALUE_META_KEY],
                 self.K_SOURCE_META_KEY: row[self.K_SOURCE_META_KEY],
                 self.K_UNITS_META_KEY: units,
                 self.K_ANNOTATION_META_KEY: annotation,
                 self.K_EDITABLE_META_KEY: 2,
                 self.K_USESOURCE_META_KEY: 2})
        else:

            self.metadataList.append(
                {self.K_KEY_META_KEY: row[self.K_KEY_META_KEY],
                 self.K_VALUE_META_KEY: row[self.K_VALUE_META_KEY],
                 self.K_SOURCE_META_KEY: row[self.K_SOURCE_META_KEY],
                 self.K_UNITS_META_KEY: units,
                 self.K_ANNOTATION_META_KEY: annotation,
                 self.K_EDITABLE_META_KEY: 0,
                 self.K_USESOURCE_META_KEY: 2})

        self.endInsertRows()

    def addExistingRow(self, row):
        self.beginInsertRows(self.index(len(self.metadataList), 0), len(
            self.metadataList), len(self.metadataList))
        if row[self.K_USESOURCE_META_KEY] == 0:
            self.metadataList.append(
             {self.K_KEY_META_KEY: row[self.K_KEY_META_KEY],
             self.K_VALUE_META_KEY: row[self.K_HTVALUE_META_KEY],
             self.K_SOURCE_META_KEY: row[self.K_SOURCE_META_KEY],
             self.K_UNITS_META_KEY: row[self.K_UNITS_META_KEY],
             self.K_ANNOTATION_META_KEY: row[self.K_ANNOTATION_META_KEY],
             self.K_EDITABLE_META_KEY: row[self.K_EDITABLE_META_KEY],
             self.K_USESOURCE_META_KEY: row[self.K_USESOURCE_META_KEY]} )
        else:
            self.metadataList.append(
             {self.K_KEY_META_KEY: row[self.K_KEY_META_KEY],
             self.K_VALUE_META_KEY: row[self.K_VALUE_META_KEY],
             self.K_SOURCE_META_KEY: row[self.K_SOURCE_META_KEY],
             self.K_UNITS_META_KEY: row[self.K_UNITS_META_KEY],
             self.K_ANNOTATION_META_KEY: row[self.K_ANNOTATION_META_KEY],
             self.K_EDITABLE_META_KEY: row[self.K_EDITABLE_META_KEY],
             self.K_USESOURCE_META_KEY: row[self.K_USESOURCE_META_KEY]} )

        self.endInsertRows()

    def addEmptyRow(self):
        self.beginInsertRows(self.index(len(self.metadataList), 0), len(
            self.metadataList), len(self.metadataList))
        self.metadataList.append(
            {self.K_KEY_META_KEY: "",
             self.K_VALUE_META_KEY: "",
             self.K_SOURCE_META_KEY: self.K_CUSTOM_INPUT,
             self.K_UNITS_META_KEY: "",
             self.K_ANNOTATION_META_KEY: "",
             self.K_EDITABLE_META_KEY: 2,
             self.K_USESOURCE_META_KEY: 0})

        self.endInsertRows()
