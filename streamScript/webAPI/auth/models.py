from streamScript.webAPI import db


class APIKey(db.Model):
    __tablename__ = 'APIKey'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(100), nullable=False, unique=True)

    def __init__(self, key):
        self.key = key