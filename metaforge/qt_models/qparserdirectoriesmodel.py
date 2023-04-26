from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex, QFileSystemWatcher, Signal
from PySide2.QtGui import QColor, QIcon, QPixmap

from pathlib import Path

from metaforge.common.constants import K_PARSER_YAML_FILE_NAME
from metaforge.ez_models.ezparserdirectoriesmodel import EzParserDirectoriesModel, EzParserDirectory

class QParserDirectoriesModel(QAbstractTableModel):
    """
    Define all of the column indices and column names in addition to any other strings
    in this section. This will make it easier to move columns around and rename items.
    """

    # Row colors
    K_RED_BG_COLOR = QColor(255, 190, 194)
    K_YELLOW_BG_COLOR = QColor(253, 255, 190)

    # These are the user facing header and the index of each column in the table.
    K_ENABLED_COL_NAME = "Enabled"
    K_ENABLED_COL_INDEX = 0

    K_PARSER_DIR_COL_NAME = "Parser Directory"
    K_PARSER_DIR_COL_INDEX = 1

    K_PARSERS_LOADED_COL_NAME = "Parsers Loaded"
    K_PARSERS_LOADED_COL_INDEX = 2

    K_CONFIGURE_COL_NAME = "Configure"
    K_CONFIGURE_COL_INDEX = 3

    # Total Number of Columns
    K_COL_COUNT = K_CONFIGURE_COL_INDEX + 1

    parser_directory_config_changed = Signal(Path)

    def __init__(self, parser_directories_model: EzParserDirectoriesModel, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.parser_directories_model = parser_directories_model

    def rowCount(self, parent=QModelIndex()):
        model_row_count = self.parser_directories_model.size()
        return model_row_count
    
    def columnCount(self, parent=QModelIndex()):
        return self.K_COL_COUNT
    
    def data(self, index, role):
        if not index.isValid():
            return None

        parser_directory: EzParserDirectory = self.parser_directories_model.directory(index.row())
        if parser_directory is None:
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole or role == Qt.ToolTipRole:
            if index.column() == self.K_PARSER_DIR_COL_INDEX:
                return str(parser_directory.directory_path)
            elif index.column() == self.K_PARSERS_LOADED_COL_INDEX:
                return '\n'.join([parser_path.stem for parser_path in parser_directory.parser_paths])
        
        if role == Qt.DecorationRole and parser_directory.default and index.column() == self.K_PARSER_DIR_COL_INDEX:
            return QIcon(QPixmap(':/resources/Images/star@2x.png'))

        if role == Qt.CheckStateRole and index.column() == self.K_ENABLED_COL_INDEX:
            return Qt.Checked if parser_directory.enabled == True else Qt.Unchecked

        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return None

        parser_directory: EzParserDirectory = self.parser_directories_model.directory(index.row())
        if parser_directory is None:
            return None

        if role == Qt.CheckStateRole and index.column() == self.K_ENABLED_COL_INDEX:
            parser_directory.enabled = (value == Qt.Checked)
            self.dataChanged.emit(index, index, [role])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        
        if orientation == Qt.Horizontal:
            if section == self.K_ENABLED_COL_INDEX:
                return self.K_ENABLED_COL_NAME
            elif section == self.K_PARSER_DIR_COL_INDEX:
                return self.K_PARSER_DIR_COL_NAME
            elif section == self.K_PARSERS_LOADED_COL_INDEX:
                return self.K_PARSERS_LOADED_COL_NAME
            elif section == self.K_CONFIGURE_COL_INDEX:
                return self.K_CONFIGURE_COL_NAME
        
        return None
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        if index.column() == self.K_ENABLED_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        elif index.column() == self.K_CONFIGURE_COL_INDEX:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def addRow(self, directory_path: Path):
        self.beginInsertRows(self.index(len(self.parser_directories_model.parser_directories), 0), len(
            self.parser_directories_model.parser_directories), len(self.parser_directories_model.parser_directories))
        self.parser_directories_model.append(directory_path)
        self.endInsertRows()
    
    def removeRow(self, row):
        self.beginRemoveRows(QModelIndex(), row, row)
        self.parser_directories_model.remove_by_index(row)
        self.endRemoveRows()

