from app import db
from datetime import datetime
import random
import ast

class Newspaper(db.Model):
    __tablename__ = "newspapers"
    _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    _game = db.relationship("Game")
    _gameId = db.Column("gameId", db.Integer, db.ForeignKey("games.id"))
    _date = db.Column("date", db.String(10))
    _format = db.Column("format", db.String)

    # referenced
    _articles = db.relationship("Article")

    def __init__(self, game, date=datetime.now().strftime("%y-%m-%d")):
        self.setGame(game)
        self.setDate(date)

    def getId(self):
        return self._id
    
    def getDate(self):
        return self._date

    def getDateFormatted(self):
        date = self.getDate()
        year, month, day = int(date[:4]), int(date[5:7]), int(date[8:])
        return datetime(year, month, day).strftime("%d %B %y")

    def setDate(self, date):
        self._date = date

    def getGame(self):
        return self._game

    def setGame(self, game):
        self._game = game   

    def getFormat(self):
        return self._format

    def setFormat(self, format):
        self._format = format
    
    def getDay(self):
        # date of first newspaper of game - date of this newspaper
        year, month, day = int(self.getDate()[:4]), int(self.getDate()[5:7]), int(self.getDate()[8:])
        selfDate = datetime(year, month, day)

        lowestDate = datetime.now()
        for newspaper in self.getGame().getNewspapers():
            year, month, day = int(newspaper.getDate()[:4]), int(newspaper.getDate()[5:7]), int(newspaper.getDate()[8:])
            date = datetime(year, month, day)
            if date < lowestDate:
                lowestDate = date
        return abs((selfDate - lowestDate).days) + 1
       

    def setDay(self, day):
        self._day = day

    def getArticles(self):
        return self._articles

    def createFormat(self):
        articles = self.getArticles()[:]
        result = []
        # Add the admin articles to articles
        random.shuffle(articles)

        randomFactor = (1/20 * (len(articles)) + 0.15)
        print(randomFactor)

        while (len(articles) > 0):
            rand = random.randint(1, 101)

            # Group 1:          x | x | x | x
            if rand < 50:
                innerResult = (1,[])
                for x in range(0,4):
                    # Display article chance
                    if random.random() <= randomFactor:
                        if len(articles) == 0:
                            innerResult[1].append(None)
                        else:
                            innerResult[1].append(articles[len(articles)-1].getId())
                            articles.pop(len(articles)-1)
                    else:
                        innerResult[1].append(None)

                # Dont add if empty.
                noneCount = 0
                for art in innerResult[1]:
                    if art == None:
                        noneCount = noneCount + 1
                if noneCount != 4:
                    result.append(innerResult)

            # Group 2:          x | iiiii | x
            if rand >= 50 and rand < 80:
                innerResult = (2,[])
                imageSet = False
                while(len(innerResult[1]) < 4):
                    if len(innerResult[1]) == 2 and not imageSet:
                        innerResult[1].append(0)
                        innerResult[1].append(0)
                        break

                    # Display image chance
                    if random.randint(0,2) == 0 and not imageSet:
                        innerResult[1].append(0)
                        innerResult[1].append(0)
                        imageSet = True

                    # Display article chance
                    if random.random() <= randomFactor:
                        if len(articles) == 0:
                            innerResult[1].append(None)
                        else:
                            innerResult[1].append(articles[len(articles)-1].getId())
                            articles.pop(len(articles)-1)
                    else:
                        innerResult[1].append(None)

                # Dont add if empty.
                noneCount = 0
                for art in innerResult[1]:
                    if art == None:
                        noneCount = noneCount + 1
                if noneCount != 2:
                    result.append(innerResult)
                    

            # Group 3:          iiiii | c | x
            #                   iiiii | c | x
            # @format 
            #       (3, [image}left0|right1], closed}left0|right1, article1, article2)
            if rand >= 80:  
                innerResult = (3,[]) 
                
                # Choose image left or right
                innerResult[1].append(random.randint(0,1))

                # Choose closed article space left or right
                innerResult[1].append(random.randint(0,1))

                for x in range(0,2):
                    if random.random() <= randomFactor:
                        if len(articles) == 0:
                            innerResult[1].append(None)
                        else:
                            innerResult[1].append(articles[len(articles)-1].getId())
                            articles.pop(len(articles)-1)
                    else:
                        innerResult[1].append(None)

                # Dont add if empty
                if not (innerResult[1][2] == None and innerResult[1][3] == None):
                    result.append(innerResult)
            
        # filter out empty rows
        rowCount = 0
        for row in result:
            if row[0] == 1:
                allNone = True
                for art in row[1]:
                    if art != None:
                        allNone = False
                if allNone == True:
                    result.pop()


            rowCount = rowCount + 1
        print(result)
        return str(result)
    
    def refresh(self):
        self.setFormat(self.createFormat())

    def getFormatList(self):
        return ast.literal_eval(self.getFormat())

    def getArticleById(self, id):
        articles = self.getArticles()
        for article in articles:
            if article.getId() == id:
                return article
        return None

    def getNext(self):
        for newspaper in self.getGame().getNewspapers():
            if newspaper.getDay() - self.getDay() == 1:
                return newspaper
        return None

    def getPrevious(self):
        for newspaper in self.getGame().getNewspapers():
            if newspaper.getDay() - self.getDay() == -1:
                return newspaper
        return None



