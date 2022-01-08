from app import db
from datetime import datetime

class ChatType(db.Model):
    __tablename__ = "chatTypes"
    __bind_key__ = "constants"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column("name", db.String(64))
    _opens = db.Column("opens", db.String(4))
    _closes = db.Column("closes", db.String(4))

    # referenced 
    _chats = db.relationship("Chat")

    def __init__(self, name, opens, closes):
        self.setName(name)
        self.setOpens(opens)
        self.setCloses(closes)

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getOpens(self):
        return self._opens

    def setOpens(self, opens):
        self._opens = opens

    def getCloses(self):
        return self._closes

    def setCloses(self, closes):
        self._closes = closes

    def isOpen(self):
        now = datetime.now().strftime("%H%M")
        if  now >= self.getOpens() and now < self.getCloses():
            return True
        return False

    def getOpensString(self):
        opens = self.getOpens()
        return opens[:2]+":"+opens[2:4]

    def getClosesString(self):
        closes = self.getCloses()
        return closes[:2]+":"+closes[2:4]