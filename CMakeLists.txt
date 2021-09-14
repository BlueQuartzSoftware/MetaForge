cmake_policy(SET CMP0002 NEW)
cmake_policy(SET CMP0054 NEW)
cmake_policy(SET CMP0079 NEW)
cmake_policy(SET CMP0077 NEW)

cmake_minimum_required(VERSION 3.14.0)

# Request C++17 standard, using new CMake variables.
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_EXTENSIONS False)

#--------------------------------------------------------------------------------------------------
# Always write out the compile_commands.json file to help out things like QtCreator and VS Code
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(MetaForge VERSION 1.0.0 LANGUAGES NONE)


find_program(RCC_EXE NAMES pyside2-rcc DOC "Pyside2 RCC Executable")
find_program(UIC_EXE NAMES pyside2-uic DOC "Pyside2 UIC Executable")

set(UI_FILES mainwindow hyperthoughtdialog newfolderdialog aboutdialog)

#--------------------------------------------------------------------------------------------------
# Depending if you use Pip or Conda to install pyside2 you will get either Qt 5.12 (Conda) or 5.12 (Pip)
# The python codes that load the generated files know to check the version of Qt that is being used
# and load from a different directory. Right now you will need to manually change this variable to
# match which Qt version is installed. THIS ONLY SUPPORTS QT 5.12 AND QT 5.15
set(QT_VERSION "5_12")
#set(QT_VERSION "5_15")

foreach(ui ${UI_FILES})
  add_custom_target(${ui}_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/${ui}.ui --from-imports  -o ${MetaForge_SOURCE_DIR}/${QT_VERSION}/ui_${ui}.py)
endforeach()


# add_custom_target(MainWindow_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/mainwindow.ui -o ${MetaForge_SOURCE_DIR}/mainwindow_ui.py)
# add_custom_target(HyperThoughtDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/hyperthoughtdialog.ui -o ${MetaForge_SOURCE_DIR}/hyperthoughtdialog.py)
# add_custom_target(NewFolderDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/newfolderdialog.ui  -o ${MetaForge_SOURCE_DIR}/newfolderdialog.py)
# add_custom_target(AboutDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/aboutdialog.ui  -o ${MetaForge_SOURCE_DIR}/aboutdialog.py)


add_custom_target(Resources_RCC ALL COMMAND "${RCC_EXE}" ${MetaForge_SOURCE_DIR}/resources.qrc  -o ${MetaForge_SOURCE_DIR}/${QT_VERSION}/resources_rc.py)
