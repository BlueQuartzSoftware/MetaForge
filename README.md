# MetaForge #

HyperThought Data/MetaData Uploading program

## How to install ##

### Conda with Pip installed dependencies ###

Best practice would be to create a virtual environment for python.
  ```lang-console
  conda create -n easybake python=3.8
  conda env create -f environment.yml
  ```
That will create a conda virtual environment called **MetaForge** using conda installed dependencies

### Conda with Conda installed dependencies ###

Best practice would be to create a virtual environment for python.
  ```lang-console
  conda create -n easybake python=3.8
  conda activate easybake
  conda install -r Requirements.txt
  ```

## Full Install Notes ##

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
(easybake) [user@host.com:EasyBake]% python MetaForge.py
```


## Current Bugs ##

[https://github.com/BlueQuartzSoftware/MetaForge/issues](https://github.com/BlueQuartzSoftware/MetaForge/issues)

