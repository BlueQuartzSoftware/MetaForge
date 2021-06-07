# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QListView


class EasyFileListView(QListView):
     def __init__(self, parent=None):
         super(EasyFileListView,self).__init__()
         self.setAcceptDrops(True)
         print("YES I GET HERE TOO 1")

     def dragEnterEven(event):
         print("YES I GET HERE TOO 2")
         event.acceptProposedAction()

     def dragMoveEvent(event):
         print("YES I GET HERE TOO 3")
         self.event.setDropAction(Qt.MoveAction);
         event.accept()

     def dropEvent(event):
         print("YES I GET HERE TOO")
         event.accept()
