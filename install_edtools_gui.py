import tkinter as tk
from tkinter import filedialog
import os
import re
import sys
import subprocess

def install_packages():
    # Get the path of the Python interpreter
    python_path = sys.executable

    # List of packages to install
    packages = ['edtools', 'pyperclip', 'prettytable', 'pyautogui', 'docx']

    # Install each package using pip
    for package in packages:
        try:
            subprocess.check_call([python_path, '-m', 'pip', 'install', package])
            print(f'{package} installed successfully')
        except subprocess.CalledProcessError:
            print(f'Failed to install {package}')

def select_folder_edtools_gui():
    # Prompt the user to select a folder
    

    # Get the EDTools_GUI script and its old path
    script = get_script(folder_path, "edtools_gui")
    old_path = get_old_path_edtools_gui(script)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths(folder_path, old_path, "edtools_gui.py")
 
def select_folder_table():
    # Prompt the user to select a folder
    #folder_path = filedialog.askdirectory()

    # Get the Table script and its old path
    script = get_script(folder_path, "table")
    old_path = get_old_path_table(script)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths(folder_path, old_path, "table.py")
        
def select_folder_solution():
    # Prompt the user to select a folder
    #folder_path = filedialog.askdirectory()

    # Get the Table script and its old path
    script = get_script(folder_path, "solution")
    old_path = get_old_path_solution(script)
    print("Old path:", old_path)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths(folder_path, old_path, "solution.py")
        
def replace_redp_path_in_edtools_gui():
    # Prompt the user to select a folder with edtools_gui.py
    folder_path = select_folder()
    
    # Prompt the user to select a redp.exe file
    file_path = filedialog.askopenfilename()   

    # Get the Table script and its old path
    script = get_script(folder_path, "edtools_gui")
    old_path = get_old_path_redp(script)
    print("Old path:", old_path)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths_for_software(folder_path, old_path, "edtools_gui.py", file_path)
        
def replace_pwt_path_in_solution():
    # Prompt the user to select a folder with solution.py
    folder_path = select_folder()
    print(folder_path)
    
    # Prompt the user to select a redp.exe file
    file_path = filedialog.askopenfilename() 
    print(file_path)

    # Get the Table script and its old path
    script = get_script(folder_path, "solution")
    old_path = get_old_path_pwt(script)
    print("Old path:", old_path)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths_for_software(folder_path, old_path, "solution.py", file_path)
        
def replace_shelxle_path_in_solution():
    # Prompt the user to select a folder with solution.py
    folder_path = select_folder()
    print(folder_path)
    
    # Prompt the user to select a redp.exe file
    file_path = filedialog.askopenfilename() 
    print(file_path)

    # Get the Table script and its old path
    script = get_script(folder_path, "solution")
    old_path = get_old_path_shelxle(script)
    print("Old path:", old_path)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths_for_software(folder_path, old_path, "solution.py", file_path)
        
def replace_vesta_path_in_solution():
    # Prompt the user to select a folder with solution.py
    folder_path = select_folder()
    print(folder_path)
    
    # Prompt the user to select a redp.exe file
    file_path = filedialog.askopenfilename() 
    print(file_path)

    # Get the Table script and its old path
    script = get_script(folder_path, "solution")
    old_path = get_old_path_vesta(script)
    print("Old path:", old_path)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths_for_software(folder_path, old_path, "solution.py", file_path)
        
def replace_mercury_path_in_solution():
    # Prompt the user to select a folder with solution.py
    folder_path = select_folder()
    print(folder_path)
    
    # Prompt the user to select a redp.exe file
    file_path = filedialog.askopenfilename() 
    print(file_path)

    # Get the Table script and its old path
    script = get_script(folder_path, "solution")
    old_path = get_old_path_mercury(script)
    print("Old path:", old_path)

    if folder_path:
        # Replace all paths in the files with the new path
        replace_paths_for_software(folder_path, old_path, "solution.py", file_path)
        
def get_script(folder_path, script_name):
    # Get the path to the script
    script_path = os.path.join(folder_path, script_name + ".py")
    # Read the script and return its contents
    with open(script_path, 'r') as f:
        script = f.read()
    return script

def replace_paths(folder_path, old_path, file_name):
    # Recursively walk through the folder and replace paths in all .py files
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename == file_name:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    script = f.read()
                if old_path:
                    # Replace the old path with the new path
                    new_path = folder_path.replace('\\', '/')
                    new_script = script.replace(old_path, new_path)
                    try:
                        with open(filepath, 'w') as f:
                            f.write(new_script)
                        # Print the new path for each file where paths were replaced
                        print("New path:", new_path)
                    except:
                        print("Error: Could not replace path in file {}".format(filepath))
                else:
                    print("Error: Could not find old path in file {}".format(filepath))
                    
def replace_paths_for_software(folder_path, old_path, file_name, file_path):
    # Recursively walk through the folder and replace paths in all .py files
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename == file_name:
                filepath = os.path.join(dirpath, filename)
                with open(filepath, 'r') as f:
                    script = f.read()
                if old_path:
                    # Replace the old path with the new path
                    new_path = file_path.replace('\\', '/')
                    new_script = script.replace(old_path, new_path)
                    try:
                        with open(filepath, 'w') as f:
                            f.write(new_script)
                        # Print the new path for each file where paths were replaced
                        print("New path:", new_path)
                    except:
                        print("Error: Could not replace path in file {}".format(filepath))
                else:
                    print("Error: Could not find old path in file {}".format(filepath))

def get_old_path_edtools_gui(script):
    # Find the old path in the EDTools_GUI script
    pattern = r'"python\s*(.+?)"'
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1)
        old_path = os.path.dirname(old_path)
        print("Old path:", old_path)
        return old_path
    else:
        return ""

def get_old_path_table(script):
    # Find the old path in the Table script
    pattern = r"self\.print_table\('(.+?)',"
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1)
        old_path = os.path.dirname(old_path)
        print("Old path:", old_path)
        return old_path
    else:
        return ""
        
def get_old_path_solution(script):
    # Find the old path in the solution script
    pattern = r'folder_path = "(.+?)"'
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1)
        print("Old path:", old_path)
        return old_path
    else:
        return ""
        
def select_all():
    folder_path = select_folder()
    select_folder_edtools_gui()
    select_folder_table()
    select_folder_solution()

folder_path = ""

def select_folder():
    global folder_path
    if not folder_path:
        folder_path = filedialog.askdirectory()
    return folder_path

def get_old_path_redp(script):
    # Find the old path in the solution script
    pattern = r"command = '(.+?)'"
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1)
        print("Old path:", old_path)
        return old_path
    else:
        return ""
      
def get_old_path_pwt(script):
    # Find the old path in the solution script
    pattern = r"'(.+?)pwt.exe'"
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1) + 'pwt.exe'
        print("Old path:", old_path)
        return old_path
    else:
        return ""
        
def get_old_path_shelxle(script):
    # Find the old path in the solution script
    pattern = r"'(.+?)shelxle64.exe'"
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1) + 'shelxle64.exe'
        print("Old path:", old_path)
        return old_path
    else:
        return ""
        
def get_old_path_vesta(script):
    # Find the old path in the solution script
    pattern = r"'(.+?)VESTA.exe'"
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1) + 'VESTA.exe'
        print("Old path:", old_path)
        return old_path
    else:
        return ""
        
def get_old_path_mercury(script):
    # Find the old path in the solution script
    pattern = r"'(.+?)mercury.exe'"
    match = re.search(pattern, script)
    if match:
        old_path = match.group(1) + 'mercury.exe'
        print("Old path:", old_path)
        return old_path
    else:
        return ""
        
root = tk.Tk()
root.title("Installation")

button_install_packages = tk.Button(text="install packages", command=install_packages, font=("Helvetica", 16))

# Create labels to show the selected folder paths
button_all = tk.Button(text="update all paths to .py files", command=select_all, font=("Helvetica", 16))
button_replace_redp = tk.Button(text="update redp path", command=replace_redp_path_in_edtools_gui, font=("Helvetica", 16))
button_replace_pwt = tk.Button(text="update pwt path", command=replace_pwt_path_in_solution, font=("Helvetica", 16))
button_replace_shelxle = tk.Button(text="update shelxle path", command=replace_shelxle_path_in_solution, font=("Helvetica", 16))
button_replace_vesta = tk.Button(text="update vesta path", command=replace_vesta_path_in_solution, font=("Helvetica", 16))
button_replace_mercury = tk.Button(text="update mercury path", command=replace_mercury_path_in_solution, font=("Helvetica", 16))

# Show the buttons
button_install_packages.pack()
button_all.pack()
button_replace_redp.pack()
button_replace_pwt.pack()
button_replace_shelxle.pack()
button_replace_vesta.pack()
button_replace_mercury.pack()

# Start the main event loop
root.mainloop()
