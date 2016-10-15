"""Models and database functions. Database named picturesdb"""

from flask_sqlalchemy import SQLAlchemy
import os

# create instance of sqlalchemy db
db = SQLAlchemy()

##############################################################################
# Define data model

class Pic(db.Model):
    """Picture class for how to store pics in database"""

    __tablename__ = "pics"

    pic_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    url = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Pics pic_id=%s url=%s>"
                % (self.pic_id, self.url))

class Datetag(db.Model):
    """DateTag pairs with corresponding urls"""

    __tablename__ = "datetags"

    datetag_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date = db.Column(db.String(100), nullable=False)
    tag = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Datetag datetag_id=%s date=%s> tag=%s"
                % (self.datetag_id, self.date, self.tag))

class DateTagToPic(db.Model):
    """Relationship table"""

    __tablename__ = "date_tags_to_pics"

    relationship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    datetag_id = db.Column(db.Integer, db.ForeignKey('datetags.datetag_id'), nullable=False)
    datetag = db.relationship('Datetag',
        backref=db.backref('datetags', lazy='dynamic'))

    pic_id = db.Column(db.Integer, db.ForeignKey('pics.pic_id'), nullable=False)
    pic = db.relationship('Pic',
        backref=db.backref('pics', lazy='dynamic'))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<DateTagToPic datetag_id=%s pic_id=%s>"
                % (self.datetag_id, self.pic_id))
        
##############################################################################
# Helper functions

# connect to flask instance
def connect_to_db(app):
    """Connect the database to Flask app."""

    print "Connecting DB"
    # Configure to PSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else 'postgresql:///picturesdb'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    if not db.engine.dialect.has_table(db.engine.connect(), "pics"):
        db.create_all()
    db.session.commit()

if __name__ == "__main__":
    # run module interactively to work with db directly 
    # db.create_all()

    from server import app
    connect_to_db(app)
    print "Connected to DB."