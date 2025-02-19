import sys
import os
import shutil
import time
from server import ServerController
from textprocessor import TextProcessor
from scraper import ArticleScraper
from model import SentimentModel

path = os.path.abspath(os.getcwd())

def compileSentiment(predictions):
  neg = 0
  neu = 0
  pos = 0
  for prediction in predictions:
    neg += prediction[0]
    neu += prediction[1]
    pos += prediction[2]
  
  neg /= len(predictions)
  neu /= len(predictions)
  pos /= len(predictions)

  result = (pos - neg) * neu

  return [neg, neu, pos]

help = """
  python sail.py [-h] <command> [<args>]

  commands:
    run [<args>]: starts a Flask development server
    train <data_dir> [<args>]: trains the model using the dataset in given directory name
    scraper <ticker> [-l | -t | -s <article_url>]: tests the scraper
    
  args:
    run
      -d: enable debug mode on flask server
    train
      -s <save_dir>: save model when finished training
"""
if __name__ == '__main__':
  args = sys.argv[1:]
  if(args[0] == '-h'):
    print(help)
  elif(args[0] == 'run'):
    debug = False
    if(len(args) > 1 and args[1] == '-d'):
      debug = True
    server = ServerController('sail')
    server.init_routes()
    server.run(debug)
    quit = True
  elif(args[0] == 'train'):
    epochs = 15
    data_path = ''
    if(len(args) > 1 and not args[1].startswith('-')):
      data_path = os.path.join(path, args[1])
    else:
      print("Missing Data Path")
      exit(1)

    save_model = False
    save_path = ''
    if(len(args) > 2 and args[2] == '-s'):
      save_model = True
      if(len(args) > 3):
        save_path = args[3]
      else:
        print("Incorrect Arguments")
        exit(1)
    # if(os.path.isdir(save_path)):
    #   shutil.rmtree(save_path)
    #   os.mkdir(save_path)
    # else:
    #   os.mkdir(save_path)
    model = SentimentModel()
    model.train(data_path, save_model=save_model, save_path=save_path)
    model.test_predict()
  elif(args[0] == 'predict'):
    model = SentimentModel()
    model.load_model(args[1])
    model.test_predict()
    pass
  elif(args[0] == 'scraper'):
    if len(args) < 2:
      print("Usage: scraper <ticker> [-l | -t | -s <article_url>]")
      exit(1)

    ticker = args[1]
    scraper = ArticleScraper()
    scraper.initializeScraper(ticker)

    if '-l' in args:
      links = scraper.getArticleLinks()
      for link in links:
        print(link)
    
    elif '-t' in args:
      titles = scraper.getArticleTitles()
      for title in titles:
        print(title)
    elif '-s' in args:
      article_index = args.index('-s') + 1
      if article_index < len(args):
        article_text = scraper.scrapeArticle(args[article_index])
        processor = TextProcessor()
        sentences = processor.splitIntoSentences(article_text)
        for sentence in sentences:
          print(sentence)
    else:
      print("Article URL required after -s")
      
    scraper.closeScraper()
  elif(args[0] == 'test'):
    if(len(args) > 1): 

      # create objects
      scraper = ArticleScraper(args[1])
      processor = TextProcessor()
      model = SentimentModel()

      # initialize objects
      model.load_model('both-culled-model-e20')
      scraper.initializeScraper()

      # main processing chain
      titles, links = scraper.getTitlesLinks()
      processed_titles = processor.processText(titles)
      predictions = model.predict(processed_titles)
      
      # compiled = []
      # for link in links[:5]:
      #   body = scraper.scrapeArticle(link)
      #   processed_body = processor.processText(body)
        
      #   predict_body = model.predict(processed_body)
      #   compiled.append(compileSentiment(predict_body))
        
      compiled = compileSentiment(predictions)

      for i, val in enumerate(predictions):
        print(titles[i])
        print(processed_titles[i])
        print(val)
        print()

      print(compiled)
      #print(compileSentiment(compiled))
      scraper.closeScraper()
    else:
      print("Syntax Error: python sail.py test <ticker>")
  else:
    print("Command not recognized")
