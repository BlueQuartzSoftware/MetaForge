# Python 2
#VER=2.7

# Python 3
VER=3.6

RCC =  $(HOME)/.local/bin/pyside2-rcc

UIC =  $(HOME)/.local/bin/pyside2-uic


ui_mainwindow.py: mainwindow.ui hyperthoughtdialog.py
	$(UIC) mainwindow.ui -o  ui_mainwindow.py
	
 
hyperthoughtdialog.py:  hyperthoughtdialog.ui
	$(UIC) hyperthoughtdialog.ui -o  hyperthoughtdialog.py


clean:
	$(RM) ui_mainwindow.py
	$(RM) hyperthoughtdialog.py
	$(RM) -rf __pycache__
