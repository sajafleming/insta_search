"""INSTA SEARCH"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from flask_debugtoolbar import DebugToolbarExtension
# from model import connect_to_db, db, Picture


app = Flask(__name__)

# required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


# raise an error in case there is an undefined variable in Jinja2, otherwise,
# it will fail silently
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/', methods=['POST'])
def get_credentials_for_search():

    tag = request.form['tag']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    print "here they are, successfully on the backend!"
    print tag, start_date, end_date
    return tag, start_date, end_date


if __name__ == "__main__":
    # debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()