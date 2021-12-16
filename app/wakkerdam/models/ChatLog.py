from app import db
from datetime import datetime

class ChatLog(db.Model):
    __tablename__ = "chatlogs"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _chatter = db.relationship("Chatter")
    _chatterId = db.Column("chatterId", db.Integer, db.ForeignKey("chatters.id"))
    _timestamp = db.Column(db.Integer)

    def __init__(self, chatter):
        self.setChatter(chatter)
        timestamp = int(round(datetime.now().timestamp()))
        self.setTimestamp(timestamp)

    def getId(self):
        return self._id

    def getChatter(self):
        return self._chatter

    def setChatter(self, chatter):
        self._chatter = chatter

    def getTimestamp(self):
        return self._timestamp

    def setTimestamp(self, timestamp):
        self._timestamp = timestamp