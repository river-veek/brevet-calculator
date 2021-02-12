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
from flask_restful import Resource, Api
import os

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

api = Api(app)

# FIXME: CHANGE BACK BEFORE SUBMISSION
# OLD IP:
client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
# client = MongoClient("172.26.0.2", 27017)
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

"""
from bson import ObjectId
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
res = json.dumps(DBResultMessage, cls=JSONEncoder)
"""

class ListAll(Resource):
    def get(self):
        # data = db.tododb.find()
        # times = [str(time) for time in db.tododb.find()]
        # valids = ['km', 'open_time', 'close_time']
        # num = int(request.args.get('top', default=0, type=int))
        times = []
        # times.append("NUM!!!: " + str(num))
        # data = db.tododb.find()
        #for i in range(num):
        for time in db.tododb.find():
            times.append("km: " + str(time['km']))
            times.append("open_time: " + time['open_time'])
            times.append("close_time: " + time['close_time'])
        return {"Times": times}
api.add_resource(ListAll, '/listAll', '/listAll/json')

class ListOpenOnly(Resource):
    def get(self):
        # data = db.tododb.find()
        # times = [str(time) for time in db.tododb.find()]
        # valids = ['km', 'open_time', 'close_time']
        times = []
        num = int(request.args.get('top', default=0, type=int))
        data = db.tododb.find()
        if num == 0:
            num = data.count()
        for i in range(num):
        # for time in db.tododb.find():
            times.append("km: " + str(data[i]['km']))
            times.append("open_time: " + data[i]['open_time'])
            # times.append("close: " + time['close_time'])
        # times = {"Times": times}
        # return times
        return {"Times": times}
api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/json')

class ListCloseOnly(Resource):
    def get(self):
        # data = db.tododb.find()
        # times = [str(time) for time in db.tododb.find()]
        # valids = ['km', 'open_time', 'close_time']
        times = []
        num = int(request.args.get('top', default=0, type=int))
        data = db.tododb.find()
        if num == 0:
            num = data.count()
        #for time in db.tododb.find():
        for i in range(num):
            times.append("km: " + str(data[i]['km']))
            # times.append("open: " + time['open_time'])
            times.append("close_time: " + data[i]['close_time'])
        # times = {"Times": times}
        # return times
        return {"Times": times}
api.add_resource(ListCloseOnly, '/listCloseOnly', '/listCloseOnly/json')

class ListAllCSV(Resource):
    def get(self):
        ret = ""
        ret += "km,open_time,close_time\n"
        for time in db.tododb.find():
            ret += (str(time['km']) + "," + time['open_time'] + "," + time['close_time'])
            ret += "\n"
        return flask.make_response(ret)
api.add_resource(ListAllCSV, '/listAll/csv')

class ListOpenOnlyCSV(Resource):
    def get(self):
        ret = ""
        ret += "km,open_time\n"
        for time in db.tododb.find():
            ret += (str(time['km']) + "," + time['open_time'])
            ret += "\n"
        return flask.make_response(ret)
api.add_resource(ListOpenOnlyCSV, '/listOpenOnly/csv')

class ListCloseOnlyCSV(Resource):
    def get(self):
        ret = ""
        ret += "km,close_time\n"
        for time in db.tododb.find():
            ret += (str(time['km']) + "," + time['close_time'])
            ret += "\n"
        return flask.make_response(ret)
api.add_resource(ListCloseOnlyCSV, '/listCloseOnly/csv')

"""
class ListAllKjson(Resource):
    def get(self):
        # data = db.tododb.find()
        # times = [str(time) for time in db.tododb.find()]
        # valids = ['km', 'open_time', 'close_time']
        times = []
        # data = db.tododb.find()
        # for i in range(num):
        num = int(request.args.get("top", default=0, type=int))
        for time in db.tododb.find().limit(num):
            times.append("km: " + str(time['km']))
            times.append("open_time: " + time['open_time'])
            times.append("close_time: " + time['close_time'])
        return {"Times": times}
api.add_resource(ListAllKjson, '/listAll/json?top=')

class ListAllKcsv(Resource):
    def get(self, num):
        # data = db.tododb.find()
        # times = [str(time) for time in db.tododb.find()]
        # valids = ['km', 'open_time', 'close_time']
        ret = "" 
        ret += "km,open_time,close_time\n"
        # data = db.tododb.find()
        for time in db.tododb.find(num):
            # for i in range(num):
            ret += (str(time['km']) + "," + time['open_time'] + "," + time['close_time'])
            ret += "\n"
        return flask.make_response(ret)
api.add_resource(ListAllKcsv, '/listAll/csv?top=<int:num>')
"""

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
# @app.route("/listAll", methods=['POST'])
# @app.route("/_display", methods=['POST'])
# class Display(Resource):
@app.route("/_display", methods=['POST'])
def display():
    print("********IN DISPLAY IN PY*********")
    data = db.tododb.find()
    items = [item for item in data]
    return flask.render_template("display.html", items=items)
# api.add_resource(Display, '/_display')

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
    app.run(port=80, host="0.0.0.0")
