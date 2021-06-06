import pandas_read_xml as pdx


df = pdx.read_xml("data/9999OPR08032021/9999OPR08032021-000001.xml", 
	['sl-bag-extract:bagStand', 'sl:standBestand', 'sl:stand'])

key_columns = ['Objecten:naam', 'Objecten:type', 'Objecten-ref:WoonplaatsRef', 'Objecten:identificatie']
df = pdx.fully_flatten(df, key_columns)
# df = pdx.flatten(df)


print(df.iloc[1])