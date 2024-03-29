from flask import Flask, render_template, request

class ServerController:
    
    def __init__(self, name):
        self.app = Flask(name, static_folder='static', template_folder='templates')

    def add_endpoint(self, endpoint: str, endpoint_name: str, handler, methods=None):
        self.app.add_url_rule(rule=endpoint, endpoint=endpoint_name, view_func=handler, methods=methods)

    def init_routes(self):
        self.add_endpoint('/', 'index', self.index, methods=['GET', 'POST'])
        self.add_endpoint('/display', 'display', self.display)

    def run(self, debug: bool):
        self.app.run(debug=debug)

    def index(self):
        # Here, you can add any logic needed for initial page load or form submission handling
        return render_template('index.html')

    def display(self):
        # If you're expecting text input from a form, ensure the form's name attribute matches
        if request.method == 'POST':
            text_input = request.form.get('text', '')  # Assuming input has name='text'
            print(text_input)
        ticker = "ABCD"  # This is just a placeholder
        # You can pass variables to the template to be rendered dynamically
        return render_template('display.html', ticker=ticker)

if __name__ == "__main__":
    app_controller = ServerController(__name__)
    app_controller.init_routes()
    app_controller.run(debug=True)
