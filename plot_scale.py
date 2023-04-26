import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate


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

def plot_scale(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None

    # Load data from file
    with open(file_path, 'r', encoding="windows-1252") as f:
        lines = f.readlines()

    # Find the indices of the lines containing "IMAGE IER  SCALE"
    start_indices = []
    for i, line in enumerate(lines):
        if line.startswith(' IMAGE IER  SCALE'):
            start_indices.append(i)

    if len(start_indices) == 0:
        print(f'Could not find "IMAGE IER  SCALE" in file {file_path}')
        return

    # Extract the data lines from each hit of "IMAGE IER SCALE"
    all_data_lines = []
    for start_index in start_indices:
        data_lines = lines[start_index+1:start_index+16]
        all_data_lines.extend(data_lines)

    # Extract the relevant data into a matrix
    data_matrix = []
    for line in all_data_lines:
        parts = line.split()
        if len(parts) >= 3:
            data_matrix.append([int(parts[0]), float(parts[2])])

    # Convert the matrix to NumPy arrays
    data_array = np.array(data_matrix)
    x = data_array[:, 0]
    y = data_array[:, 1]
    
    for i in range(1, len(y)):
        if y[i] == 0:
            y[i] = y[i-1]
        
 
    # Generate plot
    plt.plot(x, y)
    plt.xlabel('Image number')
    plt.ylabel('Scale factor')
    plt.title('SCALE plot')
    plt.xlim(0, None)
    
    # Define function to get selected points using ginput
    def get_selected_points():
        """
        Get x coordinates of two points selected on the plot.
    
        Returns:
            (float, float): Tuple containing the x coordinates of the two selected points.
        """
        points = plt.ginput(2, show_clicks=True)
    
        # Sort points in ascending order of x coordinate
        points = sorted(points, key=lambda p: p[0])
    
        # Extract x coordinates of selected points
        x_values = [int(p[0]) for p in points]
        print(f"Selected x values: {x_values}")
    
        # Draw vertical lines at selected points
        plt.axvline(x=x_values[0], color='r', linestyle='--')
        plt.axvline(x=x_values[1], color='r', linestyle='--')
    
        # Show plot with selected points
        plt.show()
    
        return tuple(x_values)

    # Call the function to get the selected points
    x_values = get_selected_points()
    
    # Find all INTEGRATE.LP files in current and subdirectories
    integrate_files = find_files_with_extension('.', 'INTEGRATE.LP')
    
    # Loop over INTEGRATE.LP files and update XDS.INP files in the same directories
    for integrate_file in integrate_files:
        xdsinp_file = os.path.join(os.path.dirname(integrate_file), 'XDS.INP')
        if os.path.exists(xdsinp_file):
            # Read contents of XDS.INP file
            with open(xdsinp_file, 'r', encoding="windows-1252") as f:
                xdsinp_contents = f.read()
    
            # Find the line with "BACKGROUND_RANGE"
            background_range_line = ''
            for line in xdsinp_contents.split('\n'):
                if 'BACKGROUND_RANGE=' in line:
                    background_range_line = line
                    break
            
            # Add "EXCLUDE_DATA_RANGE" to the line after "BACKGROUND_RANGE"
            exclude_data_range = f'EXCLUDE_DATA_RANGE={int(x_values[0])} {int(x_values[1])}\n'
            xdsinp_contents = xdsinp_contents.replace(background_range_line, f'{background_range_line}\n{exclude_data_range}')
    
            # Write updated contents to XDS.INP file
            with open(xdsinp_file, 'w', encoding="windows-1252") as f:
                f.write(xdsinp_contents)
    
                
                


if __name__ == "__main__":
    folder_path = "."  # replace with your desired folder path
    integrate_lp_files = find_files_with_extension(folder_path, "INTEGRATE.LP")
    for file_path in integrate_lp_files:
        plot_scale(file_path)
