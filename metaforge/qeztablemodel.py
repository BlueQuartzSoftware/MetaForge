from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QFont

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
    K_FROM_SOURCE = "--SOURCE--"
    K_CUSTOM_VALUE = "--CUSTOM VALUE--"

    # These are the user facing header and the index of each column in the table.
    K_SORT_COL_NAME = "#"
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
    K_HTANNOTATION_COL_INDEX = 6

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 5

    K_USESOURCE_COL_NAME = "Override Source Value"
    K_OVERRIDESOURCEVALUE_COL_INDEX = 7

    K_EDITABLE_COL_NAME = "Editable"
    K_EDITABLE_COL_INDEX = 8

    K_REMOVE_COL_NAME = "Remove"
    K_REMOVE_COL_INDEX = 9

    def __init__(self, metadata_model: EzMetadataModel, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.metadata_model = metadata_model


    def rowCount(self, parent=QModelIndex()):
        model_row_count = self.metadata_model.size()
        return model_row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT
    
    def data(self, index, role):
        if not index.isValid():
            return None

        metadata_entry: EzMetadataEntry = self.metadata_model.entry(index.row())

        if role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.ToolTipRole:
            if index.column() == self.K_SORT_COL_INDEX:
                return index.row() + 1
            elif index.column() == self.K_HTNAME_COL_INDEX:
                return metadata_entry.ht_name
            elif index.column() == self.K_SOURCEVAL_COL_INDEX:
                if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                    return str(self.K_CUSTOM_VALUE)
                else:
                    return str(metadata_entry.source_value)
            elif index.column() == self.K_SOURCE_COL_INDEX:
                if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                    return self.K_CUSTOM_VALUE
                else:
                    return metadata_entry.source_path
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                    return str(metadata_entry.ht_value)
                else:
                    if metadata_entry.override_source_value is True:
                        return str(metadata_entry.ht_value)
                    else:
                        return str(self.K_FROM_SOURCE)
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return metadata_entry.ht_annotation
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return metadata_entry.ht_units
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_EDITABLE_COL_INDEX:
                if metadata_entry.editable is True:
                    return Qt.Checked
                else:
                    return Qt.Unchecked
            elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
                    if metadata_entry.override_source_value is True:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
        elif role == Qt.FontRole:
            flags = self.flags(index)
            if not (flags & Qt.ItemIsEditable):
                italic_font = QFont()
                italic_font.setItalic(True)
                return italic_font


        return None
    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
        
        if self.metadata_model is None:
            return False
        
        metadata_entry: EzMetadataEntry = self.metadata_model.entry(index.row())
            
        if role == Qt.EditRole:
            if index.column() == self.K_SORT_COL_INDEX:
                # Move row to a different location!
                pass
            elif index.column() == self.K_HTNAME_COL_INDEX:
                metadata_entry.ht_name = value
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if metadata_entry.source_type == EzMetadataEntry.SourceType.CUSTOM or metadata_entry.override_source_value is True:
                    metadata_entry.ht_value = value
                    self.dataChanged.emit(index, index)
                    return True
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                metadata_entry.ht_annotation = value
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                metadata_entry.ht_units = value
                self.dataChanged.emit(index, index)
                return True
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_EDITABLE_COL_INDEX:
                if value == Qt.Checked:
                    metadata_entry.editable = True
                else:
                    metadata_entry.editable = False
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                if value == Qt.Checked:
                    metadata_entry.override_source_value = True
                else:
                    metadata_entry.override_source_value = False
                value_index = self.index(index.row(), self.K_HTVALUE_COL_INDEX)
                self.dataChanged.emit(index, index)
                self.dataChanged.emit(value_index, value_index)
                return True

        return False

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
            elif section == self.K_HTANNOTATION_COL_INDEX:
                return self.K_HTANNOTATION_COL_NAME
            elif section == self.K_HTUNITS_COL_INDEX:
                return self.K_HTUNITS_COL_NAME
            elif section == self.K_REMOVE_COL_INDEX:
                return self.K_REMOVE_COL_NAME
            return None
        if orientation == Qt.Vertical:
            return "    "
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        metadata_entry: EzMetadataEntry = self.metadata_model.entry(index.row())

        if index.column() == self.K_SORT_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.K_SOURCE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == self.K_SOURCEVAL_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == self.K_HTNAME_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.K_HTVALUE_COL_INDEX:
            if metadata_entry.source_type == EzMetadataEntry.SourceType.CUSTOM:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                if metadata_entry.override_source_value is True:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
                else:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == self.K_HTANNOTATION_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.K_HTUNITS_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
            if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
                return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
            elif metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            else:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == self.K_EDITABLE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable
        elif index.column() == self.K_REMOVE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def addRow(self, dataDict, source, value):
        pass
        # self.beginInsertRows(self.index(self.metadata_model.enabled_count(), 0), self.metadata_model.size(), self.metadata_model.size())
        # self.endInsertRows()

    def addCustomRow(self, numCustom):
        self.beginInsertRows(self.index(len(self.metadata_model.entries), 0), len(
            self.metadata_model.entries), len(self.metadata_model.entries))
        custom = EzMetadataEntry()
        custom.source_type =  EzMetadataEntry.SourceType.CUSTOM
        custom.source_path  = ""
        custom.source_value  = ""
        custom.ht_name  = "Custom HT Name"
        custom.ht_value  = "Custom HT Value"
        custom.ht_annotation  = ""
        custom.ht_units  = ""
        custom.override_source_value  = False
        custom.editable  = True
        custom.required  = True
        custom.enabled  = True

        self.metadata_model.append(custom)

        self.endInsertRows()
    
    def refresh_entry(self, source):
        metadata_entry: EzMetadataEntry = self.metadata_model.entry_by_source(source)
        if metadata_entry is not None:
            row = self.metadata_model.index_from_source(source)
            left_index = self.index(row, 0)
            right_index = self.index(row, self.columnCount() - 1)
            self.dataChanged.emit(left_index, right_index)
