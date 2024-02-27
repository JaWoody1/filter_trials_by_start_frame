#deletes c3d files that start over 1 frame

import pandas as pd
import numpy as np
from tkinter import filedialog
import pathlib
import os

total_dirs = []
dir_delete = []
new_data = []

#read excel file
excel_data_df = pd.read_excel('KEEP_sorted_files - Copy.xlsx', sheet_name='report')

#get directories
total_dirs = excel_data_df['Directory'].tolist()
total_backup = excel_data_df['Backup'].tolist()
total_cropped = excel_data_df['Cropped Trials'].tolist()
total_start_frame = excel_data_df['Start Frame'].tolist()
file_path = []

print(total_start_frame)

for i, dirs in enumerate(total_dirs):
    
    file_path = os.path.join(dirs, total_cropped[i])

    if total_backup[i] == "No" and "Copy" not in dirs:
        if total_start_frame[i] > 1:
            os.remove(file_path)
            new_data.append({'Directory': total_dirs[i], 'Frames': total_start_frame[i], 'Cropped Trials': total_cropped[i], 'File Path to Delete': file_path})
        else:
            continue
    else:
        continue

df = pd.DataFrame(new_data)

# Ask the user to specify name and file location for excel file
excel_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])



if excel_file_path:
    # Create a writer object to be able to use xlsxwriter
    writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')
    # Create mandatory sheet for our dataframe
    df.to_excel(writer, index=False, sheet_name='report')
    workbook = writer.book
    worksheet = writer.sheets['report']

    # TODO: Impliment custom parameters for worksheet

    #Close writer object
    writer.close()
    print("Excel Saved Success")
else:
    print("No File selected")


    
