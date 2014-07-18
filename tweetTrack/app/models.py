from tweetTrack.app import db


class Tweet(db.Model):
    __tablename__ = 'Tweet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(15), nullable=False)
    text = db.Column(db.String(140), nullable=False)
    location_lat = db.Column(db.Float, nullable=False)
    location_lng = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    hashtags = db.Column(db.String(140))
