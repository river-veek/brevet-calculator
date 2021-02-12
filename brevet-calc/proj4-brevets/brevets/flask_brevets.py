"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

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
    # distance = request.args.get('distance', "", type=float)
    # begin_time = request.args.get('begin_time', type=str)
    # begin_date = request.args.get('begin_date', type=str)
    # FIXME: Need to get brevet dist and control dist
    # maybe "name='distance'" on line 59 of calc.html
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    open_time = acp_times.open_time(km, 200, arrow.now().isoformat())
    close_time = acp_times.close_time(km, 200, arrow.now().isoformat())
    # full_date = begin_date + begin_time
    # iso_format = arrow.get(full_date, 'YYYY-MM-DD HH:mm')
    # open_time = acp_times.open_time(km, dist, iso_format)
    # close_time = acp_times.close_time(km, dist, iso_format)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
