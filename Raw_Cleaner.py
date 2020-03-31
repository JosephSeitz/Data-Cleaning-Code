# -*- coding: utf-8 -*-
"""
Raw file cleaner 
"""
### Tools used for clean up
import numpy as np
import pandas as pd



def file_to_df(path, file, f_skrow=4,h_skrow=1,raw=True):
    """
    This function takes in a path to a file then adds the correct headers 
    and makes the Timestamp the index and returns the dataframe
    
    inputs:
        path - directory of file
        file - wanted file to read in
        f_skrow - how many rows to skip for the data (default =  4)
        h_skrow - what row is the column names located
        raw - True if the timestamp is in the correct format
    output:
        df - pandas dataframe a usable format
    """    
    df = pd.read_csv(path+file, skiprows=f_skrow, na_values=['NAN', '00nan','000nan', "NaN"])
    headers_df = pd.read_csv(path+file,skiprows=h_skrow,nrows = 0)
    
    df.columns=list(headers_df)  #set the column names
    if raw:
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'])
    
    return(df)
    
def timestamp_matcher(df_names, file_num):
    """
    Takes a list of dataframes, prints the start and ends of all the files,
    then find the earliest timestamp that all dataframes have. Returns the 
    start and end time that can be used to trim the dataframes
    
    input: 
        df_names - list of dataframes 
        file_num - list of names for the files, used only for the print
    
    output:
        time-start - the starting timestampt that works with all files 
        time-end   - the ending timestampt that works with all files
    """
    
    min_lst, max_lst =[],[]

    for i in df_names:
        min_lst.append(i["TIMESTAMP"].min())
        max_lst.append(i["TIMESTAMP"].max())

        fmt = "File: {} | Start: {} | End: {}" 
    for i in range(len(min_lst)):
        print(fmt.format(file_num[i], min_lst[i],max_lst[i] ))

    time_start, time_end = max(min_lst), min(max_lst)    
    print()
    print("Start timestamp Pulled:",time_start, "| End Timestamp Pulled:",\
          time_end)

    finder = ['5T', '30S','S','.1S']
    for n in range(len(finder)):
        test_start=list(pd.date_range(start=time_start, end=time_end,\
                                      freq = finder[n]))
        test_end = test_start[::-1]
        time=[]
        for t in range(len(test_start)): 
            for df in range(len(df_names)):
                if test_start[t] not in list(df_names[df]["TIMESTAMP"]):
                    break
                else:
                    time.append(test_start[t])
                    break
            if len(time)==1:
                if t ==0 or n == len(finder)-1:
                    time_start = test_start[t]
                else:
                    time_start = test_start[t-1]
                break


        time=[]
        for t in range(len(test_end)):
            for df in range(len(df_names)):
                if test_end[t] not in list(df_names[df]["TIMESTAMP"]):
                    break
                else:
                    time.append(test_end[t])
                    break
            if len(time)==1:
                if t ==0 or n == len(finder)-1:
                    time_end = test_end[t]
                else:
                    time_end = test_end[t-1]
                break
    print()
    print("Timestamp that can actually be used to trim due to gaps:")
    print("Start Time:", str(time_start), "| End Time:", str(time_end))
    
    return time_start, time_end

def cutter(df, time_start, time_end):
    """
    This function takes in a dataframe, start time, and endtime and uses it to 
    cut the dataframe 
    
    input: 
        df - dataframe with a "TIMESTAMP" index
        time_start - the time desired for the df to start 
                     (from time_stamp_matcher)
        time_end - the time desired for the df to end (from time_stamp_matcher)
    output:
        df- the trimmed dataframe with input time start/end
    """
    s_index = df.index[df["TIMESTAMP"]==time_start].tolist()[-1]
    e_index = df.index[df["TIMESTAMP"]==time_end].tolist()[0]
    
    df = df.truncate(before=s_index, after= e_index)
    df=df.reset_index(drop = True)
    
    return df

def day_trimmer(df, t_s, t_e):
    mask =(df['TIMESTAMP'] >= t_s) & (df['TIMESTAMP'] <= t_e) 
    df=df.loc[mask]
    df=df.reset_index(drop = True)
    return(df)

def repeat(df):
    
    """
    This function takes a df with a "TIMESTAMP" column and checks for 
    repeated timestamps. If it finds repeats, it will return the index of all the 
    repeated times and print out how many and what times it spans. If it 
    doesn't find one it will return an index of zero's 
    
    input:
        df - pandas dataframe to be checked
        
    output:
        repeat_index - A list of the index's that have repeated times in this
                       format: [[],[]] 
    """
    #### Check for repeated times
    lst=list(df["TIMESTAMP"])
    u= np.unique(lst)
    if len(u)!=len(df):
        
        repeat_index, repeat_1, repeat_2 = [], [], []
        for i in range(len(u)):
            ind = df.index[df["TIMESTAMP"]==u[i]].tolist()
            if len(ind)>1:
                repeat_index.append(ind)
                repeat_1.append(df["TIMESTAMP"][ind[0]])
                repeat_2.append(df["TIMESTAMP"][ind[-1]])
        if len(repeat_index)>0:
            print("Yikes! Number of repeated times: ",len(repeat_index),)
            print("Start:", repeat_index[0],"End:",repeat_index[-1])
            print("Time stamp repeats:",repeat_1[0],"-", repeat_2[-1])
                
            return repeat_index
    else:
        print("Hurray! No time Repeats")
        
        return [[0],[0]]
        
def time_columns(df):
    """
    This function takes a df with a "TIMESTAMP" index/column and separates 
    the date and time atributes into different columns and creates a new df 
    with just the time columns separated
    
    input:
        df - pandas dataframe with "TIMESTAMP" index
        
    output:
        df_time - pandas dataframe with just the timestamp columns
    """
    #Created nan lists to append to quickly 
    fill_nan = np.nan
    year_lst  = list(np.full(len(df),fill_nan))
    month_lst = list(np.full(len(df),fill_nan))
    day_lst   = list(np.full(len(df),fill_nan))
    hour_lst  = list(np.full(len(df),fill_nan))
    min_lst   = list(np.full(len(df),fill_nan))
    second_lst= list(np.full(len(df),fill_nan))

    ### Parcing the timestamps and seperating them 
    time_stmp_lst = list(df["TIMESTAMP"].astype(str))
    for i in range(len(df)):
        time_step    = time_stmp_lst[i].replace("-", ",").replace(":",",").replace(" ",",").replace("/",',').split(",")
        year_lst[i]  = "{:.0f}".format(float(time_step[0])).zfill(4)
        month_lst[i] = "{:.0f}".format(float(time_step[1])).zfill(2)
        day_lst[i]   = "{:.0f}".format(float(time_step[2])).zfill(2)
        hour_lst[i]  = "{:.0f}".format(float(time_step[3])).zfill(2)
        min_lst[i]   = "{:.0f}".format(float(time_step[4])).zfill(2)
        second_lst[i]= "{:.1f}".format(float(time_step[5])).zfill(4)
    
    # add the lists to the DataFrame
    df_time = pd.DataFrame()
    df_time["YYYY"] = year_lst
    df_time["MM"]   = month_lst
    df_time["DD"]   = day_lst
    df_time["Hr"] = hour_lst
    df_time["Min"]  = min_lst
    df_time["Sec"]  = second_lst
    
    return df_time  

def timestamp_correction(df):
    """
    This function takes a df with a messed up timestamp column and creates one 
    with full timestamps 
    input:
        df - the pandas dataframe that has the messed up timestamp columns
        
    output:
        df -  the dataframe with the fixed timestamp column
    """
    
    time=list(df["TIMESTAMP"])
    ### initialize the t_d
    for i in range(len(time)):
        if len(time[i]) > 8:
            t_d= time[i].replace(":"," ").split()[:2]
            break
            
    for i in range(len(time)):

        if len(time[i]) > 8:
            t_d= time[i].replace(":"," ").split()[:2]

        if i !=len(df)-1 and len(time[i])>8:
            t_s = time[i+1].split(".")[0]+".0"

            time[i] = t_d[0] +" "+t_d[1]+":"+t_s 

        else:
            time[i]= t_d[0] +" "+ t_d[1]+":"+time[i]

    df["TIMESTAMP"]=time
    df.drop(df.tail(1).index,inplace=True)
    df["TIMESTAMP"] = pd.to_datetime(df['TIMESTAMP']) 
    
    return df

def formater(df,columns):
    """
    This function takes a dataframe with timestamp columns and data columns and 
    formats them so that each column looks like this: ##.## or -#.##
        
    input:
        df - pandas dataframe with the separated time columns and data columns
        columns - the columns that are not the time columns but are desired to 
                  be formated
    output:
        df - the formated dataframe 
    """
    
    for col in columns:
        lst_df=list(df[str(col)])
        for i in range(len(lst_df)):
            lst_df[i] = "{:2.2f}".format(float(lst_df[i])).zfill(5)
        df[col]= lst_df
        
    year_lst, month_lst,day_lst= list(df["YYYY"]), list(df["MM"]), list(df["DD"])
    hour_lst, min_lst, second_lst = list(df["Hr"]), list(df["Min"]), list(df["Sec"])
    for i in range(len(df)):
        year_lst[i]  = "{:.0f}".format(float(year_lst[i])).zfill(4)
        month_lst[i] = "{:.0f}".format(float(month_lst[i])).zfill(2)
        day_lst[i]   = "{:.0f}".format(float(day_lst[i])).zfill(2)
        hour_lst[i]  = "{:.0f}".format(float(hour_lst[i])).zfill(2)
        min_lst[i]   = "{:.0f}".format(float(min_lst[i])).zfill(2)
        second_lst[i]= "{:.1f}".format(float(second_lst[i])).zfill(4)
    
    df["YYYY"] = year_lst
    df["MM"]   = month_lst
    df["DD"]   = day_lst
    df["Hr"] = hour_lst
    df["Min"]  = min_lst
    df["Sec"]  = second_lst
    
    return df


def continuous_df(df_raw, t_s, t_e, frequency = ".1S"):
    """
    This function takes a df and make sure that the timestamps are continous,
    If not it creates one that is, with NaN values is missing timestamps.
    
    Inputs:
        df_raw - the df with timestamestamps trimed 
        t_s - time that the df should start
        t_e - time that the df should end
        frequency - the frequency of the timestamps, def is 10Hz 
    
    Outputs:
        df/df_raw - the edited/non-edited continuous dataframe
    """
    
    t=list(pd.date_range(t_s, t_e, freq=frequency)) #timestamps wanted
    if len(t)==len(df_raw):
        print("There Were 0 Missing Timestamps")
        
        return(df_raw)
    
    if len(t) != len(df_raw):
        col_order = list(df_raw.columns)
        df_raw = df_raw.set_index("TIMESTAMP") 


        df = pd.DataFrame(columns = list(df_raw.columns), index = t) #create NaN df
        df.update(df_raw) # Add the data onto NaN df


        df=df.reset_index(drop=True)
        df['TIMESTAMP']= t
        df = df[col_order]
        ### Show what was accomplished
        gaps = 0 
        for j in range(len(df)):
            if np.isnan(df["RECORD"][j]):
                gaps+=1
        print("There Were",gaps,"Missing Timestamps")

        return df

def scalar_wind_tilt_correction(u_i, v_i, theta = 135):
    """
    This function takes U and V wind components and will correct by a 
    specified amount. Default is 135 due to SERDP Flux tower.
    
    Inputs:
        u_i - the U wind component 
        v_i - the V wind component 
        theta - angle of desired correction in degrees (default 135 due to the
                                                        march 2019 flux tower)
    
    Outputs:
        u_f - corrected U  wind component
        v_f - corrected V  wind component
    """
    
    u_f = u_i * np.cos(theta*np.pi/180) - v_i * np.sin(theta*np.pi/180)
    v_f = u_i * np.sin(theta*np.pi/180) + v_i * np.cos(theta*np.pi/180)
    
    return u_f, v_f
    
def df_wind_tilt_correction(df, theta = 135, U_col = "U(19m)", V_col = "V(19m)"):
    """
    This function combined with the 'scalar_wind_tilt_correction' function will
    correct a data frame with U or V columns and apply the angle of correction.
    
    Inputs:
        df - pandas dataframe containing the U and V columns
        theta - angle of desired correction in degrees (default 
                +135 for  SERDP March 2019 Flux tower)
        U_col - the column name containing the U wind components ( default 
                "U(19)" for  SERDP March 2019 Flux tower)
        V_col - the column name containing the V wind components ( default 
                "U(19)" for  SERDP March 2019 Flux tower)
    
    Outputs:
        df - The pandas dataframe with the corrected wind columns
    """
    u_list, v_list = np.full(len(df), np.nan), np.full(len(df), np.nan)
    for i in range(len(df)):
        u_list[i], v_list[i] = scalar_wind_tilt_correction(float(df[U_col][i]),\
                                                float(df[V_col][i]),theta)
             
    df[U_col], df[V_col] = list(u_list), list(v_list)

    return df