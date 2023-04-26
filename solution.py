import os
import shutil
import tkinter as tk
from tkinter import Label
from tkinter import filedialog
import subprocess

def find_hkl_files(folder):
    hkl_files = [f for f in os.listdir(folder) if f.endswith('.hkl')]
    if len(hkl_files) == 0:
        print("No .hkl files found.")
    return hkl_files
    
def find_p4p_files(folder):
    p4p_files = [f for f in os.listdir(folder) if f.endswith('.p4p')]
    if len(p4p_files) == 0:
        print("No .p4p files found.")
    return p4p_files
    

def create_solution_folder(folder, solution_folder=None):
    if not solution_folder:
        solution_folder = os.path.join(os.getcwd(), 'solution')
    if not os.path.exists(solution_folder):
        os.mkdir(solution_folder)

def copy_hkl_files(folder, solution_folder):
    create_solution_folder(folder, solution_folder)
    hkl_files = [f for f in os.listdir(folder) if f.endswith('.hkl')]
    for file in hkl_files:
        shutil.copy(os.path.join(folder, file), os.path.join('.', 'solution', file))
        print(f"File '{file}' copied to folder 'solution'.")

def get_unit_cell_constants(folder):
    lp_file = os.path.join(folder, 'XDSCONV.LP')
    if not os.path.exists(lp_file):
        print(f"File '{lp_file}' not found.")
        return None
    with open(lp_file, 'r') as f:
        for line in f:
            if 'UNIT_CELL_CONSTANTS=' in line:
                constants_str = line.split('UNIT_CELL_CONSTANTS=')[1]
                constants = constants_str.strip().split()
                return constants
        print(f"Could not find 'UNIT_CELL_CONSTANTS=' in '{lp_file}'.")
        return None
        
def create_p4p_file(filename, constants):
    folder_name = 'solution'
    file_name = f"{os.path.splitext(filename)[0]}.p4p"
    file_path = os.path.join(folder_name, file_name)
    with open(file_path, 'w') as f:
        f.write(f"CELL {' '.join(constants)}")
    print(f"File '{file_name}' created in folder '{folder_name}'.")
    
def read_sfac_strings_from_res_file(file_name):
    if file_name is None:
        return None
        print("no .res file found to read")
    current_folder = os.getcwd()        
    os.chdir(current_folder)
    sfac_strings = []
    elements = []
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name == f"{file_name}.res":
                try:
                    with open(os.path.join(root, name), 'r') as file:
                        for line in file:
                            if "SFAC" in line:
                                sfac_index = line.index("SFAC")
                                sfac_string = line[sfac_index + 4:].strip() # +4 to skip over "SFAC"
                                sfac_strings.append(sfac_string)
                except FileNotFoundError:
                    print("File not found:", os.path.join(root, name))
                    return None
                    
    for sfac_string in sfac_strings:
        elements = sfac_string.split()
    if not sfac_strings:
        print("No SFAC strings found in", file_name + ".res")
    return elements

def search_text_file_for_strings(folder_path, file_name, sfac_strings):
    file_path = os.path.join(folder_path, file_name)
    matching_lines = [''] * len(sfac_strings)

    try:
        with open(file_path, 'r') as file:
            for line in file:
                for index, sfac_string in enumerate(sfac_strings):
                    if matching_lines[index] == '':
                        if f"SFAC {sfac_string} " in line:
                            matching_lines[index] = line.rstrip()
                            
                if all(matching_lines):
                    break
                            
    except FileNotFoundError:
        print("File not found:", file_path)

    return matching_lines


def replace_sfac_line(res_filename, new_lines):
    if res_filename is None:
        print("no .res file found to replace")
        return None
        
    current_folder = os.getcwd()        
    os.chdir(current_folder) 
    
    for root, dirs, files in os.walk('.'):
        for name in files:
            if name == f"{res_filename}.res":
                file_path = os.path.join(root, name)
                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()

                    with open(file_path, 'w') as file:
                        for line in lines:
                            if "SFAC" in line:
                                for new_line in new_lines:
                                    file.write(new_line + '\n')
                            else:
                                file.write(line)

                    return True
                
                except FileNotFoundError:
                    print("File not found:", file_path)

    print("there is no .res file found")
    return None

def change_cell_line(res_file):
    if res_file is None:
        print("No .res file found to replace.")
        return None

    current_folder = os.getcwd()
    os.chdir(current_folder)

    for root, dirs, files in os.walk('.'):
        for name in files:
            if name == f"{res_file}.res":
                file_path = os.path.join(root, name)
                try:
                    with open(file_path, 'r') as file:
                        lines = file.readlines()

                    with open(file_path, 'w') as file:
                        for line in lines:
                            if "CELL" in line:
                                words = line.split()
                                for i, word in enumerate(words):
                                    if word == "CELL":
                                        # Check if the next word is a float number
                                        if i < len(words) - 1 and isfloat(words[i+1]):
                                            # Replace the float number with 0.0251
                                            words[i+1] = "0.0251"
                                            line = " ".join(words) + "\n"
                                            break
                                file.write(line)
                            else:
                                file.write(line)

                    return True

                except FileNotFoundError:
                    print("File not found:", file_path)

    print("No .res file found.")
    return None   

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False    

class XPREPGUI:

    def __init__(self, master):
        self.master = master
        master.title("Solution GUI")
        
        # XPREP button
        self.xprep_button = tk.Button(master, text="XPREP", command=self.run_xprep, font=("Helvetica", 16))
        self.xprep_button.pack()
        
        self.space_label = Label(master, height=1)
        self.space_label.pack() 
        
        # Label and Entry for input file name for shelxt
        self.file_name_label = tk.Label(master, text="Input .ins file name:", font=("Helvetica", 16))
        self.file_name_label.pack()
        self.file_name_entry = tk.Entry(master, font=("Helvetica", 16), width=16)
        self.file_name_entry.insert(0, 1)
        self.file_name_entry.pack()
        
        # Label and Entry for input shelxt command name
        self.command_name_label = tk.Label(master, text="Input command name:", font=("Helvetica", 16))
        self.command_name_label.pack()
        self.command_name_entry = tk.Entry(master, font=("Helvetica", 16), width=16)
        self.command_name_entry.insert(0, "-a0.7 -q0.4")
        self.command_name_entry.pack()
        

    
        # Shelxt button
        self.shelxt_button = tk.Button(master, text="shelxt", command=self.run_shelxt, font=("Helvetica", 16))
        self.shelxt_button.pack()
 
        self.space_label = Label(master, height=1)
        self.space_label.pack()  
        
        # Label and Entry for update wl sfac
        self.res_file_name_label = tk.Label(master, text="Input .res file name:", font=("Helvetica", 16))
        self.res_file_name_label.pack()
        self.res_file_name_entry = tk.Entry(master, font=("Helvetica", 16), width=16)
        self.res_file_name_entry.insert(0, '1_a')
        self.res_file_name_entry.pack()

        self.update_button = tk.Button(master, text="update wave length and SFAC", command=self.run_update_wl_SFAC, font=("Helvetica", 16))
        self.update_button.pack()       

        self.update_button = tk.Button(master, text="update .res file after pwt", command=self.run_copy_res_file, font=("Helvetica", 16))
        self.update_button.pack()  

        self.run_button = tk.Button(master, text='mercury', command=self.run_mercury, font=("Helvetica", 16))
        self.run_button.pack()  
        
        self.run_button = tk.Button(master, text='vesta', command=self.run_vesta, font=("Helvetica", 16))
        self.run_button.pack()  
        
        self.run_button = tk.Button(master, text='shelxle', command=self.run_shelxle, font=("Helvetica", 16))
        self.run_button.pack()  
     
        self.run_button = tk.Button(master, text='pwt', command=self.run_pwt, font=("Helvetica", 16))
        self.run_button.pack()  
        
        self.run_button = tk.Button(master, text='check cif', command=self.run_check_cif, font=("Helvetica", 16))
        self.run_button.pack()     

        self.run_button = tk.Button(master, text='xcif', command=self.run_xcif, font=("Helvetica", 16))
        self.run_button.pack()           
        

    def run_xprep(self):
        folder = os.getcwd()
        folder_name = 'solution'
        p4p_files = find_p4p_files(folder)
        current_dir = os.path.basename(os.getcwd())
        if current_dir == 'solution':
            parent_folder = os.path.abspath(os.path.join(folder, os.pardir))
            print(parent_folder)
            os.chdir(parent_folder)
            hkl_files = find_hkl_files(parent_folder)
            if len(hkl_files) == 0:
                print("No .hkl files found.")
                return
            solution_folder = os.path.join(parent_folder, folder_name)
            create_solution_folder(solution_folder)
            copy_hkl_files(parent_folder, solution_folder)
            for file in hkl_files:
                os.chdir(parent_folder)
                unit_cell_constants = get_unit_cell_constants(os.path.join(parent_folder))
                if unit_cell_constants is not None:
                    print(f"Unit cell constants for file {file}: {unit_cell_constants}")
                    create_p4p_file(file, unit_cell_constants)
                    os.chdir(solution_folder)
                    command = f"XPREP {file}"
                    os.system(command)
                    print(f"XPREP run completed for file '{file}'")                
        else:
            hkl_files = find_hkl_files(folder)
            if len(hkl_files) == 0:
                print("No .hkl files found.")
                return
            solution_folder = os.path.join(folder, folder_name)
            create_solution_folder(solution_folder)
            copy_hkl_files(folder, solution_folder)
            for file in hkl_files:
                unit_cell_constants = get_unit_cell_constants(os.path.join(folder))
                if unit_cell_constants is not None:
                    print(f"Unit cell constants for file {file}: {unit_cell_constants}")
                    create_p4p_file(file, unit_cell_constants)
                    os.chdir(solution_folder)
                    command = f"XPREP {file}"
                    os.system(command)
                    print(f"XPREP {file}")
        os.chdir(folder)
    
   

                    
    def check_and_move_files(self, file_name):
        # Check if the files are already in a solution folder
        for root, dirs, files in os.walk(os.getcwd()):
            if file_name + '.ins' in files and file_name + '.hkl' in files and file_name + '.pcf' in files:
                if root.endswith('solution'):
                    print(f"Files for '{file_name}' already in solution folder.")
                    return
                else:
                    shutil.move(os.path.join(root, file_name + '.ins'), os.path.join(os.getcwd(), 'solution', file_name + '.ins'))
                    shutil.move(os.path.join(root, file_name + '.hkl'), os.path.join(os.getcwd(), 'solution', file_name + '.hkl'))
                    shutil.move(os.path.join(root, file_name + '.pcf'), os.path.join(os.getcwd(), 'solution', file_name + '.pcf'))
                    print(f"Files for '{file_name}' moved to solution folder.")
                    return
        
        # If the files are not in a solution folder, check if a solution folder exists and move them there
        solution_folder = os.path.join(os.getcwd(), 'solution')
        input_file_path = os.path.join(solution_folder, f"{file_name}.ins")
        hkl_file_path = os.path.join(solution_folder, f"{file_name}.hkl")
        pcf_file_path = os.path.join(solution_folder, f"{file_name}.pcf")
        if os.path.exists(input_file_path) and os.path.exists(hkl_file_path) and os.path.exists(pcf_file_path):
            print(f"Files for '{file_name}' already in solution folder.")
            return
        
        if os.path.exists(solution_folder):
            input_file_path = None
            hkl_file_path = None
            pcf_file_path = None
            for root, dirs, files in os.walk(solution_folder):
                if f"{file_name}.ins" in files:
                    input_file_path = os.path.join(root, f"{file_name}.ins")
                if f"{file_name}.hkl" in files:
                    hkl_file_path = os.path.join(root, f"{file_name}.hkl")
                if f"{file_name}.pcf" in files:
                    pcf_file_path = os.path.join(root, f"{file_name}.pcf")
            
            if input_file_path and os.path.exists(input_file_path):
                shutil.move(input_file_path, os.path.join(solution_folder, f"{file_name}.ins"))
            if hkl_file_path and os.path.exists(hkl_file_path):
                shutil.move(hkl_file_path, os.path.join(solution_folder, f"{file_name}.hkl"))
            if pcf_file_path and os.path.exists(pcf_file_path):
                shutil.move(pcf_file_path, os.path.join(solution_folder, f"{file_name}.pcf"))
            
            if input_file_path or hkl_file_path or pcf_file_path:
                print(f"Files for '{file_name}' moved to solution folder.")
            else:
                print(f"Input, HKL, or PCF file for '{file_name}' not found.")
        
        # If a solution folder doesn't exist, print an error message
        else:
            print("Solution folder not found. Please create a 'solution' folder and place your input, HKL, and PCF files in it.")
    
    
    
    

    def run_shelxt(self):
        file_name = self.file_name_entry.get()
        command_name = self.command_name_entry.get()
        self.check_and_move_files(file_name)
    
        # Find the folder containing the .inp file
        input_file_path = None
        for root, dirs, files in os.walk(os.getcwd()):
            if f"{file_name}.ins" in files:
                input_file_path = os.path.join(root, f"{file_name}.ins")
                break
    
        if not input_file_path:
            print(f"Input file '{file_name}.ins' not found.")
            return
    
        folder_path = os.path.dirname(input_file_path)
        os.chdir(folder_path)
    
        # Run the command in the folder containing the .inp file
        command = f"shelxt {file_name} {command_name}"
        os.system(command)
    
        # Check for output file in the same folder
        output_file_path = os.path.join(folder_path, f"{file_name}.hkl")
        if os.path.exists(output_file_path):
            print(f"HKL output file '{output_file_path}' created.")
        else:
            print("HKL output file was not created.")
            
       
            
    def run_update_wl_SFAC(self):
        # Get input parameters from tk gui
        res_filename = self.res_file_name_entry.get()
        print(res_filename)
        filename = "LMPeng1999_SHELX.txt"
        folder_path = "C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools"
    
        # Find SFAC strings in .res file
        sfac_strings = read_sfac_strings_from_res_file(res_filename)
        print("sfac_strings are", sfac_strings)        
        if sfac_strings is None:
            print("No  .res file found")
            return
        # Check if there are multiple instances of SFAC lines in the .res file
        if len(sfac_strings) > 14:
            print("Multiple SFAC lines found in file:", res_filename)
            return   
    
        # Search for matching lines in LMPeng1999_SHELX.txt file
        matching_lines = search_text_file_for_strings(folder_path, filename, sfac_strings)
        print("matching_lines are", matching_lines)
        if len(matching_lines) == 0:
            print("No matching lines found in file:", filename)
            return
    
        # Replace SFAC line in .res file with matching lines
        if replace_sfac_line(res_filename, matching_lines):
            print("SFAC line replaced in file:", res_filename)
        else:
            print("Error replacing SFAC line in file:", res_filename)
        
        change_cell_line(res_filename)
    
    def run_copy_res_file(self):
        # get the file name from the entry widget
        file_name = self.res_file_name_entry.get()
    
        # construct the source file name by adding "_pl" to the end
        source_file_name = file_name + "_pl.res"
    
        # construct the destination file name
        dest_file_name = file_name + ".res"
    
        # use the shutil module to copy the contents of the source file to the destination file
        shutil.copyfile(source_file_name, dest_file_name)
        
        # open the destination file in read mode
        with open(dest_file_name, 'r') as f:
            # read all the lines into a list
            lines = f.readlines()
    
        # find the line with the "SFAC" string and make all the letters capital
        for i, line in enumerate(lines):
            if "SFAC" in line:
                lines[i] = line.upper()
    
        # write the updated lines back to the destination file
        with open(dest_file_name, 'w') as f:
            f.writelines(lines)
        
        self.run_update_wl_SFAC()
        
    def run_mercury(self):
        command = 'F:/program/CSD_2022/Mercury/mercury.exe'
        subprocess.Popen(command)
           
    def run_vesta(self):
        command = 'E:/Program Files/Vesta/VESTA-win64/VESTA.exe'
        subprocess.Popen(command)
        
    def run_shelxle(self):
        command = 'E:/Program Files/shelxle64/shelxle64.exe'
        subprocess.Popen(command)
        
    def run_pwt(self):
        #command = 'E:/Program Files/pwt/pwt.exe'
        #subprocess.Popen(command)
        os.startfile('E:/Program Files/pwt/pwt.exe')
        
    def run_check_cif(self):
        url = 'http://checkcif.iucr.org/'
        
        # Open a user command window
        subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        # Open the website in the default browser
        os.system(f'start {url}')

    def run_xcif(self):
        file_name = self.res_file_name_entry.get()
        command_name = self.command_name_entry.get()
    
        # Find the folder containing the .cif file
        cif_file_path = None
        for root, dirs, files in os.walk(os.getcwd()):
            if f"{file_name}.cif" in files:
                cif_file_path = os.path.join(root, f"{file_name}.cif")
                break
    
        if not cif_file_path:
            print(f"cif file '{file_name}.cif' not found.")
            return
    
        folder_path = os.path.dirname(cif_file_path)
        os.chdir(folder_path)
    
        # Run the command in the folder containing the .inp file
        command = f"xcif {file_name}"
        os.system(command)
    
        # Check for output file in the same folder
        output_file_path = os.path.join(folder_path, f"{file_name}.cif")
        if os.path.exists(output_file_path):
            print(f"table output file '{output_file_path}' created.")
        else:
            print("table output file was not created.")
    
root = tk.Tk()
root.geometry("320x640")
my_gui = XPREPGUI(root)
root.mainloop()