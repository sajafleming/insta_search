"""Models and database functions"""
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


db = SQLAlchemy()

##############################################################################
# Model definitions

class Picture(db.Model):
    """Picture class for how to store pics in database"""

    __tablename__ = "pictures"

    # FIX BELOW

    pic_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    tag = db.Column(db.String(200), nullable=False)
    tag_date = db.Column(db.DateTime, nullable=False)
    pic_url = db.Column(db.String(600), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Picture pic_id=%s tag=%s tag_date=%s pic_url=%s>"
                % (self.pic_id, self.tag, self.tag_date, self.pic_url))
               #add in datetime for released_at later


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."