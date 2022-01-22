from app import db

class ActionAssociation(db.Model):
    __tablename__ = "actionAssociations"
    __bind_key__ = "constants"

    _character = db.relationship("Character")
    _characterId = db.Column("characterId", db.Integer, db.ForeignKey("characters.id"), primary_key=True)
    _actionType = db.relationship("ActionType")
    _actionTypeId = db.Column("actionTypeId", db.Integer, db.ForeignKey("actionTypes.id"), primary_key=True)

    def getCharacter(self):
        return self._character

    def getActionType(self):
        return self._actionType