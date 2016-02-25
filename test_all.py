import pandas as pd
import glob

dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

def fix(df):
    print len(df)
    s = pd.DataFrame({'start':df.index[0],'stop':df.index[-1],'avg_ppm':df.mean()})
    s = s.set_index('start')
    return s

def cut_up(data):
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
    #print cuts.head()
    return cuts

def fix_CO(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16',dtype='unicode',parse_dates={'datetime': [1]}, date_parser=dateparse)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO# 20669027, ppm (LGR S/N: 10641068)']})
    data = data.set_index('datetime')
    data = data.convert_objects(convert_numeric=True)
    #print data.head()
    return cut_up(data)

def fix_CO2(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16', parse_dates={'datetime': [0]}, date_parser=dateparse)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO2 ppm']})
    data = data.set_index('datetime')
    data = data.convert_objects(convert_numeric=True)
    return cut_up(data)

##main

# processing CO data first
CO_data = []
## CO data
for f in  glob.glob('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Downwind\CO\*.txt'):
    print f
    data = fix_CO(f)
    CO_data.append(data)
    
CO_data = pd.concat(CO_data)
CO_data = pd.DataFrame({'stop_CO' : CO_data.stop,'avg_COppm': CO_data.avg_ppm})
print CO_data.head()

CO2i_data = []

## CO2 inside
for f in  glob.glob('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Downwind\CO2 Inside\*.txt'):
    print f
    data = fix_CO2(f)
    CO2i_data.append(data)
    
CO2i_data = pd.concat(CO2i_data)
CO2i_data = pd.DataFrame({'stop_CO2i' : CO2i_data.stop,'avg_CO2ippm': CO2i_data.avg_ppm})

CO2o_data = []
## CO2 outside
for f in  glob.glob('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Downwind\CO2 Outside\*.txt'):
    print f
    data = fix_CO2(f)
    CO2o_data.append(data)
    
CO2o_data = pd.concat(CO2o_data)
CO2o_data = pd.DataFrame({'stop_CO2o' : CO2o_data.stop,'avg_CO2oppm': CO2o_data.avg_ppm})

appended_ALL_data = pd.merge(CO2o_data,CO2i_data,left_index=True,right_index=True,how='outer')
appended_ALL_data = pd.merge(appended_ALL_data,CO_data,left_index=True,right_index=True,how='outer')
#print appended_ALL_data.head()
appended_ALL_data.to_csv('averaged_data.csv')
