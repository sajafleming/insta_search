"""INSTA SEARCH"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from get_photos import request_insta_data
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Picture, Tag
import datetime 

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

    # to help limiting api rates, first check the db for the tag
    exists = False
    # exists = db.session.query(db.exists().where(Tag.tag == tag)).scalar()
    if exists:
        urls = Tags.query.filter_by(tag=tag).first()
        return 
    else:

        # make api call using params
        results = request_insta_data(tag)

        urls_within_time = []
        urls_all = []

        # add results to db and gather urls to display
        for i in range(len(results['data'])):

            url = results['data'][i]['images']['low_resolution']['url']
            # add all urls to store with tag in db
            urls_all.append(url)

            timestamp = results['data'][i]['created_time']
            # convert to date: "yyyy-mm-dd"
            time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')[:10]

            # p = Picture((url, time))
            # db.session.add(p)
            # db.session.commit()

            # t = Tag()
            
            # print start_time, time, end_time
            # check to see if pic in date range and add to urls to display
            if start_time == None and end_time == None:
                urls_within_time.append(url)
            if start_time == None and time < end_time:
                urls_within_time.append(url)
            if end_time == None and start_time < time:
                urls_within_time.append(url)
            if start_time < time < end_time:
                urls_within_time.append(url)

        # CHANGED TO RETURN URLS WITHIN TIME
        return jsonify(pic_urls=urls_within_time)


if __name__ == "__main__":
    # debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()

    app.run(host="0.0.0.0", port=5000)