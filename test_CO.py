import pandas as pd
import glob

dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

def fix(df):
    s = pd.DataFrame({'start':df.index[0],'stop':df.index[-1],'avg_ppm':df.mean()})
    s = s.set_index('start')
    return s

def cut_up(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16',parse_dates={'datetime': [1]}, date_parser=dateparse)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO# 20669027, ppm (LGR S/N: 10641068)']})
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
    #print type(cuts)
    return cuts

appended_data = []

for f in  glob.glob('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Downwind\CO\*.txt'):
    print f
    data = cut_up(f)
    appended_data.append(data)
        
appended_data = pd.concat(appended_data)
appended_data = pd.DataFrame({'stop' : appended_data.stop,'avg_COppm': appended_data.avg_ppm})
#fix columns here
appended_data .to_csv('averaged_data.csv')
