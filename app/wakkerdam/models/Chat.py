from app import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = "chats"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))
    _chatType = db.relationship("ChatType")
    _chatTypeId = db.Column("chatTypeId", db.Integer, db.ForeignKey("chatTypes.id"))

    # referenced
    _chatters = db.relationship("Chatter")

    def __init__(self, game, chatType):
        self.setGame(game)
        self.setChatType(chatType)
    
    def getId(self):
        return self._id

    def getGame(self):
        return self._game

    def setGame(self, game):
        self._game = game

    def getChatType(self):
        return self._chatType

    def setChatType(self, chatType):
        self._chatType = chatType

    def getChatters(self, orderBy="id", reverse=False):
        chatters = self._chatters
        if orderBy == "isDead":
            chatters.sort(key=lambda x : x.getPlayer().isDead(), reverse=reverse)
        return chatters
    
    def isOpen(self):
        return self.getChatType().isOpen()

    def getMessages(self, orderBy="timestamp"):
        messages = []
        for chatters in self.getChatters():
            messages.extend(chatters.getMessages())
        if orderBy == "chatter":
            pass
        elif orderBy == "timestamp":
            messages.sort(key=lambda x : x.getTimestamp())
        return messages

    def getLastChatLogs(self, minutes=10):
        result = []
        for chatter in self.getChatters():
            chatLogs = chatter.getChatLogs()
            for chatLog in chatLogs:
                if chatLog.getTimestamp() >= datetime.now().timestamp()-minutes*60:
                    result.append(chatLog)
        return result
    
    def getOnlineChatters(self, minutes=10):
        result = []
        for chatLog in self.getLastChatLogs(minutes=minutes):
            if chatLog.getChatter() not in result:
                result.append(chatLog.getChatter())
        return result

    def getOnlineAmount(self, minutes=10):
        return len(self.getOnlineChatters(minutes=minutes))