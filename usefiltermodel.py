from PySide2.QtCore import QSortFilterProxyModel, Qt, QRegExp

class FilterModelU(QSortFilterProxyModel):
    def __init__(self,data ,parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.displayed=[]
        self.fileList=[]

    def filterAcceptsRow(self,source_row, source_parent):
        curSource = self.sourceModel().metadataList[source_row]['Source']
        if curSource != "Custom Input":
            splitSource= "/".join(curSource.split("/")[1:])
            return splitSource in self.sourceModel().templatesources
        else:
            return self.sourceModel().metadataList[source_row]['Source'] == "Custom Input"

