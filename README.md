# MetaForge #

HyperThought Data/MetaData Uploading program

## How to install ##

Best practice would be to create a virtual environment for python.
  ```lang-console
  conda create -n easybake python=3.8 tqdm requests
  pip install pyside2
  pip install dataclasses-json
  ```
  or

  ```lang-console
  python3 -m venv easybake tqdm requests
  source easybake/bin/activate
  pip install pyside2
  pip install dataclasses-json
  ```


1. git clone into the directory.

  ```lang-console
  git clone https://www.github.com/bluequartzsoftware/EasyBake
  ```

2. Open up terminal and execute (if you already have not installed the dependencies from above)

```lang-console
pip install PySide2 tqdm requests
```

## How to Run ##

From a command prompt within the EasyBake directory (shown using an Anaconda prompt on a Unix Terminal)

```lang-console
(easybake) [user@host.com:EasyBake]% python main.py
```


## Features ##

+ File - Only close works.
+ Help - Only displays help.

## Help ##

Create Template
  Treeview - properly shows the heiarchy of the nested dictionary and is able to check and uncheck. Switching the check now affects the tableview.

  Tableview - properly shows the order and can navigate through the nested dictionary to show all of the values. Shows source path in the nested dictionary, index in the list, and the type. Can change value. Can move positions of listitems*. Can check and uncheck Require and Editable. Clicking on the trashcan gets rid of the row and unchecks it in the table view.

  Data File Selector - Can press select to open a .ctf, .ang. or .xml file. CTF and ANG files are properly recognized and parsed into the tree and table views. 

  Data Upload Selector - only displays the place holder. Select and upload do not work.
  
Use Template - not implemented, commented out



Current Bugs
insert in the table copies over the current index when inserting forward. Example: Changing index from 0 to 1.



Next Release

Opening packages.
Implementing Use Method
Authenticating Hyperthought.
