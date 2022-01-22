from app import db

class Character(db.Model):
    __tablename__ = "characters"
    __bind_key__ = "constants"
    _id = db.Column("id", db.Integer, primary_key=True)
    _name = db.Column("name", db.String(50))
    _description = db.Column("description", db.String(2000))
    _shortDescription = db.Column("shortDescription", db.String(500))
    _tag = db.Column("tag", db.String(50))
    _alliance = db.Column("alliance", db.Enum("GOOD", "BAD", "NEUTRAL"))


    # referenced
    _actionTypeAssociations = db.relationship("ActionAssociation")
    _actors = db.relationship("Actor")

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getShortDescription(self):
        return self._shortDescription

    def setShortDescription(self, shortDescription):
        self._shortDescription = shortDescription

    def getTag(self):
        return self._tag
        
    def setTag(self, tag):
        self._tag = tag

    def getAlliance(self):
        return self._alliance

    def setAlliance(self, alliance):
        self._alliance = alliance

    def getActionTypes(self):
        result = []
        for actionTypeAssociation in self._actionTypeAssociations:
            result.append(actionTypeAssociation.getActionType())
        return result
