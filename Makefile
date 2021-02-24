# Python 2
#VER=2.7

# Python 3
VER=3.6

RCC =  $(HOME)/.local/bin/pyside2-rcc

UIC =  $(HOME)/.local/bin/pyside2-uic


ui_mainwindow.py: mainwindow.ui
	$(UIC) mainwindow.ui -o  ui_mainwindow.py
 
clean:
	$(RM) ui_mainwindow.py
	$(RM) -rf __pycache__
