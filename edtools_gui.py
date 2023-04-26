import tkinter as tk
import os
import re
import sys
from tkinter import *
from tkinter import filedialog
import subprocess
import pyperclip
import pyautogui
import time
import platform
from tkinter import ttk

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.geometry("476x1006")
        self.master.resizable(False, False)
        
        button_frame = Frame(self)
        button_frame.grid(row=0, column=0, columnspan=2, padx=0)
       
        self.root_dir_button = Button(button_frame, text='select + open', command=self.select_and_open_root_dir, font=("Helvetica", 16))
        self.root_dir_button.grid(row=1, column=0, padx=0, pady=1,  sticky='w')     
        self.root_dir_button = Button(button_frame, text='select', command=self.select_root_dir, font=("Helvetica", 16))
        self.root_dir_button.grid(row=1, column=0, padx=155, pady=1, sticky='w') 
        self.root_dir_button = Button(button_frame, text='open folder', command=self.open_root_dir, font=("Helvetica", 16))
        self.root_dir_button.grid(row=1, column=0, padx=240, pady=1, sticky='w') 
        
        self.root_dir_entry = Entry(button_frame, font=("Helvetica", 12), width=53)
        self.root_dir_entry.grid(row=2, column=0, columnspan=2, padx=0, pady=1, sticky='w') 
        
        self.space_label3 = Label(button_frame, height=1)
        self.space_label3.grid(row=3, column=0, pady=0, sticky='w')    
        
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=3, column=0, sticky='ew', pady=0)
        
        self.run_button = Button(button_frame, text='Autoindex', command=self.run_edtools_in, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=4, column=0,  padx=0, pady=0, sticky='w') 
               
        self.run_button = Button(button_frame, text='out', command=self.run_edtools_out, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=4, column=0,  padx=130, pady=1, sticky='w') 
                
        self.space_labe1 = Label(button_frame, height=1)
        self.space_labe1.grid(row=5, column=0, pady=0, sticky='w') 
       
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=5, column=0, sticky='ew', pady=0)
        
        # Create and place input command label and entry widgets
        self.input_command_entry = tk.Entry(button_frame, font=("Helvetica", 16), width=40)
        self.input_command_entry.grid(row=6, column=0, columnspan=2, padx=0, pady=1, sticky='w') 
        

        # Create and place button widget
        self.run_button = tk.Button(button_frame, text="Update XDS.INP", command=self.run_edtools_update_xds, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=7, column=0, padx=0, pady=1, sticky='w') 
        
        self.run_button = Button(button_frame, text='open XDS.INP one by one', command=self.open_xds_inp_file, font=("Helvetica", 16))
        self.run_button.grid(row=8, column=0, padx=50, pady=1, sticky='w')  

        self.space_labe1 = Label(button_frame, height=1)
        self.space_labe1.grid(row=9, column=0, pady=0, sticky='w')        

        self.old_text_label = Label(button_frame, text='old text:', font=("Helvetica", 16))
        self.old_text_label.grid(row=10, column=0, padx=50, pady=1, sticky='w') 
        self.old_text_entry = Entry(button_frame, font=("Helvetica", 12), width=47)
        self.old_text_entry.grid(row=11, column=0, padx=50, pady=1, sticky='w') 
        
        self.new_text_label = Label(button_frame, text='new text:', font=("Helvetica", 16))
        self.new_text_label.grid(row=12, column=0, padx=50, pady=1, sticky='w') 
        self.new_text_entry = Entry(button_frame, font=("Helvetica", 12), width=47)
        self.new_text_entry.grid(row=13, column=0, padx=50, pady=1, sticky='w') 
               
        self.run_button = Button(button_frame, text='batch replace text', command=self.run_batch_replace, font=("Helvetica", 16))
        self.run_button.grid(row=14, column=0, padx=50, pady=1, sticky='w') 
        
        self.space_labe1 = Label(button_frame, height=1)
        self.space_labe1.grid(row=15, column=0, pady=0, sticky='w')

        self.run_button = Button(button_frame, text='comment tools', command=self.run_comment_tools, font=("Helvetica", 16))
        self.run_button.grid(row=16, column=0, padx=50, pady=1, sticky='w')

        self.run_button = Button(button_frame, text='update mosaicity', command=self.run_update_mosaicity, font=("Helvetica", 16))
        self.run_button.grid(row=16, column=0, padx=215, pady=1, sticky='w') 
        
        self.space_label = Label(button_frame, height=1)
        self.space_label.grid(row=17, column=0, pady=0, sticky='w') 
        
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=17, column=0, sticky='ew', pady=0)
        
        self.run_button = Button(button_frame, text='Extract xds info', command=self.run_edtools_extract_xds_info, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=18, column=0, padx=0, pady=1, sticky='w') 
      
        self.run_button = Button( button_frame, text='evaluation', command=self.run_evaluation, font=("Helvetica", 16))
        self.run_button.grid(row=19, column=0, padx=50, pady=1, sticky='w') 
        
        self.run_button = Button( button_frame, text='plot scale factors', command=self.run_plot_scale, font=("Helvetica", 16))
        self.run_button.grid(row=19, column=0, padx=173, pady=1, sticky='w') 
        
        self.run_button = Button(button_frame, text='xdsgui', command=self.run_xdsgui, font=("Helvetica", 16))
        self.run_button.grid(row=19, column=0, padx=360, pady=1, sticky='w')   
       
        self.run_button = Button(button_frame, text='REDp', command=self.run_redp, font=("Helvetica", 16))
        self.run_button.grid(row=20, column=0, padx=50, pady=1, sticky='w')  
        
        self.run_button = Button(button_frame, text='table', command=self.run_table, font=("Helvetica", 16))
        self.run_button.grid(row=20, column=0, padx=150, pady=1, sticky='w') 

        self.run_button = Button(button_frame, text='calculate symmetry', command=self.run_calculate_symmetry, font=("Helvetica", 16))
        self.run_button.grid(row=20, column=0, padx=240, pady=1, sticky='w')    
       
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=21, column=0, sticky='ew', pady=0)
        
        self.space_label3 = Label(button_frame, height=1)
        self.space_label3.grid(row=21, column=0, pady=0, sticky='w') 
        
        self.run_button = Button(button_frame, text='Clustering (unit cell)', command=self.run_edtools_find_cell, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=22, column=0, padx=0, pady=1, sticky='w') 
        
        self.space_label3 = Label(button_frame, height=1)
        self.space_label3.grid(row=23, column=0, pady=0, sticky='w')  
        
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=23, column=0, sticky='ew', pady=0)
        
        self.run_button = Button(button_frame, text='Make xscale inp file', command=self.run_edtools_make_xscale, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=24, column=0, padx=0, pady=1, sticky='w') 
        
        self.space_label3 = Label(button_frame, height=1)
        self.space_label3.grid(row=25, column=0, pady=0, sticky='w') 
        
        
        self.run_button = Button(button_frame, text='Xscale', command=self.run_xscale, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=26, column=0, padx=0, pady=1, sticky='w')
        
        self.space_label3 = Label(button_frame, height=1)
        self.space_label3.grid(row=27, column=0, padx=50, pady=1, sticky='w') 
        
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=27, column=0, sticky='ew', pady=0)
        
        self.run_button = Button(button_frame, text='Clustering (CC)', command=self.run_edtools_cluster_in, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=28, column=0, padx=0, pady=1,sticky='w')
        
        self.run_button = Button(button_frame, text='out', command=self.run_edtools_cluster_out, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=28, column=0, padx=182, pady=1,sticky='w')
        
        self.run_button = Button(button_frame, text='xdsconv', command=self.run_xdsconv, font=("Helvetica", 16))
        self.run_button.grid(row=28, column=0, padx=340, pady=1, sticky='w')

       
        self.space_label3 = Label(button_frame, height=1)
        self.space_label3.grid(row=29, column=0, pady=0, sticky='w') 
        
        ttk.Separator(button_frame, orient=HORIZONTAL).grid(row=29, column=0, sticky='ew', pady=0)
       
        self.run_button = Button(button_frame, text='Solution', command=self.run_solution, font=("Helvetica", 16, "bold"))
        self.run_button.grid(row=30, column=0, padx=0, pady=1, sticky='w') 

    def select_root_dir(self):
        root_dir = filedialog.askdirectory()
        self.root_dir_entry.delete(0, END)
        self.root_dir_entry.insert(0, root_dir)
    
#        # Open the directory in a file explorer window
#        if platform.system() == 'Windows':
#            subprocess.Popen(f'explorer "{os.path.abspath(root_dir)}"', shell=True)
#        elif platform.system() == 'Darwin':  # macOS
#            subprocess.Popen(['open', root_dir])
#        else:  # Linux and other Unix-like systems
#            subprocess.Popen(['xdg-open', root_dir])
    
    def open_root_dir(self):
        root_dir = self.root_dir_entry.get()
        if platform.system() == 'Windows':
            subprocess.Popen(f'explorer "{os.path.abspath(root_dir)}"', shell=True)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.Popen(['open', root_dir])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(['xdg-open', root_dir])
            
    def select_and_open_root_dir(self):
        root_dir = filedialog.askdirectory()
        self.root_dir_entry.delete(0, END)
        self.root_dir_entry.insert(0, root_dir)
        if platform.system() == 'Windows':
            subprocess.Popen(f'explorer "{os.path.abspath(root_dir)}"', shell=True)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.Popen(['open', root_dir])
        else:  # Linux and other Unix-like systems
            subprocess.Popen(['xdg-open', root_dir])
           
    def run_edtools_in(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.call(["edtools.autoindex"], shell=True)
        
    def run_edtools_out(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'edtools.autoindex'])

    def open_xds_inp_file(self):
        if not hasattr(self, 'found_files'):
            self.found_files = []
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        if not self.found_files:
            # Find all XDS.INP files in the directory
            for root, dirs, files in os.walk(root_dir):
                for file in files:
                    if file == "XDS.INP":
                        filepath = os.path.join(root, file)
                        if filepath not in self.found_files:
                            self.found_files.append(filepath)
            if not self.found_files:
                print("No XDS.INP files found")
                return
            self.current_index = 0  # Initialize the current index to 0
        # Print the XDS.INP file at the current index
        filepath = self.found_files[self.current_index]
        folder = os.path.dirname(filepath)
        with open(filepath, "r", encoding="windows-1252") as f:
            print(f"XDS.INP file found in {folder}:\n")
            print(f.read())
        # Increment the current index for the next function call
        self.current_index = (self.current_index + 1) % len(self.found_files)
        os.chdir(root_dir)
    
               
    def run_edtools_find_cell(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.call(["edtools.find_cell", "-c"], shell=True)
    
    def run_edtools_extract_xds_info(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.call(["edtools.extract_xds_info"], shell=True)
        
    def run_evaluation(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        os.system("python C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/evaluation.py")
        
    def run_plot_scale(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        os.system("python C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/plot_scale.py")

    def run_redp(self):
        
        # Build the command to run redp
        command = 'E:/Program Files (x86)/REDp/REDp.exe'
        
        # Open redp in the specified directory
        subprocess.Popen(command)
        
    def run_table(self):
        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', "python C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.py"])
        
    def run_calculate_symmetry(self):
        url = 'http://cci.lbl.gov/cctbx/lattice_symmetry.html'
        
        # Open a user command window
        subprocess.Popen(['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        # Open the website in the default browser
        os.system(f'start {url}')
        
    def run_comment_tools(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        os.system("python C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/comment.py")
        
    def run_update_mosaicity(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        os.system("python C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/update_mosaicity.py")
        
    def run_edtools_make_xscale(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        text = pyperclip.paste()
        subprocess.call(["edtools.make_xscale", "./", text], shell=True)    
        
    def run_xscale(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.run(["wsl", "xscale"], shell=True) 
              
    
    def run_edtools_cluster_in(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.call(["edtools.cluster"], shell=True) 
        
    def run_edtools_cluster_out(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'edtools.cluster'])
    
    def batch_replace_text(self, root_dir, old_text_pattern, new_text):
        pattern = re.compile(old_text_pattern)
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename == 'XDS.INP':
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r', encoding="windows-1252") as f:
                        content = f.read()
                    content = re.sub(pattern, new_text, content)
                    with open(file_path, 'w', encoding="windows-1252") as f:
                        f.write(content)     
                    print(f'Modified XDS.INP file: {file_path}')        

    def run_batch_replace(self):
        root_dir = self.root_dir_entry.get()
        old_text_pattern = self.old_text_entry.get()
        new_text = self.new_text_entry.get()
        self.batch_replace_text(root_dir, old_text_pattern, new_text)
        
    def run_edtools_update_xds(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        input_command = self.input_command_entry.get()
    
        # Split input command into separate arguments
        args = input_command.split()
    
        # Write arguments to log file
        with open("command.log", "w") as f:
            for arg in args:
                f.write(arg + "\n")
    
        # Call edtools.update_xds() function with arguments
        subprocess.call(["edtools.update_xds"] + args, shell=True)
        
    def run_xdsgui(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        
        # open new command prompt window
        subprocess.call(['cmd.exe', '/c', 'start'])
        
        # wait for the new command prompt window to open
        time.sleep(2)
        
        # send "bash" command and press "Enter"
        pyautogui.typewrite('bash')
        pyautogui.press('enter')
        time.sleep(2)
        
        # send "xdsgui" command and press "Enter"
        pyautogui.typewrite('xdsgui')
        pyautogui.press('enter')
        
        time.sleep(2)
        
        # send "xdsgui" command and press "Enter"
        os.system("echo 'xdsgui\n' | xclip -selection clipboard")
        subprocess.call(['xdotool', 'key', 'ctrl+shift+v'])
        
    def run_solution(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        subprocess.Popen(['cmd', '/c', 'start', 'cmd', '/k', 'python C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/solution.py'])

    def run_xdsconv(self):
        root_dir = self.root_dir_entry.get()
        os.chdir(root_dir)
        # open new command prompt window
        subprocess.call(['cmd.exe', '/c', 'start'])
        
        # wait for the new command prompt window to open
        time.sleep(1)
        
        # send "bash" command and press "Enter"
        pyautogui.typewrite('bash')
        pyautogui.press('enter')
        time.sleep(1)
        
        # send "xdsgui" command and press "Enter"
        pyautogui.typewrite('xdsconv')
        
        pyautogui.press('enter')



if __name__ == '__main__':
    app = Application()
    app.master.title('edtools interface')
    app.mainloop()