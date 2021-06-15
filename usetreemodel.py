# This Python file uses the following encoding: utf-8


from PySide2.QtCore import QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, QObject ,Qt, Signal, Slot
from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
from treeitem import TreeItem
from treemodel import TreeModel


class TreeModelU(TreeModel):
    checkChanged = Signal(int, str)
    def __init__(self, headers, data, tablemodel, required,parent=None):
        super(TreeModel, self).__init__(parent)

        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.treeDict= data
        self.tablemodel = tablemodel
        self.required = required
        self.setupModelData(data, self.rootItem)
        self.checkList()


    def checkList(self):
        for i in range(len(self.tablemodel.templatesources)):
            if "Custom Input" not in self.tablemodel.templatesources[i]:
                if self.tablemodel.templatesources[i] not in self.tablemodel.newmetadatasources:
                    QMessageBox.warning(None, QApplication.applicationDisplayName(), "Bad stuff happens. " + "The file extracted is missing Source: \n\n"+ self.tablemodel.templatesources[i] + "\n\nPlease try a different file")
                    self.tablemodel.metadataList = []
                    self.tablemodel.metadatasources = []
                    self.tablemodel.newmetadataList = []
                    self.tablemodel.newmetadatasources = []
                    return
        for i in range(len(self.tablemodel.newmetadataList)):
            if (self.tablemodel.newmetadataList[i]["Key"] in self.required and self.tablemodel.newmetadataList[i]["Value"] == None) or (self.tablemodel.newmetadataList[i]["Key"] in self.required and self.tablemodel.newmetadataList[i]["Value"] == ""):
                QMessageBox.warning(None, QApplication.applicationDisplayName(), "Bad stuff happens. " + "The file extracted is missing a value for this Key name: \n\n"+ self.tablemodel.newmetadataList[i]["Key"] + "\n\nPlease try a different file")
                self.tablemodel.metadataList = []
                self.tablemodel.metadatasources = []
                self.tablemodel.newmetadataList = []
                self.tablemodel.newmetadatasources = []
                return

        for i in range(len(self.tablemodel.newmetadataList)):
            self.tablemodel.addRow(self.tablemodel.newmetadataList[i])

        self.tablemodel.newmetadataList = []
        self.tablemodel.newmetadatasources = []

    def setupModelData(self, data, parent):
             visited={}
             queue=[]
             grandParents = {}

             for key in data.keys():
                 visited[(parent.itemData[0])]=[key]
                 queue.append((key,parent,""))
                 grandParents[key] = (data[key],parent)
             curDict = data
             tempSource= ""
             while queue:
                 poppedItem = queue.pop(0)
                 child = poppedItem[0]
                 parentOfChild = poppedItem[1]
                 childSource = poppedItem[2]
                 parent = parentOfChild
                 parent.insertChildren(parent.childCount(),1,self.rootItem.columnCount())
                 parent.child(parent.childCount() -1).setData(0,child)

                 if child in grandParents:

                     curDict =  grandParents[child][0]
                     tempSource = childSource+child+"/"
                     for curChild in range(grandParents[child][1].childCount()):
                         if child == grandParents[child][1].child(curChild).itemData[0]:
                            parent = grandParents[child][1].child(curChild)
                            visited[(parent.itemData[0])]=[]

                 if isinstance(curDict, dict):
                     for key in curDict.keys():
                         if key not in visited[(parent.itemData[0])]:
                             visited[(parent.itemData[0])].append(key)
                             queue.append((key,parent,tempSource))
                             if (isinstance(curDict[key],dict)):
                                grandParents[key]= (curDict[key],parent)
                             else:
                                self.tablemodel.prepRow(curDict,tempSource,key)


