# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class TextProcessor:

  def __init__(self):
    pass

  def filterText(self):
    pass
  
  # tokenize, lemmatize text
  # perhaps do nltk vader for lexical sentiment processing as additional info for the model
  # might help the model train faster
  def processText(self, data: list[str]):
    processed = []
    for text in data:
      text = re.sub(r'[^a-zA-Z\s]', '', text)
      tokens = text.lower().split()

      filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

      lemmatizer = WordNetLemmatizer()
      lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
      processed.append(' '.join(lemmatized_tokens))
    return processed