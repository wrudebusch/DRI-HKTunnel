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

def fix_CO(filename): 
    raw = pd.read_table(filename, sep='\t', encoding='utf-16',dtype={'user_id':'float'},parse_dates={'datetime': [1]}, date_parser=dateparse)
    data = pd.DataFrame({'datetime' : raw['datetime'],'CO2ppm': raw['CO# 20669027, ppm (LGR S/N: 10641068)']})
    data = data.set_index('datetime')
    #data = data.convert_objects(convert_numeric=True)
    print data.head()
    return cut_up(data)

##main

#downwind
part1 = []
for f in  glob.glob('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Downwind\CO\*.txt'):
    print f
    data = fix_CO(f)
    part1.append(data)
    
part1 = pd.concat(part1)
part1 = pd.DataFrame({'CO_Downwind_stop' : part1.stop,'CO_Downwind_avg': part1.avg_ppm})

#upwind
part2 = []
for f in  glob.glob('C:\Users\XPS\Dropbox\Hong Kong Tunnel\Upwind\CO\*.txt'):
    print f
    data = fix_CO(f)
    part2.append(data)
    
part2 = pd.concat(part2)
part2 = pd.DataFrame({'CO_Upwind_stop' : part2.stop,'CO_Upwind_avg': part2.avg_ppm})


dfs = [part1,part2]
appended_ALL_data = reduce(lambda left,right: pd.merge(left,right,left_index=True,right_index=True,how='outer'), dfs)

appended_ALL_data.to_csv('CO_data.csv')
