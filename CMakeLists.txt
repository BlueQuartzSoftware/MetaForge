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

add_custom_target(MainWindow_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/mainwindow.ui -o ${MetaForge_SOURCE_DIR}/ui_mainwindow.py)
add_custom_target(HyperThoughtDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/hyperthoughtdialog.ui -o ${MetaForge_SOURCE_DIR}/hyperthoughtdialog.py)
add_custom_target(NewFolderDialog_UIC ALL COMMAND "${UIC_EXE}" ${MetaForge_SOURCE_DIR}/newfolderdialog.ui  -o ${MetaForge_SOURCE_DIR}/newfolderdialog.py)
