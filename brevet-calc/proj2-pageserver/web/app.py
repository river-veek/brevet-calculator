"""
Name: River Veek
Goal: Create a simple webserver using flask.
Date: 10/20/20
"""

import flask
from flask import Flask, abort, render_template, request, send_from_directory
import os

app = Flask(__name__)


@app.route("/<name>")
def hello(name):
    # return reder_template("index.html", nameHtml=name)
    # print(f"OTHER: {name}\n")
    try:
        if name.endswith(".css"):
            return send_from_directory("static")
        else:
            # print(f"NAME={name}")
            # print(render_template(name))
            # print("RETURNING 200") 
            return render_template(name), 200
    except:
        # print(f"NAME={name}")
        # errors = ["//", "~", ".."]
        # request.environ[]
        # for error in errors:
            # if error in new:
                # print(f"ERROR={error}")
                # print("RETURNING 403")
                # page_forbidden(403)
                # abort(403)
        # print("RETURNING 404")
        # return render_template("404.html"), 400
        # page_not_found(404)
        abort(404)

@app.errorhandler(404)
def page_errors(error):
    errors = ["//", "~", ".."]
    name = request.environ['REQUEST_URI']
    # name = str(name)
    # print(("//" in name))
    for error in errors:
        # print(error)
        if error in name:
            # print("yipee")
            # abort(403)
            # page_forbidden(403)
            # return
            # print(True)
            return render_template("403.html"), 403
    return render_template("404.html"), 404


"""
@app.errorhandler(403)
def page_forbidden(error):
    return render_template("403.html"), 403
"""


if __name__ == "__main__":
    app.run(debug=True, port=5000)
