"""Models and database functions. Database named picturesdb and table 
name pictures"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create instance of sqlalchemy db
db = SQLAlchemy()

##############################################################################
# Define data model

class Picture(db.Model):
    """Picture class for how to store pics in database"""

    __tablename__ = "pictures"

    # pic_id is the id from instagram
    pic_id = db.Column(db.Integer, primary_key=True)
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

# connect to flask instance
def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to PSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///picturesdb'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # run module interactively to work with db directly 


    from server import app
    connect_to_db(app)
    print "Connected to DB."