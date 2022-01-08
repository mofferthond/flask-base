from app import db

class Localization(db.Model):
    __tablename__ = "localization"
    __bind_key__ = "constants"
    tag = db.Column(db.String, primary_key=True)
    text = db.Column(db.String, primary_key=True)
    language = db.Column(db.String, primary_key=True)