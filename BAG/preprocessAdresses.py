import pandas as pd 
import numpy as np 

def preprocess(filename = 'verblijfplaatsen.csv'):
    """ input: verblijfplaatsen.csv
    output: csv with column x and y for R3 coordinates of homes
    """
    df = pd.read_csv('./data/'+filename)
    df['pos'].to_csv('./data/temp.csv', index=False)
    df = pd.read_csv('./data/temp.csv', sep=' ', header=1, names=['x','y','z'])
    df[['x','y']].to_csv('./data/verblijfplaatsen_shorter.csv', index=False)
    return
