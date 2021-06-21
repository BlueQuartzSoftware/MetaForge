from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp

from ezmodel.ezmetadataentry import EzMetadataEntry

class QCreateEzTableModel(QSortFilterProxyModel):
    def __init__(self,data ,parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.displayed=[]
        self.fileType=[]
        self.setDynamicSortFilter(True)
        self.sort(0)


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
        
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if self.sourceModel() is None:
            return Qt.NoItemFlags

        src_index = self.mapToSource(index)
        metadata_entry: EzMetadataEntry = self.sourceModel().metadata_model.entry(src_index.row())

        if index.column() == self.sourceModel().K_SORT_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.sourceModel().K_SOURCE_COL_INDEX:
            return Qt.NoItemFlags
        elif index.column() == self.sourceModel().K_SOURCEVAL_COL_INDEX:
            return Qt.NoItemFlags
        elif index.column() == self.sourceModel().K_HTNAME_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.sourceModel().K_HTVALUE_COL_INDEX:
            if metadata_entry.override_source_value is True:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
                return Qt.NoItemFlags
        elif index.column() == self.sourceModel().K_HTANNOTATION_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.sourceModel().K_HTUNITS_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        elif index.column() == self.sourceModel().K_OVERRIDESOURCEVALUE_COL_INDEX:
            if metadata_entry.source_type is EzMetadataEntry.SourceType.FILE:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable
            elif metadata_entry.source_type is EzMetadataEntry.SourceType.CUSTOM:
                return Qt.NoItemFlags
            else:
                return Qt.NoItemFlags
        elif index.column() == self.sourceModel().K_EDITABLE_COL_INDEX:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable
        elif index.column() == self.sourceModel().K_REMOVE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.NoItemFlags

    def checkList(self, checked, source):
        metadata_entry: EzMetadataEntry = self.sourceModel().metadata_model.entry_by_source(source)
        if metadata_entry is not None:
            metadata_entry.enabled = checked > 0
            row = self.sourceModel().metadata_model.index_from_source(source)
            left_index = self.sourceModel().index(row, 0)
            right_index = self.sourceModel().index(row, self.columnCount() - 1)
            self.sourceModel().dataChanged.emit(left_index, right_index)

