from PySide2.QtNetwork import QNetworkReply
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QIcon, QColor
from PySide2.QtWidgets import QApplication, QStyle

from ezmodel.ezmetadataentry import EzMetadataEntry
from ezmodel.ezmetadatamodel import EzMetadataModel


class QEzTableModel(QAbstractTableModel):
    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """
    # Total Number of Columns
    K_COL_COUNT = 10

    # These are some misc strings that are used.
    K_CUSTOM_INPUT = "Custom Input"
    K_FROM_SOURCE = "--SOURCE--"

    # These are the keys to the Meta Data Dictionary that stores each row of data in the table.
    K_NAME_META_KEY = "Key"
    K_VALUE_META_KEY = "Value"
    K_HTNAME_META_KEY = "HT Name"
    K_HTVALUE_META_KEY = "HT Value"
    K_SOURCE_META_KEY = "Source"
    K_CHECKED_META_KEY = "Checked"
    K_EDITABLE_META_KEY = "Editable"
    K_DEFAULT_META_KEY = "Default"
    K_HTANNOTATION_META_KEY = "HT Annotation"
    K_HTUNITS_META_KEY = "HT Units"

    # These are the user facing header and the index of each column in the table.
    K_SORT_COL_NAME = "#^"
    K_SORT_COL_INDEX = 0

    K_SOURCE_COL_NAME = "Source"
    K_SOURCE_COL_INDEX = 1

    K_SOURCEVAL_COL_NAME = "Source Value"
    K_SOURCEVAL_COL_INDEX = 2

    K_HTNAME_COL_NAME = "HT Name"
    K_HTNAME_COL_INDEX = 3

    K_HTVALUE_COL_NAME = "HT Value"
    K_HTVALUE_COL_INDEX = 4

    K_HTANNOTATION_COL_NAME = "HT Annotation"
    K_HTANNOTATION_COL_INDEX = 5

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 6

    K_USESOURCE_COL_NAME = "Override Source Value"
    K_OVERRIDESOURCEVALUE_COL_INDEX = 7

    K_EDITABLE_COL_NAME = "Editable"
    K_EDITABLE_COL_INDEX = 8

    K_REMOVE_COL_NAME = "Remove Row"
    K_REMOVE_COL_INDEX = 9

    def __init__(self, tree_data: dict, metadata_model: EzMetadataModel, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.metadata_model = metadata_model
        visited = {}
        queue = []
        grandParents = {}
        source = ""
        self.treeDict = tree_data


    def rowCount(self, parent=QModelIndex()):
        model_row_count = self.metadata_model.size()
        return model_row_count

    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == self.K_SORT_COL_INDEX:
                return index.row()
            elif index.column() == self.K_HTNAME_COL_INDEX:
                return self.metadata_model.entry(index.row()).ht_name
            elif index.column() == self.K_SOURCEVAL_COL_INDEX:
                return self.metadata_model.entry(index.row()).source_value
            elif index.column() == self.K_SOURCE_COL_INDEX:
                return self.metadata_model.entry(index.row()).source_path
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                return self.metadata_model.entry(index.row()).ht_value
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return self.metadata_model.entry(index.row()).ht_annotation
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return self.metadata_model.entry(index.row()).ht_units
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_EDITABLE_COL_INDEX:
                return self.metadata_model.entry(index.row()).editable
            elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                return self.metadata_model.entry(index.row()).override_source_value

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
            elif section == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                return self.K_USESOURCE_COL_NAME
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
        if not index.isValid():
            return False
            
        if role == Qt.EditRole:
            # if index.column() == self.K_SORT_COL_INDEX:
            #     if int(value) > -1 and int(value) < len(<<<self.metadataList>>>):
            #         temp = <<<self.metadataList>>>[int(value)]
            #         <<<self.metadataList>>>[int(value)] = <<<self.metadataList>>>[index.row()]
            #         <<<self.metadataList>>>[index.row()] = temp
            if index.column() == self.K_HTNAME_COL_INDEX:
                self.metadata_model.entry(index.row()).ht_name = value
                self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                self.metadata_model.entry(index.row()).ht_value = value
                self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                self.metadata_model.entry(index.row()).ht_annotation = value
                self.dataChanged.emit(index, index)
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                self.metadata_model.entry(index.row()).ht_units = value
                self.dataChanged.emit(index, index)
            else:
                return False
            return True
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_EDITABLE_COL_INDEX or index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                self.changeChecked(index)
            return True

        return False

    def changeChecked(self, index):
        pass
        # if index.column() == self.K_EDITABLE_COL_INDEX:
        #     if <<<self.metadataList>>>[index.row()][self.K_EDITABLE_COL_NAME] == 0:
        #         <<<self.metadataList>>>[index.row()][self.K_EDITABLE_COL_NAME] = 2
        #     else:
        #         <<<self.metadataList>>>[index.row()][self.K_EDITABLE_COL_NAME] = 0
        #     self.dataChanged.emit(index, index)
        # elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
        #     if <<<self.metadataList>>>[index.row()][self.K_DEFAULT_META_KEY] == 0:
        #         <<<self.metadataList>>>[index.row()][self.K_HTVALUE_META_KEY] = self.K_FROM_SOURCE
        #         <<<self.metadataList>>>[index.row()][self.K_DEFAULT_META_KEY] = 2
        #     else:
        #         <<<self.metadataList>>>[index.row()][self.K_HTVALUE_META_KEY] = <<<self.metadataList>>>[index.row()][self.K_VALUE_META_KEY]
        #         <<<self.metadataList>>>[index.row()][self.K_DEFAULT_META_KEY] = 0
        #     anIndex = self.index(index.row(),self.K_HTVALUE_COL_INDEX)
        #     self.dataChanged.emit(anIndex,index)

    def flags(self, index):
        return Qt.NoItemFlags
        # if not index.isValid():
        #     return Qt.NoItemFlags
        # if index.column() == self.K_HTNAME_COL_INDEX:
        #     return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        # elif index.column() == self.K_HTVALUE_COL_INDEX:
        #     if <<<self.metadataList>>>[index.row()]["Default"] == 2:
        #         return Qt.ItemFlags(QAbstractTableModel.flags(self, index) ^ Qt.ItemIsEnabled)
        #     elif <<<self.metadataList>>>[index.row()]["Default"] == 0:
        #         return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable | Qt.ItemIsEnabled)
        # elif index.column() == self.K_REMOVE_COL_INDEX:
        #     return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        # elif index.column() == self.K_SORT_COL_INDEX:
        #     return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)
        # elif index.column() == self.K_EDIDEX or index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
        #     return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsUserCheckable)
        # else:
        #     return Qt.ItemFlags(QAbstractTableModel.flags(self, index) | Qt.ItemIsEditable)


    def addRow(self, dataDict, source, value):
        pass
        # self.beginInsertRows(self.index(self.metadata_model.enabled_count(), 0), self.metadata_model.size(), self.metadata_model.size())
        # self.endInsertRows()

    def addEmptyRow(self, numCustom):
        pass
        # self.beginInsertRows(self.index(len(<<<self.metadataList>>>), 0), len(
        #     <<<self.metadataList>>>), len(<<<self.metadataList>>>))
        # <<<self.metadataList>>>.append(
        #     {self.K_NAME_META_KEY: "",
        #      self.K_VALUE_META_KEY: "",
        #      self.K_SOURCE_META_KEY: self.K_CUSTOM_INPUT+" "+str(numCustom),
        #      self.K_HTVALUE_COL_NAME: "",
        #      self.K_HTNAME_COL_NAME: "",
        #      self.K_CHECKED_META_KEY: 2,
        #      self.K_HTUNITS_META_KEY: "",
        #      self.K_HTANNOTATION_META_KEY: "",
        #      self.K_EDITABLE_META_KEY: 2,
        #      self.K_DEFAULT_META_KEY: 0})
        # self.endInsertRows()
