
"""
Created on Mon Jul  1 14:26:13 2019

@author: Joey Seitz

This is a script that cleans burns 1-6 for the forestry department
"""
### Tools used for clean up
import pandas as pd
import os
import numpy as np
from Raw_Cleaner import timestamp_matcher, time_columns, file_to_df, cutter, \
    repeat, continuous_df

### Global
Burn = int(input("What Burn would you like to clean? (1-6):"))


if Burn == 1: 
    path = "http://35.12.130.8/study/2018-SERDP/02-raw-data/ALL-RAW/SERDP_SLEF_Burn_data/SERDP_SLEF_Sonic/SLEF_first_set_truss_burns/SERDP%20burn%20one/"
if Burn == 2:
    path ="http://35.12.130.8/study/2018-SERDP/02-raw-data/ALL-RAW/SERDP_SLEF_Burn_data/SERDP_SLEF_Sonic/SLEF_first_set_truss_burns/SERDP%20burn%20two/"
if Burn == 3:
    path = "http://35.12.130.8/study/2018-SERDP/02-raw-data/ALL-RAW/SERDP_SLEF_Burn_data/SERDP_SLEF_Sonic/SLEF_first_set_truss_burns/SERDP%20burn%20three/"
if Burn == 4:
    path = "http://35.12.130.8/study/2018-SERDP/02-raw-data/ALL-RAW/SERDP_SLEF_Burn_data/SERDP_SLEF_Sonic/SLEF_second_set_truss_burns/SLEF%20second%20set%20truss%20burns/SERDP%20burn%20four/"
if Burn == 5:
    path = "http://35.12.130.8/study/2018-SERDP/02-raw-data/ALL-RAW/SERDP_SLEF_Burn_data/SERDP_SLEF_Sonic/SLEF_second_set_truss_burns/SLEF%20second%20set%20truss%20burns/SERDP%20burn%20five/"
if Burn  == 6:
    path = "http://35.12.130.8/study/2018-SERDP/02-raw-data/ALL-RAW/SERDP_SLEF_Burn_data/SERDP_SLEF_Sonic/SLEF_second_set_truss_burns/SLEF%20second%20set%20truss%20burns/SERDP%20burn%20six/"

def compiler_b1_6():
    files = ["TOA5_2878.WGNover10Hz.dat","TOA5_2879.ts_data.dat",\
             "TOA5_4390.ts_data.dat","TOA5_4975.ts_data.dat",\
             "TOA5_4976.ts_data.dat","TOA5_10442.ts_data.dat",\
             "TOA5_11585.ts_data.dat"]

    file_num = ["2878","2879","4390","4975","4390","4975","4976","10442","11585"]
    ### First Loading the files into the script
    df_2878 = file_to_df(path, files[0])
    df_2879 = file_to_df(path, files[1])
    
    df_4390 = file_to_df(path, files[2])
    df_4975 = file_to_df(path, files[3])
    
    df_4976 = file_to_df(path, files[4])
    df_10442 = file_to_df(path, files[5])
    
    df_11585 = file_to_df(path, files[6])
    ### List of dataframes that is needed
    df_names= [df_2878, df_2879, df_4390, df_4975, df_4976, df_10442, df_11585]

    t_s,t_e = timestamp_matcher(df_names,file_num)
    if Burn ==6:
        t_s = '2018-03-17 14:33:33' #For Burn 6, due to a large gap
    #trim_df = input("Would you like to trim the data to these timestamps? (y/n):")
    trim_df = "y"
    print("Triming the data")
    if trim_df.lower() == "y":
        df_2878 = cutter(df_2878, t_s, t_e)
        df_2879 = cutter(df_2879, t_s, t_e)
        df_4390 = cutter(df_4390, t_s, t_e)
        df_4975 = cutter(df_4975, t_s, t_e)
        df_4976 = cutter(df_4976, t_s, t_e)
        df_10442 = cutter(df_10442, t_s, t_e)
        df_11585 = cutter(df_11585, t_s, t_e)

    df_names= [df_2878, df_2879, df_4390, df_4975, df_4976, df_10442, df_11585]
    

    #check = input("Would you like to check for repeated timestamps? Note: if there are repeats, it could take a while (y/n):")
    check = "y"
    print("Checking the repeated timestamps")
    if check == "y":
        end_repeat_times = []
        for i in range(len(df_names)):
            print(file_num[i]+':')
            end_repeat_times.append(df_names[i]["TIMESTAMP"][repeat(df_names[i])[-1][-1]+1]) 
    
        print("Cut here:",max(end_repeat_times))
        t_s = max(end_repeat_times)
    
        #cut_out_repeat = input("Would you like to cut all data at the end of the repeated times? (y/n):")
        cut_out_repeat = "y"
        if cut_out_repeat == "y":     
            df_2878 = continuous_df(cutter(df_2878, t_s, t_e),t_s,t_e)
            df_2879 = continuous_df(cutter(df_2879, t_s, t_e),t_s,t_e)
            df_4390 = continuous_df(cutter(df_4390, t_s, t_e),t_s,t_e)
            df_4975 = continuous_df(cutter(df_4975, t_s, t_e),t_s,t_e)
            df_4976 = continuous_df(cutter(df_4976, t_s, t_e),t_s,t_e)
            df_10442 =continuous_df(cutter(df_10442, t_s, t_e),t_s,t_e)
            df_11585 = continuous_df(cutter(df_11585, t_s, t_e),t_s,t_e)
    
    ### Making sure that the data is continuous
    df_names= [df_2878, df_2879, df_4390, df_4975, df_4976, df_10442, df_11585]
    #for df in range(len(df_names)):
     #   df_names[df] = continuous_df(df_names[df], t_s, t_e)

    ### Grabbing Sonic data from specific files
    sonic_columns=["Ux_","Uy_","Uz_","Ts_", "diag_rmy_"]
    time_columns_lst=["YYYY","MM","DD","Hr","Min","Sec"]
    sonc_headers = ["U", "V", "W", "T", "DIAG"]
    
    df_A1, df_A2, df_A3, df_A4 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    df_B1, df_B2, df_B3, df_B4 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    df_C1, df_C2, df_C3, df_C4 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    df_D1, df_D2, df_D3, df_D4 = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    
    a_row_lst = [df_A1, df_A2, df_A3, df_A4]
    b_row_lst = [df_B1, df_B2, df_B3, df_B4]
    c_row_lst = [df_C1, df_C2, df_C3, df_C4]
    d_row_lst = [df_D1, df_D2, df_D3, df_D4 ]
    
    all_sonics = a_row_lst+ b_row_lst + c_row_lst +d_row_lst
    
    ###  Burns 1-6 truss:
    df_4975_time, df_2879_time = time_columns(df_4975), time_columns(df_2879)
    df_11585_time, df_4976_time = time_columns(df_11585), time_columns(df_4976)
    ### WG Nover 10hz
    df_2878_time = time_columns(df_2878)
    df_WGNover = pd.DataFrame()
    
    for col in range(len(sonic_columns)):
        df_WGNover[sonc_headers[col]] = df_2878[sonic_columns[col]+"1"]
    for t in time_columns_lst:
        df_WGNover[t] = df_2878_time[t]
    
        
    for n in range(len(a_row_lst)):
       
        for i in range(len(time_columns_lst)):
            a_row_lst[n][time_columns_lst[i]]=df_4975_time[time_columns_lst[i]]
            b_row_lst[n][time_columns_lst[i]]=df_2879_time[time_columns_lst[i]]
            c_row_lst[n][time_columns_lst[i]]=df_11585_time[time_columns_lst[i]]
            d_row_lst[n][time_columns_lst[i]]=df_4976_time[time_columns_lst[i]]
        
        for i in range(len(sonic_columns)):
            a_row_lst[n][sonc_headers[i]] = df_4975[sonic_columns[i]+str(n+1)]
            b_row_lst[n][sonc_headers[i]] = df_2879[sonic_columns[i]+str(n+1)]
            c_row_lst[n][sonc_headers[i]] = df_11585[sonic_columns[i]+str(n+1)]
            d_row_lst[n][sonc_headers[i]] = df_4976[sonic_columns[i]+str(n+1)]
        
        

    #### Thermal Couple data
    time_columns_lst=["YYYY","MM","DD","Hr","Min","Sec"]
    
    df_B1_tc, df_B2_tc, df_B3_tc, df_B4_tc = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    df_C1_tc, df_C2_tc, df_C3_tc, df_C4_tc = pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame()
    
    first_tc_group = [ df_B1_tc, df_B3_tc, df_C1_tc, df_C3_tc]
    secnd_tc_group = [ df_B2_tc, df_B4_tc, df_C2_tc, df_C4_tc]
    
    df_10442_time, df_2879_time = time_columns(df_10442), time_columns(df_2879)
    df_4390_time, df_11585_time = time_columns(df_4390), time_columns(df_11585)
    
    t_c_lst_1 = ["Temp_C(1)","Temp_C(2)","Temp_C(3)","Temp_C(4)","Temp_C(5)","Temp_C(6)","Temp_C(7)"]
    t_c_lst_2 = ["Temp_C(8)","Temp_C(9)","Temp_C(10)","Temp_C(11)","Temp_C(12)","Temp_C(13)","Temp_C(14)"]
    
    df_tc_lst= [df_10442, df_2879, df_4390, df_11585]
    df_time_lst = [df_10442_time, df_2879_time, df_4390_time, df_11585_time] 
    
    for j in range(len(first_tc_group)):
        for t in range(len(time_columns_lst)):
            first_tc_group[j][time_columns_lst[t]]= df_time_lst[j][time_columns_lst[t]]
            secnd_tc_group[j][time_columns_lst[t]]= df_time_lst[j][time_columns_lst[t]]
        
        for i in range(len(t_c_lst_1)):
            first_tc_group[j][t_c_lst_1[i]]= df_tc_lst[j][t_c_lst_1[i]]
            secnd_tc_group[j][t_c_lst_2[i]]= df_tc_lst[j][t_c_lst_2[i]]
        
        
    all_tc_group = [df_B1_tc, df_B2_tc, df_B3_tc, df_B4_tc,\
                    df_C1_tc, df_C2_tc, df_C3_tc, df_C4_tc ]
    
    return all_sonics, all_tc_group, df_WGNover
    
def correction():
    all_sonics, all_tc_group, df_WGNover = compiler_b1_6()
    nam_snc=["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4", "C1","C2",\
                   "C3","C4","D1","D2","D3","D4"]
    nam_tc = ["B1", "B2", "B3", "B4", "C1","C2","C3","C4"]
    #wind speed correction
    m_speed,min_T = 40, float(-10)
    u_fctr, v_fctr = -1, -1
    
    fmt = "Default Corrections: {}*U, {}*V, Max Wind Speed=|{}| m/s, Min Temperature = {} C  " 
    print(fmt.format(u_fctr,v_fctr,m_speed,min_T))
    
    nw_corct = input("Would you like to change these corrections? (y/n): ")
    if nw_corct.lower() == "y":
        u_fctr = float(input("What to multiply the U values by?:"))
        v_fctr = float(input("What to multiply the V values by?:"))
        m_speed = float(input("What bounds do you want for the wind speed? (m/s):"))
        min_T = float(input("What is the minimum temperatue? (C):"))
    
    fill_nan = np.nan
    change_nan = input("Would you like to change the NaN's to a different value? (y/n):")
    if change_nan == "y":
        fill_nan = input("What to replace NaN's with? ex: 9999:")
    
    for df in range(len(all_sonics)):
        print("Sonic",nam_snc[df],":")
        all_sonics[df] = apply_correction(all_sonics[df],u_fctr,v_fctr,m_speed,min_T,fill_nan)
    df_WGNover = apply_correction(df_WGNover,u_fctr,v_fctr,m_speed,min_T,fill_nan)
    
    for df in range(len(all_tc_group)):
        print("Thermocouple ",nam_tc[df],":")
        all_tc_group[df] = apply_tc_correction(all_tc_group[df],min_T,fill_nan,list(all_tc_group[df].columns)[6:])
        
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
    df = df.drop("DIAG", axis=1)
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
    

def saver_b1_6():
    
    all_sonics, all_tc_group, df_WGNover = correction()
     
    TS = input("Would you like to have a single time stamp column? (y/n):")
    if TS== "y":
        for i in range(len(all_sonics)):
            all_sonics[i] = timestamp_col(all_sonics[i])
        for i in range(len(all_tc_group)):
            all_tc_group[i] = timestamp_col(all_tc_group[i])
        df_WGNover = timestamp_col(df_WGNover)
        
    ### Creating the directories to save the data
    save_me = input("Would you like to save the data into the working directory? (y/n):")
    if save_me == "y":
        cwd = os.getcwd()
    else:
        cwd = input("Full path of save directory:")
        
    save_dir = "Burn-0"+str(Burn)
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
    df_WGNover.to_csv(sonic_dir+'/WGNover_UVWT_Burn-0'+str(Burn)+".txt",sep=' ',index=False)

    ### Saving Thermal Couple dataframes
    
    save_as_lst = ["B1", "B2", "B3", "B4", "C1","C2","C3","C4"]
    for i in range(len(all_tc_group)):
        all_tc_group[i] = all_tc_group[i].round(3)
        sv_file=tc_dir+'/'+save_as_lst[i]+"_thermal_couple_Burn-0"+str(Burn)+".txt"
        all_tc_group[i].to_csv(sv_file, sep=' ',index=False)
    print("You now have the Burn sonics and thermocouple saved")



saver_b1_6()


