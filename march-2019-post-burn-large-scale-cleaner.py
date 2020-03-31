
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:49:18 2020

@author: joeyp
"""

import pandas as pd
import os
import numpy as np
from Raw_Cleaner import timestamp_matcher, time_columns, file_to_df, cutter, \
    repeat, timestamp_correction, day_trimmer, df_wind_tilt_correction
    
### W10 location
path = "C:/Users/joeyp/Desktop/2019-SERDP-Raw/" \
        "Large-scale-burn-experiment-March-13-2019/" \
        "Overstory-towers-post-burn-1/"
### 79 location
#path = '/home/joey/Desktop/2019-SERDP-Raw/SERDP_SLEF_Burn_data/' +\
#            'Large-scale-burn-experiment-March-13-2019/' + \
#            'Overstory-towers-post-burn-1/'

## 134 Location
#path = '/home/JoeySeitz/2019-SERDP-Raw/SERDP_SLEF_Burn_data/'+ \
#            "Large-scale-burn-experiment-March-13-2019/"+\
#            'Overstory-towers-post-burn-1/'

def file_finder(path,f_type = ".csv" ):
    txt_files=[]
    all_files = os.listdir(path) #tells what directory the files are in
    for i in all_files: #reading only the .txt files 
        if i[-4:] == f_type:
            txt_files.append(i)
    txt_files.sort() #alphabetizes them
    return txt_files

def Compiler():
    tower_names=['Control', 'East', 'Flux', 'North', 'West']
    
    burn_files = file_finder(path)
    df_Control = timestamp_correction(file_to_df(path,burn_files[0],6,3,False))
    df_East    = timestamp_correction(file_to_df(path,burn_files[1],6,3,False))
    df_Flux    = df_wind_tilt_correction ( timestamp_correction(file_to_df(path,\
                                        burn_files[2],6,3,False)))
    
    df_North   = timestamp_correction(file_to_df(path,burn_files[5],6,3,False))
    df_West    = timestamp_correction(file_to_df(path,burn_files[6],6,3,False))
    
    df_names = [df_Control, df_East, df_Flux, df_North, df_West]
    
    df_Mobile_3= timestamp_correction(file_to_df(path,burn_files[3],6,3,False))
    df_Mobile_2=timestamp_correction(file_to_df(path,burn_files[4],6,3,False))
    
    df_Mobile = pd.concat([df_Mobile_2, df_Mobile_3], axis = 0,\
                      sort = False,ignore_index=True)
        
    raw_column_m = ['TIMESTAMP', 'RECORD', 'Ux_1', 'Uy_1', 'Uz_1', 'Ts_1', \
                    'diag_rmy_1','Ux_2', 'Uy_2', 'Uz_2', 'Ts_2','diag_rmy_2', \
                    'Ux_3', 'Uy_3','Uz_3','Ts_3','diag_rmy_3','Temp_C(0.25 m)',\
                    'Temp_C(0.5 m)', 'Temp_C(1.0 m)', 'Temp_C(2.0 m)', \
                    'Temp_C(3.0 m)', 'Temp_C(4.0 m)', 'Temp_C(5.0 m)', \
                    'Temp_C(6.0 m)', 'Temp_C(7.0 m)', 'Temp_C(8.0 m)', \
                    'Temp_C(9.0 m)', 'Temp_C(10.0 m)']
    
    df_Mobile =df_Mobile.drop("Temp_C(0.0 m)", axis= 1)
    df_Mobile.columns = raw_column_m
    
    time_columns_lst=["YYYY","MM","DD","Hr","Min","Sec"]
   
    
    out_tc = ["TC(15m)", "TC(10m)", "TC(5m)", "TC(2.5m)", "TC(1.25m)",\
              "TC(0.5m)", "TC(0.25m)"]
    out_mobile_tc =['TC(10.0m)', 'TC(9.0m)', 'TC(8.0m)', 'TC(7.0m)', 'TC(6.0m)',\
            'TC(5.0m)', 'TC(4.0m)', 'TC(3.0m)', 'TC(2.0m)', 'TC(1.0m)', 'TC(0.5m)','TC(0.25m)']
    
    sonic_heights = ["(19m)", "(9.5m)", "(3m)"]
    sonic_headers = ["U", "V", "W", "T", "DIAG" ]
    mobile_heights =["(21.6m)", "(9.1m)", "(3.4m)"]
    
    out_sonic, out_sonic_mobile = [], []
    for i in range(len(sonic_heights)):
        for j in range(len(sonic_headers)):
            out_sonic.append(sonic_headers[j]+sonic_heights[i])
            out_sonic_mobile.append(sonic_headers[j]+mobile_heights[i])
    out_columns=out_sonic+out_tc
    out_columns_mobile = out_sonic_mobile + out_mobile_tc
    raw_data_col = ['Ux_1', 'Uy_1', 'Uz_1', 'Ts_1', 'diag_rmy_1', 'Ux_2', 'Uy_2', \
                'Uz_2', 'Ts_2', 'diag_rmy_2', 'Ux_3', 'Uy_3', 'Uz_3', 'Ts_3', \
                'diag_rmy_3', 'Temp_C(1)', 'Temp_C(2)', 'Temp_C(3)', 'Temp_C(4)', \
                'Temp_C(5)', 'Temp_C(6)','Temp_C(7)']
    
    raw_data_col_m = [ 'Ux_1', 'Uy_1', 'Uz_1', 'Ts_1', \
                    'diag_rmy_1','Ux_2', 'Uy_2', 'Uz_2', 'Ts_2','diag_rmy_2', \
                    'Ux_3', 'Uy_3', 'Uz_3','Ts_3', 'diag_rmy_3', \
                    'Temp_C(10.0 m)', 'Temp_C(9.0 m)', 'Temp_C(8.0 m)', \
                    'Temp_C(7.0 m)', 'Temp_C(6.0 m)', 'Temp_C(5.0 m)', \
                    'Temp_C(4.0 m)', 'Temp_C(3.0 m)', 'Temp_C(2.0 m)', \
                    'Temp_C(1.0 m)', 'Temp_C(0.5 m)', "Temp_C(0.25 m)"]
    
    df_Control_out, df_East_out = pd.DataFrame(), pd.DataFrame()
    df_Mobile_out, df_Flux_out  = pd.DataFrame(), pd.DataFrame()
    df_North_out, df_West_out   = pd.DataFrame(), pd.DataFrame()
    df_out_lst = [df_Control_out, df_East_out, df_Flux_out, \
                 df_North_out, df_West_out]
        
    
    for d in range(len(df_out_lst)):
        df_out_lst[d][time_columns_lst]=time_columns(df_names[d])[time_columns_lst]
        df_out_lst[d][out_columns] = df_names[d][raw_data_col]
    
    df_Mobile_out[time_columns_lst] = time_columns(df_Mobile)[time_columns_lst]
    df_Mobile_out[out_columns_mobile] = df_Mobile[raw_data_col_m]
    print(df_Mobile_out.columns)
    return df_out_lst, out_sonic, out_tc, df_Mobile_out, out_sonic_mobile, out_mobile_tc 

def correction():
    tower_names=['Control', 'East', 'Flux', 'North', 'West']
    df_out_lst, out_sonic, out_tc, df_Mobile_out, out_sonic_mobile, out_mobile_tc  = Compiler()
    #wind speed correction
    m_speed,min_T = 40, -10
    u_fctr, v_fctr = -1, -1

    fmt = "Default Corrections: {}*U, {}*V, Max Wind Speed=|{}| m/s, Min Temperature = {} C  " 
    print(fmt.format(u_fctr,v_fctr,m_speed,min_T))
    
    #nw_corct = input("Would you like to change these corrections? (y/n): ")
    nw_corct = "n"
    if nw_corct.lower() == "y":
        u_fctr = float(input("What to multiply the U values by?:"))
        v_fctr = float(input("What to multiply the V values by?:"))
        m_speed = float(input("What bounds do you want for the wind speed? (m/s):"))
        min_T = float(input("What is the minimum temperatue? (C):"))
    
    fill_nan = np.nan
    #change_nan = input("Would you like to change the NaN's to a different value? (y/n):")
    #change_nan = "n"
    #if change_nan == "y":
    #    fill_nan = input("What to replace NaN's with? ex: 9999:")
    for df in range(len(df_out_lst)):
        print("Tower",tower_names[df],":")
        df_out_lst[df] = apply_correction(df_out_lst[df], u_fctr, v_fctr, \
                  m_speed, min_T, fill_nan, out_tc, out_sonic)
    print("Tower Mobile :")
    df_Mobile_out = apply_correction(df_Mobile_out, u_fctr, v_fctr, m_speed, \
                            min_T, fill_nan, out_mobile_tc, out_sonic_mobile, \
                                     ['U(21.6m)','U(9.1m)', 'U(3.4m)'], \
                                     ['V(21.6m)','V(9.1m)', 'V(3.4m)'], \
                                     ["(21.6m)", "(9.1m)", "(3.4m)"], \
                                     ["DIAG(21.6m)", "DIAG(9.1m)", "DIAG(3.4m)"])
    df_out_lst.append(df_Mobile_out)
   
    return df_out_lst

def apply_correction(df,u_fctr,v_fctr,m_speed,min_T,fill_nan, out_tc, out_sonic, \
                     adjust_U = ['U(19m)', 'U(9.5m)', 'U(3m)'], \
                     adjust_V = ['V(19m)', 'V(9.5m)', 'V(3m)'], \
                     sonic_heights = ["(19m)", "(9.5m)", "(3m)"],
                     DIAG_lst = ["DIAG(19m)", "DIAG(9.5m)", "DIAG(3m)"]):
    fill_nan = np.nan
    ##For loop for all the sonics
    #adjust_U = ['U(19m)', 'U(9.5m)', 'U(3m)']
    #adjust_V = ['V(19m)', 'V(9.5m)', 'V(3m)']
    
    
    #adjust_temp = ['T_19m', 'T_9.5m', 'T_3m']
    for i in range(len(adjust_U)):
        df[adjust_U[i]] *= u_fctr
        df[adjust_V[i]] *= v_fctr
    
    
    #sonic_heights = ["(19m)", "(9.5m)", "(3m)"]
    indx = []
    for i in range(len(df)):
        for T in range(len(out_tc)):
            if float(df[out_tc[T]][i]) <min_T:
                indx.append(i)
        
        for h in range(len(sonic_heights)):
         if df["DIAG"+sonic_heights[h]][i] != 0.0:
            df.at[i,["U"+ str(sonic_heights[h]),"V"+ str(sonic_heights[h]), \
                     "W"+str(sonic_heights[h]),"T"+ \
                     str(sonic_heights[h])]] = fill_nan
                    
            indx.append(i)
            continue
        
        if np.abs(df["U"+ str(sonic_heights[h])][i]) > m_speed:
            df.at[i, "U"+ str(sonic_heights[h])] = fill_nan
            indx.append(i)
            
        if  np.abs(df["V"+ str(sonic_heights[h])][i])> m_speed:
            df.at[i, "V"+ str(sonic_heights[h])] = fill_nan
            indx.append(i)
            
        if np.abs(df['W'+ str(sonic_heights[h])][i])> m_speed:
            df.at[i, "W"+ str(sonic_heights[h])] = fill_nan
            indx.append(i)
            
        if df['T'+ str(sonic_heights[h])][i] < min_T:
            df.at[i, "T"+ str(sonic_heights[h])] = fill_nan
            indx.append(i)  

    if len(indx) ==0:
        print("Data fits these limits")   
    if len(indx) != 0:
        print("Removed "+str(len(indx))+" Values" )
    
    if adjust_U[0] == 'U(21.6m)':
        m_sonic = ['U(21.6m)', 'V(21.6m)', 'W(21.6m)', \
                    'T(21.6m)', 'U(9.1m)', 'V(9.1m)', 'W(9.1m)', 'T(9.1m)', \
                    'U(3.4m)', 'V(3.4m)', 'W(3.4m)', 'T(3.4m)']
        df = column_formater(df, out_tc, m_sonic)
    if adjust_U[0] != 'U(21.6m)':
        df = column_formater(df, out_tc)
    
    df.fillna(value=fill_nan, inplace=True)
    
    df = df.drop(DIAG_lst, axis=1)
    
    return df

def column_formater(df, out_tc, out_sonic = ['U(19m)', 'V(19m)', 'W(19m)', \
                    'T(19m)', 'U(9.5m)', 'V(9.5m)', 'W(9.5m)', 'T(9.5m)', \
                    'U(3m)', 'V(3m)', 'W(3m)', 'T(3m)']):
    #### need to format the data
    for col in range(len(out_sonic)):
        df[out_sonic[col]]=['{:0.2f}'.format(item).zfill(5) for item in list(df[out_sonic[col]].astype(float))]
    for tc in (range(len(out_tc))):
        df[out_tc[tc]]=['{:0.3f}'.format(item).zfill(6) for item in list(df[out_tc[tc]].astype(float))]
    return df

def Saver():
    
    tower_names=['Control', 'East', 'Flux', 'North', 'West', "Mobile"]
    df_out_lst = correction()
    
    save_me = input("Would you like to save the data into the working directory? (y/n):")
    if save_me == "y":
        cwd = os.getcwd()
    else:
        cwd = input("Full path of save directory:")
    
    save_dir  = cwd + "/March-2019-Large-Scale-Experiment-Cleaned-Data"
    
    if os.path.exists(save_dir) == False:
        os.mkdir(save_dir)
    
    for i in range(len(df_out_lst)):
        sv_file = save_dir+"/post-burn-"+tower_names[i].lower()+"_tower.txt"
        df_out_lst[i].to_csv(sv_file, sep=' ',index=False)
       
Saver()
    
    
    