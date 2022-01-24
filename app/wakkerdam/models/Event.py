from app import db

class Event(db.Model):
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))
    _actions = []


    def appendAction(self, action : Action):
        _actions.append(action)


class KillEvent(Event):
    _votedTargets = db.relationship("Player")


    def do(self):
        count = dict()
        for action in _actions:
            if action.getTarget() not in count.keys():
                count[action.getTarget()] = 1
            else:
                count[action.getTarget()] = count.get(action.getTarget()) + 1
        largestVotes = 0
        votedTargets = []
        for target, votes in count:
            if votes > largestVotes:
                votedTargets = []
                votedTargets.append(target)
            elif votes == largestVotes:
                votedTargets.append(target)

        _votedTargets = votedTargets
        if len(votedTargets) > 1:
            pass
        else:
            _game.killPlayer(votedTargets[0])