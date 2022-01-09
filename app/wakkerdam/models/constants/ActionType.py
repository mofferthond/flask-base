from app import db

class ActionType(db.Model):
    __tablename__ = "actionTypes"
    __bind_key__ = "constants"
    _id = db.Column("id", db.Integer, primary_key=True)
    _name = db.Column("name", db.String(100))
    _character = db.relationship("Character")
    _characterId = db.Column("characterId", db.Integer, db.ForeignKey('characters.id'))
    _opens = db.Column("opens", db.String(4))
    _closes = db.Column("closes", db.String(4))

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getCharacter(self):
        return self._character

    def getOpens(self):
        return self._opens

    def getCloses(self):
        return self._closes
