from flask import Flask, request, jsonify, render_template, redirect, url_for

class ServerController:
    
    def __init__(self, name):
        self.app = Flask(name, static_folder='static', template_folder='templates')

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
            sentiment = "Positive"  # integrate actual sentiment analysis logic
            redirect_url = url_for('display', ticker=ticker, sentiment=sentiment)
            return jsonify({'redirect_url': redirect_url})
        except Exception as e:
            print(e)  # For debugging
            return jsonify({'error': 'Failed to process request'}), 500


    
    def display(self):
        ticker = request.args.get('ticker', default='ABCD')
        sentiment = request.args.get('sentiment', default='Neutral')
        confidence = request.args.get('confidence', default=0)  # Assuming it's passed as a query parameter
        influential_article = request.args.get('article', default='')  # Assuming it's passed as a query parameter

        return render_template('display.html', ticker=ticker, sentiment=sentiment, confidence = confidence, influential_article=influential_article)

# run this using the cli
# python sail.py run -d

# if __name__ == "__main__":
#     app_controller = ServerController(__name__)
#     app_controller.init_routes()
#     app_controller.run(debug=True)
