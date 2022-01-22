from app import db
from datetime import datetime
from app.wakkerdam.models.Article import Article
from app.wakkerdam.models.constants.ActionType import ActionType

class Action(db.Model):
    __tablename__ = "actions"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _actor = db.relationship("Actor")
    _actorId = db.Column("actorId", db.Integer, db.ForeignKey("actors.id"))
    _actionType = db.relationship("ActionType")
    _actionTypeId = db.Column("actionTypeId", db.Integer, db.ForeignKey("actionTypes.id"))
    _isPlayed = db.Column("isPlayed", db.Boolean)
    _timeCreated = db.Column("timeCreated", db.Integer)

    def __init__(self, actor):
        self.setActor(actor)
        self._isPlayed = False

    def create(self, timeCreated=int(round(datetime.now().timestamp()))):
        self._timeCreated = timeCreated

    def getId(self):
        return self._id

    def getActor(self):
        return self._actor

    def setActor(self, actor):
        self._actor = actor

    def getActionType(self):
        return self._actionType

    def setActionType(self, actionType):
        self._actionType = actionType

    def getTimeCreated(self):
        return self._timeCreated

    def setTimeCreated(self, timeCreated):
        self._timeCreated = timeCreated

class NewspaperArticleAction(Action):
    _article = db.relationship("Article")
    _articleId = db.Column("articleId", db.Integer, db.ForeignKey("articles.id"))
    
    def __init__(self, actor):
        Action.__init__(self, actor)
        self._actionType = ActionType.query.filter_by(_tag="WRITE_NEWSPAPER_ARTICLE").first()

    def createArticle(self, newspaper, text, publisher):
        playerCreated = self.getActor().getPlayer()
        article = Article(text, publisher, playerCreated, newspaper)
        db.session.add(article)
        db.session.commit()
        self._article = article

class TargetAction(Action):
    _target = db.relationship("Player")
    _targetId = db.Column("targetId", db.Integer, db.ForeignKey("players.id"))
    _successful = db.Column("successful", db.Boolean)
    # successful is true when the action was successful in safing, killing, etc. 

    def __init__(self, actor, target):
        Action.__init__(self, actor)
        self._target = target

class KillAction(TargetAction):
    

    def __init__(self, actor, target):
        TargetAction.__init__(self, actor, target)
        self._actionType = ActionType.query.filter_by(_tag="KILL").first()

class SafeAction(TargetAction):

    
    def __init__(self, actor, target):
        TargetAction.__init__(self, actor, target)
        self._actionType = ActionType.query.filter_by(_tag="SAFE").first()
