from app import db
import random
from app.wakkerdam.models.constants.EventType import EventType

class Event(db.Model):
    __tablename__ = "events"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _eventType = db.relationship("EventType")
    _eventTypeId = db.Column("eventTypeId", db.Integer, db.ForeignKey("eventTypes.id"))
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))
    _actions = []

    def __init__(self, eventType, game):
        self._eventType = eventType
        self._game = game

    def appendAction(self, action):
        self._actions.append(action)

    def do(self):
        pass


class KillEvent(Event):
    _killedPlayer = db.relationship("Player")
    _killedPlayerId = db.Column("killedPlayerId", db.ForeignKey("players.id"))
    _wolfVotedTargets = []

    def __init__(self, game):
        Event.__init__(self, EventType.query.filter_by(_tag="EVENT_KILL").first(), game)

    def do(self):
        deadPlayer = self.determineDead()
        if deadPlayer != None:
            self._game.killPlayer(deadPlayer)
            _killedPlayer = deadPlayer
        

    def countWolfVotes(self):
        count = dict()
        for action in self._actions:
            if action.getActionType().getTag() == "WOLF_KILL":
                if action.getTarget() not in count.keys():
                    count[action.getTarget()] = 1
                else:
                    count[action.getTarget()] = count.get(action.getTarget()) + 1
        largestVotes = 0
        votedTargets = []
        for target, votes in count.items():
            if votes > largestVotes:
                votedTargets = []
                votedTargets.append(target)
            elif votes == largestVotes:
                votedTargets.append(target)

        self._wolfVotedTargets = votedTargets

    def getWitchSafe(self):
        for action in self._actions:
            if action.getActionType().getTag() == "WITCH_SAFE":
                return action.getTarget()

    def getWitchKill(self):
        for action in self._actions:
            if action.getActionType().getTag() == "WITCH_KILL":
                return action.getTarget()

    def isSafed(self, player):
        if (self.getWitchSafe() == player):
            return True
        # elif (...)
        # ...
        # More safes
    
    def determineDead(self):
        self.countWolfVotes()
        if len(self._wolfVotedTargets) > 0:
            killedPlayer = random.choice(self._wolfVotedTargets)
            if self.isSafed(killedPlayer):
                killedPlayer = None
        else:
            killedPlayer = None

        return killedPlayer


    