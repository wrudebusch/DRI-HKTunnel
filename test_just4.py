import pandas as pd
import os
dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

def fix(df):
    s = pd.DataFrame({'start':df.index[0],'stop':df.index[-1],'avg_ppm':df.mean()})
    s = s.set_index('start')
    return s

def cut_up(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16', parse_dates={'datetime': [0]}, date_parser=dateparse)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO2 ppm']})
    data = data.set_index('datetime')
    cut1 = data.between_time('8:00','10:00')
    if len(cut1) > 1 : cut1 = fix(cut1)
    cut2 = data.between_time('11:00','13:00')
    if len(cut2) > 1 : cut2 = fix(cut2)
    cut3 = data.between_time('14:00','16:00')
    if len(cut3) > 1 : cut3 = fix(cut3)
    cut4 = data.between_time('17:00','19:00')
    if len(cut4) > 1 : cut4 = fix(cut4)
    dfs = [cut2,cut3,cut4]
    cuts = cut1.append(dfs)
    return cuts

for file in os.listdir('.'):
    if file.endswith(".txt"):
        print file
        print cut_up(file)
        #cut_up(file).to_csv(file + '.csv')
        
