from app import db

class EventType(db.Model):
    __tablename__ = "eventTypes"
    __bind_key__ = "constants"
    _id = db.Column("id", db.Integer, primary_key=True)
    _tag = db.Column("tag", db.String(100))
    _deadline = db.relationship("Deadline")
    _deadlineId = db.Column("deadlineId", db.ForeignKey("deadlines.id"))

    def getId(self):
        return self._id

    def setId(self, id):
        self._id = id

    def getTag(self):
        return self._tag

    def setTag(self, tag):
        self._tag = tag

    def getDeadline(self):
        return self._deadline

    