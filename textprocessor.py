# from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag, ne_chunk
import nltk

class TextProcessor:

  def __init__(self):
    pass

  def filterText(self, text: str, company_name):
    # Remove special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Apply POS tagging
    pos_tags = pos_tag(tokens)

    # Perform named entity recognition
    chunks = ne_chunk(pos_tags)

    # Extract named entities
    entities = [(chunk[0][0], chunk.label()) for chunk in chunks if hasattr(chunk, 'label')]
    print(chunks)
    print(entities)
    return entities
  
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
