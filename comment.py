import os
import re
import tkinter as tk
from tkinter import filedialog
import subprocess

def select_root_directory():
    root_directory = os.getcwd()
    return root_directory

def comment_function(root_directory, old_text_pattern, new_text):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == 'XDS.INP':
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding="windows-1252") as f:
                    lines = f.readlines()
                with open(file_path, 'w', encoding="windows-1252") as f:
                    for line in lines:
                        if re.search(old_text_pattern, line):
                            line = '!' + line
                        f.write(line)
                print(f'Modified {file_path}')  
                
def batch_comment_function(root_directory, old_text_patterns, new_text):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == 'XDS.INP':
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding="windows-1252") as f:
                    lines = f.readlines()
                with open(file_path, 'w', encoding="windows-1252") as f:
                    for line in lines:
                        for old_text_pattern in old_text_patterns:
                            if re.search(old_text_pattern, line):
                                line = '!' + line
                        f.write(line)
                print(f'Modified {file_path}')
                
def uncomment_function(root_directory, old_text_pattern, new_text):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == 'XDS.INP':
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding="windows-1252") as f:
                    lines = f.readlines()
                with open(file_path, 'w', encoding="windows-1252") as f:
                    for line in lines:
                        line = re.sub(r'!+\s*' + re.escape(old_text_pattern), old_text_pattern, line)
                        f.write(line)
                print(f'Modified {file_path}')
                
def smart_batch_uncomment_function(root_directory, old_text_patterns, new_text):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == 'XDS.INP':
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding="windows-1252") as f:
                    lines = f.readlines()
                with open(file_path, 'w', encoding="windows-1252") as f:
                    uncommented_patterns = set()  # track which patterns have already been uncommented
                    for line in lines:
                        for old_text_pattern in old_text_patterns:
                            if old_text_pattern in line and old_text_pattern not in uncommented_patterns:
                                line = line.replace('!' + old_text_pattern, old_text_pattern, 1)  # replace only the first occurrence
                                line = re.sub(r'!+\s*' + re.escape(old_text_pattern), old_text_pattern, line)
                                uncommented_patterns.add(old_text_pattern)
                        f.write(line)
                print(f'Modified {file_path}')

                
def batch_uncomment_function(root_directory, old_text_patterns, new_text):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == 'XDS.INP':
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r', encoding="windows-1252") as f:
                    lines = f.readlines()
                with open(file_path, 'w', encoding="windows-1252") as f:
                    for line in lines:
                        for old_text_pattern in old_text_patterns:
                            line = re.sub(r'!+\s*' + re.escape(old_text_pattern), old_text_pattern, line)
                        f.write(line)
                print(f'Modified {file_path}')

                
def uncomment_space_group_and_unit_cell_clicked():
    root_directory = select_root_directory()
    old_text_pattern = ['SPACE_GROUP_NUMBER', 'UNIT_CELL_CONSTANTS']
    new_text = ''
    batch_uncomment_function(root_directory, old_text_pattern, new_text)
                    
def uncomment_unit_cell_clicked():
    root_directory = select_root_directory()
    old_text_pattern = 'UNIT_CELL_CONSTANTS'
    new_text = ''
    uncomment_function(root_directory, old_text_pattern, new_text)
                    
def uncomment_strong_pixel_clicked():
    root_directory = select_root_directory()
    old_text_pattern = 'STRONG_PIXEL'
    new_text = ''
    uncomment_function(root_directory, old_text_pattern, new_text)
                  
def uncomment_mosaicity_clicked():
    root_directory = select_root_directory()
    old_text_pattern = ['BEAM_DIVERGENCE=', 'REFLECTING_RANGE=']
    new_text = ''
    smart_batch_uncomment_function(root_directory, old_text_pattern, new_text)
    
def comment_space_group_and_unit_cell_clicked():
    root_directory = select_root_directory()
    old_text_pattern = ['SPACE_GROUP_NUMBER', 'UNIT_CELL_CONSTANTS']
    new_text = ''
    batch_comment_function(root_directory, old_text_pattern, new_text)

def comment_strong_pixel_clicked():
    root_directory = select_root_directory()
    old_text_pattern = 'STRONG_PIXEL'
    new_text = ''
    comment_function(root_directory, old_text_pattern, new_text)
    
def comment_mosaicity_clicked():
    root_directory = select_root_directory()
    old_text_pattern = ['BEAM_DIVERGENCE=', 'REFLECTING_RANGE=']
    new_text = ''
    batch_comment_function(root_directory, old_text_pattern, new_text)

root = tk.Tk()
root.title('Comment')

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

comment_space_group_number_button = tk.Button(frame, text='Comment space group and unit cell', command=comment_space_group_and_unit_cell_clicked, font=("Helvetica", 16))
comment_space_group_number_button.grid(row=1, column=1, sticky='W')

comment_strong_pixel_button = tk.Button(frame, text='Comment strong pixel', command=comment_strong_pixel_clicked, font=("Helvetica", 16))
comment_strong_pixel_button.grid(row=2, column=1, sticky='W')

comment_mosaicity_button = tk.Button(frame, text='Comment mosaicity', command=comment_mosaicity_clicked, font=("Helvetica", 16))
comment_mosaicity_button.grid(row=3, column=1, sticky='W')

comment_uncomment_space_group_number_button = tk.Button(frame, text='Uncomment space group and unit cell', command=uncomment_space_group_and_unit_cell_clicked, font=("Helvetica", 16))
comment_uncomment_space_group_number_button.grid(row=1, column=2, sticky='W')

comment_uncomment_strong_pixel_button = tk.Button(frame, text='Uncomment strong pixel', command=uncomment_strong_pixel_clicked, font=("Helvetica", 16))
comment_uncomment_strong_pixel_button.grid(row=2, column=2, sticky='W')

comment_uncomment_mosaicity_button = tk.Button(frame, text='Uncomment mosaicity', command=uncomment_mosaicity_clicked, font=("Helvetica", 16))
comment_uncomment_mosaicity_button.grid(row=3, column=2, sticky='W')

root.mainloop()
