import pandas as pd

def fix(df):
    s = pd.DataFrame({'start':df.index[0],'stop':df.index[-1],'avg_ppm':df.mean()})
   #s = s.set_index('start')
    return s

dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%Y %H:%M:%S')

raw = pd.read_table('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Downwind\CO\20150122_CO_Downwind.txt')#, sep='\t', encoding='utf-16', parse_dates={'datetime': [1]}, date_parser=dateparse)
data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO2 ppm']})
data = data.set_index('datetime')
data = data.convert_objects(convert_numeric=True)

cut1 = fix(data.between_time('8:00','10:00'))
#cut1.set_index('cut1')
print cut1

cut2 = fix(data.between_time('11:00','13:00'))
print cut2

cut3 = fix(data.between_time('14:00','16:00'))
print cut3

cut4 = fix(data.between_time('17:00','19:00'))
print cut4

dfs = [cut1,cut2,cut3,cut4]
all = pd.concat(dfs)

all.reset_index(level=0, inplace=True)

all = pd.DataFrame({'CO2_DO_start' : all['start'],'CO2_DO_avg' : all['avg_ppm'],'CO2_DO_stop' : all['stop']})

print all
