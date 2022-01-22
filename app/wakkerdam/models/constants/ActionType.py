from app import db


class ActionType(db.Model):
    __tablename__ = "actionTypes"
    __bind_key__ = "constants"
    _id = db.Column("id", db.Integer, primary_key=True)
    _tag = db.Column("tag", db.String(50))
    _name = db.Column("name", db.String(100))
    _characters = db.relationship("ActionAssociation")
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

    def createEmptyAction(self, actor):
        tag = self._tag
        if (tag == "WRITE_NEWSPAPER_ARTICLE"):
            from app.wakkerdam.models.Action import NewspaperArticleAction
            action = NewspaperArticleAction(actor)
        elif (tag == "KILL"):
            from app.wakkerdam.models.Action import KillAction
            action = KillAction(actor, None)
        elif (tag == "SAFE"):
            from app.wakkerdam.models.Action import SafeAction
            action = SafeAction(actor, None)

        db.session.add(action)
        db.session.commit()
        

