import pygame
import mysql.connector

################## connect to sql database ######################
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='multiplayer game'
)
db = connection.cursor()

# player class used to assign the user to player 1 or 2
# keeps track of movements and updates position
# draws the player on the screen


# Player class only exists within game class that holds the money and the player objects that are sent between clients
class Game:
    def __init__(self, gameID):
        self.__gameID = gameID
        self.__players = [Player(480, 1), Player(480, 2)]
        self.__ready = False
        self.__money = 2000
        self.__basementAccess = {}
        self.__legalEnding = False
        self.__playersQueue = 0
        self.__illegalEnding =False

    def getPlayers(self):
        return self.__players

    def moneyAmount(self):
        return self.__money

    def setAmount(self, amount):
        self.__money -= amount

    def ready(self):
        self.__ready = True

    def setBasementAccess(self, access, playerNum):
        if len(self.__basementAccess) == 0:
            if access[1] == "Y":
                self.__basementAccess["player 1"] = True
                self.__basementAccess["player 2"] = True
            else:
                if playerNum == 1:
                    self.__basementAccess["player 1"] = True
                    self.__basementAccess["player 2"] = False
                else:
                    self.__basementAccess["player 1"] = False
                    self.__basementAccess["player 2"] = True

            return "Granted"

        else:
            if self.__basementAccess[f"player {playerNum}"]:
                return "Granted"

        return "Denied"


class Player:
    def __init__(self, pos, player):
        self.__x = pos
        self.__y = 440
        self.__playerNum = player
        self.__location = "garden"
        print("player is:", player)
        print("player is at:", self.__location)
        self.__speed = 100
        self.__basementAccess = None
        self.__inventory = []
        self.__money = 0
    def draw(self, screen):
        if self.__playerNum == 1:
            image = pygame.image.load(
                "C:/Users/Asha Pangan/OneDrive/NEAimg/players/player1.png").convert_alpha()
        else:
            image = pygame.image.load(
                "C:/Users/Asha Pangan/OneDrive/NEAimg/players/player2.png").convert_alpha()
        image = pygame.transform.smoothscale(image, (720, 420))
        rect = image.get_rect(center=(self.__x, self.__y))
        screen.blit(image, rect)

    def getPos(self):
        pos = self.__x
        return pos

    def setPos(self, Xpos):
        self.__x = Xpos

    def getLocation(self):
        return self.__location

    def setLocation(self, location):
        self.__location = location
    def addItem(self, item):
        self.__inventory.append(item)
    def removeItem(self, item):
        self.__inventory.remove(item)
    def setBasementAccess(self, Access):
        self.__basementAccess = Access
        print(self.__basementAccess)
    def getBasementAccess(self):
        return self.__basementAccess
    def getMoney(self):
        return self.__money
    def updateMoneyAmount(self, amount):
        self.__money = amount
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.__x -= self.__speed
        if keys[pygame.K_RIGHT]:
            self.__x += self.__speed
        self.setPos(self.__x)




class Items:
    def __init__(self, itemList, shop):
        self.__itemList = itemList
        self.__shop = shop
    def getItemList(self):
        return self.__itemList

    def getShop(self):
        return self.__shop

    def getPrice(self, item):
        price = self.__itemList[item]
        return price

    def buyItem(self, item, gameCode):
        price = self.__itemList[item]
        db.execute(f"SELECT moneyAmount FROM `games` WHERE gameCode = '{gameCode}';")
        amount = db.fetchall()[0][0]
        amount -= price
        db.execute(f"UPDATE `games` SET `moneyAmount`= '{amount}' WHERE `gameCode` = 'FII1';")
        connection.commit()


class Contraband(Items):
    def __init__(self, itemList, shop):
        super().__init__(itemList, shop)
        self.__itemList = itemList
        self.__shop = "shady guy"
    def buyItem(self, item, gameCode):
        price = self.__itemList[item]
        db.execute(f"SELECT moneyAmount FROM `games` WHERE gameCode = '{gameCode}';")
        amount = db.fetchall()[0][0]
        amount -= price
        db.execute(f"UPDATE `games` SET `moneyAmount`= '{amount}' WHERE `gameCode` = 'FII1';")
        connection.commit()
        del self.__itemList[item]


