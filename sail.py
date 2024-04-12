import sys
import os
import shutil
from server import ServerController
from textprocessor import TextProcessor
from model import SentimentModel
from scraper import ArticleScraper

path = os.path.abspath(os.getcwd())

help = """
  python sail.py [-h] <command> [<args>]

  commands:
    run [<args>]: starts a Flask development server
    train <data_dir> [<args>]: trains the model using the dataset in given directory name
    scraper: tests the scraper
    
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
    if(len(args) > 2 and args[2] == '-s'):
      save_path = ''
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
  elif(args[0] == 'predict'):
    model = SentimentModel()
    model.load_model(args[1])
    model.predict()
  elif(args[0] == 'scraper'):
    if len(args) < 2:
      print("Usage: scraper <ticker> [-l | -t | -s <article_url>]")
      exit(1)

    ticker = args[1]
    scraper = ArticleScraper(ticker, "https://finviz.com/quote.ashx?t={ticker}&p=d")
    scraper.initializeScraper()

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
        print(article_text)
      else:
        print("Article URL required after -s")
      
    scraper.closeScraper()
  else:
    print("Command not recognized")