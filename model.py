import tensorflow as tf
import tensorflow.keras as keras # keras is lazy loaded so this keeps the errors down
import keras.utils as utils
from keras.models import Sequential
from keras.layers import TextVectorization, Embedding, LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Flatten
from keras.losses import SparseCategoricalCrossentropy
from keras.models import load_model
from keras.regularizers import l2

from textprocessor import TextProcessor
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
    self.model.add(Embedding(input_dim=VOCAB_SIZE, output_dim=128, input_length=100, embeddings_regularizer=l2(0.01)))
    self.model.add(Conv1D(32, 6, padding="valid", activation="relu", strides=2))
    self.model.add(MaxPooling1D(pool_size=2))
    self.model.add(Flatten())
    self.model.add(Dropout(0.8))
    self.model.add(Dense(10, activation='relu'))
    self.model.add(Dense(3, activation='sigmoid'))

    # compile and fit model on dataset
    self.model.compile(
      loss=SparseCategoricalCrossentropy(),
      optimizer='adam',
      metrics=['accuracy'])
    self.model.fit(train_data, validation_data=val_data, epochs=20)

    # save model to file
    if(save_model and len(save_path) > 0):
      save_path = f'{save_path}.keras'
      self.model.save(save_path, overwrite=True, save_format='keras')

  def predict(self, input_list):
    return self.model.predict(input_list)
  
  def load_model(self, model_path):
    model_path = f'{model_path}.keras'
    self.model = load_model(model_path, compile=True)
  
  def test_predict(self):
    test_predict = [
      "In the third quarter of 2010 , net sales increased by 5.2 % to EUR 205.5 mn , and operating profit by 34.9 % to EUR 23.5 mn .",
      "Apple reported revenue gains over the past two quarters .",
      "S&P 500 Gains and Losses Today: Apple Jumps on Report of Plans for AI-Powered Macs",
      "Apple's AI iPhone Could See 5G-Like Upgrade Cycle",
      "Apple to use new M4 chips in Mac products: Bloomberg",
      "Apple Surges on Reported Plans To Overhaul Macs With In-House Chips Focused on AI",
      "S&P 500, Nasdaq recover and close higher following March PPI",
      "Apple Plans to Overhaul Entire Mac Line With AI-Focused M4 Chips",
      "'We see several drivers for margins to go higher' for Apple, says Bank of America's Wamsi Moha",
      "Apple plans Mac line overhaul with AI-focused M4 chips, Bloomberg News reports",
      "Apple readies M4 chips for Macs, Bloomberg News reports",
      "Apples Services business is a bright spot in the companys rough 2024: BofA",
      "Is Meta Stock A Buy After Debuting Latest AI Chip?",
      "Apple Reportedly Partnering With Shutterstock for AI Model Training, Shutterstock's Attractiveness, Apple Adds More Licensed Movies to Apple TV+",
      "Apple is now blaming mercenaries after warning iPhone users about a 'state-sponsored' Apple Spyware Warning: What to Know About Mercenary Spyware Attack' Alerts",
      "Apples Moderating Valuation Draws in Hedge Funds, JPMorgan Says",
      "3 Fantastic Growth Stocks That Have Turned $10,000 Into $3 Million in 20 Years",
      "Why You Should Wait for Some Dip Before Biting Into Apple Stock",
      "Humanes Ai Pin considers life beyond the smartphone",
      "GenAI industry shifts: Apple and Google's rumored alliance and OpenAI's Asian entry sparks buzz",
      "Apple Urged to Speak Out on Vietnams Jailed Climate Activists",
      "Alternative browsers report uplift after EU's DMA choice screen mandate",
      "Apple drops term 'state-sponsored' attacks from its threat notification policy",
      "Activists press Apple to oppose Vietnam's detainments of climate experts"
    ]
    tp = TextProcessor()
    predict_processed = tp.processText(test_predict)

    #prediction = self.model.predict(test_predict)
    print(self.predict(predict_processed))
    # norm_predict = []
    # for vec in prediction:
    #   norm = np.sqrt(np.sum([x**2 for x in vec]))
    #   print(vec, norm)
    #   norm_predict.append([x/norm for x in vec])
    # pprint(norm_predict)
