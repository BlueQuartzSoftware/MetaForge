from PySide2.QtWidgets import QDialog, QApplication
import PySide2.QtCore

qt_version = PySide2.QtCore.__version_info__
if qt_version[1] == 12:
    from metaforge.generated_5_12.ui_aboutdialog import Ui_AboutDialog
elif qt_version[1] == 15:
    from metaforge.generated_5_15.ui_aboutdialog import Ui_AboutDialog




class AboutDialogImpl(QDialog):


    def __init__(self, parent=None):
        super(AboutDialogImpl, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.ApplicationNameLabel.setText(QApplication.applicationDisplayName() + " " + QApplication.applicationVersion())

        detailsText = "\n" + QApplication.organizationName() + "\n"
        detailsText += "©2021, All Rights Reserved." + "\n"

        self.ui.aboutDetailsLabel.setText( detailsText )




