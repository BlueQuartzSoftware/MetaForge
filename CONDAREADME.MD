1. You will need to install Miniconda or Anaconda, conda-build, and Git. For accurate results, Anaconda was used and all installations can be followed here: https://docs.anaconda.com/anaconda/install/
2: Uncomment  folder: my-destination/folder in the meta.yaml given below.
3: Edit the folder line as such: folder: Choose/your/destination/path. Do not create the directory, or it will error out. If directory is filled, delete it and it will repackage.
4. Please remove the conda-forge channel if you have it installed. The Pyside2 issue is linked to this channel.(Optional Step)
5. Create a new conda environment: conda create --name {name of your environment}. Eg: "conda create --name metaforge"
6. Activate the new environment. "conda activate {name of your environment}". For example: "conda activate metaforge"
7. Open up your terminal and go to where the meta.yaml file is located on your compute. For example: cd Downloads/ (if possible, a freshly made directory is best)8. Execute the following command wherever you put the meta.yaml. "conda build --numpy {version of whatever you want} ." For example: "conda build --numpy 1.7 ." (Having this tag removes that error we always see. We can also hard code this if we don't want the user to specify a version.) (It may say there was an error that the build failed. This is untrue. Check the folder you specified it to go to in the meta.yaml file and it should be there)9. Navigate to the source directory folder (The folder you made the destination to be).10. run pip install PySide2 tqdm requests dataclasses-json11. run python Metaforge.py or python3 Metaforge.py. I think it's preferred to use "python3 Metaforge.py" 

Known issues: 
    Pip Pyside2 and Conda Pyside do not sync which causes error while conda is still active and is a known issue to Conda. The workaround is to deactivate when running the project and having Pip Pyside2.
    Github saying the download was unsuccessful when it was.
