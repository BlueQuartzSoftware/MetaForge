# MetaForge #

HyperThought Data/MetaData Uploading program

## How to Install ##
### Users ###
*NOTE*: This assumes that you have Anaconda running on your system, and you are running either MacOS or 64-bit Windows.
1. Create and activate a new python 3.8 Anaconda environment:
```lang-console
  conda create -n metaforge python=3.8
  conda activate metaforge
```
2. Install the metaforge package from the BlueQuartz Software Anaconda channel: 
```lang-console
  conda install -c bluequartzsoftware metaforge
```
3. Launch the application:
```lang-console
  metaforge
```

### Developers ###
*NOTE*: This assumes that you have Anaconda and Git running on your system.
1. Clone down the MetaForge project from GitHub:
```lang-console
  git clone https://www.github.com/bluequartzsoftware/MetaForge
```
2. Create and activate a new Anaconda environment using the environment yaml file:
```lang-console
  cd MetaForge
  conda env create -f environment.yml
  conda activate metaforge
```
3. Install the metaforge package as an editable package:
```lang-console
  pip install -e .
```
4. Launch the application:
```lang-console
  python metaforge/__main__.py
```

*NOTE*: If you are using Visual Studio Code as your IDE, you can paste this into your `launch.json` file to be able to easily debug MetaForge:
```
  {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: MetaForge",
            "type": "python",
            "request": "launch",
            "program": "metaforge/__main__.py",
            "console": "integratedTerminal"
        }
    ]
  }
```


## Current Bugs ##

[https://github.com/BlueQuartzSoftware/MetaForge/issues](https://github.com/BlueQuartzSoftware/MetaForge/issues)

