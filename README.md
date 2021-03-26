# EasyBake
HyperThought Data/MetaData Uploading program

How to install

1. git clone into the directory.
2. Open up terminal and pip install PySide2

How to run
1. Cd into the easybake directory in the terminal.
2. Run make to convert the current ui file into py. (If uic does not exist, run where pyside2-uic in the terminal and change the location inside of the makefile).
3. The code can either be ran using python3 main.py or from Qt Creator after opening the project inside the directory.

Features
File - Only close works.
Help - Only displays help.

Help
Create Template
  Treeview - properly shows the heiarchy of the nested dictionary and is able to check and uncheck.

  Tableview - properly shows the order and can navigate through the nested dictionary to show all of the values. Shows source path in the nested dictionary, index in the list, and the type. Can change value. Can move positions of listitems*. Can check and uncheck Require and Editable.

  Data File Selector - Can press select to open a .ctf, .ang. or .xml file. CTF and ANG files are properly recognized and parsed into the tree and table views. 

  Data Upload Selector - only displays the place holder. Select and upload do not work.
  
Use Template - not implemented



Current Bugs
insert in the table copies over the current index when inserting forward. Example: Changing index from 0 to 1.
Tableview cannot delete items in list.
Treeview not connected to Tableview.
While tableviews can be edited, the changes will only save on value.


Next Release
Connecting tableviews
Allowing columns to be deleted and reinserted.
Opening packages.
Highlighting current mode.
Authenticating Hyperthought.
