"""INSTA SEARCH"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from get_photos import request_insta_data
# from flask_debugtoolbar import DebugToolbarExtension
# from model import connect_to_db, db, Picture

app = Flask(__name__)

# required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# raise an error in case there is an undefined variable in Jinja2, otherwise,
# it will fail silently
# app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/search-insta', methods=['GET'])
def search_insta():
    
    # get instagram search params
    tag = request.args.get("tag")
    start_time = request.args.get("start")
    end_time = request.args.get("end")

    print tag, start_time, end_time

    # make api call using params
    results = request_insta_data(tag)

    return jsonify(pic_urls=results)


if __name__ == "__main__":
    # debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()