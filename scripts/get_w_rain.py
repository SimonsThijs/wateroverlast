import pandas as pd
import numpy as np

begin = '2016-01-01 00:00:00'
end = '2021-02-23 23:59:59'
strfformat = "%Y-%m-%d %H:%M:%S"
from hoogtekaart import height_map_nl

from BAG import home_sampler
from coords import rdconverter
from neerslag import precipitation_nl

from random import randrange
from datetime import timedelta, datetime
import time

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    end = datetime.strptime(end, strfformat)
    start = datetime.strptime(start, strfformat)
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second)).strftime(strfformat)

def get_data(data, a):
    d = data
    # print(d)
    if len(d) > 0 and d[0]['geometry']['location_type'] != 'APPROXIMATE':
        return data[0]['geometry']['location'][a]
    else:
        return np.nan

def get_random_date(data):
	return random_date(begin, end)

def parse_datetime(data):
    return datetime.strptime(str(data['date']).strip(), strfformat)



# df0 = pd.read_csv('../data/randomhomescloes30000_precise.csv')
# df0['target'] = 0
# df0['date'] = df0.apply(get_random_date, axis=1)

df1 = pd.read_json('../data/parsed_w_precise_coords.json')[:]
df1 = df1.dropna()
df1['lat'] = df1['google_results'].apply(get_data, args=('lat',))
df1['lng'] = df1['google_results'].apply(get_data, args=('lng',))
df1['target'] = 1
df1 = df1[['lat','lng','target','date']]
df1 = df1.dropna()
df1['date'] = df1.apply(parse_datetime, axis=1)


df1 = pd.concat([df1], ignore_index=True)
print("df1")
print(df1)

HM = home_sampler.HomeSampler()
# print()
data0 = {'lat':[], 'lng':[], 'date':[], 'target': []}

def sample_random_houses_close(data):
    rdx = rdconverter.gps2X(data['lat'],data['lng'])
    rdy = rdconverter.gps2Y(data['lat'],data['lng'])
    da = HM.sample_in_range(rdx, rdy, 750, 250, 1)
    for d in da:
        lat = rdconverter.RD2lat(d[0], d[1])
        lng = rdconverter.RD2lng(d[0], d[1])
        data0['lat'].append(lat)
        data0['lng'].append(lng)
        data0['date'].append(data['date'])
        data0['target'].append(0)

df1.apply(sample_random_houses_close, axis=1)
df0 = pd.DataFrame(data0)

# print(df0)
df = (pd.concat([df0, df1], ignore_index=True))
df = df.reset_index()
# df['date'] = df.apply(parse_datetime, axis=1)
df = df.sort_values(by=['date'])





PNL = precipitation_nl.PrecipitationNL(queue_size=300)



total = len(df)
count = 0
btime = time.time()
def get_precipitation_data(row):
    global count
    count +=1
    now = time.time()
    avg_time = (now-btime)/count
    left = total-count
    if count % 10 == 0:
        print('====== rain ')
        print('time spent', now-btime)
        print('did', count, 'examples')
        print('avg', avg_time)
        print('left', left)
        print('time left', left*avg_time)
        print('======')

    date = row['date']
    # date = datetime.strptime(str(row['date']), strfformat)
    if date <= datetime(year=2020, month=12, day=31, hour=8):
        lat = row['lat']
        lon = row['lng']
        rain = PNL.get_precipation_data_past_hours_list(date.year, date.month, date.day, date.hour, date.minute, lat, lon, 12)
        return rain
    
    return np.nan

HMNL = height_map_nl.HeightMapNL()
HMNL.detailed = True

total = len(df)
count = 0
btime = time.time()
def get_height_data(data):
    global count
    count +=1
    now = time.time()
    avg_time = (now-btime)/count
    left = total-count
    if count % 10 == 0:
        print('====== height')
        print('time spent', now-btime)
        print('did', count, 'examples')
        print('avg', avg_time)
        print('left', left)
        print('time left', left*avg_time)
        print('======')
        
    lat = data['lat']
    lng = data['lng']
    rdx = rdconverter.gps2X(lat,lng)
    rdy = rdconverter.gps2Y(lat,lng)
    rdx = round(rdx, 2)
    rdy = round(rdy, 2)
    try:
        data =  (HMNL.get_height_area(rdx-100, rdy+100, rdx+100, rdy-100))
    except Exception as e:
        print(e)
        data = np.nan
        print("failed")
    # data = np.where(data > 1000, np.nan, data)
    return data



df['height_dtm'] = df.apply(get_height_data, axis=1)
HMNL.dsm = True

total = len(df)
count = 0
btime = time.time()

df['height_dsm'] = df.apply(get_height_data, axis=1)

total = len(df)
count = 0
btime = time.time()

df['prec12'] = df.apply(get_precipitation_data, axis=1)

df.to_pickle('test_samples_close_homes250_750_detailed.pkl')


















