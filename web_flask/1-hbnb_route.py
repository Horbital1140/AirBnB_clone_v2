#!/usr/bin/python3
"""this script Starts a Flask web application.

The web application listens on 0.0.0.0, port 5000.
Routes:
        /: it Displays 'Hello HBNB!'
        """
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def horbit():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def horbit_2():
    return 'HBNB'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
