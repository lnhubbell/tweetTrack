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


class Tweet200(db.Model):
    __tablename__ = 'Tweet200'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(15), nullable=False)
    text = db.Column(db.String(180), nullable=False)
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.Date, nullable=False)
    hashtags = db.Column(db.String(140))
    city = db.Column(db.String(100))


class TweetTest(db.Model):
    __tablename__ = 'TweetTest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(15), nullable=False)
    text = db.Column(db.String(180), nullable=False)
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.Date, nullable=False)
    hashtags = db.Column(db.String(140))


class TweetTest2(db.Model):
    __tablename__ = 'TweetTest2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(15), nullable=False)
    text = db.Column(db.String(180), nullable=False)
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    created_at = db.Column(db.Date, nullable=False)
    hashtags = db.Column(db.String(140))


class UserResponse(db.Model):
    __tablename__ = 'UserResponse'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    screen_name = db.Column(db.String(15), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    guess_location = db.Column(db.String(25), nullable=False)

    def __init__(self, screen_name, is_correct, guess_location):
        self.screen_name = screen_name
        self.is_correct = is_correct
        self.guess_location = guess_location