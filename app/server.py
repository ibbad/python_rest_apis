import connexion
from flask import render_template


# create application instance
app = connexion.App(__name__, specification_dir='./')

# Read the swagger.yml file to configure endpoints
app.add_api('swagger.yml')


# Create URL route to application for "/"
@app.route('/')
def home():
    """
    This endpoint responds to base URL i.e. localhost:5000
    :return:  Rendered template for 'home.html'
    """
    return render_template('home.html')


# Run in stand alone mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
