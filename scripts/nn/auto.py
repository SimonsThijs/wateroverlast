
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
from sklearn.model_selection import train_test_split

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

column = 'height_dtm'

df = pd.read_pickle('../save.pkl').reset_index()

df = df.sample(frac=1).reset_index(drop=True)

def normalize(row):
    height = row[column]
    nans = height>1000
    height[nans] = np.nan
    height = (height-np.nanmean(height))/np.nanstd(height)
    height[np.isnan(height)] = 3
    return height

def reshape(arr):
    result = np.reshape(arr[column], (1,200,200))
    return result

df[column] = df.apply(normalize, axis=1)
df[column] = df.apply(reshape, axis=1)

df = df[[column, 'target']]

df = df.dropna()

Y = np.asarray(df['target'])
X = np.asarray(df[column].values.tolist())
X = X.reshape((1097,200, 200))


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

print(X.shape)
print(Y.shape)
# print(Y)

# Initialize the image classifier.

input_node = ak.ImageInput()
output_node = ak.ImageBlock(
    # Only search ResNet architectures.
    block_type="vanilla",
    # Normalize the dataset.
    normalize=True,
    # Do not do data augmentation.
    augment=True,
)(input_node)
output_node = ak.ClassificationHead()(output_node)

clf = ak.AutoModel(
    inputs=input_node, outputs=output_node, overwrite=True, max_trials=200,
	loss='binary_crossentropy', directory='/data/s1830120/ImageClassifier', metrics=['accuracy']
)

# clf = ak.ImageClassifier()
# Feed the image classifier with training data.
clf.fit(X_train, y_train, epochs=100, callbacks=[callback], validation_split=0.15)


print("test val")

model = clf.export_model()
print(model.evaluate(X_test, y_test))
model.summary()









