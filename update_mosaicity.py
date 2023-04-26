import os
import tkinter as tk
from tkinter import filedialog


def find_integrate_lp_files(folder_path):
    """
    Find all "INTEGRATE.LP" files in the specified folder.
    Returns a list of file paths.
    """
    file_paths = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename == "INTEGRATE.LP":
                file_paths.append(os.path.join(dirpath, filename))
    return file_paths
    

def find_resolution_lines(file_path):
    """
    Find the last 2 lines containing "***** SUGGESTED VALUES FOR INPUT PARAMETERS *****" in the specified file.
    Writes the lines at the beginning of an existing file named "XDS.INP" in the same folder of INTEGRATE.LP.
    """
    input_dir_path = os.path.dirname(file_path)
    output_file_path = os.path.join(input_dir_path, "XDS.INP")
    with open(file_path, "r") as f:
        lines = f.readlines()
    relevant_lines = []
    for i, line in enumerate(lines):
        if "***** SUGGESTED VALUES FOR INPUT PARAMETERS *****" in line:
            relevant_lines.append(lines[i+1].strip() + "\n")
            relevant_lines.append(lines[i+2].strip() + "\n")
    if os.path.exists(output_file_path):
        with open(output_file_path, "r", encoding="windows-1252") as f:
            existing_lines = f.readlines()
        with open(output_file_path, "w", encoding="windows-1252") as f:
            f.writelines(relevant_lines + existing_lines)
    else:
        with open(output_file_path, "w", encoding="windows-1252") as f:
            for line in relevant_lines:
                f.write(line)
    print(f"Last 2 lines of {file_path} written to {output_file_path}")

def write_to_xds(folder_path):
    """
    Find the last 2 lines containing "***** SUGGESTED VALUES FOR INPUT PARAMETERS *****" in all "INTEGRATE.LP" files
    in the specified folder and write them at the beginning of the corresponding "XDS.INP" files in the same folder.
    """
    integrate_lp_files = find_integrate_lp_files(folder_path)
    for file_path in integrate_lp_files:
        resolution_lines = find_resolution_lines(file_path)
        if resolution_lines is not None:
            output_file_path = os.path.join(os.path.dirname(file_path), "XDS.INP")
            if os.path.exists(output_file_path):
                with open(output_file_path, "r", encoding="windows-1252") as f:
                    existing_lines = f.readlines()
            else:
                existing_lines = []
            with open(output_file_path, "w", encoding="windows-1252") as f:
                f.write(resolution_lines[0] + "\n")
                f.write(resolution_lines[1] + "\n")
                for line in existing_lines:
                    f.write(line.strip() + "\n")
            print(f"Relevant lines written to existing {output_file_path}")
    print(f"All relevant lines written to XDS.INP files in {folder_path}")

def find_xds_inp_files(folder_path):
    """
    Find all "XDS.INP" files in the specified folder and its subfolders.
    """
    xds_inp_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == "XDS.INP":
                file_path = os.path.join(root, file)
                xds_inp_files.append(file_path)
    return xds_inp_files

def add_beam_reflectingrange_to_xds(folder_path):
    """
    Add a "!" in front of all lines containing "BEAM_DIVERGENCE=" or "REFLECTING_RANGE=" in all "XDS.INP" files
    in the specified folder and its subfolders except for the first two lines.
    """
    xds_inp_files = find_xds_inp_files(folder_path)
    for file_path in xds_inp_files:
        with open(file_path, "r", encoding="windows-1252") as f:
            lines = f.readlines()

        with open(file_path, "w", encoding="windows-1252") as f:
            # Keep track of how many relevant lines have been written so far
            num_written = 0

            for i, line in enumerate(lines):
                if i < 2:
                    f.write(line)
                elif "BEAM_DIVERGENCE=" in line or "REFLECTING_RANGE=" in line:
                    f.write("!" + line)
                else:
                    f.write(line)

            print(f"Relevant lines written to {file_path}")
    print(f"All relevant lines written to XDS.INP files in {folder_path}")


def select_folder():
    """
    Open a file dialog to current folder.
    """
    
    folder_path = os.getcwd()
    return folder_path


if __name__ == "__main__":
    folder_path = select_folder()
    write_to_xds(folder_path)
    find_xds_inp_files(folder_path)
    add_beam_reflectingrange_to_xds(folder_path)
