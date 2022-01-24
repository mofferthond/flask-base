from app import db
from datetime import datetime

class Game(db.Model):
    __tablename__ = 'games'
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _name = db.Column("name", db.String(32))
    _ongoing = db.Column("ongoing", db.Boolean)
    _startDate = db.Column("startDate", db.String(64))
    _hostingUser = db.relationship("User")
    _hostingUserId = db.Column("hostingUserId", db.Integer, db.ForeignKey("users.id"))
    _playerAmount = db.Column("playerAmount", db.Integer)

    # referenced
    _chats = db.relationship("Chat")
    _invites = db.relationship("Invite")
    _players = db.relationship("Player")
    _newspapers = db.relationship("Newspaper")
    
    def __init__(self, name, ongoing, startDate, hostingUser, playerAmount):
        self.setName(name)
        self.setOngoing(ongoing)
        self.setStartDate(startDate)
        self.setHostingUser(hostingUser)
        self.setPlayerAmount(playerAmount)
        

    def getId(self):
        return self._id
    
    def getName(self):
        return self._name
    
    def setName(self, name):
        self._name = name

    def getOngoing(self):
        return self._ongoing

    def setOngoing(self, ongoing):
        self._ongoing = ongoing
    
    def getStartDate(self):
        return self._startDate
    
    def setStartDate(self, startDate):
        self._startDate = startDate
    
    def getHostingUser(self):
        return self._hostingUser

    def setHostingUser(self, hostingUser):
        self._hostingUser = hostingUser

    def getPlayerAmount(self):
        return self._playerAmount

    def setPlayerAmount(self, playerAmount):
        self._playerAmount = playerAmount

    def getPlayers(self, orderBy="id", reverse=False):
        players = self._players
        if orderBy == "isDead":
            players.sort(key=lambda x : x.isDead(), reverse=reverse)
        return players

    def getInvites(self):
        return self._invites

    def getChats(self):
        return self._chats

    def getNewspapers(self):
        return self._newspapers

    def getChatsForUser(self, user):
        players = self.getPlayers()
        for player in players:
            if player.getUser() == user:
                return [chatter.getChat() for chatter in player.getChatters()]
        raise Exception("User " + user + " is not in game " + game)
        
    def hasStarted(self):
        year, month, day = self.getStartDate().split('-')
        if datetime(int(year), int(month), int(day)) < datetime.now():
            return True
        return False

    def getDeadPlayerAmount(self):
        count = 0
        for player in self.getPlayers():
            if player.isDead():
                count += 1
        return count

    def getAlivedPlayerAmount(self):
        count = 0
        for player in self.getPlayers():
            if not player.isDead():
                count += 1
        return count

    def createActions(self):
        for player in self.getPlayers():
            for actor in player.getActiveActors():
                for actionType in actor.getCharacter().getActionTypes():
                    actionType.createEmptyAction(actor)

    def collectDeadlines(self, time : int):
        from app.wakkerdam.models.constants.Deadline import Deadline
        opens = Deadline.query.filter_by(_opens=time)
        closes = Deadline.query.filter_by(_closes=time)
        result = []
        result.extend(opens)
        result.extend(closes)
        return result


#   Gameplay methods

    def killPlayer(self, player):
        from app.wakkerdam.models.Actor import Dead
        deadActor = Dead(player)
        for actor in player.getActiveActors():
            # if isinstance(actor, Dead):
            #     continue
            actor.declareDead(deadActor)
        db.session.add(deadActor)
        db.session.commit()


