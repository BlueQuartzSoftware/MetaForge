from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp, QModelIndex
from PySide2.QtGui import QColor, QIcon


from ezmodel.ezmetadataentry import EzMetadataEntry
from typing import List

class QUseEzTableModel(QSortFilterProxyModel):
    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """
    # Total Number of Columns
    K_COL_COUNT = 7

    # These are some misc strings that are used.
    K_SOURCE_NOT_LOADED = "--SOURCE NOT LOADED--"

    # These are the user facing header and the index of each column in the table.
    K_SOURCE_COL_NAME = "Source"
    K_SOURCE_COL_INDEX = 0

    K_USESOURCE_COL_NAME = "Override Source Value"
    K_OVERRIDESOURCEVALUE_COL_INDEX = 1

    K_HTNAME_COL_NAME = "HT Name"
    K_HTNAME_COL_INDEX = 2

    K_HTVALUE_COL_NAME = "HT Value"
    K_HTVALUE_COL_INDEX = 3

    K_HTANNOTATION_COL_NAME = "HT Annotation"
    K_HTANNOTATION_COL_INDEX = 4

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 5

    K_ICON_COL_NAME = "Parsing Messages"
    K_ICON_COL_INDEX = 6

    def __init__(self, data, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.setDynamicSortFilter(True)
        self.sort(0)
        self.metadata_file_chosen = False
        self.missing_entries: List[EzMetadataEntry] = []

    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT

    def filterAcceptsRow(self, source_row, source_parent):
        if self.sourceModel() is None:
            return False

        metadata_model = self.sourceModel().metadata_model
        metadata_entry: EzMetadataEntry = metadata_model.entry(source_row)

        regex = self.filterRegExp()
        match = regex.exactMatch(metadata_entry.ht_name)

        # Custom data use case
        if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM and match:
            return True

        # All other use cases
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE and match:
            return metadata_entry.enabled
        else:
            return False


    def data(self, index, role):
        if not index.isValid():
            return None

        src_model = self.sourceModel()
        if src_model is None:
            return None
        
        src_index = self.mapToSource(index)
        metadata_entry: EzMetadataEntry = src_model.metadata_model.entry(src_index.row())

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.column() == self.K_HTNAME_COL_INDEX:
                return metadata_entry.ht_name
            elif index.column() == self.K_SOURCE_COL_INDEX:
                if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                    return src_model.K_CUSTOM_VALUE
                else:
                    return metadata_entry.source_path
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if metadata_entry.override_source_value is True:
                    return metadata_entry.ht_value
                elif metadata_entry.source_type is not EzMetadataEntry.SourceType.FILE:
                    return metadata_entry.ht_value
                elif self.metadata_file_chosen is True:
                    return metadata_entry.ht_value
                else:
                    return self.K_SOURCE_NOT_LOADED
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return metadata_entry.ht_annotation
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return metadata_entry.ht_units
            elif index.column() == self.K_ICON_COL_INDEX:
                if metadata_entry in self.missing_entries:
                    return "Missing from data file"
                else:
                    return ""    
        elif role == Qt.CheckStateRole:
            if index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
                    if metadata_entry.override_source_value is True:
                        return Qt.Checked
                    else:
                        return Qt.Unchecked
        elif role == Qt.BackgroundRole:
            if metadata_entry in self.missing_entries:
                return QColor(255, 190, 194)
        return None

    
    def setData(self, index, value, role):
        if not index.isValid():
            return False
    
        src_model = self.sourceModel()
        if src_model is None:
            return None

        src_index = self.mapToSource(index)
        metadata_entry: EzMetadataEntry = src_model.metadata_model.entry(src_index.row())
            
        if role == Qt.EditRole:

            if index.column() == self.K_HTNAME_COL_INDEX:
                metadata_entry.ht_name = value
                self.dataChanged.emit(index, index)
                return True
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                if metadata_entry.override_source_value is True:
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

        return False


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return
        if orientation == Qt.Horizontal:
            if section == self.K_SOURCE_COL_INDEX:
                return self.K_SOURCE_COL_NAME

            elif section == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                return self.K_USESOURCE_COL_NAME

            if section == self.K_HTNAME_COL_INDEX:
                return self.K_HTNAME_COL_NAME

            elif section == self.K_HTVALUE_COL_INDEX:
                return self.K_HTVALUE_COL_NAME

            elif section == self.K_HTANNOTATION_COL_INDEX:
                return self.K_HTANNOTATION_COL_NAME

            elif section == self.K_HTUNITS_COL_INDEX:
                return self.K_HTUNITS_COL_NAME
            
            elif section == self.K_ICON_COL_INDEX:
                return self.K_ICON_COL_NAME

        if orientation == Qt.Vertical:
            return "     "

        return None


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        source_row = self.mapToSource(index).row()
        metadata_entry: EzMetadataEntry = self.sourceModel().metadata_model.entry(source_row)
        
        if index.column() == self.K_SOURCE_COL_INDEX:
            return Qt.NoItemFlags
        elif index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
            return Qt.NoItemFlags
        elif index.column() == self.K_HTNAME_COL_INDEX:
            if metadata_entry.editable is True:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.NoItemFlags
        elif index.column() == self.K_HTVALUE_COL_INDEX:
            if metadata_entry.source_type is not EzMetadataEntry.SourceType.FILE:
                if metadata_entry.editable is True:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                if metadata_entry.override_source_value is True:
                    if metadata_entry.editable is True:
                        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
                elif self.metadata_file_chosen is True:
                    if metadata_entry.editable is True:
                        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            return Qt.NoItemFlags
        elif index.column() == self.K_HTANNOTATION_COL_INDEX:
            if metadata_entry.editable is True:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.NoItemFlags
        elif index.column() == self.K_HTUNITS_COL_INDEX:
            if metadata_entry.editable is True:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.NoItemFlags
        else:
            return Qt.NoItemFlags

