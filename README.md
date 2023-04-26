# edtools_interface
This is a tk gui window based on edtools. edtools is a package to process three-dimentional electron diffraction data. You can find out how to install and use edtools at https://github.com/instamatic-dev/edtools. edtools uses XDS packages to process diffraction data. So XDS should be installed (https://wiki.uni-konstanz.de/xds/index.php/Installation). This edtools_gui.py is developed by talking with ChatGPT.

# Requirements
This interface is based on python. You can run it with Python software. Newer versions than 3.7 are recommended. 

# How to get prepared for the edtools_gui.py
1. Install windows subsystem for linux (wsl), install XDS package, install Python.
2. Put XPREP, shelxt, xcif in a folder, and put the path to this folder into PATH in environment variables.
3. Put edtools_gui.py, evaluation.py, comment.py, update_mosaicity.py, solution.py, plot_scale.py, table.py, table.docx, LMPeng1999_SHELX.txt files into a folder. 
4. Open “install_edtools_gui.py” script.
5. Click “install packages”, the code will detect the default environment of python, and install edtools package, pyperclip, prettytable, pyautogui, docx modules automatically in that environment.
6. Select the folder that containing edtools_gui.py, evaluation.py, comment.py, update_mosaicity.py, solution.py, plot_scale.py, table.py, table.docx, LMPeng1999_SHELX.txt files, the code will update the paths to these files.
7. Click “update redp path”, select the redp.exe file in your computer, the code will update the path to redp software in corresponding .py files. Do the same thing to update paths to pwt, shelxle, vesta, and mercury softwares.

![image](https://user-images.githubusercontent.com/131879369/234630991-04587ad2-9cfc-400f-8d22-4426452dab1f.png)

NOTE: All the softwares should be licenced before use.

# How to use edtools_gui.py

You can find more details in "Manual of edtools_gui.pptx".


