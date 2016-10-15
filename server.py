"""INSTA SEARCH"""

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from get_photos import request_insta_data
# from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Pic, Datetag, DateTagToPic
import datetime 
import time

app = Flask(__name__)

# required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


def date_tag_exists(date, tag):
    """Query the DB to see if the given (date, tag) pair exists in Datetags
    Returns T or F"""

    print "Date to check: ", date, ", tag to check: ", tag
    v = Datetag.query.filter(Datetag.date==date, Datetag.tag==tag).first() is not None
    print "Result of checking existance: ", v
    return v


def get_urls(tag, start_date, end_date):
    """Get all urls matching the given tag and within the given dates from
    the database

    dates are strings, format "YYYY-MM-DD"
    """
    print "Getting urls"

    pics = Pic.query.join(DateTagToPic).join(Datetag).filter(
            Datetag.tag == tag,
            Datetag.date >= start_date, Datetag.date <= end_date).all()

    return [pic.url for pic in pics]


def get_date_string(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')[:10]


@app.route('/search-insta', methods=['GET'])
def search_insta():
    
    # get instagram search params
    tag = request.args.get("tag")
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    # in case the user does not enter dates, assign times
    if not start_date:
        start_date = None
    if not end_date:
        end_date = None

    # If end date later than today's date, set it to today's date...
    today_date = get_date_string(int(time.time()))
    if today_date < end_date:
        end_date = today_date


    print tag, start_date, end_date

    # to help limiting api rates, first check the db for the date/tag pair
    # if it's not, call api and store results
    if not date_tag_exists(end_date, tag):
        print "Date tag doesn't exist"
        # need to query Insta
        results = request_insta_data(tag)

        for result in results['data']:
            # 1. check if pic's url exists in pics table. if not, create a Pic
            #    object and add it to the table.
            url = result['images']['low_resolution']['url']
            pic = Pic.query.filter_by(url=url).first()
            if not pic:
                # if not in db, insert into table
                pic = Pic(url=url)
                print "Inserting pic wit url {}".format(url)
                db.session.add(pic)
                db.session.commit()

                # pic object with that url
                pic = Pic.query.filter_by(url=url).first()

            # get pic_id from pic object
            pic_id = pic.pic_id

            # 2. pull out date from response
            timestamp = result['created_time']
            # convert to date: "yyyy-mm-dd"
            print timestamp
            date = get_date_string(int(timestamp))

            # 3. check if (result_date, tag) exists in datetags. If not, create
            #    it and get its id.
            datetag = Datetag.query.filter(Datetag.date==date, 
                        Datetag.tag==tag).first()
            if not datetag:
                datetag = Datetag(date=date, tag=tag)
                db.session.add(datetag)
                db.session.commit()

                # Datetag object with that time/tag pair
                datetag = Datetag.query.filter(Datetag.date==date, 
                        Datetag.tag==tag).first()

            # get datetag_id from Datetag object
            datetag_id = datetag.datetag_id

            print "Datetag ID: ", datetag_id, " Pic id: ", pic_id

            # 4. insert datetag_id, pic_id record into date_tag_to_pics table
            #    if it doesn't already exist.
            relationship = DateTagToPic.query.filter(DateTagToPic.pic_id==pic_id,
                DateTagToPic.datetag_id==datetag_id).first()
            if not relationship:
                print "creating relationship..."
                relationship = DateTagToPic(pic_id=pic_id,
                    datetag_id=datetag_id)
                db.session.add(relationship)
                db.session.commit()
    else:
        print "Skipping query; already have results!"
    


    # at this point, all relevant data is in the DB.
    urls = get_urls(tag, start_date, end_date)

    return jsonify(pic_urls=urls)







    # else:
    #     # make api call using params
    #     # results = request_insta_data(tag)

    #     urls_within_time = []
    #     urls_all = []

    #     # add results to db and gather urls to display
    #     for i in range(len(results['data'])):

    #         url = results['data'][i]['images']['low_resolution']['url']
    #         # add all urls to store with tag in db
    #         urls_all.append(url)

    #         timestamp = results['data'][i]['created_time']
    #         # convert to date: "yyyy-mm-dd"
    #         time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')[:10]

    #         # add results to the database
    #         # p = Pic(url)
    #         # db.session.add(p)
    #         # db.session.commit()

    #         # t = Datetag(tag, end_date, )


    #         # not sure how to add to relationship table

    #         print start_date, time, end_date
    #         # check to see if pic in date range and add to urls to display
    #         if start_date == None and end_date == None:
    #             urls_within_time.append(url)
    #         if start_date == None and time <= end_date:
    #             urls_within_time.append(url)
    #         if end_date == None and start_date <= time:
    #             urls_within_time.append(url)
    #         if start_date <= time <= end_date:
    #             urls_within_time.append(url)




if __name__ == "__main__":
    # debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()

    app.run(host="0.0.0.0", port=5000)