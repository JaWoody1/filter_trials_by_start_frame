# This is a program that will determine how many gaps there are based on trajectory data

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
frame_list = []
point_list = []


# Function to find starting frame
def get_first_frame(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():

            if points is None:
                continue
            else:
                return i


def get_trajecory_data(trial_file):
    with open(trial_file, 'rb') as f:
        c3d_data = c3d.Reader(f)
        for i, points, analog in c3d_data.read_frames():
            frame_list.append(i)
            point_list.append(points.shape)
            
             

        return frame_list, point_list,c3d_data.header.max_gap, c3d_data.header.
            


# Functions to get subdirectories from main directory
def list_subdirectories(parent_directory):
    subdirectories = [subdir for subdir in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, subdir))]
    return subdirectories


############################################################################################################
if __name__ == '__main__':
    # Ask for the parent directory
    parent_directory = filedialog.askdirectory(title="Select directory containing participant folders")

    # Create root window
    root = tk.Tk()
    root.withdraw() #Hides root window


    if parent_directory:

        for filename in os.listdir(parent_directory):

            if filename == '7.c3d':

                file_path = os.path.join(parent_directory, filename)

                points = get_trajecory_data(file_path)

                print(points[2])
                print(points[3])

                
            else:
                break
            

