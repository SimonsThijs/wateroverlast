
import pandas as pd
import numpy as np

import math

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


df = pd.read_pickle('save_w_raw_features.pkl')
features = [col for col in df if col.startswith('height_dtm_')]
df = df.replace(np.nan, 10000)

df[features+['target']].to_csv('test.csv')
features_df = df[features]
labels = df['target']


scores = []


for i in range(10):
	train_features, test_features, train_labels, test_labels = train_test_split(features_df, labels, test_size = 0.25)

	rf = RandomForestClassifier(n_estimators=1000, max_depth=None, max_features=0.1, min_samples_leaf=10)
	rf = rf.fit(train_features, train_labels)

	print(rf.score(train_features, train_labels))

	predictions = rf.predict(test_features)


	score = (1-(predictions-test_labels).abs().mean())
	print(score)
	scores.append(score)


print(scores)
print(np.mean(scores))
print(np.std(scores))
