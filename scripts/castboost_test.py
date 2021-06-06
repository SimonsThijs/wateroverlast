import random
import ast
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def random_target(row):
	return random.choice([0,1])

def calc_sums(row):
	data = []
	lst = ast.literal_eval(row['prec12'])
	for j in range(12):
		d = np.asarray(lst[j*12:j*12+12])
		d = np.where(d == 65535, 0, d)
		d = np.where(d < 0, 0, d)
		data.append(np.sum(d))

	return data

def calc_stds(row):
	data = []
	lst = ast.literal_eval(row['prec12'])
	for j in range(12):
		d = np.asarray(lst[j*12:j*12+12])
		d = np.where(d == 65535, 0, d)
		d = np.where(d < 0, 0, d)
		data.append(np.std(d))

	return data

df = pd.read_csv('test_0_rain.csv')
df = df.dropna(axis=0)
df = df.drop(['index'], axis=1)
# df['target'] = df.apply(random_target, axis=1)
df['prec_sums'] = df.apply(calc_sums, axis=1)

cols = ['sum'+str(i+1) for i in range(12)]
df[cols] = pd.DataFrame(df.prec_sums.tolist(), index=df.index)

df['past3hours'] = df['sum1'] + df['sum2'] + df['sum3']


df = df[df.past3hours > 6000]

df.to_csv('tmp.csv')

df0 = df[df.target==0]
values = list(df0['past3hours'])
plt.hist(values, color = 'blue', edgecolor = 'black', bins = int(500))
# plt.show()
# print(len(df))
# from catboost import CatBoostClassifier, Pool

# # initialize data
# train_data = df[cols]

# train_labels = df['target']

# test_data = catboost_pool = Pool(train_data, 
#                                  train_labels)

# model = CatBoostClassifier(iterations=1000,
#                            depth=2,
#                            learning_rate=1,
#                            loss_function='Logloss',
#                            verbose=True,
#                            )
# train the model
# model.fit(train_data, train_labels)
# print(model.get_best_score())

