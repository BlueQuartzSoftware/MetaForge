from PySide2.QtCore import QSortFilterProxyModel, QModelIndex

from metaforge.qt_models.qparsercomboboxmodel import QParserComboBoxModel

class QProxyParserComboBoxModel(QSortFilterProxyModel):
  def __init__(self, parent=None):
    super().__init__(parent)
  
  def filterAcceptsRow(self, sourceRow: int, sourceParent: QModelIndex) -> bool:
    qparser_cb_model = self.sourceModel()
    model_index = qparser_cb_model.index(sourceRow, 0, sourceParent)
    return False if qparser_cb_model.data(model_index, QParserComboBoxModel.Parser) is None or qparser_cb_model.data(model_index, QParserComboBoxModel.Enabled) is False else True