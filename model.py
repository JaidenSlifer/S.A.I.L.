import tensorflow as tf
import tensorflow.keras as keras # keras is lazy loaded so this keeps the errors down
import keras.utils as utils
from keras.models import Sequential
from keras.layers import TextVectorization, Embedding, LSTM, Dense, Dropout, Conv1D, GlobalMaxPooling1D
from keras.losses import SparseCategoricalCrossentropy
from keras.callbacks import ModelCheckpoint
import os

class SentimentModel:

  def __init__(self):
    self.model = Sequential()
    
  def splitData(self, data_dir):
    train_data = utils.text_dataset_from_directory(
      data_dir,
      batch_size=32,
      validation_split=0.2,
      subset='training',
      seed=1530)
    
    val_data = utils.text_dataset_from_directory(
      data_dir,
      batch_size=32,
      validation_split=0.2,
      subset='validation',
      seed=1530)
    
    return train_data, val_data
  
  def train(self, data_dir: str, save_model: bool, save_path: str = ''):

    VOCAB_SIZE = 10000
    
    # split and optimize datasets
    train_data, val_data = self.splitData(data_dir)
    train_data = train_data.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    val_data = val_data.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    # create text vectorization layer
    vectorize_layer = TextVectorization(
        max_tokens=VOCAB_SIZE,
        output_mode='int',
        output_sequence_length=100)

    # get training text to fit text vectorization on
    train_text = train_data.map(lambda text, labels: text)
    vectorize_layer.adapt(train_text)

    # add layers to model
    self.model.add(vectorize_layer)
    self.model.add(Embedding(input_dim=VOCAB_SIZE, output_dim=128, input_length=100, embeddings_regularizer=keras.regularizers.l2(0.01)))
    #self.model.add(LSTM(128))
    #self.model.add(Dropout(0.2))
    self.model.add(Dropout(0.5))
    self.model.add(Conv1D(64, 5, padding="valid", activation="relu", strides=2))
    self.model.add(GlobalMaxPooling1D())
    self.model.add(Dense(3, activation='sigmoid'))


    callbacks = []
    if(save_model and len(save_path) > 0):
      save_path = os.path.join(save_path, 'nlp_model.ckpt')
      callbacks.append(ModelCheckpoint(filepath=save_path, save_weights_only=True, verbose=1, save_best_only=True))

    # compile and fit model on dataset
    self.model.compile(
      loss=SparseCategoricalCrossentropy(from_logits=True),
      optimizer='adam',
      metrics=['accuracy'])
    self.model.fit(train_data, validation_data=val_data, epochs=15, callbacks=callbacks)

  def test(self):
    pass