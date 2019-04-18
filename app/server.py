from flask import Flask, render_template

# Create flask app instance
app = Flask(__name__, template_folder='templates')

# Create URL route to application for "/"
@app.route('/')
def home():
    """
    This endpoint responds to base URL i.e. localhost:5000
    :return:  Rendered template for 'home.html'
    """
    return render_template('home.html')