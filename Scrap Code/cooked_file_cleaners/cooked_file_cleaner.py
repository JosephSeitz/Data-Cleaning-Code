#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 2019

This code is meant to clean up the data files of several controlled burns 
conducted by the U.S. forestry department. The inputed file contains several 
title rows that can jumble up the data and therefor will be replaced with a 
simple row of column titles. The timestamps, in the first column, will be 
broken up into seperate columns for easier analysis (year, month, day, hour, 
minute, second) and added to the end of the new file that is writen. You can 
create a 'cleaned' file with or without headers, with the option of the headers
in a read_me file seperate for easier analysis.   

@author: Joey Seitz
"""

### Tools used for clean up
import numpy as np
import pandas as pd

file_path = str(input("Input full file path:" ))
fill_nan = str(input("What value to use for NaN values? ex: (999):"))

def data_reader():
    """
    data_reader() takes a file path and reads in the file given as a pandas
    dataframe with requested title rows stripped, fills the nan values as 
    desired, and returns the data frame for further use.
    
    OUT:
        df (pandas data frame): This is the raw data with headers stripped and 
                                nan values replaced 
    """
    ### Read in the file with certain rows skipped 
    skipper= int(input("How many title rows are there in the file?:"))
    df=pd.read_csv(file_path, header=None, skiprows=skipper, \
                   na_values='NAN')
    ### Value to replace the NaN's in the data file
    df.fillna(value=fill_nan, inplace=True) 
    
    print()
    print("DateFile loaded:")
    print(df.head())
    correct_df = input("Is this the correct number of rows skipped? (y/n):")
    
    #loop until the correct format is created
    while correct_df.lower() == "n":
        ### Read in the file with certain rows skipped 
        skipper= int(input("How many title rows are there in the file?:"))
        df=pd.read_csv(file_path, header=None, skiprows=skipper, \
                   na_values='NAN')
        ### Value to replace the NaN's in the data file
        df.fillna(value=fill_nan, inplace=True) 
        
        print()
        print("DateFile loaded:")
        print(df.head())
        
        correct_df =input("Is this the correct number of rows skipped? (y/n):")
    
    return df

def new_df(df):
    """
    new_df() takes the data frame created by data_reader(), assumes that the
    first column in the data frame is the timestamp, and seperates the column 
    into new columns: year (YYYY), month (MM), day (DD), hour (Hour), minute 
    (Min), second (Sec). Then creates a new data frame, writes the data from 
    the file first then add the new time columns to the end of the df with 
    corresponding column headers
    
    INPUT:
        df (pandas dataframe): dataframe created in data_reader()
    
    OUTPUT:
        df_write(pandas dataframe): the desired dataframe with the timestamp 
                                    seperated and added to the last columns
    """
        
    ### Creating null list in the correct shape to 'append' to
    year_lst  = list(np.full(len(df),fill_nan))
    month_lst = list(np.full(len(df),fill_nan))
    day_lst   = list(np.full(len(df),fill_nan))
    hour_lst  = list(np.full(len(df),fill_nan))
    min_lst   = list(np.full(len(df),fill_nan))
    second_lst= list(np.full(len(df),fill_nan))
    
    ### Parcing the timestamps and seperating them 
    for i in range(len(df)):
        time_step    = df[0][i].replace("-", ",").replace(":",",").replace(" ",",").replace("/",',').split(",")
        year_lst[i]  = "{:.0f}".format(float(time_step[0])).zfill(4)
        month_lst[i] = "{:.0f}".format(float(time_step[1])).zfill(2)
        day_lst[i]   = "{:.0f}".format(float(time_step[2])).zfill(2)
        hour_lst[i]  = "{:.0f}".format(float(time_step[3])).zfill(2)
        min_lst[i]   = "{:.0f}".format(float(time_step[4])).zfill(2)
        second_lst[i]= "{:.1f}".format(float(time_step[5])).zfill(4)

    #### Creation of the new df headers
    headers_df = pd.read_csv(file_path,skiprows=1,nrows = 0)
    column_lst = list(headers_df.columns[1:])
    split_column_lst = ["YYYY","MM","DD","Hour","Min","Sec"]
    column_lst += split_column_lst
    
    ### Creating the new dataframe
    df_write = pd.DataFrame()
    for i in range(1,(len(df.columns))):
            df_write[i-1] = df[i]
    
    df_write["YYYY"] = year_lst
    df_write["MM"]   = month_lst
    df_write["DD"]   = day_lst
    df_write["Hour"] = hour_lst
    df_write["Min"]  = min_lst
    df_write["Sec"]  = second_lst
    
    df_write.columns=column_lst #Appending the headers for each column
    print()
    print("Cleaned Dataframe:")
    print(df_write.head())
    
    return df_write


def save_file(df_write):
    """
    save_file takes a pandas dataframe and creates the output file with either 
    header/no headers. If no header desired, there is an option to create a 
    seperate read_me file containing the headers of the .txt file.
    
    IN:
        df_write (pandas df): the dataframe desired to write to .txt file 
    """
    
    file_name =  file_path.split("/")[-1][:-4]+'_OUT' #output file name
    out_path='' #for saving in current directory
    write_q = input("Write dataframe to file? (y/n)")
    
    ### How to write the file
    if write_q.lower() == "y":
        save_cur_dir= input("Output to current directory? (y/n):")
        if save_cur_dir.lower() == 'n':
            out_path = str(input("FULL Directory path for output:"))
        
        headers_q = input("Headers on output? (y/n):")
        if headers_q.lower() == "n":
            readme_q = input("Would you like seperate a read_me file containing the headers? (y/n):")
            if readme_q.lower() == "y":
                read =list(df_write.columns)

                #creating the read_me file
                with open(out_path+file_name+"_read_me.txt", "w") as output:
                    output.write("Column_headers"+ str(read))
                
    # writing with only data, no read_me
    if write_q.lower() == 'y' and headers_q.lower() =='n':
        df_write.to_csv(out_path+file_name+".txt", sep='\t',index=False, \
                        header=False)
    #writing with data, with headers
    if write_q.lower() == 'y' and headers_q.lower() =='y':
        df_write.to_csv(out_path+file_name+ ".txt", sep='\t',index=False,\
                        header=True) 
    #to get to normal pd out file remove: "sep='\t' " from .to_csv()


def main():
    """
    Pulls all the functions in and combines them so they can all run together
    """
    df = data_reader()
    df_write = new_df(df)
    save_file(df_write)
    
main() #run everything
    








