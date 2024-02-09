#!/usr/local/bin/python
# -*- coding: iso-8859-9 -*-
import os
from os import system
import tensorflow as tf
import tensorflowjs as tfjs

system("CLS")

# Load the model
model_path = r"E:/Bole dilin/T/Training_Model/8February2024_0957.h5"
newModel = tf.keras.models.load_model(model_path.encode('iso-8859-9').decode('unicode_escape'))

# Save the model using tf.saved_model.save directly
tfjs.converters.save_keras_model(newModel, 'js_model')

print(f"Model saved successfully")