from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp, QModelIndex
from PySide2.QtGui import QColor, QIcon, QFont


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
    K_OVERRIDDEN = 'Value overridden from source'
    K_MISSING = "Missing from data file"

    # Row colors
    K_MISSING_ENTRY_COLOR = QColor(255, 190, 194)
    K_OVERRIDDEN_ENTRY_COLOR = QColor(253, 255, 190)

    # These are the user facing header and the index of each column in the table.
    K_SOURCE_COL_NAME = "Source"
    K_SOURCE_COL_INDEX = 0

    K_HTNAME_COL_NAME = "HT Name"
    K_HTNAME_COL_INDEX = 1

    K_HTVALUE_COL_NAME = "HT Value"
    K_HTVALUE_COL_INDEX = 2

    K_HTANNOTATION_COL_NAME = "HT Annotation"
    K_HTANNOTATION_COL_INDEX = 4

    K_HTUNITS_COL_NAME = "HT Units"
    K_HTUNITS_COL_INDEX = 3

    K_PARSINGMESSAGES_COL_NAME = "Parsing Messages"
    K_PARSINGMESSAGES_COL_INDEX = 5

    K_REMOVE_COL_NAME = "Remove"
    K_REMOVE_COL_INDEX = 6

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

        if role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.ToolTipRole:
            if index.column() == self.K_HTNAME_COL_INDEX:
                return self._get_htname_data(metadata_entry)
            elif index.column() == self.K_SOURCE_COL_INDEX:
                return self._get_source_data(metadata_entry)
            elif index.column() == self.K_HTVALUE_COL_INDEX:
                return str(self._get_htvalue_data(metadata_entry))
            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return self._get_htannotation_data(metadata_entry)
            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return self._get_htunits_data(metadata_entry)
            elif index.column() == self.K_PARSINGMESSAGES_COL_INDEX:
                return self._get_parsingmessages_data(metadata_entry)
        elif role == Qt.BackgroundRole:
            return self._get_background_color_data(metadata_entry)
        elif role == Qt.FontRole:
            return self._get_font_data(index)
        return self._get_default_data()
    
    def _get_source_data(self, metadata_entry: EzMetadataEntry) -> str:
        if metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
            return self.sourceModel().K_CUSTOM_VALUE
        else:
            return metadata_entry.source_path
    
    def _get_htname_data(self, metadata_entry: EzMetadataEntry) -> str:
        return metadata_entry.ht_name
    
    def _get_htvalue_data(self, metadata_entry: EzMetadataEntry) -> str:
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
            if metadata_entry.override_source_value is False:
                if metadata_entry in self.missing_entries:
                    return None
                elif self.metadata_file_chosen is False:
                    return self.K_SOURCE_NOT_LOADED
        return metadata_entry.ht_value

    def _get_htannotation_data(self, metadata_entry: EzMetadataEntry) -> str:
        return metadata_entry.ht_annotation
    
    def _get_htunits_data(self, metadata_entry: EzMetadataEntry) -> str:
        return metadata_entry.ht_units
    
    def _get_parsingmessages_data(self, metadata_entry: EzMetadataEntry) -> str:
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
            if metadata_entry.override_source_value is True:
                return self.K_OVERRIDDEN
            elif metadata_entry in self.missing_entries:
                return self.K_MISSING
        return None
    
    def _get_background_color_data(self, metadata_entry: EzMetadataEntry) -> QColor:
        if metadata_entry.override_source_value is True:
            return self.K_OVERRIDDEN_ENTRY_COLOR
        elif metadata_entry in self.missing_entries:
            return self.K_MISSING_ENTRY_COLOR
        return None
    
    def _get_font_data(self, index: QModelIndex) -> QFont:
        flags = self.flags(index)
        if not (flags & Qt.ItemIsEditable):
            italic_font = QFont()
            italic_font.setItalic(True)
            return italic_font
        return None
    
    def _get_default_data(self):
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
            if section == self.K_HTNAME_COL_INDEX:
                return self.K_HTNAME_COL_NAME
            elif section == self.K_HTVALUE_COL_INDEX:
                return self.K_HTVALUE_COL_NAME
            elif section == self.K_HTANNOTATION_COL_INDEX:
                return self.K_HTANNOTATION_COL_NAME
            elif section == self.K_HTUNITS_COL_INDEX:
                return self.K_HTUNITS_COL_NAME
            elif section == self.K_PARSINGMESSAGES_COL_INDEX:
                return self.K_PARSINGMESSAGES_COL_NAME
            elif section == self.K_REMOVE_COL_INDEX:
                return self.K_REMOVE_COL_NAME
        if orientation == Qt.Vertical:
            return "     "

        return None


    def flags(self, index) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        source_row = self.mapToSource(index).row()
        metadata_entry: EzMetadataEntry = self.sourceModel().metadata_model.entry(source_row)
        
        if index.column() == self.K_SOURCE_COL_INDEX:
            return self._get_source_flags(metadata_entry)
        elif index.column() == self.K_HTNAME_COL_INDEX:
            return self._get_htname_flags(metadata_entry)
        elif index.column() == self.K_HTVALUE_COL_INDEX:
            return self._get_htvalue_flags(metadata_entry)
        elif index.column() == self.K_HTANNOTATION_COL_INDEX:
            return self._get_htannotation_flags(metadata_entry)
        elif index.column() == self.K_HTUNITS_COL_INDEX:
            return self._get_htunits_flags(metadata_entry)
        elif index.column() == self.K_PARSINGMESSAGES_COL_INDEX:
            return self._get_parsingmessages_flags(metadata_entry)
        elif index.column() == self.K_REMOVE_COL_INDEX:
            return self._get_removecolumn_flags(metadata_entry)
        else:
            return self._get_default_flags()

    def _get_source_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def _get_htname_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
            if metadata_entry not in self.missing_entries:
                if metadata_entry.editable is True:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif metadata_entry.editable is True:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def _get_htvalue_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
            if metadata_entry.override_source_value is True:
                if metadata_entry.editable is True:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            elif self.metadata_file_chosen is True:
                if metadata_entry.editable is True:
                    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            if metadata_entry.editable is True:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def _get_htannotation_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        if metadata_entry.editable is True:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def _get_htunits_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        if metadata_entry.editable is True:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def _get_parsingmessages_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def _get_removecolumn_flags(self, metadata_entry: EzMetadataEntry) -> Qt.ItemFlags:
        return self._get_default_flags() | Qt.ItemIsEditable
    
    def _get_default_flags(self):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
