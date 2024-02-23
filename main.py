#This is a program that will take in multiple directories and read the trial contents from vicon to determine which ones have been cropped or not

import os
import tkinter as tk
from tkinter import filedialog
import c3d
import pandas as pd


zero_frame_trials = []
cropped_trials = []
data = []

#function used later to get the first frame of a trial 
def get_trial_start_frame(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():
            if i == 1:
                return points
            
#create root window
root = tk.Tk()
root.withdraw() #Hides root window

dirs = []

#Ask the user to select multiple directories and store them in dirs
while True:
    #sets directories equal to selection
    directories = filedialog.askdirectory(title="Select directories containing trial files")

    #If statement that determines if you hit cancel or selected a directory
    if directories != '':
        dirs.append(directories)
        if not directories:
            break
    else:
        break

print (dirs)

#Main loop to iterate through each file
if dirs:
    for directory in dirs:
        
        #Lists to store trials starting at 0 frames and trials starting at >0 frames
        

        #Now that we'er in a directory go through each file 
        for filename in os.listdir(directory):
            #find the files that end with .c3d
            if filename.endswith(".c3d"):
                file_path = os.path.join(directory, filename)

                #run our file through get trial start frame
                start_frame = get_trial_start_frame(file_path)

                #test
                print(start_frame)

                #deciding which list to put the file in


                if start_frame is None:
                    cropped_trials.append(filename)
                else:
                    zero_frame_trials.append(filename)
                
        #append the sorted lists to the data
        data.append({
            'Directory': directory,
            'Trials starting at 0 frames': ', '.join(zero_frame_trials),
            'Trials starting after 0 frames': ', '.join(cropped_trials)
        })

    #DataFrame from data
    df = pd.DataFrame(data)

    #Ask the user to specify name and file location for excel file
    excel_file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[("Excel files", "*.xlsx")])

                


                


else:
    print("No directories selected.")

print (f'{zero_frame_trials}{cropped_trials}')