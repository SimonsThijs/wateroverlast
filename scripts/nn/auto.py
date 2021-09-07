
import numpy as np
import pandas as pd
import tensorflow as tf
import autokeras as ak
from sklearn.model_selection import train_test_split

callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=6)

column = 'layers'

# df = pd.read_pickle('/data/s1830120/50-500.pkl').reset_index()
# length = len(df)
# df = df.sample(frac=1).reset_index(drop=True)

# # def normalize(row):
# #     height = row[column]
# #     nans = height>1000
# #     height[nans] = np.nan
# #     height = (height-np.nanmean(height))/np.nanstd(height)
# #     height[np.isnan(height)] = 3
# #     return height

# # def reshape(arr):
# #     result = np.reshape(arr[column], (400,400, 6))
# #     return result

# # df[column] = df.apply(normalize, axis=1)
# # df[column] = df.apply(reshape, axis=1)

# df = df[[column, 'target']]

# df = df.dropna()

# Y = np.asarray(df['target'])
# X = np.asarray(df[column].values.tolist())
# X = X.swapaxes(1,3)

# np.save('/data/s1830120/Y.npy', Y)
# np.save('/data/s1830120/X.npy', X)

Y = np.load('/data/s1830120/Y.npy')
X = np.load('/data/s1830120/X2.npy')
X = np.where(X==255, 1, X) 
X = np.where(X>1000, -10, X) 


weight_for_0 = 1
weight_for_1 = 5

class_weight = {0: weight_for_0, 1: weight_for_1}


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)


# print(X.shape)
# print(Y.shape)
# print(Y)

# Initialize the image classifier.

input_node = ak.ImageInput()
output_node = ak.ImageBlock(
    # Only search vanilla architectures.
    block_type="vanilla",
    # Normalize the dataset.
    normalize=True,
    # Do data augmentation.
    augment=True,
)(input_node)
output_node = ak.ClassificationHead()(output_node)

mets=[
    tf.keras.metrics.TruePositives(name='tp'),
    tf.keras.metrics.FalsePositives(name='fp'),
    tf.keras.metrics.TrueNegatives(name='tn'),
    tf.keras.metrics.FalseNegatives(name='fn'), 
    'accuracy']

clf = ak.AutoModel(
    inputs=input_node, outputs=output_node, overwrite=True, max_trials=200,
	loss='binary_crossentropy', directory='/data/s1830120/ImageClassifier', metrics=[mets]
)

# clf = ak.ImageClassifier()
# Feed the image classifier with training data.
clf.fit(X_train, y_train, epochs=100, callbacks=[callback], validation_split=0.15, 
        class_weight=class_weight, use_multiprocessing=True, workers=5, max_queue_size=100)


print("test val")

model = clf.export_model()
print(model.evaluate(X_test, y_test))
model.summary()









