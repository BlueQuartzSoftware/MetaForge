from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp, QModelIndex


from ezmodel.ezmetadataentry import EzMetadataEntry

class QUseEzTableModel(QSortFilterProxyModel):
    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """
    # Total Number of Columns
    K_COL_COUNT = 7

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

    K_REMOVE_COL_NAME = "Remove Row"
    K_REMOVE_COL_INDEX = 6

    def __init__(self, data, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.displayed = []
        self.fileType = []
        self.setDynamicSortFilter(True)
        self.sort(0)

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
        metadata_model = self.sourceModel().metadata_model
        source_row = self.mapToSource(index).row()
        if role == Qt.DisplayRole:
            if index.column() == self.K_SOURCE_COL_INDEX:
                self.mapToSource
                return self.sourceModel().metadata_model.entry(source_row).source_path

            elif index.column() == self.K_HTNAME_COL_INDEX:
                return self.sourceModel().metadata_model.entry(source_row).ht_name

            elif index.column() == self.K_HTVALUE_COL_INDEX:
                return self.sourceModel().metadata_model.entry(source_row).ht_value

            elif index.column() == self.K_HTANNOTATION_COL_INDEX:
                return self.sourceModel().metadata_model.entry(source_row).ht_annotation

            elif index.column() == self.K_HTUNITS_COL_INDEX:
                return self.sourceModel().metadata_model.entry(source_row).ht_units

        elif role == Qt.CheckStateRole:
            if index.column() == self.K_OVERRIDESOURCEVALUE_COL_INDEX:
                return self.sourceModel().metadata_model.entry(source_row).override_source_value
                
            if index.column() == self.K_REMOVE_COL_INDEX:
                #return self.sourceModel().metadata_model.entry(source_row).override_source_value
                return "Remove This Row"
        return None


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

            elif section == self.K_REMOVE_COL_INDEX:
                return self.K_REMOVE_COL_NAME

            return None


    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        source_row = self.mapToSource(index).row()
        metadata_entry = self.sourceModel().metadata_model.entry(source_row)
        
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
            if metadata_entry.editable is True:
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
            else:
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
        elif index.column() == self.K_REMOVE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.NoItemFlags

