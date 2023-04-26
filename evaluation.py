import os

def find_files_with_extension(folder_path, extension):
    matching_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(extension):
                file_path = os.path.join(dirpath, filename)
                matching_files.append(file_path)
    if len(matching_files) == 0:
        print(f"No files with extension '{extension}' found in folder '{folder_path}'")
    return matching_files

def find_observed_spots(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    observed_spots = []
    for i, line in enumerate(lines):
        if "INDEXING OF OBSERVED SPOTS IN SPACE GROUP" in line:
            observed_spots.append(f"{file_path}\n{line.strip()}\n{lines[i+1].strip()}")
    return observed_spots

        
def find_resolution_lines(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    resolution_lines = []
    last_resolution_lines = []
    for i, line in enumerate(lines):
        if "RESOLUTION     NUMBER OF REFLECTIONS" in line:
            last_resolution_lines = lines[i:i+14]
            last_resolution_lines = list(filter(None, last_resolution_lines)) # remove empty lines
            last_resolution_lines.insert(0, file_path) # add file path to the beginning
            resolution_lines.append(last_resolution_lines)
            last_resolution_lines.insert(0, file_path) # add file path to the beginning
    return last_resolution_lines


def write_evaluation_file(folder_paths):
    for folder_path in folder_paths:
        observed_spots = []
        last_resolution_lines = []  # list to store all the resolution lines found in each file
        for file_path in find_files_with_extension(folder_path, "IDXREF.LP"):
            observed_spots.extend(find_observed_spots(file_path))
            corresponding_correct_file = file_path.replace("IDXREF.LP", "CORRECT.LP")
            if os.path.isfile(corresponding_correct_file):
                last_resolution_lines.extend(find_resolution_lines(corresponding_correct_file))

        with open(os.path.join(folder_path, "evaluation.txt"), "w") as f:
            f.write("Observed Spots:\n")
            for spot in observed_spots:
                f.write(f"{spot.strip()}\n")
            f.write("\nResolution Lines:\n")
            for line in last_resolution_lines:
                f.write(f"{line.strip()}")
                f.write("\n")
            if not observed_spots and not last_resolution_lines:
                f.write("No observed spots or resolution lines found in this folder.")
        os.startfile(os.path.join(folder_path, "evaluation.txt"))               

if __name__ == "__main__":
    folder_path = "."  # replace with your desired folder path
    integrate_lp_files = find_files_with_extension(folder_path, "INTEGRATE.LP")
    idxref_lp_files = find_files_with_extension(folder_path, "IDXREF.LP")
    correct_lp_files = find_files_with_extension(folder_path, "CORRECT.LP")
    write_evaluation_file(folder_path)

