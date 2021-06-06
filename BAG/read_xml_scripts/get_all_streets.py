import pandas_read_xml as pdx
import pandas as pd


final_df = pd.DataFrame()


for i in range(1,35):
	df = pdx.read_xml("data/9999OPR08032021/9999OPR08032021-0000{:02d}.xml".format(i), 
		['sl-bag-extract:bagStand', 'sl:standBestand', 'sl:stand'])

	key_columns = ['Objecten:naam', 'Objecten:type', 'Objecten-ref:WoonplaatsRef', 'Objecten:identificatie']
	df = pdx.fully_flatten(df, key_columns)
	# df = pdx.flatten(df)

	cols = ['sl-bag-extract:bagObject|Objecten:OpenbareRuimte|Objecten:identificatie|#text', 
				'sl-bag-extract:bagObject|Objecten:OpenbareRuimte|Objecten:naam', 
				'sl-bag-extract:bagObject|Objecten:OpenbareRuimte|Objecten:ligtIn|Objecten-ref:WoonplaatsRef|#text'
				]

	df = df[cols]
	final_df = pd.concat([final_df, df], ignore_index=True)

final_df.columns = ['id', 'naam', 'woonplaatsid']
final_df.drop_duplicates()
final_df.to_csv('straatnamen.csv')