# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 17:12:53 2022

@author: otman
"""

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.utils import to_categorical
import matplotlib.pyplot as plt


(X_train, y_train), (X_test, y_test) = mnist.load_data()

for i in range(6):
    plt.subplot(int('23'+str(i+1)))
    plt.imshow(X_train[i],cmap=plt.get_cmap('gray'))
    
X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

y_train=to_categorical(y_train)
y_test=to_categorical(y_test)

X_train=X_train/255
X_test=X_test/255
input_shape = (28, 28, 1)
def create_model():
    num_classes = 10
    model = Sequential()
    model.add(Convolution2D(32, kernel_size=(3, 3),activation='relu',input_shape=input_shape))
    model.add(Convolution2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    return model

model=create_model()
model.fit(X_train, y_train,validation_data=(X_test,y_test),batch_size=112,epochs=30,verbose=2)
print("The model has successfully trained")
model.save('C:\\Users\\otman\\Downloads\\train_model.h5')
print("Saving the model as train_model.h5")
scores = model.evaluate(X_test, y_test, verbose=0)
print('cnn error : %.2f%%' %(100-scores[1]*100))