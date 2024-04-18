from flask import Flask, request, jsonify, render_template, redirect, url_for
from scraper import ArticleScraper
from textprocessor import TextProcessor
from model import SentimentModel
import math
import re
import time

def sigmoid(x):
  return 1 / (1 + math.exp(-1 * x))

class ServerController:
    
    def __init__(self, name):
        self.app = Flask(name, static_folder='static', template_folder='templates')
        self.scraper = ArticleScraper()
        self.processor = TextProcessor()
        self.model = SentimentModel()

    def add_endpoint(self, endpoint: str, endpoint_name: str, handler, methods=None):
        self.app.add_url_rule(rule=endpoint, endpoint=endpoint_name, view_func=handler, methods=methods)

    def init_routes(self):
    #    self.add_endpoint('/', 'index', self.index, methods=['GET', 'POST'])
    #    self.add_endpoint('/display', 'display', self.display)

        self.add_endpoint('/', 'index', self.index, methods=['GET', 'POST'])
        self.add_endpoint('/analyze', 'analyze', self.analyze, methods=['POST'])  # Add this line
        self.add_endpoint('/display', 'display', self.display)

    def run(self, debug: bool):
        self.app.run(debug=debug)
    
    def index(self):
        # Here, you can add any logic needed for initial page load or form submission handling
        return render_template('index.html')

    def analyze(self):
        try:
            data = request.get_json()
            ticker = data['ticker']
            sentiment, confidence, influential_article = self.analyzeSentiment(ticker)
            if(sentiment is None):
                time.sleep(1)
            redirect_url = url_for('display', ticker=ticker, sentiment=sentiment, confidence=confidence, influential_article=influential_article)
            return jsonify({'redirect_url': redirect_url})
        except Exception as e:
            print(e)  # For debugging
            return jsonify({'error': 'Failed to process request'}), 500

    
    def display(self):
        ticker = request.args.get('ticker', default='ABCD')
        sentiment = request.args.get('sentiment', default='Neutral')
        confidence = request.args.get('confidence', default=0)  # Assuming it's passed as a query parameter
        influential_article = request.args.get('influential_article', default='')  # Assuming it's passed as a query parameter

        return render_template('display.html', ticker=ticker, sentiment=sentiment, confidence=confidence, influential_article=influential_article)

    def compileSentiment(self, predictions):
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

        return [neg, neu, pos]

    def results(self, compiled_sent):
        [neg, neu, pos] = compiled_sent
        if(pos > neg):
            result = 'Positive'
            confidence = sigmoid((pos - neg) / neu)
        elif(neg > pos):
            result = 'Negative'
            confidence = sigmoid((neg - pos) / neu)
        else:
            result = 'Neutral'
            confidence = neu#sigmoid(neu - pos)

        return result, confidence
    
    def analyzeSentiment(self, ticker):

        # initialize objects
        self.model.load_model('both-culled-model-e20')
        self.scraper.initializeScraper(ticker)

        # main processing chain

        # scrape relevant data from site
        titles, links, company = self.scraper.getAll()
        # titles = titles[:5]
        # links = links[:5]
        # article_info = []
        # for i, title in enumerate(titles):
        #     if(re.search('.*youtube.*', links[i]) is not None): continue
        #     article_info.append({
        #         'title': title,
        #         'link': links[i]
        #     })
        from pprint import pprint
        # # process article titles and text
        # article_bodies = []
        # for article in article_info:
        #     body = self.scraper.scrapeArticle(article['link'])
        #     sentences = self.processor.splitIntoSentences(body)
        #     #filtered_sentences = self.processor.filterText(sentences, company)
        #     pprint(sentences)
        #     # filtered_sentences = []
        #     # for sentence in sentences:
        #     #     if(sentence.isalnum()):
        #     #         filtered_sentences.append(sentence)
        #     # print('filtered sentences')
        #     # pprint(filtered_sentences)
        #     processed_body = self.processor.processText(sentences) # temp
        #     processed_title = self.processor.processText(article['title'])
        #     processed_all = processed_title.extend(processed_body)
        #     print('processed all')
        #     pprint(processed_all)
        #     article_bodies.append({
        #         'title': article['title'],
        #         'text': processed_all
        #     })

        # # predict sentiment
        # article_sentiment = []
        # for article in article_bodies:
        #     predictions = self.model.predict(article['text'])
        #     compiled = self.compileSentiment(predictions)
        #     article_sentiment.append({
        #         'title': article['title'],
        #         'sentiment': compiled
        #     })

        processed_titles = self.processor.processText(titles)
        predictions = self.model.predict(processed_titles)
        article_sentiment = []
        for i, title in enumerate(titles):
            article_sentiment.append({
                'title': title,
                'sentiment': predictions[i]
            })

        final_compiled = self.compileSentiment(predictions)
        
        # compile and compute results
        #sents = [article['sentiment'] for article in article_sentiment]
        #final_compiled = self.compileSentiment(sents)
        final_class, final_conf = self.results(final_compiled)

        # compute most influential article title
        if(final_class == 'Positive'):
            max_pos = 0
            for article in article_sentiment:
                val_pos = article['sentiment'][2]
                if(max_pos < val_pos):
                    max_pos = val_pos
                    most_influential = article['title']
        elif(final_class == 'Negative'):
            max_neg = 0
            for article in article_sentiment:
                val_neg = article['sentiment'][0]
                if(max_neg < val_neg):
                    max_neg = val_neg
                    most_influential = article['title']
        else:
            most_influential = ''
        
        self.scraper.closeScraper()
        return final_class, round(final_conf * 100), most_influential

# run this using the cli
# python sail.py run -d

# if __name__ == "__main__":
#     app_controller = ServerController(__name__)
#     app_controller.init_routes()
#     app_controller.run(debug=True)
