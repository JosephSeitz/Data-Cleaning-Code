#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:06:33 2019

@author: joey
"""
import pandas as pd
import os
import numpy as np
from Raw_Cleaner import timestamp_matcher, time_columns, file_to_df, \
    repeat, continuous_df, day_trimmer

Burn = int(input("What Burn would you like to clean? (20-34):"))
    
def pick_burn(burn):
    
    path_20_22 = "/Users/joeyp/Desktop/10X10_Truss_SERDP_Burns/"\
                    "Raw-Sonic-TC-Data/SERDP-Burns-20-to-22/"
    #path_20_22 = "/home/joey/Desktop/10X10_Truss_SERDP_Burns/"\
    #               "Raw-Sonic-TC-Data/SERDP-Burns-20-to-22/" #79
    
    path_23_26 = "/Users/joeyp/Desktop/10X10_Truss_SERDP_Burns/"\
                    "Raw-Sonic-TC-Data/SERDP-Burns-23-to-26/"
    #path_23_26 = "/home/joey/Desktop/10X10_Truss_SERDP_Burns/"\
    #                "Raw-Sonic-TC-Data/SERDP-Burns-23-to-26/" #79
    
    path_27_30 = "/Users/joeyp/Desktop/10X10_Truss_SERDP_Burns/"\
                    "Raw-Sonic-TC-Data/SERDP-Burns-27-to-30/" 
    #path_27_30 = "/home/joey/Desktop/10X10_Truss_SERDP_Burns/"\
    #                "Raw-Sonic-TC-Data/SERDP-Burns-27-to-30/"  #79
    
    path_31_33 = "/Users/joeyp/Desktop/10X10_Truss_SERDP_Burns/"\
                    "Raw-Sonic-TC-Data/SERDP-Burns-31-to-33/"  #79
    #path_31_33 = "/home/joey/Desktop/10X10_Truss_SERDP_Burns/"\
    #                "Raw-Sonic-TC-Data/SERDP-Burns-31-to-33/"  #79
    
    path_34_35 = "/Users/joeyp/Desktop/10X10_Truss_SERDP_Burns/"\
                    "Raw-Sonic-TC-Data/SERDP-Burns-34-to-35/"  #79
    #path_34_35 = "/home/joey/Desktop/10X10_Truss_SERDP_Burns/"\
    #                "Raw-Sonic-TC-Data/SERDP-Burns-34-to-35/"  #79
    
    
    # Setting the cut times for each burn
    if Burn == 20:
        t_s, t_e = "2019-05-20 13:24:07.5", "2019-05-20 15:09:07.5"
        path = path_20_22
    if Burn == 21:
        t_s, t_e = "2019-05-20 15:24:07.5", "2019-05-20 17:06:37.4"
        path = path_20_22
    if Burn == 22: 
        t_s, t_e = "2019-05-20 17:06:37.5", "2019-05-20 18:15:28.5"
        path = path_20_22
        
    if Burn == 23:
        path = path_23_26
        t_s, t_e = "2019-05-21 10:47:11.9", "2019-05-21 13:08:51.9"
    if Burn == 24:
        path = path_23_26
        t_s, t_e = "2019-05-21 13:28:51.9", "2019-05-21 15:02:11.9"
    if Burn == 25:
        path = path_23_26
        t_s, t_e = "2019-05-21 15:02:12.0", "2019-05-21 16:38:51.9"
    if Burn == 26:
        path = path_23_26
        t_s, t_e = "2019-05-21 16:38:52.0", "2019-05-21 17:42:11.9"
    
    if Burn == 27:
        path = path_27_30
        t_s, t_e = "2019-05-22 09:34:50.6", "2019-05-22 11:34:22.1"
    if Burn == 28:
        path = path_27_30
        t_s, t_e = "2019-05-22 11:40:20.0", "2019-05-22 13:30:20.0"
    if Burn == 29:
        path = path_27_30
        t_s, t_e = "2019-05-22 13:30:20.1", "2019-05-22 14:55:20.0"
    if Burn ==30:
        path = path_27_30
        t_s, t_e = "2019-05-22 14:55:20.1", "2019-05-22 15:44:50.6"
        
    if Burn == 31:
        path = path_31_33
        t_s, t_e = "2019-05-29 10:00:00.0", "2019-05-29 12:10:00.0"
    if Burn == 32:
        path = path_31_33
        t_s, t_e = "2019-05-29 12:10:00.0", "2019-05-29 15:30:00.0"
    if Burn == 33:
        path = path_31_33
        t_s, t_e = "2019-05-29 15:30:00.1", "2019-05-29 16:36:33.9"
        
    if Burn == 34:
        path = path_34_35
        t_s, t_e = "2019-05-31 10:00:00.0", "2019-05-31 12:45:00.0"
        
    return path, t_s, t_e

def compiler(): 
    files = ["TOA5_4976.ts_data.dat", "TOA5_4975.ts_data.dat", \
             "TOA5_11585.ts_data.dat", "TOA5_2879.ts_data.dat", \
             "TOA5_4390.ts_data.dat", "TOA5_2005.ts_data.dat", \
             "TOA5_2878.ts_data.dat", "TOA5_11584.ts_data.dat",\
             "TOA5_10442.ts_data.dat"]

    file_names = ["4976", "4975","11585", "2879", "4390", "2005", "2878",\
                  "11584", "10442" ]

    path, t_s, t_e = pick_burn(Burn)
    
    
    # Loading in all the Data 
    df_4976  = day_trimmer(file_to_df(path, files[0]),t_s, t_e)
    df_4975  = day_trimmer(file_to_df(path, files[1]),t_s, t_e)
    df_11585 = day_trimmer(file_to_df(path, files[2]),t_s, t_e)
    
    df_2879  = day_trimmer(file_to_df(path, files[3]),t_s, t_e)
    df_4390  = day_trimmer(file_to_df(path, files[4]),t_s, t_e)
    df_2005  = day_trimmer(file_to_df(path, files[5]),t_s, t_e)
    
    df_2878  = day_trimmer(file_to_df(path, files[6]),t_s, t_e)
    df_11584 = day_trimmer(file_to_df(path, files[7]),t_s, t_e)
    df_10442 = day_trimmer(file_to_df(path, files[8]),t_s, t_e)
    
    df_lst = [df_4976, df_4976, df_11585, df_2879, df_4390, df_2005,\
              df_2878, df_11584, df_10442]
    
    ### Matching the timestamps 
    t_s,t_e = timestamp_matcher(df_lst,file_names)
    df_4976  = day_trimmer(df_4976, t_s, t_e)
    df_4975  = day_trimmer(df_4975, t_s, t_e)
    df_11585 = day_trimmer(df_11585, t_s, t_e)
    df_2879  = day_trimmer(df_2879, t_s, t_e)
    df_4390  = day_trimmer(df_4390, t_s, t_e)
    df_2005  = day_trimmer(df_2005, t_s, t_e)
    df_2878  = day_trimmer(df_2878, t_s, t_e)
    df_11584 = day_trimmer(df_11584, t_s, t_e)
    df_10442 = day_trimmer(df_10442, t_s, t_e)
    
    df_lst = [df_4976, df_4976, df_11585, df_2879, df_4390, df_2005,\
              df_2878, df_11584, df_10442]
    
    check = input("Would you like to check for repeated timestamps? Note: if"\
              " there are repeats, it could take a while (y/n):")
    if check == "y":
        end_repeat_times = []
        for i in range(len(df_lst)):
            print(file_names[i]+':')
            end_repeat_times.append(df_lst[i]["TIMESTAMP"][repeat(df_lst[i])[-1][-1]+1])
        print(max(end_repeat_times))
        if max(end_repeat_times) != t_s:
            
            
            cut_out_check = input("Would you like to cut all data at the end "\
                                  " of repeated times? (y/n):")
            print("Cut here:",max(end_repeat_times))
            t_s = max(end_repeat_times)
            
            if cut_out_check == "y":
                df_4976  = day_trimmer(df_4976, t_s, t_e)
                df_4975  = day_trimmer(df_4975, t_s, t_e)
                df_11585 = day_trimmer(df_11585, t_s, t_e)
                df_2879  = day_trimmer(df_2879, t_s, t_e)
                df_4390  = day_trimmer(df_4390, t_s, t_e)
                df_2005  = day_trimmer(df_2005, t_s, t_e)
                df_2878  = day_trimmer(df_2878, t_s, t_e)
                df_11584 = day_trimmer(df_11584, t_s, t_e)
                df_10442 = day_trimmer(df_10442, t_s, t_e)
                
                df_lst = [df_4976, df_4976, df_11585, df_2879, df_4390, df_2005, \
                          df_2878, df_11584, df_10442]
            
    print("Making sure the file has continous timestamps")
    print(file_names[0],":")
    df_4976  = continuous_df(df_4976, t_s, t_e)
    print(file_names[1],":")
    df_4975  = continuous_df(df_4975, t_s, t_e)
    print(file_names[2],":")
    df_11585 = continuous_df(df_11585, t_s, t_e)
    print(file_names[3],":")
    df_2879  = continuous_df(df_2879, t_s, t_e)
    print(file_names[4],":")
    df_4390  = continuous_df(df_4390, t_s, t_e)
    print(file_names[5],":")
    df_2005  = continuous_df(df_2005, t_s, t_e)
    print(file_names[6],":")
    df_2878  = continuous_df(df_2878, t_s, t_e)
    print(file_names[7],":")
    df_11584 = continuous_df(df_11584, t_s, t_e)
    print(file_names[8],":")
    df_10442 = continuous_df(df_10442, t_s, t_e)
    
    ### Grabbing Sonic data from specific files
    sonic_columns=["Ux_","Uy_","Uz_","Ts_","diag_rmy_"]
    time_columns_lst=["YYYY","MM","DD","Hr","Min","Sec"]
    sonc_headers = ["U", "V", "W", "T" ,"DIAG"]
    
    df_A1, df_A2, df_A3 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df_A4, df_B1, df_B2 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df_B3, df_B4, df_C1 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame() 
    df_C2, df_C3, df_C4 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    df_D1, df_D2, df_D3 = pd.DataFrame(), pd.DataFrame(), pd.DataFrame() 
    df_D4 = pd.DataFrame()
    
    a_row_lst = [df_A1, df_A2, df_A3, df_A4]
    b_row_lst = [df_B1, df_B2, df_B3, df_B4]
    c_row_lst = [df_C1, df_C2, df_C3, df_C4]
    d_row_lst = [df_D1, df_D2, df_D3, df_D4 ]
    
    all_sonics = a_row_lst+ b_row_lst + c_row_lst +d_row_lst
    
    ###  Burns truss:
    df_4976_time, df_4975_time  = time_columns(df_4976), time_columns(df_4975)
    df_11585_time, df_2879_time = time_columns(df_11585), time_columns(df_2879)
    df_4390_time, df_2005_time = time_columns(df_4390), time_columns(df_2005)
    df_2878_time, df_11584_time = time_columns(df_2878), time_columns(df_11584)
    ### WG Nover 10hz
    df_10442_time = time_columns(df_10442)
    df_WGNover = pd.DataFrame()
    
    for col in range(len(sonic_columns)):
        df_WGNover[sonc_headers[col]] = df_10442[sonic_columns[col]+"1"]
    for t in time_columns_lst:
        df_WGNover[t] = df_10442_time[t]
    
        
    for n in range(len(a_row_lst)):
        
        for i in range(len(sonic_columns)):
            a_row_lst[n][sonc_headers[i]] = df_4976[sonic_columns[i]+str(n+1)]
            b_row_lst[n][sonc_headers[i]] = df_4975[sonic_columns[i]+str(n+1)]
            c_row_lst[n][sonc_headers[i]] = df_11585[sonic_columns[i]+str(n+1)]
            d_row_lst[n][sonc_headers[i]] = df_2879[sonic_columns[i]+str(n+1)]
        
        for i in range(len(time_columns_lst)):
            a_row_lst[n][time_columns_lst[i]]=df_4976_time[time_columns_lst[i]]
            b_row_lst[n][time_columns_lst[i]]=df_4975_time[time_columns_lst[i]]
            c_row_lst[n][time_columns_lst[i]]=df_11585_time[time_columns_lst[i]]
            d_row_lst[n][time_columns_lst[i]]=df_2879_time[time_columns_lst[i]]
    
    #### Thermal Couple data
    time_columns_lst=["YYYY","MM","DD","Hr","Min","Sec"]
    
    df_B1_tc, df_B2_tc = pd.DataFrame(), pd.DataFrame()
    df_B3_tc, df_B4_tc = pd.DataFrame(), pd.DataFrame()
    df_B5_tc, df_B6_tc = pd.DataFrame(), pd.DataFrame()
    df_B7_tc, df_C1_tc = pd.DataFrame(), pd.DataFrame()
    df_C2_tc, df_C3_tc = pd.DataFrame(), pd.DataFrame()
    df_C4_tc, df_C5_tc = pd.DataFrame(), pd.DataFrame()
    df_C6_tc, df_C7_tc = pd.DataFrame(), pd.DataFrame()
    
    t_c_lst_1 = ["Temp_C(1)", "Temp_C(2)", "Temp_C(3)", "Temp_C(4)", \
                 "Temp_C(5)", "Temp_C(6)", "Temp_C(7)"]
    t_c_lst_2 = ["Temp_C(8)", "Temp_C(9)", "Temp_C(10)", "Temp_C(11)", \
                 "Temp_C(12)", "Temp_C(13)", "Temp_C(14)"]
    
    first_tc_group = [ df_B5_tc, df_B7_tc, df_B1_tc, df_B3_tc,\
                       df_C5_tc, df_C7_tc, df_C1_tc, df_C3_tc]
    
    secnd_tc_group = [ df_B6_tc, df_B2_tc, df_B4_tc,\
                      df_C6_tc, df_C2_tc, df_C4_tc]
    
    df_tc_lst_1 = [df_4976, df_4390, df_4975, df_2005, df_11585, df_2878,\
                df_2879, df_11584]
    
    df_time_lst_1 =[df_4976_time, df_4390_time, df_4975_time, df_2005_time,\
                    df_11585_time, df_2878_time, df_2879_time, df_11584_time]
    
    for j in range(len(first_tc_group)):
        for i in range(len(t_c_lst_1)):
            first_tc_group[j][t_c_lst_1[i]]= df_tc_lst_1[j][t_c_lst_1[i]]
    
        for t in range(len(time_columns_lst)):
            first_tc_group[j][time_columns_lst[t]]= df_time_lst_1[j][time_columns_lst[t]]
    
    df_tc_lst_2 = [df_4976, df_4975, df_2005, df_11585, df_2879, df_11584]
    
    df_time_lst_2 = [df_4976_time, df_4975_time, df_2005_time, df_11585_time,\
                   df_2879_time, df_11584_time]
    
    for j in range(len(secnd_tc_group)):
        for i in range(len(t_c_lst_2)):
            secnd_tc_group[j][t_c_lst_2[i]]= df_tc_lst_2[j][t_c_lst_2[i]]
    
        for t in range(len(time_columns_lst)):
            secnd_tc_group[j][time_columns_lst[t]]= df_time_lst_2[j][time_columns_lst[t]]
    
    all_tc_group = [df_B1_tc, df_B2_tc, df_B3_tc, df_B4_tc, df_B5_tc,\
                    df_B6_tc, df_B7_tc,df_C1_tc, df_C2_tc, df_C3_tc, df_C4_tc,\
                    df_C5_tc, df_C6_tc, df_C7_tc]
    
    return all_sonics, all_tc_group, df_WGNover
    
def correction():
    all_sonics, all_tc_group, df_WGNover = compiler()
    nam_snc=["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1","C2",\
                   "C3","C4","D1","D2","D3","D4"]
    nam_tc = ["B1", "B2", "B3", "B4", "B5", "B6", "B7","C1","C2","C3","C4", \
              "C5", "C6", "C7"]
    #wind speed correction
    m_speed,min_T = 40, -10
    u_fctr, v_fctr = -1, -1
    
    fmt = "Default Corrections: {}*U, {}*V, Max Wind Speed=|{}| m/s, Min "\
            "Temperature = {} C  " 
    print(fmt.format(u_fctr,v_fctr,m_speed,min_T))
    
    nw_corct = input("Would you like to change these corrections? (y/n): ")
    if nw_corct.lower() == "y":
        u_fctr = float(input("What to multiply the U values by?:"))
        v_fctr = float(input("What to multiply the V values by?:"))
        m_speed = float(input("What bounds do you want for the wind speed? "\
                              "(m/s):"))
        min_T = float(input("What is the minimum temperatue? (C):"))
    
    fill_nan = np.nan
    change_nan = input("Would you like to change the NaN's to a different "\
                       "value? (y/n):")
    if change_nan == "y":
        fill_nan = input("What to replace NaN's with? ex: 9999:")
    
    for df in range(len(all_sonics)):
        print("Sonic",nam_snc[df],":")
        all_sonics[df] = apply_correction(all_sonics[df] ,u_fctr, v_fctr, \
                        m_speed, min_T, fill_nan)
    df_WGNover = apply_correction(df_WGNover, u_fctr, v_fctr, m_speed, \
                                  min_T, fill_nan)
    
    for df in range(len(all_tc_group)):
        print("Thermocouple ",nam_tc[df],":")
        all_tc_group[df] = apply_tc_correction(all_tc_group[df], min_T, \
                    fill_nan, list(all_tc_group[df].columns)[:7])
        
    return all_sonics, all_tc_group, df_WGNover

def apply_correction(df,u_fctr,v_fctr,m_speed,min_T,fill_nan):

    ##For loop for all the sonics
    df["U"] *= u_fctr
    df["V"] *= v_fctr
    
    indx = []
    for i in range(len(df)):
        if df["DIAG"][i] != 0.0:
            df.at[i,["U","V","W","T"]] = fill_nan
            indx.append(i)
            indx.append(i)
            indx.append(i)
            indx.append(i)
            continue
        
        if np.abs(df["U"][i]) > m_speed:
            df.at[i, "U"] = fill_nan
            #df["U"][i] =fill_nan
            indx.append(i)
            
        if  np.abs(df["V"][i])> m_speed:
            df.at[i, "V"] = fill_nan
            #df["V"][i] =fill_nan
            indx.append(i)
            
        if np.abs(df['W'][i])> m_speed:
            df.at[i, "W"] = fill_nan
            #df['W'][i] = fill_nan
            indx.append(i)
            
        if df['T'][i] < min_T:
            df.at[i, "T"] = fill_nan
            #df['T'][i] = fill_nan
            indx.append(i)
    
    if len(indx) ==0:
        print("Data fits these limits")
    if len(indx) != 0:
        print("Removed "+str(len(indx))+" Values" )
    
    df.fillna(value=fill_nan, inplace=True)
    df = df.drop(["DIAG"], axis = 1)
    
    return df
    
def apply_tc_correction(df, min_T, fill_nan, tc_columns):
    indx = []
    for i in range(len(df)):    
        for col in range(len(tc_columns)):
            if df[tc_columns[col]][i] < min_T:
                df.at[i, tc_columns[col]] = fill_nan
                #df[tc_columns[col]][i] = fill_nan
                indx.append(i)
            #print("--"*15,"LINE:",i,"--"*15)
            #print(df.iloc[[i]])
            
    if len(indx) ==0:
        print("Data fits these limits")
    if len(indx) != 0:
        print("Removed "+str(len(indx))+" Values" )
    
    df.fillna(value=fill_nan, inplace=True)
    
    return df
    
def timestamp_col(df):
    drop_col = ["YYYY", "MM", "DD", "Hr", "Min", "Sec"]
    timestamp_lst = list(np.full(len(df), np.nan))
    for t in range(len(df)):
        timestamp_lst[t] = pd.Timestamp(str(df["YYYY"][t])+"-"+str(df["MM"][t])+"-"+str(df["DD"][t]) +" "+str(df["Hr"][t])+":"+str(df["Min"][t])+":"+str(df["Sec"][t]),freq = ".1S")
    
    df.insert(0, column= "TIMESTAMP", value = timestamp_lst)
    df = df.drop(drop_col, axis=1)
    
    return df

def saver():
    
    all_sonics, all_tc_group, df_WGNover = correction()
      
    #TS = input("Would you like to have a single time stamp column? (y/n):")
    TS = "y" 
    if TS== "y":
        for i in range(len(all_sonics)):
            all_sonics[i] = timestamp_col(all_sonics[i])
        for i in range(len(all_tc_group)):
            all_tc_group[i] = timestamp_col(all_tc_group[i])
        df_WGNover = timestamp_col(df_WGNover)
    
    ### Creating the directories to save the data
    save_me = input("Would you like to save the data into the working "\
                    "directory? (y/n):")
    if save_me == "y":
        cwd = os.getcwd()
    else:
        cwd = input("Full path of save directory:")
        
    save_dir = "Burn-"+str(Burn)
    os.mkdir(cwd+"/" + save_dir)
    
    tc_dir =cwd+"/" + save_dir + "/thermal_couples"
    sonic_dir =cwd+"/" + save_dir + "/sonics"
    
    os.mkdir(tc_dir)
    os.mkdir(sonic_dir)

    ### Save the Sonic data
    save_as_lst = ["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1","C2",\
                   "C3","C4","D1","D2","D3","D4"]
    for i in range(len(all_sonics)):
        sv_file = sonic_dir+'/'+save_as_lst[i]+"_UVWT_Burn-"+str(Burn)+".txt"
        all_sonics[i].to_csv(sv_file, sep=' ',index=False)
    df_WGNover.to_csv(sonic_dir+'/WGNover_UVWT_Burn-'+str(Burn)+".txt", \
                      sep=' ',index=False)

    ### Saving Thermal Couple dataframes
    
    save_as_lst = ["B1", "B2", "B3", "B4", "B5", "B6", "B7","C1","C2","C3", \
                      "C4", "C5", "C6", "C7"]
    for i in range(len(all_tc_group)):
        all_tc_group[i] = all_tc_group[i].round(3)
        sv_file=tc_dir+'/'+save_as_lst[i]+"_thermal_couple_Burn-"+\
                        str(Burn)+".txt"
        all_tc_group[i].to_csv(sv_file, sep=' ',index=False)
    print("You now have the Burn sonics and thermocouple saved")

saver()
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    