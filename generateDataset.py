import os
import shutil
from textprocessor import TextProcessor
import random

path = os.path.abspath(os.getcwd())
file_path = path+'\\FinancialPhraseBank-v1.0\\Sentences_50Agree.txt'
dataset_path = path+'\\train_data_culled_both'

# reset dataset directory
if(os.path.isdir(dataset_path)):
  shutil.rmtree(dataset_path)
  os.mkdir(dataset_path)
else:
  os.mkdir(dataset_path)


# key to encode and decode sentiment annotations
classify = {
  'negative': 0,
  'neutral': 1,
  'positive': 2
}


counts = [0, 0, 0]
tp = TextProcessor()
with open(file_path, 'r', encoding='utf-8') as fpb:
  os.mkdir(dataset_path+'\\positive')
  os.mkdir(dataset_path+'\\neutral')
  os.mkdir(dataset_path+'\\negative')
  for line in fpb.readlines():
    tokens = line.split('@')
    text = tokens[0]
    [text] = tp.processText([text])
    sent = tokens[1].strip('\n')
    if(not (sent == 'neutral' and random.randint(0,1) == 1) and not (sent == 'positive' and random.randint(0,2) == 1) and len(text) > 0): # cull a proportion of neutral lines
      f = open(f'{dataset_path}\\{sent}\\{counts[classify[sent]]}.txt', 'w+')
      f.write(text)
      counts[classify[sent]] += 1

    