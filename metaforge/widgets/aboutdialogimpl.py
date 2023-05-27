from PySide6.QtWidgets import QDialog, QApplication

from metaforge.widgets.generated_6_5.ui_aboutdialog import Ui_AboutDialog




class AboutDialogImpl(QDialog):


    def __init__(self, parent=None):
        super(AboutDialogImpl, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.ApplicationNameLabel.setText(QApplication.applicationDisplayName() + " " + QApplication.applicationVersion())

        detailsText = "\n" + QApplication.organizationName() + "\n"
        detailsText += "©2021, All Rights Reserved." + "\n"

        self.ui.aboutDetailsLabel.setText( detailsText )




