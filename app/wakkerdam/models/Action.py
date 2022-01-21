from app import db

class Action(db.Model):
    __tablename__ = "actions"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _actor = db.relationship("Actor")
    _actorId = db.Column("actorId", db.Integer, db.ForeignKey("actors.id"))
    _actionType = db.relationship("ActionType")
    _actionTypeId = db.Column("actionTypeId", db.Integer, db.ForeignKey("actionTypes.id"))
    _timeCreated = db.Column("timeCreated", db.Integer)

    def __init__(self, actor, actionType, timeCreated=int(round(datetime.now().timestamp()))):
        self.setActor(actor)
        self.setActionType(actionType)
        self.setTimeCreated(timeCreated)

    def getId(self):
        return self._id

    def getActor(self):
        return self._actor

    def setActor(self, actor):
        self._actor = actor

    def getActiontype(self):
        return self._actionType

    def setActiontype(self, actionType):
        self._actionType = actionType

    def getTimecreated(self):
        return self._timeCreated

    def setTimecreated(self, timeCreated):
        self._timeCreated = timeCreated
