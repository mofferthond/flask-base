from app import db
from datetime import datetime

class Deadline(db.Model):
    __tablename__ = "deadlines"
    __bind_key__ = "constants"

    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _opens = db.Column("opens", db.Integer)
    _closes = db.Column("closes", db.Integer)
    _description = db.Column("description", db.String(100))

    def __init__(self, opens, closes):
        self._opens = opens
        self._closes = closes

    def isOpen(self):
        now = int(datetime.now().strftime("%H%M"))
        if  now >= self._opens and now < self._closes:
            return True
        return False

    def getOpensString(self):
        opens = str(self._opens)
        return opens[:2]+":"+opens[2:4]

    def getClosesString(self):
        closes = str(self._closes)
        return closes[:2]+":"+closes[2:4]