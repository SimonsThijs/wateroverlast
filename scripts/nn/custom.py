

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
# import autokeras as ak
from tensorflow.keras import datasets, layers, models
# import matplotlib.pyplot as plt

mets=[
    tf.keras.metrics.TruePositives(name='tp'),
    tf.keras.metrics.FalsePositives(name='fp'),
    tf.keras.metrics.TrueNegatives(name='tn'),
    tf.keras.metrics.FalseNegatives(name='fn'), 
    'accuracy']

column = 'layers'

df = pd.read_pickle('/data/s1830120/50-500.pkl').reset_index()
df = df.sample(frac=1).reset_index(drop=True)
Y = np.asarray(df['target'])
X = np.asarray(df[column].values.tolist())
X = X.swapaxes(1,3)
X = np.where(X==255, 1, X) 
X = np.where(X>1000, -10, X) 

X_rain = np.asarray(df['prec12'].values.tolist())


# X_rain = np.where(X==np.nan, 0, X_rain) 

weight_for_0 = 1
weight_for_1 = 5

class_weight = {0: weight_for_0, 1: weight_for_1}




# datagen = ImageDataGenerator(
#         featurewise_center=False,  # set input mean to 0 over the dataset
#         samplewise_center=False,  # set each sample mean to 0
#         featurewise_std_normalization=True,  # divide inputs by std of the dataset
#         samplewise_std_normalization=False,  # divide each input by its std
#         zca_whitening=False,  # dimesion reduction
#         rotation_range=5,  # randomly rotate images in the range 5 degrees
#         zoom_range = 0.05, # Randomly zoom image 10%
#         width_shift_range=0.1,  # randomly shift images horizontally 10%
#         height_shift_range=0.1,  # randomly shift images vertically 10%
#         horizontal_flip=True,  # randomly flip images
#         vertical_flip=True)  # randomly flip images

# datagen.fit(X_train)

p = 0.1


# create train test set
train_split = np.random.choice(a=[False, True], size=(len(X),), p=[p, 1-p])

X_train = X[train_split]
X_rain_train = X_rain[train_split]
y_train = Y[train_split]

X_test = X[~train_split]
X_rain_test = X_rain[~train_split]
y_test = Y[~train_split]


# create validation set for validating while training from train set
train_split = np.random.choice(a=[False, True], size=(len(X_train),), p=[p, 1-p])

X_val = X_train[~train_split]
X_rain_val = X_rain_train[~train_split]
y_val = y_train[~train_split]

X_train = X_train[train_split]
X_rain_train = X_rain_train[train_split]
y_train = y_train[train_split]



# kernel_regularizer=keras.regularizers.l1_l2(0.01)

model = models.Sequential()
model.add(layers.Conv2D(32, (2, 2), activation='relu', input_shape=(400, 400, 6)))
model.add(layers.Conv2D(32, (2, 2), activation='relu'))
model.add(layers.Conv2D(32, (2, 2), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (5, 5), activation='relu'))
model.add(layers.Conv2D(64, (5, 5), activation='relu'))
model.add(layers.Conv2D(64, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(5, (5, 5), activation='relu'))
# model.add(layers.Conv2D(5, (5, 5), activation='relu'))
# model.add(layers.Conv2D(5, (5, 5), activation='relu'))
# model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())  # this converts our 3D feature maps to 1D feature vectors
# model.add(layers.Dropout(0.2))
# model.add(layers.Dense(32, activation='relu'))
# model.add(layers.Dropout(0.05))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dropout(0.05))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dropout(0.05))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dropout(0.05))
# kernel_regularizer=keras.regularizers.l1_l2(l1=0.1, l2=0.01)
# kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)

model_B = models.Sequential()
model_B.add(layers.Dense(32, activation='relu', input_shape=(144,)))


# concatenated model
inputs = layers.Concatenate()([model.output, model_B.output])
output = layers.Dense(1, activation='sigmoid')(inputs)
model_C = keras.Model(inputs=[model.input, model_B.input], outputs=output, name="concatenated_model")
model_C.summary()


# sgd = tf.keras.optimizers.SGD(lr=0.1, decay=0.000225, momentum=0.5)

model_C.compile(optimizer='Adam',
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=mets)

# history = model.fit_generator(datagen.flow(X_train,y_train), epochs=200, validation_split=0.1, class_weight=class_weight)

history = model_C.fit([X_train, X_rain_train], y_train, epochs=200, validation_data=([X_val, X_rain_val], y_val), class_weight=class_weight) #class_weight=class_weight






