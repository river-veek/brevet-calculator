"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request, redirect, url_for
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

# FIXME: CHANGE BACK BEFORE SUBMISSION
# OLD IP:
    # os.environ['DB_PORT_27017_TCP_ADDR']
client = MongoClient("172.17.0.2", 27017)
db = client.tododb


###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

# submit ACP brevet data
@app.route("/_submit")
def submit():
    # print("TEST in flask")
    km = request.args.get('km', "", type=float)
    open_time = request.args.get("open_time", "", type=str)
    close_time = request.args.get("close_time", "", type=str)
    data = {'km': km, 
            'open_time': open_time,
            'close_time': close_time
            }
    print("DATA:", data)
    db.tododb.insert_one(data)
    return flask.jsonify(km=km)

# display ACP brevet data
@app.route("/_display")
def display():
    print("********IN DISPLAY IN PY*********")
    data = db.tododb.find()
    items = [item for item in data]
    return flask.render_template("display.html", items=items)


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    # request all needed args (names outlined in HTML file)
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', "", type=float)
    distance = request.args.get("distance", "", type=float)
    begin_time = request.args.get("begin_time", "", type=str)
    begin_date = request.args.get("begin_date", "", type=str)
    
    # convert time into ISO 8601 STRING 
    new_time = begin_date + "T" + begin_time + ":00"
    
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    
    # call funcs
    open_time = acp_times.open_time(km, distance, new_time)
    close_time = acp_times.close_time(km, distance, new_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
