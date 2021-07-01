# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QDateTime, QTimer, QObject, Slot, Qt, Signal

class HyperThoughtTokenVerifier(QObject):

    currentTokenExpired = Signal()

    def __init__(self,parent = None):
        super(HyperThoughtTokenVerifier, self).__init__(parent)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tokenExpired)

    @Slot()
    def tokenExpired(self):
        self.timer.stop()
        self.currentTokenExpired.emit()

    def setExpireTime(self, time):
        self.timer.start(int(time) * 1000)
