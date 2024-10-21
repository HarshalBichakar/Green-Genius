import tensorflow as tf
import keras.models 
from keras.models import load_model

path='Backend/medecinal_plant_identify_cnn.h5'
model=load_model(path)