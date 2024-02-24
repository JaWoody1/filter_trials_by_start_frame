#This is a program that will take in multiple directories and read the trial contents from vicon to determine which ones have been cropped or not
import base64
import os
import tkinter as tk
from tkinter import filedialog
import c3d
import pandas as pd
import numpy as np
import xlsxwriter

#encryption
code = base64.b64encode(b"""

zero_frame_trials = []
cropped_trials = []
data = []
dirs = []
dir_filename = {}
longest_string_a = 0

#function used later to get the first frame of a trial 
def get_trial_start_frame(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():
            if i == 1:
                return points
            
#function to find starting frame
def get_first_frame(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():

            if points is None:
                continue
            else:
                return i
            
#functions to get subdirectories from main directory
def list_subdirectories(parent_directory):
    subdirectories = [subdir for subdir in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, subdir))]
    return subdirectories

#ask for the parent directory
parent_directory = filedialog.askdirectory(title="Select directory containing trial files")

dirs = [x[0] for x in os.walk(parent_directory)]
print(dirs)
            
#create root window
root = tk.Tk()
root.withdraw() #Hides root window

############################################################################################################
#Main loop to iterate through each file
if dirs:
    for directory in dirs:
        
        #get longest directory name
        if len(directory) >= longest_string_a:
            longest_string_a = len(directory)

        #Lists to store trials starting at 0 frames and trials starting at >0 frames
        

        #Now that we'er in a directory go through each file 
        for filename in os.listdir(directory):

            

            #find the files that end with .c3d
            if filename.endswith(".c3d"):
                file_path = os.path.join(directory, filename)

                #run our file through get trial start frame
                first_info = get_trial_start_frame(file_path)
                start_frame = get_first_frame(file_path)

                #test
                #print(first_info)

                #deciding which list to put the file in
                if first_info is None:
                    cropped_trials.append(filename)
                    data.append({'Directory': directory, 'Start Frame': start_frame, 'Clipped Trials': ''.join(filename)})

                    #getting the size of the column
                    longest_string_b = 14
                    if len(filename) >= longest_string_b:
                        longest_string_b = len(filename)
                else:
                    zero_frame_trials.append(filename)
                    data.append({'Directory': directory, 'Start Frame': start_frame, 'Full Length Trials': ''.join(filename)})
                    
                    #getting the size of the column
                    longest_string_c = len('Full Length Trials')
                    if len(filename) >= longest_string_c:
                        longest_string_c = len(filename)
            
                 

    #DataFrame from data
    df = pd.DataFrame(data)

    #Ask the user to specify name and file location for excel file
    excel_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])

    #Write DataFram to excel

    print(data)

    if excel_file_path:
        #Create a writer object to be able to use xlsxwriter
        writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')
        #create mandatory sheet for our dataframe
        df.to_excel(writer, index=False, sheet_name='report')
        workbook = writer.book
        worksheet = writer.sheets['report']

        #custom parameters for our worksheet

        #max_length = max(len(str(value)) for value in data['Directory'])
        
        worksheet.set_column('A:A', longest_string_a+5)
        worksheet.set_column('C:C', longest_string_b+5)
        worksheet.set_column('D:D', longest_string_c+5)
        worksheet.set_column('B:B', len('Start Frame')+5)


        

        
        writer.close()
        print("Excel Saved Success")
    else:
        print("No File selected")
    
    

    




                


else:
    print("No directories selected.")

                        
""")

exec(base64.b64decode(code))
