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
#--------------------------------------------------------------------------------------------------
# This next sections extracts out the version of Qt5 that is being used
#--------------------------------------------------------------------------------------------------
execute_process(
  COMMAND "${RCC_EXE}" -version
  OUTPUT_VARIABLE qt_version
  ERROR_VARIABLE rcc_error
  OUTPUT_STRIP_TRAILING_WHITESPACE 
  ERROR_STRIP_TRAILING_WHITESPACE
)
set(qt_version ${rcc_error}) # Because the output is in the error variable?
string(REPLACE " " ";" qt_version "${qt_version}") # Make a list out of the output
list(LENGTH qt_version qt_version_length) # Get the length of the list
math(EXPR qt_version_length "${qt_version_length}-1") # Subtract 1 from the length to get the last index
list(GET qt_version ${qt_version_length} qt_version) # Pull out the version number Major.minor.patch
string(REPLACE "." ";" qt_version "${qt_version}") # Turn that into a list
list(GET qt_version 0 Qt_Major) # Extract out the major Qt version
list(GET qt_version 1 Qt_Minor) # Extract out the minor Qt version
set(QT_VERSION ${Qt_Major}_${Qt_Minor}) # Set the Qt 5 version variable
message(STATUS "UI and RCC Files will be generated into '${MetaForge_SOURCE_DIR}/generated_${QT_VERSION}'")


set(UI_FILES
    mainwindow
    createtemplatewidget
    usetemplatewidget
    hyperthoughtdialog
    newfolderdialog
    aboutdialog
    metaforge_preferences)

#--------------------------------------------------------------------------------------------------
# Depending if you use Pip or Conda to install pyside2 you will get either Qt 5.12 (Conda) or 5.12 (Pip)
# The python codes that load the generated files know to check the version of Qt that is being used
# and load from a different directory. Right now you will need to manually change this variable to
# match which Qt version is installed. THIS ONLY SUPPORTS QT 5.12 AND QT 5.15
# set(QT_VERSION "5_12")
# set(QT_VERSION "5_15")

file(MAKE_DIRECTORY ${MetaForge_SOURCE_DIR}/generated_${QT_VERSION})

foreach(ui ${UI_FILES})
  add_custom_target(${ui}_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/UI_Files/${ui}.ui --from-imports  -o ${MetaForge_SOURCE_DIR}/generated_${QT_VERSION}/ui_${ui}.py)
endforeach()


# add_custom_target(MainWindow_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/mainwindow.ui -o ${MetaForge_SOURCE_DIR}/mainwindow_ui.py)
# add_custom_target(HyperThoughtDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/hyperthoughtdialog.ui -o ${MetaForge_SOURCE_DIR}/hyperthoughtdialog.py)
# add_custom_target(NewFolderDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/newfolderdialog.ui  -o ${MetaForge_SOURCE_DIR}/newfolderdialog.py)
# add_custom_target(AboutDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/aboutdialog.ui  -o ${MetaForge_SOURCE_DIR}/aboutdialog.py)


add_custom_target(Resources_RCC ALL COMMAND "${RCC_EXE}" ${MetaForge_SOURCE_DIR}/resources.qrc  -o ${MetaForge_SOURCE_DIR}/generated_${QT_VERSION}/resources_rc.py)
