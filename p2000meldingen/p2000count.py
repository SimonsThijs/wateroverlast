
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import json

with open('../data/parsed_w_precise_coords.json', 'r') as file:
    data = json.load(file)
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df['date'],format='%Y-%m-%d %H:%M:%S')
    ticks = (df.groupby(by=[df.index.year, df.index.month, df.index.day]).count().index.tolist())
    ticks_str = ["{}-{}-{}".format(x[0], x[1], x[2]) for x in ticks]
    df = df.groupby(by=[df.index.year, df.index.month, df.index.day]).count()['service']
    df.plot(rot=90)
    plt.xticks(range(0,len(df)), ticks_str)
    plt.show()