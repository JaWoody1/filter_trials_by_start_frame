# This is a program that will take in multiple directories and read the trial contents from vicon to determine which ones have been cropped or not

# DEFAULT IMPORTS
import os

# PACKAGE IMPORTS
import tkinter as tk
from tkinter import filedialog
import c3d
import pandas as pd
import xlsxwriter

zero_frame_trials = []
cropped_trials = []
data = []
dirs = []
dir_filename = {}
longest_string_a = 0
longest_string_c = len('Full Length Trials')
longest_string_d = len('Cropped Trials')


# Function to find starting frame
def get_first_frame(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():

            if points is None:
                continue
            else:
                return i


# Functions to get subdirectories from main directory
def list_subdirectories(parent_directory):
    subdirectories = [subdir for subdir in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, subdir))]
    return subdirectories


############################################################################################################
if __name__ == '__main__':
    # Ask for the parent directory
    parent_directory = filedialog.askdirectory(title="Select directory containing participant folders")

    # Loop that gets all subdirectories in directory
    dirs = [x[0] for x in os.walk(parent_directory)]
                
    # Create root window
    root = tk.Tk()
    root.withdraw() #Hides root window

    # Main loop to iterate through each file
    if dirs:

        for directory in dirs:
            
            # Get longest directory name
            if len(directory) >= longest_string_a:
                longest_string_a = len(directory)

            # Go through each file in each directory
            for filename in os.listdir(directory):

                #find the files that end with .c3d
                if filename.endswith(".c3d"):
                    file_path = os.path.join(directory, filename)

                    # Returns the first frame that contains information
                    start_frame = get_first_frame(file_path)

                    # Deciding which list to put the file in depending on where the start frame is
                    if start_frame != 1:
                        cropped_trials.append(filename)
                        data.append({'Directory': directory, 'Start Frame': start_frame, 'Full Length Trials': " ", 'Cropped Trials': ''.join(filename)})

                        # Getting the size of the column                        
                        if len(filename) >= longest_string_d:
                            longest_string_d= len(filename)
                    
                    else:
                        zero_frame_trials.append(filename)
                        data.append({'Directory': directory, 'Start Frame': start_frame, 'Full Length Trials': ''.join(filename), 'Cropped Trials': " "})
                        
                        # Getting the size of the column                        
                        if len(filename) >= longest_string_c:
                            longest_string_c = len(filename)            
                
                    
        print (data)
        # DataFrame from data
        df = pd.DataFrame(data)
        

        # Ask the user to specify name and file location for excel file
        excel_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])

        # Write DataFram to excel
        print(data)

        if excel_file_path:
            # Create a writer object to be able to use xlsxwriter
            writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')
            # Create mandatory sheet for our dataframe
            df.to_excel(writer, index=False, sheet_name='report')
            workbook = writer.book
            worksheet = writer.sheets['report']

            # TODO: Impliment custom parameters for worksheet

            # Set column width to max length strings in column
            worksheet.set_column('A:A', longest_string_a+5)
            worksheet.set_column('B:B', len('Start Frame')+5)
            worksheet.set_column('C:C', longest_string_c+5)
            worksheet.set_column('D:D', longest_string_d+5)

            #Close writer object
            writer.close()
            print("Excel Saved Success")
        else:
            print("No File selected")
        
    else:
        print("No directories selected.")
