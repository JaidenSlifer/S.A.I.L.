import nltk
import os
import shutil

path = os.path.abspath(os.getcwd())

if(os.path.isdir(path+'\\nltk_data')):
  shutil.rmtree(path+'\\nltk_data')

os.mkdir('nltk_data')

os.environ['NLTK_DATA'] = path+'\\nltk_data'

if(os.environ['NLTK_DATA'] == path+'\\nltk_data'):
  nltk.download('wordnet')
  nltk.download('stopwords')
  nltk.download('punkt')
  nltk.download('averaged_perceptron_tagger')
  nltk.download('maxent_ne_chunker')
  nltk.download('words')
else:
  print('Failed to set environment variable')
  print(os.environ['NLTK_DATA'])