import pandas as pd
import glob

dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

def fix(df):
    start = pd.Timestamp(long(round(df.index[0].value, -10)))
    stop = pd.Timestamp(long(round(df.index[-1].value, -10)))
    s = pd.DataFrame({'start' : start,'stop' : stop,'avg_ppm' : df.mean()})
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

def fix_CO2(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16', parse_dates={'datetime': [0]}, date_parser=dateparse).convert_objects(convert_numeric=True)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO2 ppm']})
    data = data.set_index('datetime')
    #data = data.convert_objects(convert_numeric=True)
    print data.head()
    return cut_up(data)

##main

CO2_DI_data = []

## CO2 inside
for f in  glob.glob('G:\Dropbox\Hong Kong Tunnel\Downwind\CO2 Inside\*.txt'):
    print f
    data = fix_CO2(f)
    CO2_DI_data.append(data)
    
CO2_DI_data = pd.concat(CO2_DI_data)
CO2_DI_data = pd.DataFrame({'CO2_DI_stop' : CO2_DI_data.stop,'CO2_DI_avg': CO2_DI_data.avg_ppm})

CO2_DO_data = []
## CO2 outside
for f in  glob.glob('G:\Dropbox\Hong Kong Tunnel\Downwind\CO2 Outside\*.txt'):
    print f
    data = fix_CO2(f)
    CO2_DO_data.append(data)
    
CO2_DO_data = pd.concat(CO2_DO_data)
CO2_DO_data = pd.DataFrame({'CO2_DO_stop' : CO2_DO_data.stop,'CO2_DO_avg': CO2_DO_data.avg_ppm})

CO2_UI_data = []

## CO2 inside
for f in  glob.glob('G:\Dropbox\Hong Kong Tunnel\Upwind\CO2Inside\*.txt'):
    print f
    data = fix_CO2(f)
    CO2_UI_data.append(data)
    
CO2_UI_data = pd.concat(CO2_UI_data)
CO2_UI_data = pd.DataFrame({'CO2_UI_stop' : CO2_UI_data.stop,'CO2_UI_avg': CO2_UI_data.avg_ppm})

CO2_UO_data = []
## CO2 outside
for f in  glob.glob('G:\Dropbox\Hong Kong Tunnel\Upwind\CO2Outside\*.txt'):
    print f
    data = fix_CO2(f)
    CO2_UO_data.append(data)
    
CO2_UO_data = pd.concat(CO2_UO_data)
CO2_UO_data = pd.DataFrame({'CO2_UO_stop' : CO2_UO_data.stop,'CO2_UO_avg': CO2_UO_data.avg_ppm})

dfs = [CO2_DO_data,CO2_DI_data,CO2_UI_data,CO2_UO_data]
appended_ALL_data = reduce(lambda left,right: pd.merge(left,right,left_index=True,right_index=True,how='outer'), dfs)

appended_ALL_data.to_csv('CO2_data_rounded_Wang.csv')
