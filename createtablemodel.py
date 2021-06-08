from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle


class TableModelC(QAbstractTableModel):
    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """
    # Total Number of Columns
    K_COL_COUNT = 11

    # These are some misc strings that are used.
    K_CUSTOM_INPUT = "Custom Input"
    K_FROM_SOURCE = "--SOURCE--"

    # These are the keys to the Meta Data Dictionary that stores each row of data in the table.
    K_NAME_META_KEY = "Key"
    K_VALUE_META_KEY = "Value"
    K_SOURCE_META_KEY = "Source"
    K_CHECKED_META_KEY = "Checked"
    K_REQUIRED_META_KEY = "Required"
    K_EDITABLE_META_KEY = "Editable"

    # These are the user facing header and the index of each column in the table.
    K_SORT_COL_NAME = "#^"
    K_SORT_COL_INDEX = 0

    K_SOURCE_COL_NAME = "Source"
    K_SOURCE_COL_INDEX = 1

    K_HTNAME_COL_NAME = "HT Name"
    K_HTNAME_COL_INDEX = 2

    K_SOURCEVAL_COL_NAME = "Source Value"
    K_SOURCEVAL_COL_INDEX = 3

    K_HTVALUE_COL_NAME = "HT Value"
    K_HTVALUE_COL_INDEX = 4

    K_HTANNOTATION_COL_NAME = "HT Annotation"
    K_HTANNOTATION_COL_INDEX = 5

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 6

    K_USESOURCE_COL_NAME = "Use Source Value"
    K_USESOURCE_COL_INDEX = 7

    K_REQUIRE_COL_NAME = "Required"
    K_REQUIRE_COL_INDEX = 8

    K_EDITABLE_COL_NAME = "Editable"
    K_EDITABLE_COL_INDEX = 9

    K_REMOVE_COL_NAME = "Remove Row"
    K_REMOVE_COL_INDEX = 10

    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.metadataList = []
        visited = {}
        queue = []
        grandParents = {}
        source = ""
        self.hiddenList = []
        self.treeDict = data
        self.requiredList = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.metadataList)

    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == self.K_SORT_COL_INDEX:
                return index.row()
            elif index.column() == self.K_HTNAME_COL_INDEX:
                return self.metadataList[index.row()][self.K_NAME_META_KEY]
            elif index.column() == self.K_SOURCEVAL_COL_INDEX:
                if self.metadataList[index.row()][self.K_VALUE_META_KEY] == "None":
                    return ""
                return str(self.metadataList[index.row()][self.K_VALUE_META_KEY])
            elif index.column() == self.K_SOURCE_COL_INDEX:
                return self.metadataList[index.row()][self.K_SOURCE_COL_NAME]
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                return self.metadataList[index.row()][self.K_HTVALUE_COL_NAME]
            # elif index.column() == self.K_HTVALUE_COL_INDEX:
            #    return self.metadataList[index.row()][0]
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_REQUIRE_COL_INDEX:
                return self.metadataList[index.row()][self.K_REQUIRE_COL_NAME]
            elif index.column() == self.K_EDITABLE_COL_INDEX:
                return self.metadataList[index.row()][self.K_EDITABLE_COL_NAME]
            elif index.column() == self.K_USESOURCE_COL_INDEX:
                return 0

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == self.K_SORT_COL_INDEX:
                return self.K_SORT_COL_NAME
            elif section == self.K_HTNAME_COL_INDEX:
                return self.K_HTNAME_COL_NAME
            elif section == self.K_SOURCEVAL_COL_INDEX:
                return self.K_SOURCEVAL_COL_NAME
            elif section == self.K_SOURCE_COL_INDEX:
                return self.K_SOURCE_COL_NAME
            elif section == self.K_HTVALUE_COL_INDEX:
                return self.K_HTVALUE_COL_NAME
            elif section == self.K_USESOURCE_COL_INDEX:
                return self.K_USESOURCE_COL_NAME
            elif section == self.K_REQUIRE_COL_INDEX:
                return self.K_REQUIRE_COL_NAME
            elif section == self.K_EDITABLE_COL_INDEX:
                return self.K_EDITABLE_COL_NAME
            elif section == self.K_REMOVE_COL_INDEX:
                return self.K_REMOVE_COL_NAME
            elif section == self.K_HTANNOTATION_COL_INDEX:
                return self.K_HTANNOTATION_COL_NAME
            elif section == self.K_HTUNITS_COL_INDEX:
                return self.K_HTUNITS_COL_NAME
            return None

    def setData(self, index, value, role):
        print(f'setData: {index}, {value}')
        if role == Qt.EditRole:
            if not index.isValid():
                return False
            if index.column() == self.K_SORT_COL_INDEX:
                if int(value) > -1 and int(value) < len(self.metadataList):
                    temp = self.metadataList[int(value)]
                    self.metadataList[int(
                        value)] = self.metadataList[index.row()]
                    self.metadataList[index.row()] = temp
            if index.column() == self.K_HTNAME_COL_INDEX:
                if self.metadataList[index.row()][self.K_SOURCE_COL_NAME] == self.K_CUSTOM_INPUT:
                    self.metadataList[index.row(
                    )][self.K_NAME_META_KEY] = value
                    self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if value == "":
                    self.metadataList[index.row(
                    )][self.K_HTVALUE_COL_NAME] = self.K_FROM_SOURCE
                else:
                    self.dataChanged.emit(index, index)
                    treeDict = self.treeDict
                    sourcePath = self.metadataList[index.row()][self.K_SOURCE_COL_NAME].split(
                        "/")
                    for i in range(len(sourcePath)-1):
                        treeDict = treeDict[sourcePath[i]]
                    treeDict[sourcePath[-1]] = value
                    self.metadataList[index.row(
                    )][self.K_HTVALUE_COL_NAME] = value
                    self.dataChanged.emit(index, index)
            #elif index.column() == self.K_REMOVE_COL_INDEX:
#                self.metadataList.remove(index.row())

            return True
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_REQUIRE_COL_INDEX or index.column() == self.K_EDITABLE_COL_INDEX or index.column() == K_USESOURCE_COL_INDEX:
                self.changeChecked(index)
                self.dataChanged.emit(index, index)
            return True

        return False

    def changeChecked(self, index):
        if index.column() == self.K_REQUIRE_COL_INDEX:
            if self.metadataList[index.row()][self.K_REQUIRE_COL_NAME] == 0:
                self.metadataList[index.row()][self.K_REQUIRE_COL_NAME] = 2
                self.requiredList.append(
                    self.metadataList[index.row()][self.K_NAME_META_KEY])
            else:
                self.metadataList[index.row()][self.K_REQUIRE_COL_NAME] = 0
                self.requiredList.remove(
                    self.metadataList[index.row()][self.K_NAME_META_KEY])
            print(self.requiredList)
        elif index.column() == self.K_EDITABLE_COL_INDEX:
            if self.metadataList[index.row()][self.K_EDITABLE_COL_NAME] == 0:
                self.metadataList[index.row()][self.K_EDITABLE_COL_NAME] = 2
            else:
                self.metadataList[index.row()][self.K_EDITABLE_COL_NAME] = 0

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        if index.column() == self.K_HTVALUE_COL_INDEX:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        elif index.column() == self.K_REMOVE_COL_INDEX:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        elif index.column() == self.K_SORT_COL_INDEX:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        elif index.column() == self.K_REQUIRE_COL_INDEX or index.column() == self.K_EDITABLE_COL_INDEX or index.column() == self.K_USESOURCE_COL_INDEX:
            return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsUserCheckable)
        else:
            if index.data() == "":
                return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
            return Qt.ItemIsEnabled

    def addRow(self, dataDict, source, value):
        self.beginInsertRows(self.index(len(self.metadataList), 0), len(
            self.metadataList), len(self.metadataList))
        self.metadataList.append(
            {self.K_NAME_META_KEY: value,
             self.K_VALUE_META_KEY: dataDict[value],
             self.K_SOURCE_META_KEY: source+value,
             self.K_HTVALUE_COL_NAME: self.K_FROM_SOURCE,
             self.K_CHECKED_META_KEY: 0,
             self.K_REQUIRED_META_KEY: 0,
             self.K_EDITABLE_META_KEY: 0})
        self.endInsertRows()

    def addEmptyRow(self):
        self.beginInsertRows(self.index(len(self.metadataList), 0), len(
            self.metadataList), len(self.metadataList))
        self.metadataList.append(
            {self.K_NAME_META_KEY: "",
             self.K_VALUE_META_KEY: "",
             self.K_SOURCE_META_KEY: self.K_CUSTOM_INPUT,
             self.K_HTVALUE_COL_NAME: "",
             self.K_CHECKED_META_KEY: 0,
             self.K_REQUIRED_META_KEY: 0,
             self.K_EDITABLE_META_KEY: 0})
        self.endInsertRows()
