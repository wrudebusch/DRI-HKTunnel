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
    cut1 = fix(data.between_time('00:00','2:00'))
    cut2 = fix(data.between_time('2:00','4:00'))
    cut3 = fix(data.between_time('4:00','6:00'))
    cut4 = fix(data.between_time('6:00','8:00'))
    cut5 = fix(data.between_time('8:00','10:00'))
    cut6 = fix(data.between_time('10:00','12:00'))
    cut7 = fix(data.between_time('12:00','14:00'))
    cut8 = fix(data.between_time('14:00','16:00'))
    cut9 = fix(data.between_time('16:00','18:00'))
    cut10 = fix(data.between_time('18:00','20:00'))
    cut11 = fix(data.between_time('20:00','22:00'))
    cut12 = fix(data.between_time('22:00','00:00'))
    dfs = [cut2,cut3,cut4,cut5,cut6,cut7,cut8,cut9,cut10,cut11,cut12]
    cuts = cut1.append(dfs)
    return cuts

#for file in os.listdir("\mydir"):
for file in os.listdir('.'):
    if file.endswith(".txt"):
        cut_up(file).to_csv(file + '.csv')
