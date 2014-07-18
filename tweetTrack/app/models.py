from tweetTrack.app import db


class Tweet(db.Model):
    __tablename__ = 'Tweet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(15), nullable=False)
    text = db.Column(db.String(140), nullable=False)
    sw_latitude = db.Column(db.Float, nullable=False)
    sw_longitude = db.Column(db.Float, nullable=False)
    ne_latitude = db.Column(db.Float, nullable=False)
    ne_longitude = db.Column(db.Float, nullable=False)
    time_zone = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    hashtags = db.Column(db.String(140))
    country_code = db.Column(db.String(10))
