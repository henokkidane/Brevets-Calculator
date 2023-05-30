"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import pymongo
import os
from pymongo import MongoClient

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###
def insert(request):
    app.logger.debug("Hey we submitted")
    client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'],27017)
    if not request:
        return 403
    formtable = request.form['Controls']
    if formtable == "[]":
        return 403
    else:
        table = {
            'Start': request.form['Start'],
            'MaxDist': request.form['MaxDist'],
            'Checkpoints': request.form['Controls']
            }
        mdb = client.mydb
        mdb.posts.insert_one(table)
        client.close()
        return 200


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
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
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    max = request.args.get('max',999,type=float)
    date = request.args.get('date',type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug(f"max_dist= {max}")
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, max, arrow.get(date)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, max, arrow.get(date)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/submit",methods=['POST'])
def submit():
    return insert(request)


@app.route("/display")
def display():
    app.logger.debug("Hey we're trying to display")
    client = MongoClient('mongodb://'+os.environ['MONGODB_HOSTNAME'],27017)
    if not client:
        app.logger.debug("Client is no?")
        raise Exception('bad connection with db')
        return flask.jsonify(status=500,brevets={"Start":"","MaxDist":"", "Checkpoints":""})
    mdb = client.mydb
    table = mdb.posts.find_one(sort=[('_id', pymongo.DESCENDING)])
    if not table:
        raise Exception('table of controle times not found')
        return flask.jsonify(status=404,brevets={"Start":"","MaxDist":"", "Checkpoints":""})
    Start = table['Start']
    MaxDist = table['MaxDist']
    Checkpoints = table['Checkpoints']
    client.close()
    return flask.jsonify(status=200,brevets={"Start":Start,"MaxDist":MaxDist, "Checkpoints":Checkpoints})

    
#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
