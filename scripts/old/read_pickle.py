

import pandas as pd


df = pd.read_pickle('test_samples_close_homes250_750_detailed.pkl')

print(df.at[1, 'height_dtm'].shape)