# This Python file uses the following encoding: utf-8


from PySide2.QtCore import QAbstractItemModel, QFile, QIODevice, QItemSelectionModel, QModelIndex, QObject ,Qt, Signal, Slot
from PySide2.QtWidgets import QApplication, QMainWindow
from metaforge.treeitem import TreeItem
from metaforge.treemodel import TreeModel

class TreeModelR(TreeModel):
    checkChanged = Signal(int, str)
    def __init__(self, headers, data, tablemodel, newList, filterModel,parent=None):
        super(TreeModel, self).__init__(parent)

        rootData = [header for header in headers]
        self.rootItem = TreeItem(rootData)
        self.treeDict = data
        self.tablemodel = tablemodel
        self.newList = newList
        self.filterModel = filterModel
        self.setupModelData(data, self.rootItem)

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
                 for i in range(len(self.newList)):
                     if child == self.newList[i]["Key"]:
                         self.tablemodel.beginInsertRows(self.tablemodel.index(len(self.tablemodel.metadataList), 0), i, i)
                         self.tablemodel.metadataList.append(self.newList[i])
                         self.tablemodel.endInsertRows()
                         parent.child(parent.childCount() -1).checked = self.newList[i]["Checked"]
                         self.filterModel.checkList(self.newList[i]["Checked"],self.newList[i]["Source"])



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
                                pass




