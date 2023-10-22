#!/usr/bin/python3
""" the route to the /states_list """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def horbit_clos_db(exception):
    """it closes the database again after each request"""
    storage.close()


@app.route('/states_list')
def horbit_states_list():
    states = list(storage.all("state").values())
    states.sort(key=lambda x: x.name)
    return render_template("8-cities_by_states.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    