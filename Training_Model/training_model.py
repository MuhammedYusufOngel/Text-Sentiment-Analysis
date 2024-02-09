#!/usr/local/bin/python
# -*- coding: iso-8859-9 -*-
import os, sys

from os import system
import numpy as np
import pandas as pd
import json

from keras.models import Sequential
from keras.layers import Dense, GRU, Embedding, CuDNNGRU
from keras.optimizers import Adam

system("CLS")

dataframe = pd.read_csv("../Compile_Comments/comments_final.csv", encoding="iso-8859-9", delimiter="\t")

target = dataframe['Puan'].values.tolist()
data = dataframe['Yorum'].values.tolist()


def makeToken(yorumList):
    y_comments = []

    for comment in yorumList:
        y_comment = []
        #We find the words in the comments.
        for word in comment.split():
            #We limit number of word with 50 and we don't add same word
            if(len(y_comment) < 50 and word in jsonTokenizer):
                y_comment.append(jsonTokenizer[word])

        #If number of word less than 50, we add zero to array until length of array is 50.
        if(len(y_comment) < 50):
            zeros = list(np.zeros(50 - len(y_comment), dtype=int))
            y_comment = zeros + y_comment

        y_comments.append(y_comment)
    
    return np.array(y_comments, dtype=np.dtype(np.int32))

#We determine cut off point.
cutoff = int(len(data) * 0.85)

#We take one for testing, one for training.
x_train, x_test = data[:cutoff], data[cutoff:]
y_train, y_test = target[:cutoff], target[cutoff:]

#load the tokenizer
with open('../Tokenizer/tokenizer.json', encoding="iso-8859-9") as jsonFile:
    jsonTokenizer = json.load(jsonFile)

#We must convert to np.array because return of "makeToken" function is np.array.
y_train = np.array(y_train)
y_test = np.array(y_test)
x_train = np.array(x_train)
x_test = np.array(x_test)

#We create trainingGroup and testGroup
trainingGroup = makeToken(x_train)
testGroup = makeToken(x_test)

#It allows you to add layers sequentially.
model = Sequential()

#The Embedding layer is used to represent text data with numerical vectors.
#input_dim = number of words
#output_dim = Total length to represent words
#input_length = Size of input arrays
model.add(Embedding(input_dim=10001,
                    output_dim=50,
                    input_length=50,
                    name = 'embedding_layer'))

#units = The number of neurons in the layer or the size of the output space.
#return_sequences = Whether the layer will always produce a time step output and not
#reset_after = The reset gates of the GRU layer determine what happens before or after multiplying the matrices between the input and the cell state.
model.add(GRU(units=16, return_sequences=True, reset_after=False))
model.add(GRU(units=8, return_sequences=True, reset_after=False))
model.add(GRU(units=4, reset_after=False))
model.add(Dense(1, activation='sigmoid'))

#1e-3 = 0.0001
#lr = Learning rate (Determines how many steps to take)
optimizer = Adam(lr=1e-3)

#loss = Calculates how much is lost in learning (binary_crossentropy = a function)
#metrics = This parameter determines the metrics that will be evaluated during training of the model.
model.compile(loss='binary_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

#It is used to visualize the architecture of the model and the dimensions of the layers in the model.
model.summary()

#epochs = This parameter determines how many periods the model will be trained during training.
#batch_size = This parameter determines how many samples will be used in each training step.
model.fit(trainingGroup, y_train, epochs=5, batch_size=64)
print("--------")

#We test the model.
model.evaluate(testGroup, y_test)

#We save the model
model.save('8February2024_0957.h5')