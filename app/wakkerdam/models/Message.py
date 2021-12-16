from app import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "messages"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _chatter = db.relationship("Chatter")
    _chatterId = db.Column("chatterId", db.Integer, db.ForeignKey("chatters.id"))
    _text = db.Column("text", db.String(500))
    _timestamp = db.Column("timestamp", db.Integer)
    _replyToId = db.Column("replyToId", db.Integer, db.ForeignKey("messages.id"))
    _replyTo = db.relationship("Message", remote_side=[_id])

    # referenced
    _replies = db.relationship("Message", remote_side=[_replyToId])

    def __init__(self, chatter, text, replyTo=None, timestamp=int(round(datetime.now().timestamp()))):
        self.setChatter(chatter)
        self.setText(text)
        self.setTimestamp(timestamp)
        if replyTo != None:
            self.setReplyTo(replyTo)


    def getId(self):
        return self._id

    def getChatter(self):
        return self._chatter

    def setChatter(self, chatter):
        self._chatter = chatter

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text

    def getTimestamp(self):
        return self._timestamp

    def setTimestamp(self, timestamp):
        self._timestamp = timestamp

    def getReplyTo(self):
        return self._replyTo

    def setReplyTo(self, replyTo):
        self._replyTo = replyTo

    def getReplies(self):
        return self._replies