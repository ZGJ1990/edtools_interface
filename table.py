from prettytable import PrettyTable
from docx import Document
import tkinter as tk

class TableViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Table Viewer")
        
        self.monoclinic_button = tk.Button(self.master, text="Monoclinic", command=self.search_monoclinic, font=("Helvetica", 16))
        self.monoclinic_button.pack()
        
        self.orthorhombic_button = tk.Button(self.master, text="Orthorhombic", command=self.search_orthorhombic, font=("Helvetica", 16))
        self.orthorhombic_button.pack()
        
        self.tetragonal_button = tk.Button(self.master, text="Tetragonal", command=self.search_tetragonal, font=("Helvetica", 16))
        self.tetragonal_button.pack()
        
        self.trigonal_button = tk.Button(self.master, text="Trigonal", command=self.search_trigonal, font=("Helvetica", 16))
        self.trigonal_button.pack()
        
        self.hexagonal_button = tk.Button(self.master, text="Hexagonal", command=self.search_hexagonal, font=("Helvetica", 16))
        self.hexagonal_button.pack()
        
        self.cubic_button = tk.Button(self.master, text="Cubic", command=self.search_cubic, font=("Helvetica", 16))
        self.cubic_button.pack()

    def find_table(self, document, text):
        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if text in cell.text:
                        return table
        return None

    def print_table(self, document_path, text):
        document = Document(document_path)
        table = self.find_table(document, text)
        if table is None:
            print("Table not found.")
        else:
            data = []

            # get the data from the table
            keys = None
            for i, row in enumerate(table.rows):
                text = (cell.text for cell in row.cells)

                # Establish the mapping based on the first row
                # headers; these will become the keys of our dictionary
                if i == 0:
                    keys = tuple(text)
                    continue

                # Construct a dictionary for this row, mapping
                # keys to values for this row
                row_data = tuple(text)
                data.append(row_data)

            # check which headers are not unique and add suffix
            header_count = {}
            column_headers = []
            for header in keys:
                if header in header_count:
                    header_count[header] += 1
                    header = f"{header}_{header_count[header]}"
                else:
                    header_count[header] = 0
                column_headers.append(header)

            # create a PrettyTable object and populate it with the data
            pretty_table = PrettyTable(column_headers)
            for row in data:
                pretty_table.add_row(row)

            # print the table
            print(f"Table containing '{text}' in '{document_path}':")
            print(pretty_table)
            
    def search_monoclinic(self):
        self.print_table('C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.docx', 'MONOCLINIC')
        
    def search_orthorhombic(self):
        self.print_table('C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.docx', "ORTH")
        
    def search_tetragonal(self):
        self.print_table('C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.docx', "TET")
        
    def search_trigonal(self):
        self.print_table('C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.docx', "TRI")
        
    def search_hexagonal(self):
        self.print_table('C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.docx', "HEXAGONAL")
        
    def search_cubic(self):
        self.print_table('C:/Users/guzh3353/AppData/Local/Programs/Python/Python38/Lib/site-packages/edtools/table.docx', "CUBIC")
        
        
if __name__ == "__main__":
    root = tk.Tk()
    table_viewer = TableViewer(root)
    root.mainloop()
