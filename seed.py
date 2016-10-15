# file to seed postgres database
from sqlalchemy import func
from model import Picture
from model import connect_to_db, db
from server import app

def load_pictures():
    """Load pictures into database."""

    print "Picturess"

    # # delete all rows in table, so if we need to run this a second time,
    # # we won't be trying to add duplicate pics
    # User.query.delete()

    # # Read u.user file and insert data
    # for row in open("seed_data/u.user"):
    #     row = row.rstrip()
    #     user_id, age, gender, occupation, zipcode = row.split("|")

    #     user = User(user_id=user_id,
    #                 age=age,
    #                 zipcode=zipcode)

    #     # We need to add to the session or it won't ever be stored
    #     db.session.add(user)

    # # Once we're done, we should commit our work
    # db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()
