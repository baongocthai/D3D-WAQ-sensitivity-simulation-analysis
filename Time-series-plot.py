# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 10:41:03 2022

@author: baongoc.thai
"""
# =============================================================================
# This script plots all paramaters from WAQ output to compare among simulations (used for sensitivity tests)
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

directory = r'C:\Users\baongoc.thai\OneDrive - Hydroinformatics Institute Pte Ltd\Desktop\Work\LSR\WAQ_Update\WAQ_2019_without_veg'
os.chdir(directory)

#%% Function to import all results
def ReadRawData(filename, parameters, stations):
    mod = pd.read_csv(filename,sep=',',skiprows=range(3), nrows=1)
    parameters_mod = mod.columns.tolist()
    locations_mod = mod.values.tolist()
    parameters_mod_clean = []
    
    for parameter in parameters_mod[1:]: #Extract only parameters name in model results
        a = parameter.split('.')[0]
        parameters_mod_clean.append(a)
        
    locations_mod_clean = locations_mod[0][1:]
    par_loc_mod = [] 
    
    #Merge parameters & locations to create column names in raw data file
    for i in range(len(parameters_mod_clean)): #Combine parameters & locations in model results
        b = parameters_mod_clean[i]+'_'+locations_mod_clean[i]
        par_loc_mod.append(b)
        
    # Import data
    df_mod_raw = pd.read_csv(filename,sep=',',skiprows=range(4),parse_dates = [0],dayfirst=True)
    df_mod_raw.columns = ['time']+par_loc_mod
    df_mod_raw['time'] = pd.to_datetime(df_mod_raw['time'], format='%Y-%m-%d %H:%M:%S')
    df_mod_raw.index = df_mod_raw.pop('time')
    
    #Select paramters of interest
    list = []
    for parameter in parameters:
        for station in stations:
            a = parameter + '_' + station
            list.append(a)
    df_mod_raw_selected = df_mod_raw[df_mod_raw.columns.intersection(list)]
    return df_mod_raw_selected

#%% Main block: Extract results from interested stations
list_file = glob.glob('*.csv')
parameters = ['TotN', 'NO3', 'NH4','TON','DON',
              'Chlfa', 'CYLINFIX', 'ARTHROSP', 'FDIATOMS', 'GREENS', 'MICROCYS', 'OSCILAT', 'PLANKTOL', 'PSEUDOAN', 
              'TotP', 'PO4', 'DOP', 'TOP',
              'TOC', 'POC', 'DOC',
              'OXY']
stations = ['RLS C (1)', 'RLS C (2)', 
            'RLS E (1)', 'RLS E (2)', 
            'RLS P (2)', 
            'RLS A (2)',
            'LSR-W']

#merge all result datasets, calculate daily average
all_data = []
for filename in list_file:
    data = ReadRawData(filename, parameters, stations)
    data = data.groupby([data.index.date]).mean()       #Calculate daily average
    all_data.append(data)
    
columns = all_data[0].columns.tolist()

#%% Time series plot for hourly data
for column in columns:
    for i in range(len(all_data)):
        plt.plot(all_data[i].index,all_data[i][column], linewidth=1,label=list_file[i][0:-4])
    plt.legend()
    plt.title(column)
    plt.ylabel(column)
    plt.xlabel("Time")
    plt.rcParams.update({'font.size': 15})
    plt.tight_layout()
    figure = plt.gcf()
    figure.set_size_inches(18, 6)
    print (column)
    plt.savefig("TimeSeriesPlot\\"+column+'.png', bbox_inches='tight',dpi=600)
    plt.close()
