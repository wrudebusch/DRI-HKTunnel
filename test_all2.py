import pandas as pd
import os
dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

def fix(df):
    s = pd.DataFrame({'start':df.index[0],'avg_ppm':df.mean()})
    s = s.set_index('start')
    return s

def cut_up(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16', parse_dates={'datetime': [0]}, date_parser=dateparse)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO2 ppm']})
    data = data.set_index('datetime')
    ## fix this structure. this does not scale.
    start_of_file = data.index[0]
    end_of_file = data.index[-1]
    start_of_cut = start_of_file
    end_of_cut = start_of_file + pd.offsets.Hour(2)
    cut = data.between_time(start_of_cut,end_of_cut)
    fixed_cut = fix(cut)
    print fixed_cut.head()
    while (end_of_cut + pd.offsets.Hour(2)) <= end_of_file :
        start_of_cut = start_of_cut + pd.offsets.Hour(2)
        end_of_cut = end_of_cut + pd.offsets.Hour(2)
        cut = data.between_time(start_of_cut,end_of_cut)
        fixed_cut = fix(cut)
        print fixed_cut.head()
        

for file in os.listdir('.'):
    if file.endswith(".txt"):
        print file
        cuts = cut_up(file)
        #print cuts.head()
        #cut_up(file).to_csv(file + '.csv')
        
