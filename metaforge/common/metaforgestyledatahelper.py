import os
import sys
import platform

from typing import List

from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QFontDatabase
from PySide2.QtCore import QObject, QFileSystemWatcher, Qt, Signal, Slot

class MetaForgeStyleDataHelper(QObject):
  
  def __init__(self, application: QApplication):
    
    self.app = application
    self.watcher = QFileSystemWatcher()

    self.css_file_path = ""
    if platform.system() == 'Darwin':
        # IF YOU DO NOT WANT A STYLE SHEET THEN COMMENT OUT the lines that set the css_file_path
        # there are 2 choices for StyleSheets. Pick one
        # self.css_file_path = "resources/StyleSheets/light.css"
        # self.css_file_path = "resources/StyleSheets/dark.css"
        self.initFonts()
        self.initStyleSheet()


    if self.css_file_path != '':
      self.watcher.addPath(self.css_file_path)
      self.watcher.fileChanged.connect(self.fileChanged)

  def initFonts(self):
    fontList = ["resources/fonts/FiraSans-Regular.ttf", 
                "resources/fonts/Lato-Regular.ttf",
                "resources/fonts/Lato-Black.ttf", 
                "resources/fonts/Lato-BlackItalic.ttf",
                "resources/fonts/Lato-Bold.ttf", 
                "resources/fonts/Lato-BoldItalic.ttf", 
                "resources/fonts/Lato-Hairline.ttf", 
                "resources/fonts/Lato-HairlineItalic.ttf",
                "resources/fonts/Lato-Italic.ttf", 
                "resources/fonts/Lato-Light.ttf", 
                "resources/fonts/Lato-LightItalic.ttf"]
    for f in fontList:
        fontID = QFontDatabase.addApplicationFont(f)

  def initStyleSheet(self):
    if self.css_file_path == '':
      return

    with open(self.css_file_path) as css_file:
      print(f'  Reloading style sheet from {self.css_file_path}')
      cssContent = css_file.read()
      css_file.close()
      self.app.setStyleSheet(cssContent)

  @Slot(None)
  def fileChanged(self):
     # print('css file changed.....')
      self.initStyleSheet()
