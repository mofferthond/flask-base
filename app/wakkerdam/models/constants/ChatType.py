from app import db
from datetime import datetime

class ChatType(db.Model):
    __tablename__ = "chatTypes"
    __bind_key__ = "constants"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column("name", db.String(64))
    _deadline = db.relationship("Deadline")
    _deadlineId = db.Column("deadlineId", db.ForeignKey("deadlines.id"))

    # referenced 
    _chats = db.relationship("Chat")

    def __init__(self, name, deadline):
        self.setName(name)
        self.setDeadline(deadline)


    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getDeadline(self):
        return self._deadline

    def setDeadline(self, deadline):
        self._deadline = deadline